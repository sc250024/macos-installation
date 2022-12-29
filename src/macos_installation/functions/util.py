import datetime
import hashlib
import pathlib
import shutil
import typing as t


def create_backup(path: pathlib.Path, suffix: str = None) -> pathlib.Path:
    """
    The create_backup function creates a backup of the specified file or directory.
    If the path is a file, then it will create a copy of that file with the current date and time as its suffix.
    If the path is a directory, then it will create an exact copy of that directory with the current date and time as its suffix.

    :param path:pathlib.Path: Specify the path to a file or directory
    :param suffix:str=None: Specify a suffix for the backup file
    :return: The path of the backup file or directory
    """
    # If no suffix specified, get the current date and time, and
    # format the date and time as a string in the format "YYYY-MM-DD_HH-MM-SS"
    suffix = suffix or datetime.datetime.now().strftime("%Y-%m-%d")

    new_path = pathlib.Path(f"{path}_{suffix}")

    # Check if the path is a file or a directory
    if path.is_file():
        # If the path is a file, create a backup of the file with the date and time suffix
        shutil.copy2(path, new_path)
        return new_path
    elif path.is_dir():
        # If the path is a directory, create a backup of the directory with the date and time suffix
        shutil.copytree(path, new_path, dirs_exist_ok=True)
        return new_path
    else:
        # If the path is neither a file nor a directory, raise an exception
        raise ValueError(f"{path} is neither a file nor a directory")


def get_recursive_file_list(
    locations: t.Iterable[t.Union[str, pathlib.Path]]
) -> t.Iterator[pathlib.Path]:
    """
    The get_recursive_file_list function accepts a list of file paths and returns a generator
    of all the files in those locations. If any of the input locations are directories, this function
    will recurse through each directory to find all files contained within it.

    :param locations:t.Iterable[t.Union[str, pathlib.Path]]: Specify the location of the files to be searched
    :return: A generator object that contains all the files the directories given
    """

    for location in locations:
        # First check if the input is string
        # Convert to 'pathlib.Path' object
        if isinstance(location, str):
            location = pathlib.Path(location)

        # If location is directory, recurse
        if location.is_dir():
            # Recursively search the directory for files
            for p in location.glob("**/*"):
                # Yield each file
                if p.is_file():
                    yield p
        # Otherwise give the file path back
        elif location.is_file():
            yield location


def get_file_sha256_hash(file_path: pathlib.Path) -> str:
    """
    The get_file_sha256_hash function accepts a pathlib.Path object representing the file to be hashed,
    and returns the SHA256 hash of that file as a string.

    :param file_path:pathlib.Path: Pass the file path to the function
    :return: The sha256 hash of the contents of a file
    """
    # Open the file in binary mode
    with file_path.open("rb") as f:
        # Read the contents of the file into memory
        contents = f.read()

    # Calculate the SHA256 hash of the contents
    return hashlib.sha256(contents).hexdigest()


def get_terminal_size(
    fallback: t.Optional[t.Tuple[int, int]] = (80, 24)
) -> t.Tuple[int, int]:
    """
    The get_terminal_size function returns the current terminal size.

    :param fallback:t.Optional[t.Tuple[int, int]]=(80, 24): Set a fallback value for the terminal size
    :return: The terminal size in rows and columns
    """
    try:
        # Get the terminal size using the shutil module
        rows, columns = shutil.get_terminal_size(fallback=fallback)
    except OSError:
        rows, columns = fallback

    return rows, columns
