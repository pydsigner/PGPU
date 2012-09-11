#! /usr/bin/env python
'''
All `if __name__ == '__main__': do_x()` code has been transformed into this 
module.
'''

import random
import os
from os import listdir as ls
from os.path import join

from pgpu.compatibility import Print
from pgpu import security as sec
from pgpu import math_utils as m_u
from pgpu import file_utils as f_u
from pgpu import iter_utils as i_u


def rand_folder(d):
    return random.choice([join(d, f) for f in ls(d) 
                          if os.path.isdir(join(d, f))])


tests = {'security': [
            (sec.multi_pass, 'random_user', 'PiTH0N2012', 
                random.randint(500, 3000), sec.fetcher('sHa512'))], 
        'math_utils': [
            (m_u.convert_to_base, -100, 10), 
            (m_u.convert_to_base, 340.4, 30), 
            (m_u.convert_to_base, 560, 4.3), 
            (m_u.sgp_with_base, 534, 10), 
            (m_u.sgp_with_base, 353, 19), 
            (m_u.legs, 2), 
            (m_u.legs, random.randint(10, 30), (16, 9)), 
            (m_u.euclidean_dist, (3, 6), (5, 8)),
            (m_u.euclidean_dist, (9, 2), (7, 1)),
            (m_u.pascals_triangle, 5),
            (m_u.polyroots, 1, 2, 'x**3 - 2*x**2 - x + 2')
            (m_u.factor, 5),
            (m_u.factor, 34),
            (m_u.factor, 132),
            (m_u.factors,  36)],
        'file_utils': [(f_u.size_of_dir, rand_folder(os.environ['HOME']))],
        'iter_utils': [
            (i_u.replace_many, 'quantum_junk10', 
                {'1': '', '0': 'o', '_': ' '}), 
            (i_u.replace_many, 'quantum_junk10', {'a': '0', 'b': '1'}, True), 
            (i_u.remove_many, 'quantum_junk10', '_0123456789'), 
            (i_u.keep_many, 'quantum_junk10', 'abcdefghijklmnopq'), 
            (i_u.section, 'quantum_junk10', 3),
            (i_u.flatten, [1, [2, [3]], 4], 1)]
        }


def form(test):
    '''
    Builds a representation of a test as it might appear in normal code.
    '''
    shell = '%s.%s(%s)'
    com_module = test[0].__module__
    com_name = test[0].__name__
    argstring = ', '.join(repr(arg) for arg in test[1:])
    return shell % (com_module, com_name, argstring)


def main(tests = tests):
    for m in sorted(tests):
        Print('-' * 80, '-- Testing %s --' % m, '-' * 80, sep = '\n')
        for t in tests[m]:
            Print('>>>', form(t))
            Print(t[0](*t[1:]))
        Print()


if __name__ == '__main__':
    main()
