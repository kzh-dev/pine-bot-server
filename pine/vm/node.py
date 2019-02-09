# coding=utf-8

import copy
import numpy

from ..base import PineError
from .helper import Series, NaN

# AST Node
class Node (object):

    def __init__ (self):
        self.children = []
        self.args = []
        self.lno = None
        self.to_dump = True

    def __str__ (self):
        me = "{0}: {1}".format(self.__class__.__name__, ", ".join([str(a) for a in self.args]))
        if self.to_dump:
            self.to_dump = False
            ln = [me]
            for n in self.children:
                for l in str(n).splitlines():
                    ln.append('  ' + l)
            return "\n".join(ln)
        else:
            return me + " ..."

    def _reset_dump (self):
        self.to_dump = True
        for n in self.children:
            n._reset_dump()
        return self

    def dump (self):
        print(self._reset_dump())

    def append (self, node):
        self.children.append(node)
        return self

    def lineno (self, lineno):
        self.lno = lineno
        return self

    def expand_func (self, ctxt):
        self.children = [n.expand_func(ctxt) for n in self.children]
        self.children = [n for n in self.children if n is not None]
        return self

    def resolve_var (self, ctxt):
        self.children = [n.resolve_var(ctxt) for n in self.children]
        return self

    def eval (self, vm):
        v = None
        for c in self.children:
            v = c.eval(vm)
        return v

class LiteralNode (Node):
    def __init__ (self, literal):
        super().__init__()
        if isinstance(literal, Node):
            self.children = literal.children.copy()
        else:
            self.args.append(literal)

    def eval (self, vm):
        if self.args:
            return self.args[0]
        else:
            return [e.eval(vm) for e in self.children]

class ExprNode (Node):

    def __init__ (self, node):
        super().__init__()
        self.append(node)

class OrNode (Node):

    def eval (self, vm):
        r = False
        for n in self.children:
            v = n.eval(vm)
            if not isinstance(v, Series):
                if bool(v):
                    return v
            elif r is False:
                r = v
            else:
                r = numpy.logical_or(r, v)
        return r

class AndNode (Node):

    def eval (self, vm):
        r = True
        for n in self.children:
            v = n.eval(vm)
            if not isinstance(v, Series):
                if not bool(v):
                    return v
            elif r is True:
                r = v
            else:
                r = numpy.logical_and(r, v)
        return r


def _eq (a, b):
    return a + b
class BinOpNode (Node):
    def __init__ (self, op, a, b):
        super().__init__()
        self.args.append(op)
        self.append(a)
        self.append(b)

    def eval (self, vm):
        operator = self.args[0]
        a = self.children[0].eval(vm)
        b = self.children[1].eval(vm)

        if operator == r'[':
            return self.eval_index_access(a, b)
        
        if operator == r'==':
            op = lambda a,b: a == b
        elif operator == r'!=':
            op = lambda a,b: a != b
        elif operator == r'>':
            op = lambda a,b: a > b
        elif operator == r'>=':
            op = lambda a,b: a >= b
        elif operator == r'<':
            op = lambda a,b: a < b
        elif operator == r'<=':
            op = lambda a,b: a <= b
        elif operator == r'+':
            op = lambda a,b: a + b
        elif operator == r'-':
            op = lambda a,b: a - b
        elif operator == r'*':
            op = lambda a,b: a * b
        elif operator == r'/':
            op = lambda a,b: a / b
        elif operator == r'%':
            op = lambda a,b: a % b
        else:
            raise PineError('invalid opertor: {}'.format(opertor))

        # FIXME need type check
        return op(a, b)
        
    def eval_index_access (self, a, b):
        if not isinstance(a, Series):
            raise PineError('cannot access by index for: {}'.format(a))
        if not isinstance(b, int):
            raise PineError('index must be an interger'.format(b))

        if len(a) <= b:
            r = Series([NaN] * len(a))
        else:
            r = numpy.roll(a, b)
            for i in range(0, b):
                r[i] = r[b]

        return r


class UniOpNode (Node):
    def __init__ (self, op, a):
        super().__init__()
        self.args.append(op)
        self.append(a)

    def eval (self, vm):
        op = self.args[0]
        rhv = self.children[0].eval(vm)
        if op == 'not':
            return not bool(rhv)
        if op == '+':
            return rhv
        if op == '-':
            return -rhv
        raise PineError('invalid unary op: {}'.format(op))

class BuiltinVarRefNode (Node):
    def __init__ (self, ident, func):
        super().__init__()
        self.args.append(ident)
        self.args.append(func)

class VarRefNode (Node):
    def __init__ (self, ident):
        super().__init__()
        self.args.append(ident)

    def resolve_var (self, ctxt):
        ident = self.args[0]
        v = ctxt.lookup_variable(ident)
        if not isinstance(v, Node): # built-in variable
            v_ = v()
            if v_ is None:
                return BuiltinVarRefNode(ident, v).lineno(self.lno)
            else:
                return LiteralNode(v_).lineno(self.lno)
        # User-defined var
        self.append(v)
        return self

    def eval (self, vm):
        raise NotImplementedError

class KwArgsNode (Node):

    def __init__ (self, kwargs):
        super().__init__()
        if kwargs:
            for k, n in kwargs.items():
                self.args.append(k)
                self.append(n)

    def eval (self, vm):
        raise NotImplementedError

