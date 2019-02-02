# coding=utf-8

import numpy

from ..base import PineError
from .helper import Series

# AST Node
class Node (object):

    def __init__ (self, child=None):
        self.children = []
        if child:
            self.append(child)
        self.args = []

    def __str__ (self):
        me = "{0}: {1}".format(self.__class__.__name__, ", ".join([str(a) for a in self.args]))
        ln = [me]
        for n in self.children:
            for l in str(n).splitlines():
                ln.append('  ' + l)
        return "\n".join(ln)

    def eval (self, vm):
        v = None
        for c in self.children:
            v = c.eval(vm)
        return v

    def append (self, node):
        self.children.append(node)
        return self


class MulOpNode (Node):
    # FIXME: Need to eval one by one.
    def eval_inner (self, vm, op):
        return op([e.eval(vm) for e in self.children])

class OrNode(MulOpNode):

    def eval (self, vm):
        self.eval_inner(vm, any)

class AndNode(MulOpNode):
    def eval (self, vm):
        self.eval_inner(vm, all)


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
            r = Series([float('nan')] * len(a))
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

class VarRefNode (Node):
    def __init__ (self, ident):
        super().__init__()
        self.args.append(ident)

    def eval (self, vm):
        return vm.lookup_variable(self.args[0])

class FunCallNode (Node):
    def __init__ (self, fname, args):
        super().__init__()
        self.args.append(fname)
        self.args.append(args[0])
        self.args.append(args[1])

    def eval (self, vm):
        fname, args, kwargs = self.args
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


class IfNode (Node):
    def __init__ (self, condition, ifclause, elseclause=None):
        super().__init__()
        self.append(condition)
        self.append(ifclause)
        if elseclause:
            self.append(elseclause)

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
                if not isinstance(s1, Series):
                    s1 = Series([s1] * len(c))
                if s2 is not None:
                    s2 = s2.eval(vm)
                    if not isinstance(s2, Series):
                        s2 = Series([s2] * len(c))
                else:
                    s2 = Series([float('nan')] * len(c))

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

class ForNode (Node):
    def __init__ (self, var_def, to_clause, stmts_block):
        super().__init__()
        self.args.append(var_def)
        self.append(to_clause)
        self.append(stmts_block)

    def eval (self, vm):
        var_def = self.args[0]
        counter_name = var_def.name()
        to_node = self.children[0]
        body = self.children[1]
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

class FunDefNode (Node):
    def __init__ (self, fname, args, body):
        super().__init__()
        self.args.append(fname)
        self.args.append(args)
        self.append(body)

    def eval (self, vm):
        vm.register_function(self.args[0], self.args[1].children, self.children[0])

class VarDefNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)

    def name (self):
        return self.args[0]

    def eval (self, vm):
        rhv = self.children[0].eval(vm)
        vm.define_variable(self.args[0], rhv)
        return rhv

class VarAssignNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)

    def eval (self, vm):
        rhv = self.children[0].eval(vm)
        vm.assign_variable(self.args[0], rhv)
        return rhv

