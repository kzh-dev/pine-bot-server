# coding=utf-8

from .vm.vm import InputScanVM
from .vm.compile import compile_pine
from .market.base import Market

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        node = compile_pine(f.read())

        vm = InputScanVM(Market())
        vm.load_node(node)
        #vm.node.dump()
        print(vm.meta)
        print(vm.run())
