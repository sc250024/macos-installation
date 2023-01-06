import tempfile
import typing as t

from macos_installation.classes.data import BackupManifest  # type: ignore
from macos_installation.classes.zip import InMemoryZip  # type: ignore

class RestoreCommand:
    debug: bool
    dry_run: bool
    def __init__(self, zip_object: InMemoryZip, **kwargs) -> None: ...
    @property
    def backup_manifest(self) -> BackupManifest: ...
    @property
    def temp_dir(self) -> tempfile.TemporaryDirectory: ...
    def main(self) -> t.NoReturn: ...
