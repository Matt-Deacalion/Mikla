"""
A command line tool to edit text files encrypted with GnuPG whilst
preventing the plaintext from being written to the hard drive.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.2.1'

import getpass
import hashlib
import os
import shutil
import subprocess
import uuid
from pathlib import Path


class Mikla:
    def __init__(self, **kwargs):
        self.encrypted = kwargs.get('<encrypted-file>')
        self.tmpfs = kwargs.get('--tmpfs')
        self.editor = kwargs.get('--editor')

        if self.editor == '$EDITOR':
            self.editor = os.environ['EDITOR']

    def run(self):
        """
        Call to run Mikla.
        """
        self.system_checks()

        password = getpass.getpass()
        plaintext = self.decrypt(password)

        if self.launch_editor(plaintext):
            self.encrypt(password, plaintext)

        os.unlink(plaintext)

    def launch_editor(self, plain, editor=None):
        """
        Takes a plaintext path and launches the text editor. Returns
        `True` if the plaintext file was changed while the text
        editor was running.
        """
        if editor is None:
            editor = self.editor

        before_checksum = self.checksum(plain)

        subprocess.run([editor, plain])

        return before_checksum != self.checksum(plain)

    def checksum(self, text_file):
        """
        Takes a path to a text file and returns a string containing
        the SHA1 checksum digest for it's content.
        """
        hasher = hashlib.sha1()
        hasher.update(open(text_file).read().encode())

        return hasher.hexdigest()

    def encrypt(self, password, plain, encrypted=None):
        """
        Takes a password string, a plaintext file path and an
        encrypted file path. Then encrypts the plaintext file to the
        encrypted path.
        """
        if encrypted is None:
            encrypted = self.encrypted

        backup = '{}.bak'.format(encrypted)
        shutil.move(encrypted, backup)

        completed_process = subprocess.run(
            [
                'gpg',
                '--symmetric',
                '--armor',
                '--batch',
                '--passphrase',
                password,
                '--output',
                encrypted,
                plain,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if completed_process.returncode == 0:
            os.unlink(backup)
        else:
            shutil.move(backup, encrypted)

            raise RuntimeError(
                'Encryption of "{}" failed'.format(plain),
            )

    def decrypt(self, password, encrypted=None, tmpfs=None):
        """
        Takes a password string, an encrypted file path and a
        temporary filesystem path. Then decrypts the encrypted file
        using GnuPG. Returns the path to a file containing the
        plaintext.
        """
        if encrypted is None:
            encrypted = self.encrypted

        if tmpfs is None:
            tmpfs = self.tmpfs

        plain = self.get_available_file_path(tmpfs)

        completed_process = subprocess.run(
            [
                'gpg',
                '--decrypt',
                '--batch',
                '--passphrase',
                password,
                '--output',
                plain,
                encrypted,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if completed_process.returncode != 0:
            raise RuntimeError(
                'Decryption of "{}" failed, '
                'was the password correct?'.format(encrypted),
            )

        return plain

    def gpg_exists(self, gpg_executable='gpg'):
        """
        Returns `True` if GnuPG is installed, `False` if not.
        """
        return bool(shutil.which(gpg_executable))

    def get_available_file_path(self, directory):
        """
        Takes a directory string and returns an available file path.
        """
        while True:
            filepath = Path(directory) / str(uuid.uuid4())

            if not filepath.exists():
                return str(filepath)

    def system_checks(self, encrypted=None, tmpfs=None):
        """
        Perform system checks. Instead of catching exceptions this is
        done manually so we don't pointlessly run GnuPG.
        """
        if encrypted is None:
            encrypted = self.encrypted

        if tmpfs is None:
            tmpfs = self.tmpfs

        if not self.gpg_exists():
            raise FileNotFoundError('GnuPG not installed')

        if not os.access(encrypted, os.F_OK):
            raise FileNotFoundError(
                'File not found: {}'.format(encrypted),
            )

        if not os.access(encrypted, os.R_OK):
            raise FileNotFoundError(
                'File not readable: {}'.format(encrypted),
            )

        if not os.access(tmpfs, os.W_OK):
            raise FileNotFoundError(
                'tmpfs directory not writable: {}'.format(tmpfs),
            )
