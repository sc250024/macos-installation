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
