"""
A command line tool to edit text files encrypted with GnuPG whilst
preventing the plaintext from being written to the hard drive.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.0.1'

import getpass


class Mikla:
    def __init__(self):
        pass

    def get_password(self):
        """
        Prompts user for a password, returns password string.
        """
        while True:
            password = getpass.getpass('Enter password: ')

            if password == getpass.getpass('Verify password: '):
                return password

            print("Passwords don't match.")
