#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from future.builtins import bytes

from .base_lexer import BaseEnamlLexer


class Python3EnamlLexer(BaseEnamlLexer):
    """Lexer specialized for Python.

    """
    operators = BaseEnamlLexer.operators + ((r'->', 'RETURNARROW'),)

    reserved = dict(list(BaseEnamlLexer.reserved.items()) +
                    [('nonlocal', 'NONLOCAL'),
                     ]
                    )

    def format_string(self, string, quote_type):
        """Python support u r and b as quote type.

        """
        if quote_type == "" or quote_type == "u" or quote_type == "ur":
            u8 = string.encode('utf-8')
            if quote_type == "ur":
                aux = u8.decode('raw_unicode_escape')
            else:
                aux = u8.decode('unicode_escape')
            return aux.encode('latin-1').decode('utf-8')
        elif quote_type == "r":
            return string
        elif quote_type == "b":
            return bytes(string)
        else:
            msg = 'Unknown string quote type: %r' % quote_type
            raise AssertionError(msg)


class Python34EnamlLexer(Python3EnamlLexer):
    """Lexer specialized for Python.

    """
    reserved = dict(list(Python3EnamlLexer.reserved.items()) +
                    [('True', 'TRUE'),
                     ('False', 'FALSE'),
                     ('None', 'NONE'),
                     ]
                    )


class Python35EnamlLexer(Python34EnamlLexer):
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
