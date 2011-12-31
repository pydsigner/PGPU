#! /usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
import sys

#############################################################################
### Main setup stuff
#############################################################################

def main():
	
	# perform the setup action
	import pgpu
	setup_args = {
		'script_args': sys.argv[1:] if len(sys.argv) > 1 else ['install'],
		'name': "pgpu",
		'version': pgpu.__version__,
		'description': "Pydsigner's Generic Python Utilities - a collection of "
		"handy modules and scripts for Python.",
		'long_description': "Pydsigner's Generic Python Utilities"
		''' - a collection of handy modules and packages for Python.

__init__		--	generic iterable utilities
compatibility	--	module to make it easier to write modules compatible with 
					both 2.x and 3.x
file_utils		--	file utility module
math_utils		--	utilities to work with bases plus some trig utilities
security		--	security and encoding module
time_widgets	--	tkinter time widgets
tk_utils		--	tkinter widgets and helper functions
wrappers		--	utility value wrappers for places requiring functions

tkinter2x		--	2.x and 3.x compatibility layer for tkinter

''',
		'author': "Daniel Foerster/pydsigner",
		'author_email': "pydsigner@gmail.com",
		'packages': ['pgpu','pgpu.tkinter2x'],
		'license': 'GPLv2',
		'url': "http://github.com/pydsigner/PGPU",
		'classifiers': [
			'Development Status :: 4 - Beta',
			'Intended Audience :: Developers',
			'Operating System :: MacOS :: MacOS X',
			'Operating System :: Microsoft :: Windows',
			'Operating System :: POSIX',
			'Programming Language :: Python',
		]}
	setup(**setup_args)

if __name__ == '__main__':
	main()
