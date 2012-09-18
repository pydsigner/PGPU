#! /usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

### Main setup stuff

import pgpu

NL = '\n'

def main():
    
    # perform the setup action
    setup_args = {
        'script_args': (sys.argv[1:] if len(sys.argv) > 1 
                        else ['install']),
        'name': 'pgpu',
        'version': pgpu.__version__,
        'description': pgpu.__doc__.strip().split(NL * 2, 1)[0],
        'long_description': pgpu.__doc__.strip().rsplit(NL * 3, 1)[0],
        'author': 'Daniel Foerster/pydsigner',
        'author_email': 'pydsigner@gmail.com',
        'packages': ['pgpu','pgpu.tkinter2x'],
        'license': 'LGPLv3',
        'url': 'http://github.com/pydsigner/PGPU',
        'classifiers': [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
        ]}
    setup(**setup_args)

if __name__ == '__main__':
    main()
