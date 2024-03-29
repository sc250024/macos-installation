
# CLI Documentation

Quick reference for CLI commands and flags.

## macos-install

```console
Usage: macos-install [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug      Enable debug messages  [default: no-debug]
  --dry-run / --no-dry-run  Enable dry-run functionality  [default: dry-run]
  --help                    Show this message and exit.

Commands:
  backup                  Backup current macOS installation.
  decrypt                 Decrypt an encrypted backup file.
  encrypt                 Encrypt an unencrypted backup file.
  print-backup-locations  Print base backup locations.
  restore                 Restore a previous macOS installation backup.
```

### backup

```console
Usage: macos-install backup [OPTIONS]

  Backup current macOS installation.

Options:
  -b, --backup-file PATH     Location of backup/restore ZIP file  [required]
  -l, --extra-location PATH  Extra location to back up; multiple allowed
  -p, --password TEXT        Password to decrypt/encrypt backup file
  --help                     Show this message and exit.
```

### decrypt

```console
Usage: macos-install decrypt [OPTIONS]

  Decrypt an encrypted backup file.

Options:
  -b, --backup-file PATH  Location of backup/restore ZIP file  [required]
  -p, --password TEXT     Password to decrypt/encrypt backup file  [required]
  --help                  Show this message and exit.
```

### encrypt

```console
Usage: macos-install encrypt [OPTIONS]

  Encrypt an unencrypted backup file.

Options:
  -b, --backup-file PATH  Location of backup/restore ZIP file  [required]
  -p, --password TEXT     Password to decrypt/encrypt backup file  [required]
  --help                  Show this message and exit.
```

### print-backup-locations

```console
Usage: macos-install print-backup-locations [OPTIONS]

  Print base backup locations.

Options:
  -t, --tablefmt TEXT  Table format output (uses 'tabulate' module)  [default:
                       github]
  --help               Show this message and exit.
```

### restore

```console
Usage: macos-install restore [OPTIONS]

  Restore a previous macOS installation backup.

Options:
  -b, --backup-file PATH  Location of backup/restore ZIP file  [required]
  -p, --password TEXT     Password to decrypt/encrypt backup file
  --help                  Show this message and exit.
```
