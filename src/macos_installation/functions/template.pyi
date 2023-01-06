import pathlib
import typing as t

def render_template(src: t.Union[pathlib.Path, str], sub: dict) -> str: ...
