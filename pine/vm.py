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

    def eval (self, ctxt=None):
        raise NotImplemented

    def append (self, node):
        self.children.append(node)
        return self


class MulOpNode (Node):
    pass

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

class UniOpNode (Node):
    def __init__ (self, op, a):
        super().__init__()
        self.args.append(op)
        self.append(a)

class VarRefNode (Node):
    def __init__ (self, ident):
        super().__init__()
        self.args.append(ident)

class FunCallNode (Node):
    def __init__ (self, fname, args):
        super().__init__()
        self.args.append(fname)
        self.args.append(args[0])
        self.args.append(args[1])

class KwArgsNode (Node):
    def __init__ (self, kwargs):
        super().__init__()
        self.args += kwargs.keys()
        self.children += kwargs.values()

class LiteralNode (Node):
    def __init__ (self, literal):
        super().__init__()
        self.args.append(literal)


class IfNode (Node):
    def __init__ (self, condition, ifclause, elseclause=None):
        super().__init__()
        self.append(condition)
        self.append(ifclause)
        if elseclause:
            self.append(elseclause)

class ForNode (Node):
    def __init__ (self, var_def, to_clause, stmts_block):
        super().__init__()
        self.args.append(var_def)
        self.append(to_clause)
        self.append(stmts_block)

class FunDefNode (Node):
    def __init__ (self, fname, args, body):
        super().__init__()
        self.args.append(fname)
        self.args.append(args)
        self.append(body)

class VarDefNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)

class VarAssignNode (Node):
    def __init__ (self, ident, expr):
        super().__init__()
        self.args.append(ident)
        self.append(expr)
