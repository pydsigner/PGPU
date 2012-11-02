#! /usr/bin/env python
"""
All `if __name__ == '__main__': do_x()` code has been transformed into this 
module.
"""

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


tests = {'math_utils': [
            (m_u.convert_to_base, repr('-100'), -100, 10), 
            (m_u.convert_to_base, repr('ba'), 340.4, 30), 
            (m_u.convert_to_base, repr('20300'), 560, 4.3), 
            (m_u.sgp_with_base, repr(3), 534, 10), 
            (m_u.sgp_with_base, repr(2), 353, 19), 
            (m_u.legs, repr((1.414213562373095, 1.414213562373095)), 2), 
            (m_u.legs, repr((11.33048198261914, 6.373396115223267)), 13, 
             (16, 9)), 
            (m_u.euclidean_dist, repr(2.8284271247461903), (3, 6), (5, 8)),
            (m_u.euclidean_dist, repr(2.23606797749979), (9, 2), (7, 1)),
            (m_u.pascals_triangle, repr([[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], 
                                        [1, 4, 6, 4, 1]]), 
             5),
            (m_u.polyroots, repr(set([1, 2, -1])), 1, 2, 
             'x**3 - 2*x**2 - x + 2'),
            (m_u.factor, repr([]), 5),
            (m_u.factor, repr([2, 17]), 34),
            (m_u.factor, repr([2, 2, 3, 11]), 132),
            (m_u.factors, repr(set([1, 2, 3, 4, 6, 9, 12, 18, 36])),  36)],
        'file_utils': [(f_u.size_of_dir, 'a number depending upon the folder ' 
                                         'chosen; check your FS to determine ' 
                                         'accuracy', 
                        rand_folder(os.environ['HOME']))],
        'iter_utils': [
            (i_u.replace_many, repr('quantum junko'), 'quantum_junk10', 
             {'1': '', '0': 'o', '_': ' '}), 
            (i_u.replace_many, repr('quantum_junkba'), 'quantum_junk10', 
             {'a': '0', 'b': '1'}, True), 
            (i_u.remove_many, repr('quantumjunk'), 'quantum_junk10', 
             '_0123456789'), 
            (i_u.keep_many, repr('qanmjnk'), 'quantum_junk10', 
             'abcdefghijklmnopq'), 
            (i_u.section, repr(['qua', 'ntu', 'm_j', 'unk', '10']), 
             'quantum_junk10', 3),
            (i_u.flatten, repr([1, 2, [3], 4]), [1, [2, [3]], 4], 1)]
        }


def form(test):
    """
    Builds a representation of a test as it might appear in normal code.
    """
    shell = '%s.%s(%s)'
    com_module = test[0].__module__
    com_name = test[0].__name__
    argstring = ', '.join(repr(arg) for arg in test[2:])
    return shell % (com_module, com_name, argstring)


def main(tests=tests):
    for m in sorted(tests):
        Print('-' * 80, '-- Testing %s --' % m, '-' * 80, sep = '\n')
        for t in tests[m]:
            Print('>>> # Should be', t[1])
            Print('...', form(t))
            Print(repr(t[0](*t[2:])))
            Print()


if __name__ == '__main__':
    main()
