import pathlib
import random
import string
import tempfile
import typing as t
import unittest


class TestBase(unittest.TestCase):
    maxDiff = None

    @staticmethod
    def generate_random_string(length: int = 100) -> str:
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
        )

    @staticmethod
    def create_temp_file_with_content(
        path: pathlib.Path,
    ) -> t.Tuple[tempfile.NamedTemporaryFile, pathlib.Path, str]:

        temp_file = tempfile.NamedTemporaryFile("w+t", dir=path, delete=False)
        temp_file_path = pathlib.Path(temp_file.name)

        temp_file_content = TestBase.generate_random_string()
        temp_file.write(temp_file_content)
        temp_file.seek(0)

        return temp_file, temp_file_path, temp_file_content

    def setUp(self) -> t.NoReturn:
        # Create a temporary directory for various functions
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = pathlib.Path(self.temp_dir.name)

        # Create temporary files with content
        (
            self.file1,
            self.file1_path,
            self.file1_content,
        ) = TestBase.create_temp_file_with_content(self.temp_dir_path)
        (
            self.file2,
            self.file2_path,
            self.file2_content,
        ) = TestBase.create_temp_file_with_content(self.temp_dir_path)
        (
            self.file3,
            self.file3_path,
            self.file3_content,
        ) = TestBase.create_temp_file_with_content(self.temp_dir_path)

        # Create a subdirectory in the temporary directory
        self.sub_dir = tempfile.TemporaryDirectory(dir=self.temp_dir.name)
        self.sub_dir_path = pathlib.Path(self.sub_dir.name)

        # Create temporary files in subdirectory with content
        (
            self.file4,
            self.file4_path,
            self.file4_content,
        ) = TestBase.create_temp_file_with_content(self.sub_dir_path)
        (
            self.file5,
            self.file5_path,
            self.file5_content,
        ) = TestBase.create_temp_file_with_content(self.sub_dir_path)

        # Test locations
        self.test_locations: t.List = [".gitconfig", ".ssh", ".vim", "iterm2-colors"]

    def tearDown(self) -> t.NoReturn:
        self.temp_dir.cleanup()
