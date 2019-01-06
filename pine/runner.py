# coding=utf-8

from .preprocess import preprocess
from .parser import parse
from .vm.vm import VM
from .market.base import Market

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        data = preprocess(f.read())
        node = parse(data)
        market = Market()
        vm = VM(market)
        node.eval(vm)
