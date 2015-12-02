import unittest
from pathlib import Path
from unittest.mock import patch

from mikla import Mikla


class MiklaTest(unittest.TestCase):
    def setUp(self):
        self.mikla = Mikla()

    @patch('uuid.uuid4')
    def test_get_available_file_path_exists(self, mock_uuid4):
        """
        Does the `get_available_file_path` method return an available
        file path?
        """
        mock_uuid4.side_effect = ['Voltaire', 'Franklin']

        directory = Path(__file__, '..').resolve()
        taken_file = directory / 'Voltaire'

        taken_file.write_text('Common sense is not so common.')

        self.assertEqual(
            self.mikla.get_available_file_path(directory),
            str(directory / 'Franklin'),
        )

        taken_file.unlink()

    def test_gpg_exists(self):
        """
        Does the `gpg_exists` method return `True` if an executable
        exists?
        """
        self.assertTrue(self.mikla.gpg_exists('ls'))

    def test_gpg_not_exist(self):
        """
        Does the `gpg_exists` method return `False` if an executable
        does not exist?
        """
        self.assertFalse(self.mikla.gpg_exists('the-amber-room'))

    @patch('mikla.subprocess')
    @patch('mikla.shutil')
    @patch('mikla.os')
    def test_encrypt_creates_and_cleans_up_backup(
        self,
        mock_os,
        mock_shutil,
        mock_subprocess,
    ):
        """
        The `encrypt` method should create a backup copy of the
        encrypted file and only remove it if the encryption process
        is successful.
        """
        mock_subprocess.run.return_value.returncode = 0

        self.mikla.encrypt('Chunky Hunky', 'plain', 'enc')

        mock_shutil.move.assert_called_once_with('enc', 'enc.bak')
        mock_os.unlink.assert_called_once_with('enc.bak')

    @patch('mikla.subprocess')
    @patch('mikla.shutil')
    @patch('mikla.os')
    def test_encrypt_creates_and_restores_backup(
        self,
        mock_os,
        mock_shutil,
        mock_subprocess,
    ):
        """
        The `encrypt` method should create a backup copy of the
        encrypted file and restore it to it's original name if the
        encryption process is unsuccessful.
        """
        mock_subprocess.run.return_value.returncode = 1

        with self.assertRaises(RuntimeError):
            self.mikla.encrypt('Chunky Hunky', 'plain', 'enc')

        mock_os.unlink.assert_not_called()
        mock_shutil.move.assert_called_with('enc.bak', 'enc')
        self.assertEqual(mock_shutil.move.call_count, 2)
