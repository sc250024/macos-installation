import unittest

from Cryptodome import Random

from macos_installation.functions import encryption


class TestEncryptDecrypt(unittest.TestCase):
    def test_encrypt_decrypt(self):
        # Generate a random password
        password = Random.get_random_bytes(16).hex()

        # Generate a random file
        data = Random.get_random_bytes(1024)

        # Encrypt the file and write it
        encrypted_data = encryption.encrypt_bytes(data, password)

        # Check that the encrypted data is not the same as the original data
        self.assertNotEqual(data, encrypted_data)

        # Decrypt the bytes
        decrypted_data = encryption.decrypt_bytes(encrypted_data, password)

        # Check that the decrypted data is the same as the original data
        self.assertEqual(data, decrypted_data)

    def test_encrypt_decrypt_tampering(self):
        # Generate a random password
        password = Random.get_random_bytes(16).hex()

        # Generate a random file
        data = Random.get_random_bytes(1024)

        # Encrypt the file and write it
        encrypted_data = encryption.encrypt_bytes(data, password)

        # Tamper with the data to later raise the exception
        encrypted_data = encrypted_data[:-1]

        # Decrypt the bytes, but fail gracefully
        with self.assertRaises(ValueError, msg="MAC check failed") as context:
            encryption.decrypt_bytes(encrypted_data, password)


class TestGenerateKey(unittest.TestCase):
    def test_generate_key(self):
        salt = b"salt"
        password = "password"

        # Test with default arguments
        key1, _ = encryption.generate_key(password=password, salt=salt)
        self.assertEqual(len(key1), 32)
        self.assertIsInstance(key1, bytes)
        self.assertEqual(
            key1,
            b"G\xfe\x7f\x81\xaeJO\t\xbcX\x8b=\x16\xab\xaa'\x1ch \x00\xa27\xc3\xc6I;\xfd\x1a\xf0\xeb$\xef",
        )

        # Test with different key length
        key2, _ = encryption.generate_key(password=password, salt=salt, key_length=64)
        self.assertEqual(len(key2), 64)
        self.assertIsInstance(key2, bytes)
        self.assertEqual(
            key2,
            b"G\xfe\x7f\x81\xaeJO\t\xbcX\x8b=\x16\xab\xaa'\x1ch \x00\xa27\xc3\xc6I;\xfd\x1a\xf0\xeb$\xef"
            b"N:\x18\xc4q\xffy\x90\xb2`\xb9\xc0\x17Ib\xb6pj\xbe\x90\x05\xb7&\xa1\r+&\xc3\xf2\xdc7X",
        )


class TestGenerateSalt(unittest.TestCase):
    def test_generate_salt(self):
        # Test salt generation with various sizes
        for size in [1, 16, 32, 64]:
            salt = encryption.generate_salt(size)
            self.assertEqual(len(salt), size)
            self.assertIsInstance(salt, bytes)

        # Test that different sizes produce different salts
        self.assertNotEqual(encryption.generate_salt(16), encryption.generate_salt(16))
        self.assertNotEqual(encryption.generate_salt(32), encryption.generate_salt(32))
        self.assertNotEqual(encryption.generate_salt(64), encryption.generate_salt(64))
