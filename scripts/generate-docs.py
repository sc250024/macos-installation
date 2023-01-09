#!/usr/bin/env python3

import textwrap
import typing as t

import click

from macos_installation.cli import cli_entrypoint


def recursive_help(
    cmd: click.Command, parent: click.Context = None, section: str = "#"
) -> t.NoReturn:

    ctx = click.core.Context(cmd, info_name=cmd.name, parent=parent)

    if not parent:
        print(
            textwrap.dedent(
                """
                # CLI Documentation

                Quick reference for CLI commands and flags.

                ## macos-install
                """
            )
        )
    else:
        print(f"\n{section} {cmd.name}\n")

    print("```console")
    print(cmd.get_help(ctx))
    print("```")

    commands = getattr(cmd, "commands", {})

    for sub in commands.values():
        section = "###"
        recursive_help(cmd=sub, parent=ctx, section=section)


if __name__ == "__main__":
    recursive_help(cli_entrypoint)
