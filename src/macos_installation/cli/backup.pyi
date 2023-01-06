import pathlib
import typing as t

from macos_installation.classes.data import BackupManifest  # type: ignore
from macos_installation.classes.zip import InMemoryZip  # type: ignore

class BackupCommand:
    backup_file: pathlib.Path
    debug: bool
    dry_run: bool
    extra_location: t.List[pathlib.Path]
    def __init__(self, zip_object: InMemoryZip, **kwargs) -> None: ...
    @property
    def backup_locations(self) -> t.List[pathlib.Path]: ...
    @property
    def backup_manifest(self) -> BackupManifest: ...
    def main(self) -> t.NoReturn: ...
