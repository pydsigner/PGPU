'''
Module to make it easier to write code compatible with both 2.x and 3.x.

AUTHORS:
v0.2.0+         --> pydsigner
'''

import sys

__all__ = ['input', 'range', 'chr', 'str', 'Print']

try:
    input = raw_input
    range = xrange
    chr = unichr
    str = unicode
    
    def Print(*args, **kw):
        '''
        Non version-specific printing utility emulating the 3.x print(), even
        down to its errors, so that any code using that won't break.

        keyword args: file, sep, end.

        Example:

        >>> fl = open("logger.txt", "w")
        >>> Print("spam", "eggs", sep = ", ", end = "!", file = fl)
        >>> fl.close()
        >>> fl = open("logger.txt")
        >>> fl.readlines()
        ["spam, eggs!"]
        
        AUTHORS:
        v0.2.0+         --> pydsigner
        '''
        if len(kw) > 3:
            raise TypeError(
                    'Print() takes at most 3 arguments (%s given)' % len(kw))
        
        fl = kw.pop('file', sys.stdout)
        sep = str(kw.pop('sep', ' '))
        end = str(kw.pop('end', '\n'))
        
        if kw:
            raise TypeError(
                    '\%s\' is an invalid keyword argument for this function' % 
                    kw.keys()[0])
        
        args = [str(a) for a in args]
        fl.write(sep.join(args) + end)

except NameError:
    # Hack to allow this assignment to go undetected in Python2
    Print = getattr(__builtins__, 'print')


