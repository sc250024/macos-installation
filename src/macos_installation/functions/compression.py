import contextlib
import io
import pathlib
import typing as t
import zipfile


@contextlib.contextmanager
def open_zip_file(
    zip_buffer: t.IO[bytes], mode: t.Literal["r", "w", "x", "a"] = "w"
) -> zipfile.ZipFile:
    """
    The open_zip_file function opens a zip file for reading or writing.

    :param zip_buffer:t.IO[bytes]: Pass the zip file buffer to the function
    :param mode:t.Literal["r", "w", "x", "a"]="w": Specify the mode in which the file is opened
    :return: A zipfile object
    """
    zip_file = zipfile.ZipFile(
        file=zip_buffer, mode=mode, compression=zipfile.ZIP_DEFLATED
    )
    try:
        yield zip_file
    finally:
        zip_file.close()


def create_zip_buffer(locations: t.List[pathlib.Path]) -> t.IO[bytes]:
    """
    The create_zip_buffer function creates a ZIP file in memory and returns it as a bytes object.

    :param locations:t.List[pathlib.Path]: Pass a list of locations that should be added to the zip file
    :return: A bytesio object that contains the zip file
    """
    # Create a new ZIP file object in memory
    zip_buffer = io.BytesIO()

    # Open the ZIP file with a context manager
    with open_zip_file(zip_buffer=zip_buffer) as zip_file:
        for location in locations:
            zip_file.write(location)

    # Seek to the beginning of the ZIP file buffer
    zip_buffer.seek(0)

    # Return the ZIP file object
    return zip_buffer
