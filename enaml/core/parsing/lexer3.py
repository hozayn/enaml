#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from .base_lexer import BaseEnamlLexer


class Python3EnamlLexer(BaseEnamlLexer):
    """Lexer specialized for Python > 3.5.

    """
    operators = BaseEnamlLexer.operators + ('->', 'RETURNARROW')

    reserved = dict(list(BaseEnamlLexer.reserved.items()) +
                    [('nonlocal', 'NONLOCAL'),
                     ]
                    )
