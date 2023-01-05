import os.path
import pathlib
import tempfile
import unittest
from unittest import mock

from click.testing import CliRunner

from macos_installation import config
from macos_installation.cli import cli_entrypoint
from tests import TestBase


class TestCliRunner(TestBase):
    def test_print_backup_locations(self):
        runner = CliRunner()
        result = runner.invoke(cli_entrypoint, ["print-backup-locations"])
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

            backup_file_name = "test.zip"
            backup_file_path = os.path.join(isolated_area, backup_file_name)
            base_message = (
                f"Creating backup file '{backup_file_name}' of the following locations"
            )
            backup_dry_run_result = runner.invoke(
                cli_entrypoint, ["backup", "--backup-file", backup_file_path]
            )
            self.assertEqual(backup_dry_run_result.exit_code, 0)
            self.assertIn(f"[DRY-RUN] {base_message}", backup_dry_run_result.output)

            backup_real_result = runner.invoke(
                cli_entrypoint,
                ["--no-dry-run", "backup", "--backup-file", backup_file_path],
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
                    cli_entrypoint,
                    ["--no-dry-run", "restore", "--backup-file", backup_file_path],
                )
                self.assertEqual(restore_result.exit_code, 0)

                for test_location in self.test_locations:
                    message = f" to '{config.CURRENT_USER_HOME_DIR / test_location}'"
                    self.assertIn(message, restore_result.output)

    def test_encrypted_backup_restore(self):
        runner = CliRunner()
        with runner.isolated_filesystem() as isolated_area:
            password = TestBase.generate_random_string(16)

            ##########
            # Backup #
            ##########

            backup_file_name = "test.zip"
            backup_file_path = os.path.join(isolated_area, backup_file_name)
            base_message = (
                f"Creating backup file '{backup_file_name}' of the following locations"
            )
            backup_dry_run_result = runner.invoke(
                cli_entrypoint,
                ["backup", "--backup-file", backup_file_path, "--password", password],
            )
            self.assertEqual(backup_dry_run_result.exit_code, 0)
            self.assertIn(f"[DRY-RUN] {base_message}", backup_dry_run_result.output)

            backup_real_result = runner.invoke(
                cli_entrypoint,
                [
                    "--no-dry-run",
                    "backup",
                    "--backup-file",
                    backup_file_path,
                    "--password",
                    password,
                ],
            )
            self.assertEqual(backup_real_result.exit_code, 0)
            self.assertIn(base_message, backup_real_result.output)

            ###########
            # Decrypt #
            ###########

            decrypt_result = runner.invoke(
                cli_entrypoint,
                [
                    "decrypt",
                    "--backup-file",
                    f"{backup_file_path}.enc",
                    "--password",
                    password,
                ],
            )
            self.assertEqual(decrypt_result.exit_code, 0)
            try:
                message = f"Decrypted file written to '{backup_file_path}'"
                self.assertIn(message, decrypt_result.output)
            except AssertionError:
                # Test may be running on macOS; try this as well
                message = f"Decrypted file written to '/private{backup_file_path}'"
                self.assertIn(message, decrypt_result.output)

            bad_password = password[:-2]
            decrypt_result = runner.invoke(
                cli_entrypoint,
                [
                    "decrypt",
                    "--backup-file",
                    f"{backup_file_path}.enc",
                    "--password",
                    bad_password,
                ],
            )
            self.assertEqual(decrypt_result.exit_code, 1)
            self.assertIn("was incorrect", decrypt_result.output)

            ###########
            # Restore #
            ###########

            with mock.patch(
                "macos_installation.config.CURRENT_USER_HOME_DIR",
                pathlib.Path(tempfile.TemporaryDirectory().name),
            ):
                restore_result = runner.invoke(
                    cli_entrypoint,
                    [
                        "--no-dry-run",
                        "restore",
                        "--backup-file",
                        f"{backup_file_path}.enc",
                        "--password",
                        password,
                    ],
                )
                self.assertEqual(restore_result.exit_code, 0)

                for test_location in self.test_locations:
                    message = f" to '{config.CURRENT_USER_HOME_DIR / test_location}'"
                    self.assertIn(message, restore_result.output)

            ###########
            # Encrypt #
            ###########

            encrypt_result = runner.invoke(
                cli_entrypoint,
                [
                    "encrypt",
                    "--backup-file",
                    backup_file_path,
                    "--password",
                    password,
                ],
            )
            self.assertEqual(encrypt_result.exit_code, 0)
            try:
                message = f"Encrypted file written to '{backup_file_path}.enc'"
                self.assertIn(message, encrypt_result.output)
            except AssertionError:
                # Test may be running on macOS; try this as well
                message = f"Encrypted file written to '/private{backup_file_path}.enc'"
                self.assertIn(message, encrypt_result.output)


if __name__ == "__main__":
    unittest.main()
