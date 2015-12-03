# coding=utf-8

"""Usage:
  mikla [--editor=<editor>] [--tmpfs=<path>] <encrypted-file>
  mikla (-h | --help | --version)

Options:
  --version                   show program's version number and exit.
  -h, --help                  show this help message and exit.
  -e, --editor=<editor>       specify the editor to use [default: $EDITOR].
  -t, --tmpfs=<path>          the path to a temporary file system [default: /dev/shm].
"""
from docopt import docopt

from mikla import __version__


def main():
    docopt(__doc__, version=__version__)

if __name__ == '__main__':
    main()
