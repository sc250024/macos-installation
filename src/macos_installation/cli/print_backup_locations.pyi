import typing as t

class PrintBackupLocationsCommand:
    debug: bool
    dry_run: bool
    tablefmt: str
    def __init__(self, **kwargs) -> None: ...
    def main(self) -> t.NoReturn: ...
