import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from mikla import Mikla


class MiklaTest(unittest.TestCase):
    def setUp(self):
        self.mikla = Mikla()

    @patch('getpass.getpass')
    def test_get_password_match(self, mock_getpass):
        """
        Does the `get_password` method return a password if both
        entered passwords match?
        """
        mock_getpass.side_effect = ['Euclid', 'Euclid']

        self.assertEqual(self.mikla.get_password(), 'Euclid')

    @patch('getpass.getpass')
    def test_get_password_differ(self, mock_getpass):
        """
        Does the `get_password` method notify the user if the entered
        passwords don't match?
        """
        mock_getpass.side_effect = [
            'Descartes',
            'Locke',
            'Wittgenstein',
            'Wittgenstein',
        ]

        bucket = StringIO()

        with redirect_stdout(bucket):
            password = self.mikla.get_password()

        self.assertEqual(password, 'Wittgenstein')
        self.assertIn("Passwords don't match", bucket.getvalue())

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
