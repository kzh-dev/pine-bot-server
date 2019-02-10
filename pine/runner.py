# coding=utf-8

from .vm.vm import InputScanVM, VM
from .vm.compile import compile_pine
from .market.base import Market
from .market.bitmex import BitMexMarket

if __name__ == '__main__':
    import sys
    op = sys.argv[1]
    with open(sys.argv[2]) as f:
        node = compile_pine(f.read())

        if op == 'input':
            vm = InputScanVM(Market())
            vm.load_node(node)
            vm.node.dump()
            print(vm.meta)
            print(vm.run())
        else:
            vm = VM(BitMexMarket())
            vm.load_node(node)
            print(vm.registers)
