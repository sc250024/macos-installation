import getpass
import pathlib
import typing as t

from macos_installation.functions import util

# Basic variables
CURRENT_USER: t.Final[str] = getpass.getuser()
CURRENT_USER_HOME_DIR: t.Final[pathlib.Path] = pathlib.Path.home()
DEFAULT_ENCODING: t.Final[str] = "utf-8"
PACKAGE_DIR: t.Final[pathlib.Path] = (
    pathlib.Path(__file__).parent.joinpath("../").resolve()
)

# Compound variables
TEMPLATES_DIR: t.Final[pathlib.Path] = PACKAGE_DIR / "templates"

# CLI options
BASE_CLI_CONTEXT_SETTINGS = {
    "auto_envvar_prefix": "MACOS_INSTALL",
    "help_option_names": ["-h", "--help"],
    "ignore_unknown_options": True,
    "max_content_width": util.get_terminal_size()[0],
    "token_normalize_func": lambda x: x.lower(),
}
BASE_CLI_OPTIONS: t.Final[t.Dict[str, t.Any]] = {
    "show_default": True,
    "show_envvar": True,
}

# Files / directories to back up
BACKUP_LOCATIONS: t.List[pathlib.Path] = [
    CURRENT_USER_HOME_DIR / ".git-template",
    CURRENT_USER_HOME_DIR / ".gitconfig",
    CURRENT_USER_HOME_DIR / ".gitignore_global",
    CURRENT_USER_HOME_DIR / ".gnupg",
    CURRENT_USER_HOME_DIR / ".jump",
    CURRENT_USER_HOME_DIR / ".ssh",
    CURRENT_USER_HOME_DIR / ".vim",
    CURRENT_USER_HOME_DIR / ".vimrc",
    CURRENT_USER_HOME_DIR / ".zprofile",
    CURRENT_USER_HOME_DIR / ".zsh_history",
    CURRENT_USER_HOME_DIR / ".zshrc",
    CURRENT_USER_HOME_DIR / "iterm2-colors",
    CURRENT_USER_HOME_DIR / "iterm2-prefs",
]
