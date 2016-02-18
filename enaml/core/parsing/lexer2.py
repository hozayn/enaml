#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from .base_lexer import BaseEnamlLexer


class Python2EnamlLexer(BaseEnamlLexer):
    """Lexer specialized for Python 2.

    """

    lex_id = '2'

    reserved = dict(list(BaseEnamlLexer.reserved.items()) +
                    [('exec', 'EXEC'),
                     ('print', 'PRINT'),
                     ]
                    )
