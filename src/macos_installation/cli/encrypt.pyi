import typing as t

from macos_installation.classes.zip import InMemoryZip  # type: ignore

class EncryptCommand:
    debug: bool
    dry_run: bool
    def __init__(self, zip_object: InMemoryZip, **kwargs) -> None: ...
    def main(self) -> t.NoReturn: ...
