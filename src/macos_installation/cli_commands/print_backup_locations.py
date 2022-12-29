import typing as t

import tabulate

from macos_installation import config


class PrintBackupLocationsCommand(object):
    def __init__(self, **kwargs):
        self.debug: bool = kwargs["debug"]
        self.dry_run: bool = kwargs["dry_run"]
        self.tablefmt: str = kwargs["tablefmt"]

    def main(self) -> t.NoReturn:
        """
        Print the base backup locations.
        """
        table = []
        headers = ["Location", "Path Type", "Exists"]

        for backup_location in config.BACKUP_LOCATIONS:
            table.append(
                [
                    backup_location.absolute(),
                    "File"
                    if backup_location.is_file()
                    else "Directory"
                    if backup_location.is_dir()
                    else "N/A",
                    "✅" if backup_location.exists() else "❌",
                ]
            )
        print(tabulate.tabulate(table, headers, tablefmt=self.tablefmt))
