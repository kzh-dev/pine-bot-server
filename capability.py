import sys
import ccxt
from ccxt.base.errors import NotSupported

for e in ccxt.exchanges:
    try:
        xchg = getattr(ccxt, e)()
        if xchg.has[sys.argv[1]]:
            print(e)
            print(xchg.has)
    except NotSupported:
        pass
