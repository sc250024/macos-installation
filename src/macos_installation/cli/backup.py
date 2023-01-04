import io
import json
import pathlib
import typing as t

import click

from macos_installation import config
from macos_installation.classes.zip import InMemoryZip
from macos_installation.functions import util


class BackupCommand(object):
    def __init__(self, zip_object: InMemoryZip, **kwargs):
        self.backup_file: pathlib.Path = kwargs["backup_file"]
        self.debug: bool = kwargs["debug"]
        self.dry_run: bool = kwargs["dry_run"]
        self.extra_location: t.Tuple[pathlib.Path] = kwargs["extra_location"]

        self.__zip_object = zip_object

        # Evaluated later
        self._all_backup_files: t.List[pathlib.Path] = None
        self._backup_locations: t.List[pathlib.Path] = None

    @property
    def all_backup_files(self) -> t.List[pathlib.Path]:
        if self._all_backup_files is None:
            self._all_backup_files = [
                location
                for location in util.get_recursive_file_list(self.backup_locations)
            ]
        return self._all_backup_files

    @property
    def backup_locations(self) -> t.List[pathlib.Path]:
        if self._backup_locations is None:
            self._backup_locations = list(
                set(config.BACKUP_LOCATIONS + list(self.extra_location))
            )
        return self._backup_locations

    def _get_info_bytes(self) -> t.IO[bytes]:
        # Create the info dictionary and write it to the root of the archive
        info_dict = {
            "BACKUP_LOCATIONS": sorted(str(p) for p in self.backup_locations),
            "FILE_DIGESTS": {
                str(f): util.get_file_sha256_hash(f) for f in self.all_backup_files
            },
            "OLD_USER": config.CURRENT_USER,
            "OLD_USER_HOME_DIR": config.CURRENT_USER_HOME_DIR,
        }
        return io.BytesIO(
            json.dumps(info_dict, default=str, indent=2, sort_keys=True).encode(
                config.DEFAULT_ENCODING
            )
        )

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
                for backup_file in self.all_backup_files:
                    zip_file.write(backup_file)

                # Add extra information like the current home folder
                # So that it can be stripped from paths later on
                info_bytes = self._get_info_bytes()
                zip_file.writestr("info.json", info_bytes.getvalue())

            # Use this temporary variable in case it needs to be updated
            backup_path = self.backup_file

            if self.__zip_object.has_password:
                self.__zip_object.encrypt()
                backup_path = pathlib.Path(f"{backup_path.absolute()}.enc")

            self.__zip_object.write_to_file(backup_path)
        else:
            message = f"[DRY-RUN] {message}"
            click.secho(message, fg="yellow")
