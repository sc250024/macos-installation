import datetime
import os.path
import pathlib
import tempfile
import unittest
from unittest import mock

from click.testing import CliRunner

from macos_installation import config
from macos_installation.cli_commands import cli
from tests import TestBase


class TestCliRunner(TestBase):
    def test_print_backup_locations(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["print-backup-locations"])
        self.assertEqual(result.exit_code, 0)

        for test_location in self.test_locations:
            self.assertIn(
                str(config.CURRENT_USER_HOME_DIR / test_location), result.output
            )

    def test_backup_restore(self):
        runner = CliRunner()
        with runner.isolated_filesystem() as isolated_area:
            ##########
            # Backup #
            ##########

            backup_file_name = f"test-{datetime.datetime.utcnow()}.zip"
            backup_file_path = os.path.join(isolated_area, backup_file_name)
            base_message = (
                f"Creating backup file '{backup_file_name}' of the following locations"
            )
            backup_dry_run_result = runner.invoke(
                cli, ["backup", "--backup-file", backup_file_path]
            )
            self.assertEqual(backup_dry_run_result.exit_code, 0)
            self.assertIn(f"[DRY-RUN] {base_message}", backup_dry_run_result.output)

            backup_real_result = runner.invoke(
                cli, ["--no-dry-run", "backup", "--backup-file", backup_file_path]
            )
            self.assertEqual(backup_real_result.exit_code, 0)
            self.assertIn(base_message, backup_real_result.output)

            ###########
            # Restore #
            ###########

            with mock.patch(
                "macos_installation.config.CURRENT_USER_HOME_DIR",
                pathlib.Path(tempfile.TemporaryDirectory().name),
            ):
                restore_result = runner.invoke(
                    cli, ["restore", "--restore-file", backup_file_path]
                )
                self.assertEqual(restore_result.exit_code, 0)

                for test_location in self.test_locations:
                    message = f" to '{config.CURRENT_USER_HOME_DIR / test_location}'"
                    self.assertIn(message, restore_result.output)


if __name__ == "__main__":
    unittest.main()