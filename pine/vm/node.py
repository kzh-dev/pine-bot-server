# coding=utf-8

import copy
import math
import numpy

from ..base import PineError
from .helper import Series, NaN, series_mutable

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

    def collect_anotation (self, ctxt):
        for n in self.children:
            n.collect_anotation(ctxt)

    def evaluate (self, vm):
        v = None
        for c in self.children:
            v = c.evaluate(vm)
        return v


class LiteralNode (Node):
    def __init__ (self, literal):
        super().__init__()
        if isinstance(literal, Node):
            self.children = literal.children.copy()
        else:
            self.args.append(literal)

    def evaluate (self, vm):
        if self.args:
            return self.args[0]
        else:
            return [e.evaluate(vm) for e in self.children]


class OrNode (Node):

    def evaluate (self, vm):
        r = False
        for n in self.children:
            v = n.evaluate(vm)
            if not isinstance(v, Series):
                if bool(v):
                    return v
            elif r is False:
                r = v
            else:
                r = v.logical_or(r)
        return r

class AndNode (Node):

    def evaluate (self, vm):
        r = True
        for n in self.children:
            v = n.evaluate(vm)
            if not isinstance(v, Series):
                if not bool(v):
                    return v
            elif r is True:
                r = v
            else:
                r = v.logical_and(r)
        return r


class BinOpNode (Node):
    def __init__ (self, op, a, b):
        super().__init__()
        self.args.append(op)
        self.append(a)
        self.append(b)

    def evaluate (self, vm):
        operator = self.args[0]
        a = self.children[0].evaluate(vm)
        b = self.children[1].evaluate(vm)

        if operator == r'[':
            return self.index_access(vm, a, b)
        
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
            raise PineError('invalid operator: {}'.format(operator))

        # FIXME need type check
        s = op(a, b)
        if not isinstance(s, Series):
            return s
        else:
            return s.set_valid_index(a, b)
        
    def index_access (self, vm, a, b):
        if not isinstance(a, Series): # and not isinstance(a, list):
            raise PineError('cannot access by index for: {0}'.format(type(a)))
        if not isinstance(b, int):
            raise PineError('index must be an interger'.format(b))
        return a.shift(b)


class UniOpNode (Node):
    def __init__ (self, op, a):
        super().__init__()
        self.args.append(op)
        self.append(a)

    def evaluate (self, vm):
        op = self.args[0]
        rhv = self.children[0].evaluate(vm)
        if isinstance(rhv, Series):
            raise NotImplementedError
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

    def evaluate (self, vm):
        func = self.args[1]
        return func(vm)

class VarRefNode (Node):
    def __init__ (self, ident):
        super().__init__()
        self.args.append(ident)

    def resolve_var (self, ctxt):
        ident = self.args[0]
        v = ctxt.lookup_variable(ident)
        if not isinstance(v, Node): # built-in variable
            try:
                v_ = v()
            except NotImplementedError:
                v_ = None
            if v_ is None:
                return BuiltinVarRefNode(ident, v).lineno(self.lno)
            else:
                return LiteralNode(v_).lineno(self.lno)
        # User-defined var
        self.append(v)
        return self

class KwArgsNode (Node):

    def __init__ (self, kwargs):
        super().__init__()
        if kwargs:
            for k, n in kwargs.items():
                self.args.append(k)
                self.append(n)

    def evaluate (self, vm):
        kws = {}
        for k, n in zip(self.args, self.children):
            kws[k] = n.evaluate(vm)
        return kws

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

    @property
    def fname (self):
        return self.args[0]

    def expand_func (self, ctxt):
        fname = self.args[0]
        func = ctxt.lookup_function(fname)

        self.children = [n.expand_func(ctxt) for n in self.children]

        if isinstance(func, Node):  # user-defined
            return UserFuncCallNode(fname, self.children, copy.deepcopy(func))
        else:
            if fname == 'study' or fname == 'strategy':
                cls = MetaInfoFuncNode
            elif fname == 'input':
                cls = InputFuncNode
            elif fname == 'security':
                cls = SecurityFuncNode
            elif ctxt.is_strategy_func(fname):
                cls = StrategyFuncNode
            elif ctxt.is_plot_func(fname):
                cls = PlotFuncNode
            else:
                cls = BuiltinFunCallNode
            return cls(fname, self.children, func)

    def evaluate (self, vm):
        raise NotImplementedError

class BuiltinFunCallNode (FunCallNode):

    def __init__ (self, fname, args, func):
        super().__init__(fname, args)
        self.func = func

    def _pre_evaluate (self, vm):
        fn = self.fname
        cb = self.func
        if hasattr(vm, fn):
            cb = getattr(vm, fn)
            
        args, kwargs = self.children
        _args = [a.evaluate(vm) for a in args.children]
        _kwargs = kwargs.evaluate(vm)
        return (cb, _args, _kwargs)

    def evaluate (self, vm):
        cb, args, kwargs = self._pre_evaluate(vm)
        return cb(vm, args, kwargs)

class MetaInfoFuncNode (BuiltinFunCallNode):
    def collect_anotation (self, ctxt):
        ctxt.register_meta(self)

    def evaluate (self, vm):
        if not vm.meta:
            return super().evaluate(vm)

class InputFuncNode (BuiltinFunCallNode):
    def collect_anotation (self, ctxt):
        ctxt.register_input(self)

    def evaluate (self, vm):
        cb, args, kwargs = self._pre_evaluate(vm)
        return cb(vm, args, kwargs, self)
        

