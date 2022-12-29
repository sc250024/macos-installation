import typing as t

from macos_installation import config
from macos_installation.cli_commands import cli


def main() -> t.NoReturn:
    cli(**config.BASE_CLI_CONTEXT_SETTINGS)


if __name__ == "__main__":
    main()