class FunCallNode (Node):
    def __init__ (self, fname, args):
        super().__init__()
        self.args.append(fname)
        aargs = args[0]
        if not isinstance(aargs, Node):
            aargs = Node()
        self.append(aargs)
        kwargs = args[1]
        if not isinstance(kwargs, Node):
            kwargs = KwArgsNode(kwargs)
        self.append(kwargs)

    def expand_func (self, ctxt):
        fname = self.args[0]
        func = ctxt.lookup_function(fname)

        if isinstance(func, Node):  # user-defined
            return UserFuncCallNode(fname, self.children, copy.deepcopy(func))
        else:
            return BuiltinFunCallNode(fname, self.children, func)

    def eval (self, vm):
        raise NotImplementedError
        fname = self.args[0]
        args, kwargs = self.children
        if args:
            _args = [a.eval(vm) for a in args.children]
        else:
            _args = None
        if kwargs:
            _kwargs = {}
            for k, n in kwargs.items():
                _kwargs[k] = n.eval(vm)
        else:
            _kwargs = None
        return vm.func_call(fname, _args, _kwargs)

class BuiltinFunCallNode (FunCallNode):

    def __init__ (self, fname, args, func):
        super().__init__(fname, args)
        self.func = func

class UserFuncCallNode (Node):

    # args: fname, [arg_id, ...]
    # children: arg_var_defs, body
    def __init__ (self, fname, args, node):
        super().__init__()
        self.args.append(fname)

        arg_ids = node.args[1].children
        self.args.append(arg_ids)

        argdef = Node()
        argn = args[0]  # FIXME kwarg should be denied.
        for v, n in zip(arg_ids, argn.children):
            argdef.append(VarDefNode(v, n, True).lineno(node.lno))

        self.append(argdef)
        self.append(node.children[0])

    def resolve_var (self, ctxt):
        try:
            ctxt.push_scope()
            return super().resolve_var(ctxt)
        finally:
            ctxt.pop_scope()

class IfNode (ExprNode):
    def __init__ (self, condition, ifclause, elseclause=None):
        super().__init__(condition)
        self.append(ifclause)
        if elseclause:
            self.append(elseclause)

    def resolve_var (self, ctxt):
        # condition
        self.children[0] = self.children[0].resolve_var(ctxt)
        # true
        try:
            ctxt.push_scope()
            self.children[1] = self.children[1].resolve_var(ctxt)
        finally:
            ctxt.pop_scope()
        # false
        if len(self.children) > 2:
            try:
                ctxt.push_scope()
                self.children[2] = self.children[2].resolve_var(ctxt)
            finally:
                ctxt.pop_scope()
        return self

    def eval (self, vm):
        vm.push_scope()
        try:
            c =  self.children[0].eval(vm)
            s1 = self.children[1].eval(vm)
            if len(self.children) > 2:
                s2 = self.children[2]
            else:
                s2 = None

            # FIXME
            if isinstance(c, Series):
                if isinstance(s1, Series):
                    s1 = s1.copy()
                else:
                    s1 = Series([s1] * len(c))
                if s2 is not None:
                    s2 = s2.eval(vm)
                    if not isinstance(s2, Series):
                        s2 = Series([s2] * len(c))
                else:
                    s2 = Series([NaN] * len(c))

                for i in range(0, len(c)):
                    if not bool(c[i]):
                        s1[i] = s2[i]
                return s1
            else:
                if bool(c):
                    return s1
                elif s2:
                    return s2.eval(vm)
        finally:
            vm.pop_scope()

class ForNode (ExprNode):

    def __init__ (self, var_def, to_clause, stmts_block):
        super().__init__(var_def)
        self.append(to_clause)
        self.append(stmts_block)

    def resolve_var (self, ctxt):
        try:
            ctxt.push_scope()
            return super().resolve_var(ctxt)
        finally:
            ctxt.pop_scope()

    def eval (self, vm):
        raise NotImplementedError
        var_def, to_node, body = self.children
        counter_name = var_def.name()
        retval = None

        vm.push_scope()
        try:
            counter_init = var_def.eval(vm)
            counter_last = to_node.eval(vm)
            if counter_init <= counter_last:
                op = '>'
            else:
                op = '<'
                
            while True:
                # TODO continue, break
                retval = body.eval(vm)

                counter = vm.lookup_variable(counter_name)
                if op == '>':
                    counter += 1
                    if counter > counter_last:
                        break
                else:
                    counter -= 1
                    if counter < counter_last:
                        break
                vm.assign_variable(counter_name, counter)
        finally:
            vm.pop_scope()

class DefNode (Node):

    def __init__ (self, name):
        super().__init__()
        self.args.append(name)

    @property
    def name (self):
        return self.args[0]

class FunDefNode (DefNode):
    def __init__ (self, fname, args, body):
        super().__init__(fname)
        self.args.append(args)
        self.append(body)

    def expand_func (self, ctxt):
        ctxt.register_function(self)
        return None

    def resolve_var (self, ctxt):
        raise NotImplementedError

    def eval (self, vm):
        vm.register_function(self.args[0], self.args[1].children, self.children[0])

class VarDefNode (DefNode):
    def __init__ (self, ident, expr, volatile=False):
        super().__init__(ident)
        self.args.append(False)     # mutable
        self.args.append(volatile)  # volatile
        self.args.append(None)      # type
        self.append(expr)

    def resolve_var (self, ctxt):
        super().resolve_var(ctxt)
        ctxt.define_variable(self)
        return self

    def make_mutable (self):
        self.args[1] = True

    def eval (self, vm):
        raise NotImplementedError
        rhv = self.children[0].eval(vm)
        vm.define_variable(self.args[0], rhv)
        return rhv

class VarAssignNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)

    def resolve_var (self, ctxt):
        ident = self.args[0]
        v = ctxt.lookup_variable(ident)
        if not isinstance(v, Node):
            raise PineError('cannot assign to built-in variable: {}'.format(ident))
        v.make_mutable()
        self.children.insert(0, v)
        return self

    def eval (self, vm):
        raise NotImplementedError
        rhv = self.children[0].eval(vm)
        vm.assign_variable(self.args[0], rhv)
        return rhv

