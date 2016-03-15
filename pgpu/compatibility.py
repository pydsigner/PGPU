"""
Module to make it easier to write code compatible with both 2.x and 3.x.

AUTHORS:
v0.2.0+             --> pydsigner
v1.0.1+             --> pydsigner
"""

__all__ = ['input', 'range', 'chr', 'str', 'Print']

try:
    input = raw_input
    range = xrange
    chr = unichr
    str = unicode
except NameError:
    # Localize these names so that Python 3 can import them
    input = input
    range = range
    chr = chr
    str = str

Print = __builtins__.get('print')
