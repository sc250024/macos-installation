import hashlib
import os
import struct

from Cryptodome.Cipher import AES

from macos_installation import config


def encrypt_bytes(unencrypted_data: bytes, password: str) -> bytes:
    """
    The encrypt_bytes function encrypts unencrypted data using AES-256 in CBC mode.

    :param unencrypted_data:bytes: Data that is to be encrypted
    :param password:str: Encrypt the unencrypted_data
    :return: The encrypted unencrypted_data in bytes
    """
    # Generate a salt
    salt = os.urandom(8)

    try:
        password = password.encode(config.DEFAULT_ENCODING)
    except AttributeError:
        # Password is already encoded
        pass

    # Derive the key and iv from the password and salt
    key_iv = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)
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


def decrypt_bytes(encrypted_data: bytes, password: str) -> bytes:
    """
    The decrypt_bytes function takes in a byte string and a password. It then
    decrypts the data using AES-256 in CBC mode with PKCS7 padding. The function
    returns the decrypted bytes.

    :param encrypted_data:bytes: Store the encrypted data
    :param password:str: Specify the password used to encrypt the data
    :return: The decrypted data from the encrypted data and password
    """
    # Extract the salt, iv, and encrypted data from the input
    salt = encrypted_data[:8]
    iv = encrypted_data[8:24]
    data = encrypted_data[24:]

    try:
        password = password.encode(config.DEFAULT_ENCODING)
    except AttributeError:
        # Password is already encoded
        pass

    # Derive the key and iv from the password and salt
    key_iv = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)
    key = key_iv[:32]

    # Decrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)

    # Strip off the padding
    pad = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad]

    # Return the decrypted data
    return decrypted_data
