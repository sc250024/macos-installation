# macos-installation

Files and scripts needed to perform installation of development environment on macOS.

## Table of Contents

- [macos-installation](#macos-installation)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
    - [Poetry](#poetry)
    - [Virtualenv](#virtualenv)
  - [Backup](#backup)
  - [Restore](#restore)
    - [Step 1: Homebrew](#step-1-homebrew)
    - [Step 2: Restore script](#step-2-restore-script)

## Install

To install the CLI tool, you can use one of the below methods depending on which package manager you use.

### Poetry

To install the CLI tool using Poetry, run the following commands:

```console
$ poetry shell
$ poetry install --sync --verbose

$ macos-install --help
Usage: macos-install [OPTIONS] COMMAND [ARGS]...
```

### Virtualenv

To install the CLI tool in the traditional way, run the following commands:

```console
$ python3 -m venv venv/
$ source venv/bin/activate
$ pip3 install -e .

$ macos-install --help
Usage: macos-install [OPTIONS] COMMAND [ARGS]...
```

## Backup

Examples of running a `backup` operation:

```console
# Simple backup; dry-run
$ macos-install backup --backup-file test-backup-$(date +%s).zip
[DRY-RUN] Creating backup file 'test-backup-1672389922.zip' of the following locations:
- /Users/<user>/.vimrc
- /Users/<user>/iterm2-prefs
...

# Simple backup; actually create the backup
$ macos-install --no-dry-run backup --backup-file test-backup-$(date +%s).zip
Creating backup file 'test-backup-1672389977.zip' of the following locations:
- /Users/<user>/.zshrc
- /Users/<user>/.gitignore_global
```

## Restore

The restore operation has two steps.

### Step 1: Homebrew

Run the following command to install all files from the `Brewfile`:

```console
$ brew bundle --file brew/Brewfile --verbose
```

### Step 2: Restore script

Examples of running a `restore` operation:

```console
$ macos-install restore --restore-file some-restore-file.zip
```
