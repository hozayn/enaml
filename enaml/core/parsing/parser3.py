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

# TODO support advanced unpacking
# TODO support kwarg only in functions


class Python3EnamlParser(BaseEnamlParser):
    """Enaml parser supporting Python syntax.

    Main differences from base parser are :


    """
    parse_id = '3'

    lexer = Python3EnamlLexer

    def p_decl_funcdef3(self, p):
        ''' decl_funcdef : NAME NAME parameters RETURNARROW test COLON suite '''
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

    def p_small_stmt1(self, p):
        ''' small_stmt : expr_stmt
                       | del_stmt
                       | pass_stmt
                       | flow_stmt
                       | import_stmt
                       | global_stmt
                       | assert_stmt
                       | nonlocal_stmt'''
        p[0] = p[1]

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

        args = p[4]  # This is an Arguments instance
        classdef.bases = args.args
        classdef.keywords = args.keywords
        classdef.starargs = args.starargs
        classdef.kwargs = args.kwargs

        classdef.body = p[7]
        classdef.decorator_list = []
        classdef.lineno = p.lineno(1)
        ast.fix_missing_locations(classdef)
        p[0] = classdef

    # XXXX support for ellipsis as expr

    def _make_args(self, args, defaults=[], vararg=None, kwonlyargs=[],
                   kw_defaults=[], kwarg=None):
        """Build an ast node for function arguments.

        """
        # This is valid only for Python 3.3
        va = vararg.annotation if vararg else None
        vararg = vararg.arg if vararg else None
        ka = kwarg.annotation if kwarg else None
        kwarg = kwarg.arg if kwarg else None

        return ast.arguments(args=args, defaults=defaults, vararg=vararg,
                             varargannotation=va, kwonlyargs=kwonlyargs,
                             kw_defaults=kw_defaults, kwarg=kwarg,
                             kwargannotation=ka)

    # XXXX add rules for kw only

    def p_fpdef(self, p):
        ''' fpdef : NAME '''
        p[0] = ast.arg(arg=p[1], annotation=None)

    def p_tfpdef1(self, p):
        ''' tfpdef : NAME '''
        p[0] = ast.arg(arg=p[1], annotation=None)

    def p_tfpdef2(self, p):
        ''' tfpdef : NAME COLON test'''
        p[0] = ast.arg(arg=p[1], annotations=p[3])


def _make_typedarg_rule(func):
    """Copy a rule and allow for annotations.

    """
    def rule(self, p):
        return func(self, p)

    new_doc = func.__doc__.replace('fpdef', 'tfpdef')
    rule.__doc__ = new_doc.replace('varargslist', 'typedargslist')
    return rule


for f in filter(lambda x: 'varargslist' in x, dir(Python3EnamlParser)):
    setattr(Python3EnamlParser, f.replace('varargslist', 'typedargslist'),
            _make_typedarg_rule(getattr(Python3EnamlParser, f)))
