#!/usr/bin/env python3

import getpass
import logging
import os
import pathlib
import string
import sys
import typing

#############
# Constants #
#############

CURRENT_DIR: typing.Final = pathlib.Path(__file__).parent.absolute()
CURRENT_USER: typing.Final = getpass.getuser()
HOME_DIR: typing.Final = pathlib.Path.home()
DROPBOX_DIR: typing.Final = os.path.join(
    HOME_DIR.parent, CURRENT_USER, "Dropbox", "shell"
)
TEMPLATES_DIR: typing.Final = os.path.join(CURRENT_DIR, "templates")

SYMLINK_FILES: typing.Final = {
    os.path.join(DROPBOX_DIR, ".gitignore_global"): os.path.join(
        HOME_DIR, ".gitignore_global"
    ),
    os.path.join(DROPBOX_DIR, ".zshrc"): os.path.join(HOME_DIR, ".zshrc"),
}

SYMLINK_DIRS: typing.Final = {
    os.path.join(DROPBOX_DIR, ".git-template"): os.path.join(HOME_DIR, ".git-template"),
    os.path.join(DROPBOX_DIR, ".oh-my-zsh"): os.path.join(HOME_DIR, ".oh-my-zsh"),
    os.path.join(DROPBOX_DIR, "extra-zsh-completions"): os.path.join(
        HOME_DIR, "extra-zsh-completions"
    ),
}

#############
# Functions #
#############


def create_symlinks() -> None:
    """
    Create all symlinks in the home directory.
    """
    for src, dst in SYMLINK_FILES.items():
        pathlib.Path(dst).unlink(missing_ok=True)
        os.symlink(src=src, dst=dst)

    for src, dst in SYMLINK_DIRS.items():
        pathlib.Path(dst).unlink(missing_ok=True)
        os.symlink(src=src, dst=dst, target_is_directory=True)


def render_template(src: typing.Union[pathlib.PosixPath, str], sub: typing.Dict) -> str:
    """
    Renders a template using the standard library.
    """

    with open(src, "r") as f:
        template = string.Template(f.read())

    return template.substitute(sub)


def configure_git() -> None:
    """
    Configures Git for the new system.
    """
    sub = {"home_dir": HOME_DIR}
    gitconfig_filepath = os.path.join(HOME_DIR, ".gitconfig")

    # Render the contents of the 'gitconfig' file
    contents = render_template(src=os.path.join(TEMPLATES_DIR, ".gitconfig"), sub=sub)

    # Delete current config if it exists
    pathlib.Path(gitconfig_filepath).unlink(missing_ok=True)

    # Write the config
    with open(gitconfig_filepath, "w") as f:
        f.write(contents)

    # Set permissions on '.ssh' folder and 'config' file
    os.chmod(gitconfig_filepath, 0o644)


def configure_ssh() -> None:
    """
    Configures SSH for the new system.
    """
    sub = {"current_user": CURRENT_USER, "home_dir": HOME_DIR}
    ssh_filepath = os.path.join(HOME_DIR, ".ssh")
    ssh_config_filepath = os.path.join(ssh_filepath, "config")

    # Create '.ssh' directory
    pathlib.Path(ssh_filepath).mkdir(parents=True, exist_ok=True)

    # Render the contents of the 'config' file
    contents = render_template(
        src=os.path.join(TEMPLATES_DIR, "ssh", "config"), sub=sub
    )

    # Add 'UseKeychain' if macOS
    if sys.platform == "darwin":
        contents = contents + "    UseKeychain yes\n"

    # Write the config
    with open(ssh_config_filepath, "w") as f:
        f.write(contents)

    # Set permissions on '.ssh' folder and 'config' file
    os.chmod(ssh_filepath, 0o700)
    os.chmod(ssh_config_filepath, 0o600)


########
# Main #
########


def main() -> None:
    # Create home directory symlinks
    create_symlinks()

    # Git config
    configure_git()

    # SSH config
    configure_ssh()


if __name__ == "__main__":
    logging.basicConfig(
        level=(logging.DEBUG if os.getenv("DEBUG", None) is not None else logging.INFO)
    )
    main()
