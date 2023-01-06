import logging
import pathlib
import typing as t
import zipfile

logger: logging.Logger

class InMemoryZip:
    file_path: t.Optional[pathlib.Path]
    zip_contents: t.Optional[str]
    def __init__(
        self, file: t.Optional[pathlib.Path] = ..., password: t.Optional[str] = ...
    ) -> None: ...
    @property
    def is_encrypted(self) -> bool: ...
    def decrypt(self) -> t.NoReturn: ...
    def encrypt(self) -> t.NoReturn: ...
    @property
    def has_password(self) -> bool: ...
    def open_zip_file(
        self, mode: t.Literal["r", "w", "x", "a"] = ...
    ) -> zipfile.ZipFile: ...
    def read(self) -> bytes: ...
    def read_unencrypted(self) -> t.IO[bytes]: ...
    def write_to_file(self, filename: pathlib.Path) -> t.NoReturn: ...
