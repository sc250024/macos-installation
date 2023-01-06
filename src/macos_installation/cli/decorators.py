import pathlib
import typing as t

import click

from macos_installation import config


def common_backup_file(exists: bool = True) -> t.Callable:
    def inner_f(f):
        """
        The inner_f function is a decorator that takes the function f as an argument.
        It then adds the click option -b/--backup-file to it, which is required and has a help message.
        The inner_f function returns f with this added functionality.

        :param f: Pass the function to be decorated
        :return: The function f with the added option
        """
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
    """
    The common_password function is a decorator that adds the common password
    option to a click command. The common_password option is used for decrypting
    backup files and encrypting new backups. It has several options:

    :param confirmation_prompt:bool=True: Determine if the user should be prompted for a confirmation of their password
    :param prompt_required:bool=False: Determine if the password prompt should be shown
    :param required:bool=False: Tell click that the parameter is not required
    :return: A function that is decorated with the click
    """

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
