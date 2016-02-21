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
from .lexer3 import Python3EnamlLexer


class Python3EnamlParser(BaseEnamlParser):
    """Enaml parser supporting Python syntax.

    Main differences from base parser are :


    """

    lexer = Python3EnamlLexer

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

    def p_nonlocal_stmt1(self, p):
        ''' nonlocal_stmt : NONLOCAL NAME'''
        nonlocal_stmt = ast.Nonlocal()
        nonlocal_stmt.names = [p[2]]
        nonlocal_stmt.lineno = p.lineno(1)
        p[0] = nonlocal_stmt

    def p_nonlocal_stmt2(self, p):
        ''' global_stmt : NONLOCAL NAME globals_list '''
        nonlocal_stmt = ast.Global()
        nonlocal_stmt.names = [p[2]] + p[3]
        nonlocal_stmt.lineno = p.lineno(1)
        p[0] = nonlocal_stmt

    def p_raise_stmt3(self, p):
        ''' raise_stmt : RAISE test FROM test '''
        raise_stmt = ast.Raise()
        raise_stmt.type = p[1]
        raise_stmt.cause = p[4]
        p[0] = raise_stmt

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

    def p_classdef3(self, p):
        ''' classdef : CLASS NAME LPAR arglist RPAR COLON suite '''
        classdef = ast.ClassDef(keywords=[])
        classdef.name = p[2]

        # XXXX modifiy analysis to extract the arguments
        bases = p[4]
        if not isinstance(bases, list):
            bases = [bases]
        classdef.bases = bases
        classdef.body = p[7]
        classdef.decorator_list = []
        classdef.lineno = p.lineno(1)
        ast.fix_missing_locations(classdef)
        p[0] = classdef

    # XXXX support for ellipsis as expr

    def _make_arg(self, arg, annotation=None, lineno=None):
        """Build a argument node.

        Parameters
        ----------
        arg : str
            Name of the argument

        annotation : ast.Node
            Annotation (Python 3 only)

        lineno :
            Line number (Python 2 only)

        """
        return ast.arg(arg=arg, annotation=annotation)

    def _make_args(self, args, defaults=[], vararg=None, kwonlyargs=[],
                   kw_defaults=[], kwarg=None):
        """Build an ast node for function arguments.

        """
        # On Python 3.3 extract name and annotation
        # After should be straight forward
        raise NotImplementedError()

    # XXXX add rules for kw only

    # XXXX Python 3 add support for function annotation add tfpdef

# XXXX Use an iteration on vararg and vararglist rules to generate typedarg
# and typedarglist rules
