import contextlib
import io
import logging
import pathlib
import sys
import typing as t
import zipfile
from pprint import pformat

import click

from macos_installation.functions import encryption

logger: logging.Logger = logging.getLogger(__name__)


class InMemoryZip(object):
    def __init__(
        self, file: t.Optional[pathlib.Path] = None, password: t.Optional[str] = None
    ):
        # Inputs
        self.file_path = file
        self.__password = password

        self.zip_contents: t.Optional[t.IO[bytes]] = io.BytesIO(
            self.file_path.read_bytes() if self.file_path else None
        )

        logger.debug(
            "Class 'InMemoryZip' instantiated: "
            f"{pformat({k: v for k, v in self.__dict__.items() if '__password' not in k})}"
        )

    @property
    def is_encrypted(self) -> bool:
        """
        The is_encrypted function returns True if the file is encrypted and False otherwise.
        Admittedly, this is not the best test in the world considering that a corrupt
        ZIP file that's unencrypted would show up as being encrypted in this check.
        In the future, will look into replacing the encryption with a better method
        which can actually verify if something is encrypted or not.

        If False, then it is not encrypted.
        If True, then it is encrypted.

        :param self: Access attributes of the class
        :return: True if the file is encrypted, and false otherwise
        """
        try:
            zipfile.ZipFile(
                file=self.zip_contents, mode="r", compression=zipfile.ZIP_DEFLATED
            )
            return False
        except zipfile.BadZipFile:
            return True

    def decrypt(self) -> t.NoReturn:
        """
        The decrypt function is used to decrypt the contents of a zip file that has been encrypted with
        the encrypt function.

        :param self: Access the attributes and methods of the class in python
        :return: None
        """
        if self.is_encrypted:
            if self.has_password:
                try:
                    self.zip_contents = io.BytesIO(
                        encryption.decrypt_bytes(
                            self.zip_contents.getvalue(), self.__password
                        )
                    )
                    restore_zip = zipfile.ZipFile(
                        file=self.zip_contents,
                        mode="r",
                        compression=zipfile.ZIP_DEFLATED,
                    )
                    if crc_test := restore_zip.testzip() is not None:
                        click.secho(
                            f"Bad CRC or file headers on '{self.file_path.name}': {crc_test}",
                            fg="red",
                        )
                        sys.exit(1)
                except ValueError:
                    click.secho(
                        f"Password for encrypted ZIP file '{self.file_path.name}' was incorrect!",
                        fg="red",
                    )
                    sys.exit(1)
            else:
                click.secho(
                    "A password must be specified for an encrypted ZIP file!", fg="red"
                )
                sys.exit(1)

    def encrypt(self) -> t.NoReturn:
        """
        The encrypt function encrypts the zip file in memory.

        :param self: Access the attributes and methods of the class in python
        :return: None
        """
        if not self.is_encrypted:
            self.zip_contents = io.BytesIO(
                encryption.encrypt_bytes(self.zip_contents.getvalue(), self.__password)
            )

    @property
    def has_password(self) -> bool:
        """
        Determines if the in-memory ZIP is using a password or not.
        """
        return self.__password is not None

    @contextlib.contextmanager
    def open_zip_file(
        self, mode: t.Literal["r", "w", "x", "a"] = "w"
    ) -> zipfile.ZipFile:
        """
        The open_zip_file function opens a zip file for reading or writing.

        :param mode:t.Literal["r", "w", "x", "a"]="w": Specify the mode in which the file is opened
        :return: A zipfile object
        """
        zip_file = zipfile.ZipFile(
            file=self.zip_contents, mode=mode, compression=zipfile.ZIP_DEFLATED
        )
        try:
            yield zip_file
        finally:
            zip_file.close()

    def read(self) -> bytes:
        """
        The read function reads the in memory zip file and returns it as bytes.

        :param self: Refer to the object of the class
        :return: The bytes of the in-memory zip file
        """
        return self.zip_contents.getvalue()

    def read_unencrypted(self) -> t.IO[bytes]:
        if self.is_encrypted:
            self.decrypt()
            contents = self.zip_contents
            self.encrypt()
        else:
            contents = self.zip_contents

        return contents

    def write_to_file(self, filename: pathlib.Path) -> t.NoReturn:
        """
        The write_to_file function writes the contents of the file to a new file.

        :param self: Access the attributes and methods of the class in which it is used
        :param filename: Specify the file to write the data to
        :return: None
        """
        with open(filename, "wb") as f:
            f.write(self.read())
