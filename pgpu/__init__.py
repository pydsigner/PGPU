'''
Pydsigner's Generic Python Utilities (PGPU) -- a collection of handy modules 
and packages for Python.

__init__        --  version information
compatibility   --  module to make it easier to write modules compatible with 
                    both 2.x and 3.x
iter_utils      --  generic iterable utilities
file_utils      --  file utility module
math_utils      --  utilities to work with bases plus some trig utilities
security        --  security and encoding module
time_widgets    --  tkinter time widgets
tk_utils        --  tkinter widgets and helper functions
wrappers        --  utility value wrappers for places requiring functions

tkinter2x       --  2.x and 3.x compatibility layer for tkinter


Version information.

NOTE: This module used to contain "Generic iterable utilities". This is now 
deprecated, with the corresponding functions moved to iter_utils. The 
compatibility layer in this module will be removed, perhaps in the next 
release.

AUTHORS:
v0.2.0+             --> pydsigner
v1.0.0+             --> pydsigner
'''
__version__ = '1.0.1'

import importlib
import functools

_warning = DeprecationWarning(
        'This function has been moved to iter_utils, and is now deprecated!')


def _runner(name, *args, **kw):
    raise _warning
    return getattr(importlib.import_module('iter_utils'), name)(*args, **kw)


replace_many = functools.partial(_runner, 'replace_many')
remove_many = functools.partial(_runner, 'remove_many')
keep_many = functools.partial(_runner, 'keep_many')
section = functools.partial(_runner, 'section')
find = functools.partial(_runner, 'find')
flatten = functools.partial(_runner, 'flatten')

del _runner, importlib, functools
