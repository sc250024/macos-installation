import unittest

from Cryptodome.Random import get_random_bytes

from macos_installation.functions import encryption


class TestEncryptDecrypt(unittest.TestCase):
    def test_encrypt_decrypt(self):
        # Generate a random password
        password = get_random_bytes(16).hex()

        # Generate a random file
        data = get_random_bytes(1024)

        # Encrypt the file and write it
        encrypted_data = encryption.encrypt_bytes(data, password)

        # Check that the encrypted data is not the same as the original data
        self.assertNotEqual(data, encrypted_data)

        # Decrypt the bytes
        decrypted_data = encryption.decrypt_bytes(encrypted_data, password)

        # Check that the decrypted data is the same as the original data
        self.assertEqual(data, decrypted_data)


class TestHashPassword(unittest.TestCase):
    def test_default_arguments(self):
        hashed_password, salt = encryption.generate_hashed_password("password")
        self.assertIsInstance(hashed_password, bytes)
        self.assertIsInstance(salt, bytes)
        self.assertEqual(len(salt), 8)

    def test_custom_hash_name(self):
        hashed_password, salt = encryption.generate_hashed_password(
            "password", hash_name="sha3-512"
        )
        self.assertIsInstance(hashed_password, bytes)
        self.assertIsInstance(salt, bytes)
        self.assertEqual(len(salt), 8)

    def test_custom_rounds(self):
        hashed_password, salt = encryption.generate_hashed_password(
            "password", rounds=500000
        )
        self.assertIsInstance(hashed_password, bytes)
        self.assertIsInstance(salt, bytes)
        self.assertEqual(len(salt), 8)

    def test_custom_salt(self):
        salt = b"salt"
        hashed_password, salt_output = encryption.generate_hashed_password(
            "password", salt=salt
        )
        self.assertIsInstance(hashed_password, bytes)
        self.assertIsInstance(salt_output, bytes)
        self.assertEqual(salt, salt_output)

    def test_custom_salt_size(self):
        hashed_password, salt = encryption.generate_hashed_password(
            "password", salt_size=4
        )
        self.assertIsInstance(hashed_password, bytes)
        self.assertIsInstance(salt, bytes)
        self.assertEqual(len(salt), 4)
