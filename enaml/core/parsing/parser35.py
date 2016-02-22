#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import ast

from .lexer3 import Python35EnamlLexer
from .parser34 import Python34EnamlParser


class Python35EnamlParser(Python34EnamlParser):
    """Enaml parser supporting Python 3.4 syntax.

    Main differences from base parser are :


    """
    parser_id = '35'

    lexer = Python35EnamlLexer

    augassign_table = dict(list(Python34EnamlParser.augassign_table.items()) +
                           [('@=', ast.MatMult)])

    _NOTIFICATION_DISALLOWED =\
        dict(list(Python34EnamlParser._NOTIFICATION_DISALLOWED.items()) +
             [(ast.AsyncFuncDef, 'async function definition')])

    def p_augassign(self, p):
        ''' augassign : AMPEREQUAL
                      | CIRCUMFLEXEQUAL
                      | DOUBLESLASHEQUAL
                      | DOUBLESTAREQUAL
                      | LEFTSHIFTEQUAL
                      | MINUSEQUAL
                      | PERCENTEQUAL
                      | PLUSEQUAL
                      | RIGHTSHIFTEQUAL
                      | SLASHEQUAL
                      | STAREQUAL
                      | VBAREQUAL
                      | ATEQUAL '''
        super(Python35EnamlParser, self).p_augassign(p)

    def p_compound_stmt(self, p):
        ''' compound_stmt : if_stmt
                          | while_stmt
                          | for_stmt
                          | try_stmt
                          | with_stmt
                          | funcdef
                          | async_funcdef
                          | classdef
                          | decorated '''
        super(Python35EnamlParser, self).p_compound_stmt(p)

    def p_decorated(self, p):
        ''' decorated : decorators funcdef
                      | decorators classdef
                      | decorators async_funcdef'''
        decs = p[1]
        target = p[2]
        target.decorator_list = decs
        p[0] = target

    def p_async_funcdef1(self, p):
        ''' funcdef : ASYNC DEF NAME parameters COLON suite '''
        funcdef = ast.AsyncFunctionDef()
        funcdef.name = p[2]
        funcdef.args = p[3]
        funcdef.body = p[5]
        funcdef.decorator_list = []
        funcdef.lineno = p.lineno(1)
        ast.fix_missing_locations(funcdef)
        p[0] = funcdef

    def p_async_funcdef2(self, p):
        ''' funcdef : ASYNC DEF NAME parameters RIGHTARROW test COLON suite '''
        funcdef = ast.AsyncFunctionDef()
        funcdef.name = p[2]
        funcdef.args = p[3]
        funcdef.body = p[7]
        funcdef.decorator_list = []
        funcdef.lineno = p.lineno(1)
        ast.fix_missing_locations(funcdef)
        p[0] = funcdef

# XXXX support for await and async for async with
