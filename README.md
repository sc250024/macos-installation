# macos-installation

Files and scripts needed to perform installation of development environment on macOS.

## Table of Contents

- [macos-installation](#macos-installation)
  - [Table of Contents](#table-of-contents)
  - [Restoration](#restoration)
    - [1. Homebrew](#1-homebrew)
    - [2. Restore script](#2-restore-script)

## Restoration

### 1. Homebrew

Run the following command to install all files from the `Brewfile`:

```console
$ brew bundle --file brew/Brewfile --verbose
```

### 2. Restore script

Run the following command to run the restore script:

```console
$ python3 restore.py
```
