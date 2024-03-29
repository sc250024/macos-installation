import json
import logging
import os
import pathlib
import shutil
import sys
import tempfile
import typing as t
import zipfile
from pprint import pformat

import click

from macos_installation import config
from macos_installation.classes.data import BackupManifest
from macos_installation.classes.zip import InMemoryZip
from macos_installation.functions import template, util

logger: logging.Logger = logging.getLogger(__name__)


class RestoreCommand(object):
    def __init__(self, zip_object: InMemoryZip, **kwargs):
        self.debug: bool = kwargs["debug"]
        self.dry_run: bool = kwargs["dry_run"]

        # Injected dependencies
        self.__zip_object = zip_object

        # Evaluated later
        self._backup_manifest: t.Optional[BackupManifest] = None
        self._temp_dir: t.Optional[tempfile.TemporaryDirectory] = None

        logger.debug(f"Class 'RestoreCommand' instantiated: {pformat(self.__dict__)}")

    @property
    def backup_manifest(self) -> BackupManifest:
        if self._backup_manifest is None:
            restore_zip = zipfile.ZipFile(
                self.__zip_object.read_unencrypted(),
                mode="r",
                compression=zipfile.ZIP_DEFLATED,
            )

            # Extract contents
            restore_zip.extractall(path=self.temp_dir.name)

            # Get the info dict
            temp_json: t.Dict[str, str] = json.loads(
                restore_zip.read("manifest.json").decode(config.DEFAULT_ENCODING)
            )
            self._backup_manifest = BackupManifest(existing=True, **temp_json)

        return self._backup_manifest

    @property
    def temp_dir(self) -> tempfile.TemporaryDirectory:
        if self._temp_dir is None:
            self._temp_dir = tempfile.TemporaryDirectory()

        return self._temp_dir

    def _configure_git(self) -> t.NoReturn:
        if not self.dry_run:
            substitutions = {
                "gpg_path": shutil.which("gpg") or "/usr/local/bin/gpg",
                "home_dir": str(config.CURRENT_USER_HOME_DIR),
                "sops_path": shutil.which("sops") or "/opt/homebrew/bin/sops",
            }
            gitconfig_path = config.CURRENT_USER_HOME_DIR / ".gitconfig"

            # Render contents of '.gitconfig' template
            contents = template.render_template(
                config.TEMPLATES_DIR / ".gitconfig", substitutions
            )

            # Delete current '.gitconfig' file if it exists
            gitconfig_path.unlink(missing_ok=True)

            # Write the config
            with open(gitconfig_path, "w") as f:
                f.write(contents)

            # Set permissions on '.ssh' folder and 'config' file
            os.chmod(gitconfig_path, 0o644)

    def _configure_ssh(self) -> t.NoReturn:
        if not self.dry_run:
            substitutions = {
                "current_user": config.CURRENT_USER,
                "home_dir": config.CURRENT_USER_HOME_DIR,
            }
            ssh_path = config.CURRENT_USER_HOME_DIR / ".ssh"
            ssh_config_path = ssh_path / "config"

            # Create '.ssh' directory
            ssh_path.mkdir(parents=True, exist_ok=True)

            # Render the contents of the 'config' file
            contents = template.render_template(
                config.TEMPLATES_DIR / "ssh" / "config", substitutions
            )

            # Add 'UseKeychain' if macOS
            if sys.platform.lower() == "darwin":
                contents = contents + "    UseKeychain yes\n"

            # Write the config
            with open(ssh_config_path, "w") as f:
                f.write(contents)

            # Set permissions on '.ssh' folder and 'config' file
            os.chmod(ssh_path, 0o700)
            os.chmod(ssh_config_path, 0o640)

            # Set permissions on SSH keys
            for key in ssh_path.glob("**/*id_*"):
                os.chmod(key, 0o600)

    def _validate_extracted_files(self) -> t.NoReturn:
        for sp, digest_hash in self.backup_manifest.file_digests.items():
            extracted_hash = util.get_file_sha256_hash(
                file_path=pathlib.Path(self.temp_dir.name + sp)
            )
            assert extracted_hash == digest_hash

    def _restore_files(self) -> t.NoReturn:
        for backup_location in self.backup_manifest.backup_locations:
            temp_location = pathlib.Path(self.temp_dir.name + backup_location)
            restore_location = pathlib.Path(
                backup_location.replace(
                    self.backup_manifest.old_user_home_dir,
                    str(config.CURRENT_USER_HOME_DIR),
                )
            )

            message = f"Moving '{temp_location}' to '{restore_location}'"
            if not self.dry_run:
                click.secho(message, fg="green")
                if restore_location.exists():
                    backup_path = util.create_backup(restore_location)

                    try:
                        shutil.rmtree(restore_location, ignore_errors=True)
                    except NotADirectoryError:
                        restore_location.unlink()

                    click.secho(
                        f"Path '{restore_location}' exists. Creating backup to '{backup_path}'.",
                        fg="yellow",
                    )
                shutil.move(src=temp_location, dst=restore_location)
            else:
                click.secho(f"[DRY-RUN] {message}", fg="yellow")

    def main(self) -> t.NoReturn:
        """
        Perform the main restore function.
        """
        self._validate_extracted_files()
        self._restore_files()
        self._configure_git()
        self._configure_ssh()
