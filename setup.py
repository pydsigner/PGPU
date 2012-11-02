#! /usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

### Main setup stuff

import pgpu

NL = '\n'
# Get the first section, and convert all whitespace to spaces
description = ' '.join(pgpu.__doc__.strip().split(NL * 2, 1)[0].split())
# Get everything but the version info.
long_description = pgpu.__doc__.strip().rsplit(NL * 3, 1)[0]

def main():
    setup(script_args=(sys.argv[1:] if len(sys.argv) > 1 else ['install']),
          name='pgpu',
          version=pgpu.__version__,
          description=description,
          long_description=long_description,
          author='Daniel Foerster/pydsigner',
          author_email='pydsigner@gmail.com',
          packages=['pgpu','pgpu.tkinter2x'],
          # Convert this into a classifier
          license='LGPLv3',
          url='http://github.com/pydsigner/PGPU',
          classifiers=['Development Status :: 5 - Production/Stable',
                       'Intended Audience :: Developers',
                       'Operating System :: MacOS :: MacOS X',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: POSIX',
                       'Programming Language :: Python',])

if __name__ == '__main__':
    main()
