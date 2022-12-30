# CLI Commands

## Table of Contents

- [CLI Commands](#cli-commands)
  - [Table of Contents](#table-of-contents)
  - [macos-install](#macos-install)
  - [backup](#backup)
  - [print-backup-locations](#print-backup-locations)
  - [restore](#restore)


## macos-install
Usage: macos-install [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug      Enable debug messages  [default: no-debug]
  --dry-run / --no-dry-run  Enable dry-run functionality  [default: dry-run]
  --help                    Show this message and exit.

Commands:
  backup                  Backup current macOS installation.
  print-backup-locations  Print base backup locations.
  restore                 Restore a previous macOS installation backup.

## backup
Usage: macos-install backup [OPTIONS]

  Backup current macOS installation.

Options:
  -b, --backup-file PATH     Location of backup zip file  [required]
  -l, --extra-location PATH  Extra location to back up; multiple allowed
  --help                     Show this message and exit.

## print-backup-locations
Usage: macos-install print-backup-locations [OPTIONS]

  Print base backup locations.

Options:
  -t, --tablefmt TEXT  Table format output (uses 'tabulate' module)  [default:
                       github]
  --help               Show this message and exit.

## restore
Usage: macos-install restore [OPTIONS]

  Restore a previous macOS installation backup.

Options:
  -r, --restore-file PATH  Location of restore ZIP file  [required]
  --help                   Show this message and exit.
