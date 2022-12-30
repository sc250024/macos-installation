import logging
import pathlib
import typing as t

import click
import coloredlogs

from macos_installation import config
from macos_installation.cli_commands.backup import BackupCommand
from macos_installation.cli_commands.print_backup_locations import (
    PrintBackupLocationsCommand,
)
from macos_installation.cli_commands.restore import RestoreCommand

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
def cli(ctx, **kwargs) -> None:
    ctx.ensure_object(dict)
    ctx.obj["debug"] = kwargs["debug"]
    ctx.obj["dry_run"] = kwargs["dry_run"]

    logging.basicConfig(
        level=(logging.DEBUG if kwargs.get("debug", None) is not None else logging.INFO)
    )
    coloredlogs.install(level=logging.DEBUG)


# ---------------------------------------------------------------------
# backup
# ---------------------------------------------------------------------


@cli.command("backup")
@click.option(
    "-b",
    "--backup-file",
    help="Location of backup zip file",
    required=True,
    type=click.Path(path_type=pathlib.Path, resolve_path=True),
    **config.BASE_CLI_OPTIONS,
)
@click.option(
    "-l",
    "--extra-location",
    help="Extra location to back up; multiple allowed",
    multiple=True,
    type=click.Path(exists=True, path_type=pathlib.Path, resolve_path=True),
    **config.BASE_CLI_OPTIONS,
)
@click.option(
    "-p",
    "--password",
    confirmation_prompt=True,
    help="Password to encrypt backup file",
    hide_input=True,
    prompt=True,
    prompt_required=False,
    type=str,
    **config.BASE_CLI_OPTIONS,
)
@click.pass_context
def backup(ctx, **kwargs) -> t.Any:
    """
    Backup current macOS installation.
    """
    params = {**ctx.obj, **kwargs}
    BackupCommand(**params).main()


# ---------------------------------------------------------------------
# print-backup-locations
# ---------------------------------------------------------------------


@cli.command("print-backup-locations")
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


@cli.command("restore")
@click.option(
    "-p",
    "--password",
    confirmation_prompt=True,
    help="Password to decrypt backup file",
    hide_input=True,
    prompt=True,
    prompt_required=False,
    type=str,
    **config.BASE_CLI_OPTIONS,
)
@click.option(
    "-r",
    "--restore-file",
    help="Location of restore ZIP file",
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path, resolve_path=True),
    **config.BASE_CLI_OPTIONS,
)
@click.pass_context
def restore(ctx, **kwargs) -> t.Any:
    """
    Restore a previous macOS installation backup.
    """
    params = {**ctx.obj, **kwargs}
    RestoreCommand(**params).main()
