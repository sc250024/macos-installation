import pathlib
import typing as t

import click

from macos_installation.classes.zip import InMemoryZip


class EncryptCommand(object):
    def __init__(self, zip_object: InMemoryZip, **kwargs):
        self.debug: bool = kwargs["debug"]
        self.dry_run: bool = kwargs["dry_run"]

        self.__zip_object = zip_object

    def main(self) -> t.NoReturn:
        self.__zip_object.encrypt()
        encrypted_file_path = pathlib.Path(
            f"{self.__zip_object.file_path.absolute()}.enc"
        )
        self.__zip_object.write_to_file(encrypted_file_path)
        click.secho(f"Encrypted file written to '{encrypted_file_path}'", fg="green")
