'''
File utility module.

AUTHORS:
v0.2.0+         --> pydsigner
'''

import os

FAIL = 0
SKIP = 1

def parse_conf(lines):
    '''
    A simple configuration file parser.
    this parser supports comments and multiple values assigned to one key. One
    possible gotcha is that every item will be returned as a list.
    
    >>> parse_conf(["q 1, 2, 3", "d   w", "# doesn't do anything"])
    {"q": ["1", "2", "3"], "d": ["w"]}
    
    AUTHORS:
    v0.2.0+         --> pydsigner
    '''
    dt = {}
    for l in lines:
        if l.startswith('#'):
            continue
        p = l.split(None, 1)
        dt[p[0]] = p[1].split(', ')
    return dt

def make_conf(data):
    '''
    A simple dict-to-configuration-file converter. designed to work with
    parse_conf(lines) above.
    Example:
    
    make_conf({"q": ["1", "2", "3"], "d": ["w"]})
    ["q 1, 2, 3", "d   w"]
    
    AUTHORS:
    v0.2.0+         --> pydsigner
    '''
    lines = []
    for k in data:
        lines.append(k + '\t' + ', '.join(data[k]))
    return lines

def size_of_dir(directory, error_handling = SKIP):
    '''
    Returns the overall size of directory @directory. @error_handling 
    determines whether OSError()'s will cause the function to fail.
    
    AUTHORS:
    v0.2.0+         --> pydsigner
    '''
    cwd = os.getcwd()
    d = os.path.abspath(directory)
    os.chdir(d)
    size = os.path.getsize(d)
    for f in os.listdir(d):
        try:
            if os.path.isdir(f):
                if not os.path.islink(f):
                    size += size_of_dir(f)
            else:
                if not os.path.islink(f):
                    size += os.path.getsize(f)
        
        except OSError:
            if error_handling == FAIL:
                raise
    os.chdir(cwd)
    return size

def exists_in_path(f, case = True):
    '''
    AUTHORS:
    v0.2.10+            --> pydsigner
    '''
    for p in os.environ['PATH'].split(os.path.pathsep):
        for i in os.listdir(p):
            if not case:
                if i.lower() == f.lower():
                    return p
            else:
                if i == f:
                    return p

if __name__ == '__main__':
    f = os.environ['HOME']
    s = size_of_dir(f)
    print('Size of ' + f + ':')
    if s < 1024 * 4:
        print('%s bytes' % s)
    elif s < 1024 ** 2* 4:
        print('%s kilobytes' % (s / 1024.0))
    elif s < 1024 ** 3 * 4:
        print('%s megabytes' % (s / 1024.0 ** 2))
    else:
        print('%s gigabytes' % (s / 1024.0 ** 3))
