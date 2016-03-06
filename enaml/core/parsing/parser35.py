#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import ast

from .lexer3 import Python35EnamlLexer
from .base_parser import Load
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
             [(ast.AsyncFunctionDef, 'async function definition')])

    _DECL_FUNCDEF_DISALLOWED =\
        dict(list(Python34EnamlParser._DECL_FUNCDEF_DISALLOWED.items()) +
             [(ast.AsyncFunctionDef, 'async function definition')])

    def set_call_arguments(self, node, args):
        """Set the arguments for an ast.Call node.

        On Python 3.5+, the starargs and kwargs attributes does not exists
        anymore.

        Parameters
        ----------
        node : ast.Call
            Node was arguments should be set.

        args : Arguments
            Arguments for the function call.

        """
        pos_args = args.args
        if args.starargs:
            pos_args += [ast.Starred(value=args.starargs, ctx=Load)]
        key_args = args.keywords
        if args.kwargs:
            key_args += [ast.keyword(arg=None, value=args.kwargs)]
        node.args = pos_args
        node.keywords = key_args

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

#    def p_compound_stmt(self, p):
#        ''' compound_stmt : if_stmt
#                          | while_stmt
#                          | for_stmt
#                          | try_stmt
#                          | with_stmt
#                          | funcdef
#                          | async_funcdef
#                          | classdef
#                          | decorated '''
#        super(Python35EnamlParser, self).p_compound_stmt(p)
#
#    def p_decorated(self, p):
#        ''' decorated : decorators funcdef
#                      | decorators classdef
#                      | decorators async_funcdef'''
#        decs = p[1]
#        target = p[2]
#        target.decorator_list = decs
#        p[0] = target

#    def p_async_funcdef1(self, p):
#        ''' async_funcdef : ASYNC DEF NAME parameters COLON async_suite '''
#        funcdef = ast.AsyncFunctionDef()
#        funcdef.name = p[2]
#        funcdef.args = p[3]
#        funcdef.body = p[5]
#        funcdef.decorator_list = []
#        funcdef.lineno = p.lineno(1)
#        ast.fix_missing_locations(funcdef)
#        p[0] = funcdef
#
#    def p_async_funcdef2(self, p):
#        ''' async_funcdef : ASYNC DEF NAME parameters RIGHTARROW test COLON async_suite '''
#        funcdef = ast.AsyncFunctionDef()
#        funcdef.name = p[2]
#        funcdef.args = p[3]
#        funcdef.body = p[7]
#        funcdef.decorator_list = []
#        funcdef.lineno = p.lineno(1)
#        ast.fix_missing_locations(funcdef)
#        p[0] = funcdef
#
#    def p_async_suite1(self, p):
#        ''' async_suite : async_simple_stmt '''
#        # stmt may be a list of simple_stmt due to this piece of grammar:
#        # simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
#        stmt = p[1]
#        if isinstance(stmt, list):
#            res = stmt
#        else:
#            res = [stmt]
#        p[0] = res
#
#    def p_async_suite2(self, p):
#        ''' async_suite : NEWLINE INDENT async_stmt_list DEDENT '''
#        p[0] = p[3]

# XXXX support for await and async for async with
