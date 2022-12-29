import pathlib
import string
import typing as t


def render_template(src: t.Union[pathlib.Path, str], sub: dict) -> str:
    """
    It takes a file path and a dictionary of substitutions, and returns the contents of the file with
    the substitutions applied

    :param src: The path to the template file
    :type src: t.Union[pathlib.Path, str]
    :param sub: A dictionary of substitutions to make in the template
    :type sub: dict
    :return: A string.
    """
    if isinstance(src, str):
        src = pathlib.Path(src)

    with src.open("r") as f:
        template = string.Template(f.read())

    return template.substitute(sub)
