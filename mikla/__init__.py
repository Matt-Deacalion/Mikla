"""
A command line tool to edit text files encrypted with GnuPG whilst
preventing the plaintext from being written to the hard drive.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.0.1'

import getpass
import os
import shutil
import subprocess
import uuid
from pathlib import Path


class Mikla:
    def __init__(self, **kwargs):
        self.encrypted_file = kwargs.get('<encrypted-file>')
        self.tmpfs = kwargs.get('--tmpfs')
        self.editor = kwargs.get('--editor')

        if self.editor == '$EDITOR':
            self.editor = os.environ['EDITOR']

    def decrypt(self, password, encrypted_file=None, tmpfs=None):
        """
        Takes a password string, an encrypted file path and a
        temporary filesystem path. Then decrypts the encrypted file
        using GnuPG. Returns the path to a file containing the
        plaintext.
        """
        if encrypted_file is None:
            encrypted_file = self.encrypted_file

        if tmpfs is None:
            tmpfs = self.tmpfs

        # do all of the checking manually,
        # so we don't pointlessly run GnuPG
        if not self.gpg_exists():
            raise FileNotFoundError('GnuPG not installed')

        if not os.access(encrypted_file, os.F_OK):
            raise FileNotFoundError(
                'File not found: {}'.format(encrypted_file),
            )

        if not os.access(encrypted_file, os.R_OK):
            raise FileNotFoundError(
                'File not readable: {}'.format(encrypted_file),
            )

        if not os.access(tmpfs, os.W_OK):
            raise FileNotFoundError(
                'tmpfs directory not writable: {}'.format(tmpfs),
            )

        plaintext_path = self.get_available_file_path(tmpfs)

        completed_process = subprocess.run(
            [
                'gpg',
                '--decrypt',
                '--batch',
                '--passphrase',
                password,
                '--output',
                plaintext_path,
                encrypted_file,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if completed_process.returncode != 0:
            raise RuntimeError(
                'Decryption of "{}" failed'.format(encrypted_file),
            )

        return plaintext_path

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
