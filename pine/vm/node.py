# coding=utf-8

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

    def as_bool (self, val):
        if isinstance(val, list):
            return bool(val[-1])
        else:
            return bool(val)

class MulOpNode (Node):

    def eval (self, vm):
        print(self)
        raise NotImplementedError

class OrNode(MulOpNode):
    pass
class AndNode(MulOpNode):
    pass
class EqNode(MulOpNode):
    pass

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
        if isinstance(a, list):
            if isinstance(b, list):
                return [op(i, j) for i,j in zip(a, b)]
            else:
                return [op(i, b) for i in a]
        else:
            if isinstance(b, list):
                return op(a, b[-1])
            else:
                return op(a, b)
        
    def eval_index_access (a, b):
        if not isinstance(a, list):
            raise PineError('cannot access by index for: {}'.format(a))
        if not isinstance(b, int):
            raise PineError('index must be an interger'.format(b))
        return a[b]


class UniOpNode (Node):
    def __init__ (self, op, a):
        super().__init__()
        self.args.append(op)
        self.append(a)

    def eval (self, vm):
        print(self)
        raise NotImplementedError

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
            _kwargs = kwargs.eval(vm)
        else:
            _kwargs = None
        return vm.func_call(fname, _args, _kwargs)

class KwArgsNode (Node):
    def __init__ (self, kwargs):
        super().__init__()
        self.args += kwargs.keys()
        self.children += kwargs.values()

    def eval (self, vm):
        print(self)
        raise NotImplementedError

class LiteralNode (Node):
    def __init__ (self, literal):
        super().__init__()
        if isinstance(literal, Node):
            self.append(literal)
        else:
            self.args.append(literal)

    def eval (self, vm):
        if self.args:
            return self.args[0]
        else:
            return [e.eval(vm) for e in self.children[0]]


class IfNode (Node):
    def __init__ (self, condition, ifclause, elseclause=None):
        super().__init__()
        self.append(condition)
        self.append(ifclause)
        if elseclause:
            self.append(elseclause)

    def eval (self, vm):
        if self.as_bool(self.children[0].eval(vm)):
            try:
                vm.push_scope()
                return self.children[1].eval(vm)
            finally:
                vm.pop_scope()
        elif len(self.children) > 2:
            try:
                vm.push_scope()
                return self.children[2].eval(vm)
            finally:
                vm.pop_scope()

class ForNode (Node):
    def __init__ (self, var_def, to_clause, stmts_block):
        super().__init__()
        self.args.append(var_def)
        self.append(to_clause)
        self.append(stmts_block)

    def eval (self, vm):
        print(self)
        raise NotImplementedError

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

    def eval (self, vm):
        rhv = self.children[0].eval(vm)
        vm.define_variable(self.args[0], rhv)

class VarAssignNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)

    def eval (self, vm):
        print(self)
        raise NotImplementedError

