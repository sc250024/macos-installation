import pathlib
import typing as t

import click

from macos_installation import config


def common_backup_file(exists: bool = True) -> t.Callable:
    def inner_f(f):
        f = click.option(
            "-b",
            "--backup-file",
            help="Location of backup/restore ZIP file",
            required=True,
            type=click.Path(exists=exists, path_type=pathlib.Path, resolve_path=True),
            **config.BASE_CLI_OPTIONS,
        )(f)

        return f

    return inner_f


def common_password(
    confirmation_prompt: bool = True,
    prompt_required: bool = False,
    required: bool = False,
) -> t.Callable:
    def inner_f(f):
        f = click.option(
            "-p",
            "--password",
            confirmation_prompt=confirmation_prompt,
            help="Password to decrypt/encrypt backup file",
            hide_input=True,
            prompt=True,
            prompt_required=prompt_required,
            required=required,
            type=str,
            **config.BASE_CLI_OPTIONS,
        )(f)

        return f

    return inner_f
