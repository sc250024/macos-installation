import pathlib
import typing


# We use the `type(pathlib.Path())` for a tricky reason
# The `pathlib` module is very complicated in that it does some
# hacky stuff to account for the face that Posix and Windows paths
# are so different. Essentially, we use `type` to determine whether
# this class will inherit the `PosixPath` class, or the
# `WindowsPath` class.
class BaseItem(type(pathlib.Path())):
    def __new__(cls, src: str, **kwargs):
        return super(BaseItem, cls).__new__(cls, src)

    def __init__(self, src: str, overwrite: bool = False) -> typing.NoReturn:
        self.src = src
        self.overwrite = overwrite
