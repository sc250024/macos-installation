import io
import unittest
import zipfile

from macos_installation.functions import compression, util
from tests import TestBase


class TestOpenZipFile(TestBase):
    def test_open_zip_file(self):
        # Set up test data and expected results
        zip_buffer = io.BytesIO()
        expected_result = ["file1.txt", "file2.txt"]

        # Use the context manager to open the ZIP file
        with compression.open_zip_file(zip_buffer) as zip_file:
            # Add the temporary files to the ZIP file
            zip_file.write(self.file1.name, "file1.txt")
            zip_file.write(self.file2.name, "file2.txt")

        # Seek to the beginning of the ZIP file buffer
        zip_buffer.seek(0)

        # Ensure the ZIP file contains the expected files
        result = zip_file.namelist()
        self.assertEqual(result, expected_result)


class TestCreateZipBuffer(TestBase):
    def test_create_zip_buffer(self):
        # Set up test data and expected results
        files = [p for p in util.get_recursive_file_list([self.temp_dir.name])]

        # Create the encrypted ZIP file
        zip_buffer = compression.create_zip_buffer(files)
        self.assertIsNotNone(zip_buffer)

        # Create a zip file from the buffer
        zip_file = zipfile.ZipFile(zip_buffer, "r")

        # Assert that the zip file contains the correct number of files
        self.assertEqual(len(zip_file.namelist()), len(files))

        # Assert that the zip file contains the correct filenames
        self.assertEqual(
            [f"/{name}" for name in zip_file.namelist()],
            [str(p.absolute()) for p in files],
        )

        # Close the zip file
        zip_file.close()


if __name__ == "__main__":
    unittest.main()
