"""
A command line tool to edit text files encrypted with GnuPG whilst
preventing the plaintext from being written to the hard drive.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.0.1'

import getpass
import os
import shutil
import uuid
from pathlib import Path


class Mikla:
    def __init__(self, **kwargs):
        self.ciphertext = kwargs.get('<encrypted-file>')
        self.tmpfs = kwargs.get('--tmpfs')
        self.editor = kwargs.get('--editor')

        if self.editor == '$EDITOR':
            self.editor = os.environ['EDITOR']

    def gpg_exists(self, gpg_executable='gpg'):
        """
        Returns `True` if GnuPG is installed, `False` if not.
        """
        return bool(shutil.which(gpg_executable))

    def get_password(self):
        """
        Prompts user for a password, returns password string.
        """
        while True:
            password = getpass.getpass('Enter password: ')

            if password == getpass.getpass('Verify password: '):
                return password

            print("Passwords don't match.")

    def get_available_file_path(self, directory):
        """
        Takes a directory string and returns an available file path.
        """
        while True:
            filepath = Path(directory) / str(uuid.uuid4())

            if not filepath.exists():
                return str(filepath)
