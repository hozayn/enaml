#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import ast

from .. import enaml_ast
from .base_lexer import syntax_error
from .base_parser import BaseEnamlParser, FakeToken, ast_for_testlist


class Python3EnamlParser(BaseEnamlParser):
    """Enaml parser supporting Python syntax.

    Main differences from base parser are :


    """
    def p_decl_funcdef3(self, p):
        ''' decl_funcdef : NAME NAME parameters RIGHTARROW test COLON suite '''
        lineno = p.lineno(1)
        if p[1] != 'func':
            syntax_error('invalid syntax', FakeToken(p.lexer.lexer, lineno))
        funcdef = ast.FunctionDef()
        funcdef.name = p[2]
        funcdef.args = p[3]
        funcdef.returns = p[5]
        funcdef.body = p[7]
        funcdef.decorator_list = []
        funcdef.lineno = lineno
        ast.fix_missing_locations(funcdef)
        self._validate_decl_funcdef(funcdef, p.lexer.lexer)
        decl_funcdef = enaml_ast.FuncDef()
        decl_funcdef.lineno = lineno
        decl_funcdef.funcdef = funcdef
        decl_funcdef.is_override = False
        p[0] = decl_funcdef

    def p_decl_funcdef2(self, p):
        ''' decl_funcdef : NAME RIGHTARROW parameters RIGHTARROW test COLON suite '''
        lineno = p.lineno(1)
        funcdef = ast.FunctionDef()
        funcdef.name = p[1]
        funcdef.args = p[3]
        funcdef.returns = p[5]
        funcdef.body = p[7]
        funcdef.decorator_list = []
        funcdef.lineno = lineno
        ast.fix_missing_locations(funcdef)
        self._validate_decl_funcdef(funcdef, p.lexer.lexer)
        decl_funcdef = enaml_ast.FuncDef()
        decl_funcdef.lineno = lineno
        decl_funcdef.funcdef = funcdef
        decl_funcdef.is_override = True
        p[0] = decl_funcdef

    def p_yield_expr3(self, p):
        ''' yield_expr : YIELD FROM testlist '''
        value = ast_for_testlist(p[2])
        p[0] = ast.Yield(value=value, lineno=p.lineno(1))

    def p_funcdef2(self, p):
        ''' funcdef : DEF NAME parameters RETURNARROW test COLON suite '''
        funcdef = ast.FunctionDef()
        funcdef.name = p[2]
        funcdef.args = p[3]
        funcdef.returns = p[5]
        funcdef.body = p[7]
        funcdef.decorator_list = []
        funcdef.lineno = p.lineno(1)
        ast.fix_missing_locations(funcdef)
        p[0] = funcdef

    def p_parameters2(self, p):
        ''' parameters : LPAR typedargslist RPAR '''
        p[0] = p[2]

    def p_classdef4(self, p):
        ''' '''
        pass


# XXXX Use an iteration on vararg and vararglist rules to generate typedarg
# and typedarglist rules


class Python34EnamlParser(Python3EnamlParser):
    """Enaml parser supporting Python 3.4 syntax.

    Main differences from base parser are :


    """

    def p_atom11(self, p):
        ''' atom : NONE '''
        p[0] = ast.NameConstant(None)

    def p_atom12(self, p):
        ''' atom : FALSE '''
        p[0] = ast.NameConstant(False)

    def p_atom13(self, p):
        ''' atom : TRUE '''
        p[0] = ast.NameConstant(True)
