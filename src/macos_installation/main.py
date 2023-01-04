import typing as t

from macos_installation import config
from macos_installation.cli import cli_entrypoint


def main() -> t.NoReturn:
    cli_entrypoint(**config.BASE_CLI_CONTEXT_SETTINGS)


if __name__ == "__main__":
    main()
