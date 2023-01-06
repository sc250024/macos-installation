import dataclasses
import logging
import pathlib
import typing as t
from pprint import pformat

from macos_installation import config
from macos_installation.functions import util

logger: logging.Logger = logging.getLogger(__name__)


@dataclasses.dataclass
class EncryptedData:
    encrypted_data: bytes
    salt_size: int = dataclasses.field(default=32)
    nonce_size: int = dataclasses.field(default=16)
    tag_size: int = dataclasses.field(default=16)

    # Initialized later
    salt: bytes = dataclasses.field(init=False)
    nonce: bytes = dataclasses.field(init=False)
    raw_data: bytes = dataclasses.field(init=False)
    tag: bytes = dataclasses.field(init=False)

    def __post_init__(self):
        self.salt: bytes = self.encrypted_data[: self.salt_size]
        self.nonce: bytes = self.encrypted_data[
            self.salt_size : (self.salt_size + self.nonce_size)
        ]
        self.raw_data: bytes = self.encrypted_data[
            (self.salt_size + self.nonce_size) : -(self.tag_size)
        ]
        self.tag: bytes = self.encrypted_data[-(self.tag_size) :]

        logger.debug(f"Class 'EncryptedData' instantiated: {pformat(self)}")

    def __repr__(self):
        return (
            f"EncryptedData(encrypted_data_size={len(self.encrypted_data)}"
            f", salt_size={self.salt_size}"
            f", nonce_size={self.nonce_size}"
            f", tag_size={self.tag_size}"
            ")"
        )


@dataclasses.dataclass
class BackupManifest:
    backup_locations: t.List[t.Union[str, pathlib.Path]]
    existing: bool = dataclasses.field(default=False)
    old_user: str = dataclasses.field(default=config.CURRENT_USER)
    old_user_home_dir: str = dataclasses.field(default=config.CURRENT_USER_HOME_DIR)

    # Initialized later
    all_backup_files: t.List[pathlib.Path] = None
    file_digests: t.Dict[str, str] = None

    def __post_init__(self):
        if not self.existing:
            self.all_backup_files = [
                location
                for location in util.get_recursive_file_list(self.backup_locations)
            ]
            self.file_digests = {
                str(f): util.get_file_sha256_hash(f) for f in self.all_backup_files
            }

        logger.debug(f"Class 'BackupManifest' instantiated: {pformat(self)}")

    def __repr__(self):
        return (
            f"BackupManifest(backup_locations={self.backup_locations}, "
            f"old_user={self.old_user}, "
            f"old_user_home_dir={self.old_user_home_dir})"
        )

    def dict(self):
        return {
            k: v
            for k, v in dataclasses.asdict(self).items()
            if k not in ["all_backup_files", "existing"]
        }
