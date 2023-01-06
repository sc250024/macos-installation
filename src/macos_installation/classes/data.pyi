import pathlib
import typing as t

class EncryptedData:
    encrypted_data: bytes
    salt_size: int
    nonce_size: int
    tag_size: int
    salt: bytes
    nonce: bytes
    raw_data: bytes
    tag: bytes
    def __post_init__(self) -> None: ...
    def __init__(self, encrypted_data, salt_size, nonce_size, tag_size) -> None: ...

class BackupManifest:
    backup_locations: t.List[t.Union[str, pathlib.Path]]
    existing: bool
    old_user: str
    old_user_home_dir: str
    all_backup_files: t.List[pathlib.Path]
    file_digests: t.Dict[str, str]
    def __post_init__(self) -> None: ...
    def dict(self): ...
    def __init__(
        self,
        backup_locations,
        existing,
        old_user,
        old_user_home_dir,
        all_backup_files,
        file_digests,
    ) -> None: ...
