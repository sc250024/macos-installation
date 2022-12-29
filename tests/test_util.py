import hashlib
import pathlib
import unittest
from datetime import datetime

from macos_installation.functions import util
from tests import TestBase


class TestCreateBackup(TestBase):
    def test_create_backup_file(self):
        # Create a backup of the temporary file
        suffix = "test"

        returned_path = util.create_backup(self.file1_path, suffix)
        expected_path = pathlib.Path(f"{self.file1_path}_{suffix}")

        self.assertTrue(expected_path.exists())
        self.assertEqual(expected_path, returned_path)

    def test_create_backup_dir(self):
        # Create a backup of the temporary directory
        returned_path = util.create_backup(self.temp_dir_path)

        date_time_str = datetime.now().strftime("%Y-%m-%d")
        expected_path = pathlib.Path(f"{self.temp_dir_path}_{date_time_str}")

        self.assertTrue(expected_path.exists())
        self.assertEqual(expected_path, returned_path)


class TestGetSHA256Hash(TestBase):
    def test_get_sha256_hash(self):
        expected_hash = hashlib.sha256(self.file1_content.encode()).hexdigest()
        self.assertEqual(
            util.get_file_sha256_hash(pathlib.Path(self.file1.name)), expected_hash
        )


class TestGetRecursiveFileList(TestBase):
    def test_get_recursive_file_list(self):

        # Find the files in the temporary directory
        paths = [self.temp_dir.name]
        files = list(util.get_recursive_file_list(paths))

        # Check that the correct files are found
        self.assertEqual(len(files), 5)
        self.assertIn(self.file1_path, files)
        self.assertIn(self.file2_path, files)
        self.assertIn(self.file3_path, files)
        self.assertIn(self.file4_path, files)
        self.assertIn(self.file5_path, files)


class TestGetTerminalSize(unittest.TestCase):
    def test_get_terminal_size(self):
        terminal_size = util.get_terminal_size()
        self.assertIsInstance(terminal_size, tuple)
        self.assertIsInstance(terminal_size[0], int)
        self.assertIsInstance(terminal_size[1], int)

    def test_get_terminal_size_fallback(self):
        terminal_size = util.get_terminal_size(fallback=(50, 100))
        self.assertEqual(terminal_size, (50, 100))


if __name__ == "__main__":
    unittest.main()
