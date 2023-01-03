import logging
import pathlib
import typing as t

import click
import coloredlogs

from macos_installation import config
from macos_installation.classes.zip import InMemoryZip
from macos_installation.cli import decorators
from macos_installation.cli.backup import BackupCommand
from macos_installation.cli.decrypt import DecryptCommand
from macos_installation.cli.encrypt import EncryptCommand
from macos_installation.cli.print_backup_locations import PrintBackupLocationsCommand
from macos_installation.cli.restore import RestoreCommand

# ---------------------------------------------------------------------
# Main CLI group
# ---------------------------------------------------------------------


@click.group()
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Enable debug messages",
    **config.BASE_CLI_OPTIONS,
)
@click.option(
    "--dry-run/--no-dry-run",
    default=True,
    help="Enable dry-run functionality",
    **config.BASE_CLI_OPTIONS,
)
@click.pass_context
def cli_entrypoint(ctx, **kwargs) -> None:
    ctx.ensure_object(dict)
    ctx.obj["debug"] = kwargs["debug"]
    ctx.obj["dry_run"] = kwargs["dry_run"]

    level = logging.DEBUG if kwargs.get("debug", False) else logging.INFO

    logging.basicConfig(level=level)
    coloredlogs.install(level=level)


# ---------------------------------------------------------------------
# backup
# ---------------------------------------------------------------------


@cli_entrypoint.command("backup")
@decorators.common_backup_file(exists=False)
@click.option(
    "-l",
    "--extra-location",
    help="Extra location to back up; multiple allowed",
    multiple=True,
    type=click.Path(exists=True, path_type=pathlib.Path, resolve_path=True),
    **config.BASE_CLI_OPTIONS,
)
@decorators.common_password()
@click.pass_context
def backup(ctx, **kwargs) -> t.Any:
    """
    Backup current macOS installation.
    """
    params = {**ctx.obj, **kwargs}
    zip_object = InMemoryZip(password=kwargs["password"])

    BackupCommand(zip_object, **params).main()


# ---------------------------------------------------------------------
# decrypt
# ---------------------------------------------------------------------


@cli_entrypoint.command("decrypt")
@decorators.common_backup_file()
@decorators.common_password(
    confirmation_prompt=False, prompt_required=True, required=True
)
@click.pass_context
def decrypt(ctx, **kwargs) -> t.Any:
    """
    Decrypt an encrypted backup file.
    """
    params = {**ctx.obj, **kwargs}
    zip_object = InMemoryZip(kwargs["backup_file"], kwargs["password"])

    DecryptCommand(zip_object, **params).main()


# ---------------------------------------------------------------------
# encrypt
# ---------------------------------------------------------------------


@cli_entrypoint.command("encrypt")
@decorators.common_backup_file()
@decorators.common_password(prompt_required=True, required=True)
@click.pass_context
def encrypt(ctx, **kwargs) -> t.Any:
    """
    Encrypt an unencrypted backup file.
    """
    params = {**ctx.obj, **kwargs}
    zip_object = InMemoryZip(kwargs["backup_file"], kwargs["password"])

    EncryptCommand(zip_object, **params).main()


# ---------------------------------------------------------------------
# print-backup-locations
# ---------------------------------------------------------------------


@cli_entrypoint.command("print-backup-locations")
@click.option(
    "-t",
    "--tablefmt",
    default="github",
    help="Table format output (uses 'tabulate' module)",
    type=str,
    **config.BASE_CLI_OPTIONS,
)
@click.pass_context
def print_backup_locations(ctx, **kwargs) -> t.Any:
    """
    Print base backup locations.
    """
    params = {**ctx.obj, **kwargs}
    click.secho(
        f"==> Printing backup files / folders for user '{config.CURRENT_USER}'",
        fg="green",
    )
    PrintBackupLocationsCommand(**params).main()


# ---------------------------------------------------------------------
# restore
# ---------------------------------------------------------------------


@cli_entrypoint.command("restore")
@decorators.common_backup_file()
@decorators.common_password(confirmation_prompt=False)
@click.pass_context
def restore(ctx, **kwargs) -> t.Any:
    """
    Restore a previous macOS installation backup.
    """
    params = {**ctx.obj, **kwargs}
    zip_object = InMemoryZip(kwargs["backup_file"], kwargs["password"])

    RestoreCommand(zip_object, **params).main()
