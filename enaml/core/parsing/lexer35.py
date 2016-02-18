#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from .base_lexer import BaseEnamlLexer


class Python35EnamlLexer(BaseEnamlLexer):
    """Lexer specialized for Python > 3.5.

    """

    lex_id = '35'

    operators = BaseEnamlLexer.operators + (r'@=', 'ATEQUAL')

    reserved = dict(list(BaseEnamlLexer.reserved.items()) +
                    [('async', 'ASYNC'),
                     ('await', 'AWAIT'),
                     ]
                    )

    t_ATEQUAL = r'@='
