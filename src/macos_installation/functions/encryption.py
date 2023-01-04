import hashlib
import os
import struct
import typing as t

from Cryptodome.Cipher import AES

from macos_installation import config


def encrypt_bytes(
    unencrypted_data: bytes,
    password: t.Union[bytes, str],
) -> bytes:
    """
    The encrypt_bytes function encrypts the given bytes using AES-256 in CBC mode.

    :param unencrypted_data:bytes: Pass the unencrypted data to be encrypted
    :param password:t.Union[bytes, str]: Specify the password
    :return: A byte string containing the encrypted data, along with the salt and initialization vector
    """
    # Derive the key and iv from the password and salt
    key_iv, salt = generate_hashed_password(password)
    key = key_iv[:32]
    iv = key_iv[-16:]

    # Pad the data to a multiple of 16 bytes
    pad = 16 - (len(unencrypted_data) % 16)
    unencrypted_data += pad * struct.pack("b", pad)

    # Encrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(unencrypted_data)

    # Return the encrypted data along with the salt and initialization vector
    return salt + iv + encrypted_data


def decrypt_bytes(encrypted_data: bytes, password: t.Union[bytes, str]) -> bytes:
    """
    The decrypt_bytes function takes in a bytes object and a password, and returns the decrypted data.

    :param encrypted_data:bytes: Store the encrypted data
    :param password:t.Union[bytes, str]: Specify the password
    :return: The decrypted data
    """
    # Extract the salt, iv, and encrypted data from the input
    salt = encrypted_data[:8]
    iv = encrypted_data[8:24]
    data = encrypted_data[24:]

    # Derive the key and iv from the password and salt
    key_iv, salt = generate_hashed_password(password, salt=salt)
    key = key_iv[:32]

    # Decrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)

    # Strip off the padding
    pad = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad]

    # Return the decrypted data
    return decrypted_data


def generate_hashed_password(
    password: str,
    hash_name: str = "sha256",
    rounds: int = 100_000,
    salt: t.Optional[bytes] = None,
    salt_size: t.Optional[int] = 8,
) -> t.Tuple[bytes, bytes]:
    """
    The generate_hashed_password function hashes a password using the PBKDF2 algorithm.

    :param password:str: Store the password that will be hashed
    :param hash_name:str='sha256': Specify the hash algorithm to use
    :param rounds:int=100_000: Determine how many times the password is hashed
    :param salt:t.Optional[bytes]=None: Set a default value for the salt parameter
    :param salt_size:t.Optional[int]=8: Specify the size of the salt
    :param : Specify the hashing algorithm
    :return: A tuple of a hashed password and the salt used to generate it
    """
    try:
        password = password.encode(config.DEFAULT_ENCODING)
    except AttributeError:
        pass

    salt = os.urandom(salt_size) if not salt else salt

    return hashlib.pbkdf2_hmac(hash_name, password, salt, rounds), salt
