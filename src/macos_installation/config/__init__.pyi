import pathlib
import typing as t

CURRENT_USER: t.Final[str]
CURRENT_USER_HOME_DIR: t.Final[pathlib.Path]
DEFAULT_ENCODING: t.Final[str]
PACKAGE_DIR: t.Final[pathlib.Path]
TEMPLATES_DIR: t.Final[pathlib.Path]
BASE_CLI_CONTEXT_SETTINGS: t.Final[t.Dict[str, t.Any]]
BASE_CLI_OPTIONS: t.Final[t.Dict[str, t.Any]]
BACKUP_LOCATIONS: t.List[pathlib.Path]
