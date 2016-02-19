#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import ast

from .base_parser import BaseEnamlParser, ast_for_testlist


class Python3EnamlParser(BaseEnamlParser):
    """Enaml parser supporting Python syntax.

    Main differences from base parser are :


    """

    def p_yield_expr3(self, p):
        ''' yield_expr : YIELD FROM testlist '''
        value = ast_for_testlist(p[2])
        p[0] = ast.Yield(value=value, lineno=p.lineno(1))

#    def p_funcdef2(self, p):
#        ''' funcdef : DEF NAME parameters RETURNARROW ??? COLON suite '''
#        funcdef = ast.FunctionDef()
#        funcdef.name = p[2]
#        funcdef.args = p[3]
#        funcdef.body = p[5]
#        funcdef.decorator_list = []
#        funcdef.lineno = p.lineno(1)
#        ast.fix_missing_locations(funcdef)
#        p[0] = funcdef

    def p_classdef4(self, p):
        ''' '''
        pass
