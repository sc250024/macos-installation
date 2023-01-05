import secrets
import typing as t

from Cryptodome.Cipher import AES
from Cryptodome.Protocol import KDF

from macos_installation import config
from macos_installation.classes.data import EncryptedData


def encrypt_bytes(
    unencrypted_data: bytes,
    password: t.Union[bytes, str],
) -> bytes:
    """
    The encrypt_bytes function encrypts the given unencrypted_data using AES-GCM
    with the given password. The function returns a byte string containing the salt,
    nonce, encrypted data, and digest tag concatenated together in that order.

    :param unencrypted_data:bytes: Store the data that will be encrypted
    :param password:t.Union[bytes, str]: Specify the password; string or bytes object allowed
    :param : Generate a key from the password
    :return: The encrypted data along with the salt, nonce, and digest tag
    """
    try:
        password = password.encode(config.DEFAULT_ENCODING)
    except AttributeError:
        # Password is already encoded
        pass

    key, salt = generate_key(password)

    # Encrypt the data
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    encrypted_data = cipher.encrypt(unencrypted_data)
    tag = cipher.digest()

    # Return the encrypted data along with the salt, nonce, and digest tag
    return salt + nonce + encrypted_data + tag


def decrypt_bytes(encrypted_data: bytes, password: t.Union[bytes, str]) -> bytes:
    """
    The decrypt_bytes function takes in a bytes object and a password, and returns the decrypted data.
    The function uses AES-GCM to decrypt the data,
    which is an authenticated encryption algorithm that provides both confidentiality and integrity.
    The function also checks if the encrypted data has been tampered with by comparing its tag with what it should be.

    :param encrypted_data:bytes: Store the encrypted data
    :param password:t.Union[bytes, str]: Specify the password; string or bytes object allowed
    :return: The decrypted data
    """
    # Extract the salt from the encrypted data, and generate the decryption key
    encrypted_data = EncryptedData(encrypted_data)

    key, _ = generate_key(password, encrypted_data.salt)

    # Create cipher with the nonce
    cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_data.nonce)

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data.raw_data)

    # Verify the data
    cipher.verify(encrypted_data.tag)

    # Return the decrypted data
    return decrypted_data


def generate_salt(size: int = 32) -> bytes:
    """
    The generate_salt function generates a random salt of the specified size.
    The default size is 32 bytes, or 256 bits.

    :param size:int=32: Specify the size of the salt to be generated
    :return: A random sequence of bytes
    """
    return secrets.token_bytes(size)


def generate_key(
    password: str,
    salt: t.Optional[bytes] = None,
    key_length: t.Optional[int] = 32,
) -> t.Tuple[bytes, bytes]:
    """
    The generate_key function generates a key and salt for use in the encrypt
    and decrypt functions. The password is hashed using scrypt, which is then used
    to generate the key and salt. The function returns both of these values as a tuple.

    :param password:str: Provide the password that will be used to generate the key
    :param salt:t.Optional[bytes]=None: Generate a new salt if one is not provided
    :param key_length:t.Optional[int]=32: Specify the length of the key to be generated
    :return: A tuple of the key and salt
    """
    if not salt:
        salt = generate_salt(key_length)
    return KDF.scrypt(password, salt, key_len=key_length, N=2**20, r=8, p=1), salt
