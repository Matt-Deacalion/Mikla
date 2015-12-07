from __future__ import print_function

import sys

from setuptools import setup

if sys.version_info[:2] < (3, 5):
    print('Mikla only runs on Python 3.5 or later', file=sys.stderr)
    sys.exit(1)

import mikla


setup(
    name='mikla',
    version=mikla.__version__.strip(),
    url='http://dirtymonkey.co.uk/mikla',
    license='MIT',
    author=mikla.__author__.strip(),
    author_email='matt@dirtymonkey.co.uk',
    description=mikla.__doc__.strip().replace('\n', ' '),
    long_description=open('README.rst').read(),
    keywords='encryption security gnupg gpg',
    packages=['mikla'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mikla = mikla.main:main',
        ],
    },
    install_requires=[
        'docopt>=0.6.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Security :: Cryptography',
        'Topic :: Communications',
        'Topic :: Utilities',
    ],
)
