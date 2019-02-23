# coding=utf-8

import ccxt
from collections import OrderedDict
import requests
import json

exchanges = OrderedDict()

# cryptowatch
def _initialize_bitmex (symbols, pair):
    if pair.endswith('-perpetual-futures'):
        symbols[pair.split('-')[0]] = pair
    if pair == 'btcusd-perpetual-futures':
        symbols['xbtusd'] = pair

cryptowatch = OrderedDict()
API_SERVER_URL = 'https://api.cryptowat.ch'
res = requests.get(API_SERVER_URL+'/markets')
for m in res.json(object_pairs_hook=OrderedDict)['result']:
    exchange = m['exchange']
    pair = m['pair']
    symbols = cryptowatch.setdefault(exchange, OrderedDict())
    symbols[pair] = pair
    if exchange == 'bitmex':
        _initialize_bitmex(symbols, pair)

with open('static/cryptowatch-support.json', 'w') as f:
    f.write(json.dumps(cryptowatch, indent=2))

def resolution_to_str (*args):
    r = []
    for a in args:
        if a >= 1440 * 7:
            r.append('{}w'.format(int(a / 1440 / 7)))
        elif a >= 1440:
            r.append('{}d'.format(int(a / 1440)))
        elif a >= 60:
            r.append('{}h'.format(int(a / 60)))
        else:
            r.append('{}m'.format(a % 60))
    return r
            
exchanges = OrderedDict(exchanges)

for xchg_name in ccxt.exchanges:
    try:
        xchg_obj = getattr(ccxt, xchg_name)()
        xchg_id = xchg_obj.id
        xchg = OrderedDict(
            name=xchg_obj.name,
            ids=(xchg_id,),
        )

        xchg['cryptowatch'] = xchg_cw = xchg_id in cryptowatch
        markets = xchg.setdefault('markets', OrderedDict())
        for name, m in xchg_obj.load_markets().items():
            m_ = markets.setdefault(name, OrderedDict())
            m_['ids'] = (name, m['id'], m['symbol'])
            cw = False
            for i in m_['ids']:
                if i in cryptowatch[xchg_id] or i.lower() in cryptowatch[xchg_id] or\
                   i.upper() in cryptowatch[xchg_id]:
                    cw = True
                    break
            m_['cryptowatch'] = cw
            if cw:
                resolutions = resolution_to_str(
                    1, 3, 5, 15, 30,
                    60, 60*2, 60*4, 60*6, 60*12,
                    1440, 1440*3, 1440*7
                )
            else:
                ohlcv_support = xchg_obj.has['fetchOHLCV']
                if ohlcv_support and ohlcv_support != 'emulated':
                    resolutions = list(xchg_obj.timeframes.keys())
                else:
                    resolutions = []
            m_['resolutions'] = resolutions
        exchanges[xchg_name] = xchg
        print(xchg_name)
    except Exception as e:
        print(f'error: {xchg_name}: {e}')
            
with open('static/exchange-support.json', 'w') as f:
    f.write(json.dumps(exchanges, indent=2))
