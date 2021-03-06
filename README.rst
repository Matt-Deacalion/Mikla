=====
Mikla
=====

A command line tool to edit text files encrypted with GnuPG while keeping the decrypted plaintext
solely in RAM and off the hard drive. Preventing the plaintext from being recovered. This is
achieved using the POSIX shared memory API.

Installation
------------
You can install *Mikla* using pip:

.. code-block:: bash

    $ pip install mikla

Usage
-----
Use the `mikla` command to run Mikla::

    $ mikla --help

    Usage:
      mikla [--editor=<editor>] [--tmpfs=<path>] <encrypted-file>
      mikla (-h | --help | --version)

    Options:
      --version                   show program's version number and exit.
      -h, --help                  show this help message and exit.
      -e, --editor=<editor>       specify the editor to use [default: $EDITOR].
      -t, --tmpfs=<path>          the path to a temporary file system [default: /dev/shm].

License
-------
Copyright © 2017 `Matt Deacalion Stevens`_, released under The `MIT License`_.

.. _Matt Deacalion Stevens: http://dirtymonkey.co.uk
.. _MIT License: http://deacalion.mit-license.org
