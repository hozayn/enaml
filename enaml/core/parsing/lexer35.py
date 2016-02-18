#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from .lexer3 import Python3EnamlLexer


class Python35EnamlLexer(Python3EnamlLexer):
    """Lexer specialized for Python > 3.5.

    """

    lex_id = '35'

    operators = Python3EnamlLexer.operators + (r'@=', 'ATEQUAL')

    reserved = dict(list(Python3EnamlLexer.reserved.items()) +
                    [('async', 'ASYNC'),
                     ('await', 'AWAIT'),
                     ]
                    )

    t_ATEQUAL = r'@='