class SecurityFuncNode (BuiltinFunCallNode):
    def collect_anotation (self, ctxt):
        ctxt.register_security(self)

class StrategyFuncNode (BuiltinFunCallNode):
    def collect_anotation (self, ctxt):
        ctxt.register_strategy(self)

class PlotFuncNode (BuiltinFunCallNode):
    def collect_anotation (self, ctxt):
        ctxt.register_plot(self)


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
            argdef.append(VarDefNode(v, n).lineno(node.lno))

        self.append(argdef)
        self.append(node.children[0])

    def resolve_var (self, ctxt):
        try:
            ctxt.push_scope()
            return super().resolve_var(ctxt)
        finally:
            ctxt.pop_scope()

class IfNode (Node):
    def __init__ (self, condition, ifclause, elseclause, is_expr=True):
        super().__init__()
        self.append(condition)
        self.append(ifclause)
        if elseclause:
            self.append(elseclause)
        self.is_expr = is_expr

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

    def _first_eval_as_series (self, vm, c, s1, s2):
        if self.is_expr and c.filled():
            s1 = s1.evaluate(vm)
            if isinstance(s1, Series):
                r = s1.copy()
            else:
                r = Series([s1] * len(c))
            if s2:
                s2 = s2.evaluate(vm)
                if not isinstance(s2, Series):
                    s2 = Series([s2] * len(c))
            else:
                s2 = Series([s1.default_elem()] * len(c))

            c_ = c.to_bool_safe()
            for i in range(0, len(c)):
                if not bool(c_[i]):
                    r[i] = s2[i]

            r.set_valid_index(c)
            return r
        else:
            # return mutable Series
            if c.to_bool_safe(vm.ip):
                r = s1.evaluate(vm)
            elif s2:
                r = s2.evaluate(vm)
            else:
                r = None
            if isinstance(r, Series):
                return r.to_mutable_series()
            else:
                return series_mutable(r, c.size)

    def evaluate (self, vm):
        c =  self.children[0].evaluate(vm)
        s1 = self.children[1]
        if len(self.children) > 2:
            s2 = self.children[2]
        else:
            s2 = None

        if isinstance(c, Series):
            if vm.ip == 0:
                return self._first_eval_as_series(vm, c, s1, s2)
            else:
                c = c.to_bool_safe(vm.ip)
        if c:
            return s1.evaluate(vm)
        elif s2:
            return s2.evaluate(vm)
        else:
            return None

class ForNode (Node):

    def __init__ (self, var_def, to_clause, stmts_block):
        super().__init__()
        self.append(var_def)
        self.append(to_clause)
        self.append(stmts_block)

    def resolve_var (self, ctxt):
        try:
            ctxt.push_scope()
            return super().resolve_var(ctxt)
        finally:
            ctxt.pop_scope()

    def evaluate (self, vm):
        var_def, to_node, body = self.children
        retval = None

        counter_init = var_def.evaluate(vm)
        counter_last = to_node.evaluate(vm)
        if counter_init <= counter_last:
            op = '+'
        else:
            op = '-'
            
        counter = counter_init
        while True:
            # TODO continue, break
            try:
                # TODO this is doable in resolve_var...
                vm.push_register_scope()
                retval = body.evaluate(vm)
            finally:
                vm.pop_register_scope()

            if counter == counter_last:
                break

            if op == '+':
                counter += 1
            else:
                counter -= 1
            vm.set_register(var_def, counter)

        vm.set_register(var_def, counter_init)
        return retval

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
        super().expand_func(ctxt)
        ctxt.register_function(self)
        return None

    def resolve_var (self, ctxt):
        raise NotImplementedError

    def evaluate (self, vm):
        raise NotImplementedError

class VarDefNode (DefNode):
    def __init__ (self, ident, expr):
        super().__init__(ident)     # ident
        self.args.append(False)     # mutable
        self.args.append(None)      # type
        self.append(expr)

    def resolve_var (self, ctxt):
        super().resolve_var(ctxt)
        ctxt.define_variable(self)
        return self

    def make_mutable (self):
        self.args[1] = True

    def evaluate (self, vm):
        val = vm.get_register(self)
        rhv = self.children[0]
        if val is None:
            rhv = rhv.evaluate(vm)
            mutable = self.args[1]
            if mutable:
                val = vm.alloc_register(self, rhv)
            else:
                val = vm.set_register(self, rhv)
        elif isinstance(val, Series):
            if val.out_of_date(vm):
                rhv = rhv.evaluate(vm)
                if isinstance(rhv, Series):
                    rhv = rhv[vm.ip]
                vm.set_register_value(self, rhv)
        return val

class VarAssignNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)

    def resolve_var (self, ctxt):
        # rhv
        super().resolve_var(ctxt)
        # make lookup node
        ident = self.args[0]
        v = ctxt.lookup_variable(ident)
        if not isinstance(v, Node):
            raise PineError('cannot assign to built-in variable: {}'.format(ident))
        v.make_mutable()
        self.children.insert(0, v)
        # rhv
        return self

    def evaluate (self, vm):
        dest = self.children[0]
        rhv = self.children[1].evaluate(vm)
        if isinstance(rhv, Series):
            rhv = rhv[vm.ip]
        vm.set_register_value(dest, rhv)
        return dest
