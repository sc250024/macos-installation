import dataclasses


@dataclasses.dataclass
class EncryptedData:
    encrypted_data: bytes
    salt_size: int = dataclasses.field(default=32)
    nonce_size: int = dataclasses.field(default=16)
    tag_size: int = dataclasses.field(default=16)

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
