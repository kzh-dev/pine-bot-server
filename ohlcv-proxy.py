# coding=utf-8

from mprpc import RPCServer
class OhlcvProxyServer (RPCServer):

    def __init__ (self):
        super().__init__()
        self.adaptors = {}

    def register_adaptor (self, adaptor):
        self.adaptors[adaptor.tickerid] = adaptor

    def ohlcv (self, tickerid, resolution, count):
        return self.adaptors[tickerid].ohlcv(resolution, count)
        

if __name__ == '__main__':
    import os
    from gevent.server import StreamServer
    from pine.market.bitmex import BitMexOhlcAdaptor
    from pine.market.base import PROXY_PORT

    server = OhlcvProxyServer()
    server.register_adaptor(BitMexOhlcAdaptor())

    port = int(os.environ.get('PORT', PROXY_PORT))
    server = StreamServer(('127.0.0.1', port), server)
    server.serve_forever()
