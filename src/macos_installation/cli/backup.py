import json
import logging
import pathlib
import typing as t
from pprint import pformat

import click

from macos_installation import config
from macos_installation.classes.data import BackupManifest
from macos_installation.classes.zip import InMemoryZip

logger: logging.Logger = logging.getLogger(__name__)


class BackupCommand(object):
    def __init__(self, zip_object: InMemoryZip, **kwargs):
        self.backup_file: pathlib.Path = kwargs["backup_file"]
        self.debug: bool = kwargs["debug"]
        self.dry_run: bool = kwargs["dry_run"]
        self.extra_location: t.List[pathlib.Path] = list(kwargs["extra_location"])

        # Injected dependencies
        self.__zip_object = zip_object

        # Evaluated later
        self._backup_locations: t.Optional[t.List[pathlib.Path]] = None
        self._backup_manifest: t.Optional[BackupManifest] = None

        logger.debug(f"Class 'BackupCommand' instantiated: {pformat(self.__dict__)}")

    @property
    def backup_locations(self) -> t.List[pathlib.Path]:
        if self._backup_locations is None:
            self._backup_locations = sorted(
                list(set(config.BACKUP_LOCATIONS + self.extra_location))
            )
        return self._backup_locations

    @property
    def backup_manifest(self) -> BackupManifest:
        if self._backup_manifest is None:
            self._backup_manifest = BackupManifest(self.backup_locations)
        return self._backup_manifest

    def main(self) -> t.NoReturn:
        """
        Perform the main backup function.
        """
        message = f"Creating backup file '{self.backup_file.name}' of the following locations:\n"
        for bl in self.backup_locations:
            message += f"- {bl.absolute()}\n"

        if not self.dry_run:
            click.secho(message, fg="green")

            with self.__zip_object.open_zip_file(mode="a") as zip_file:
                # Write all files
                for backup_file in self.backup_manifest.all_backup_files:
                    zip_file.write(backup_file)

                # Add backup manifest of all files, and user information
                # for later usage
                zip_file.writestr(
                    "manifest.json",
                    json.dumps(
                        self.backup_manifest.dict(),
                        default=str,
                        indent=2,
                        sort_keys=True,
                    ),
                )

            # Use this temporary variable in case it needs to be updated
            backup_path = self.backup_file

            if self.__zip_object.has_password:
                self.__zip_object.encrypt()
                backup_path = pathlib.Path(f"{backup_path.absolute()}.enc")

            self.__zip_object.write_to_file(backup_path)
        else:
            message = f"[DRY-RUN] {message}"
            click.secho(message, fg="yellow")
