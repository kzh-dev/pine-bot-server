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

class BinOpNode (Node):
    def __init__ (self, op, a, b):
        super().__init__()
        self.args.append(op)
        self.append(a)
        self.append(b)

    def eval (self, vm):
        print(self)
        raise NotImplementedError

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
        print(self)
        raise NotImplementedError

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
        self.args.append(literal)

    def eval (self, vm):
        return self.args[0]


class IfNode (Node):
    def __init__ (self, condition, ifclause, elseclause=None):
        super().__init__()
        self.append(condition)
        self.append(ifclause)
        if elseclause:
            self.append(elseclause)

    def eval (self, vm):
        print(self)
        raise NotImplementedError

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
        print(self)
        raise NotImplementedError

class VarDefNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)

    def eval (self, vm):
        print(self)
        raise NotImplementedError

class VarAssignNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)

    def eval (self, vm):
        print(self)
        raise NotImplementedError
