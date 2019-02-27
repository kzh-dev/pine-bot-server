# coding=utf-8

import log

from logging import getLogger
logger = getLogger()

from datetime import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSON_SORT_KEYS'] = False

from pine.base import PineError
from pine.vm.vm import InputScanVM
from pine.vm.step import StepVM
from pine.vm.compile import compile_pine
from pine.market.base import Market
from pine.market.mirror import MirrorMarket
from pine.broker.mirror import MirrorBroker

import traceback
from collections import OrderedDict

from datetime import datetime, timezone
def utctimestamp ():
    return datetime.now(timezone.utc).timestamp()

# exchange information
import json
with open('static/exchange-support.json') as f:
    exchanges = json.loads(f.read(), object_pairs_hook=OrderedDict)

@app.route('/exchange-support', methods=['POST'])
def exchange_support ():
    try:
        exchange = request.json.get('exchange', None)
        if not exchange:
            return jsonify(exchanges=tuple(exchanges.keys()))
        xchg = exchanges.get(exchange.lower(), None)
        if xchg is None:
            return jsonify(markets=[])
        
        market = request.json.get('market', None)
        if market is None:
            return jsonify(markets=xchg['markets'])

        market = market.lower()
        markets = []
        for name, m in xchg['markets'].items():
            if market == name:
                markets.append(m)
            else:
                for mi in m['ids']:
                    if mi.lower() == market:
                        markets.append(m)
                        break
        return jsonify(markets=markets)

    except Exception as e:
        logger.exception(f'request={request.path}: {request.data}')
        return jsonify(error=traceback.format_exc())

from log import record_pine

@app.route('/scan-input', methods=['POST'])
def scan_input ():
    try:
        code = request.json['code']
        node = compile_pine(code)
        if node is None:
            raise PineError("pine script is empty")

        # Exract input
        vm = InputScanVM(Market())
        vm.load_node(node)
        inputs = vm.run()

        record_pine(code, vm)

        default_qty_value = vm.meta.get('default_qty_value', 1.0)
        pyramiding  = vm.meta.get('pyramiding ', 0)
        max_bars_back = vm.meta.get('max_bars_back', 0)

        params = OrderedDict(
            exchange='BITMEX',
            symbol='XBTUSD',
            resolution=30,
            strategy=OrderedDict(
                default_qty_value=default_qty_value,
                pyramiding=pyramiding,
                max_bars_back=max_bars_back,
            )
        )
        params['inputs'] = inputs = OrderedDict()
        for i in inputs:
            inputs[i['title']] = i['defval']

        return jsonify(params=params)

    except Exception as e:
        logger.exception(f'request={request.path}: {request.data}')
        return jsonify(error=traceback.format_exc())


import threading
vm_cache = OrderedDict()
vm_cache_lock = threading.Lock()
MAX_VM_CACHE_COUNT = 256
def register_vm_to_cache (vm):
    with vm_cache_lock:
        vm_cache[vm.ident] = vm
        while len(vm_cache) > MAX_VM_CACHE_COUNT:
            vm_cache.pop_item(False)    # From most oldest
        
def get_vm_from_cache (vmid):
    with vm_cache_lock:
        vm = vm_cache[vmid]
        vm_cache.move_to_end(vmid)
        return vm

@app.route('/install-vm', methods=['POST'])
def install_vm ():
    try:
        code = request.json['code']
        inputs = request.json['inputs']
        market = request.json['market']

        # compile PINE
        node = compile_pine(code)
        if node is None:
            raise PineError("pine script is empty")

        # VM
        vm = StepVM(MirrorMarket(*market), code)

        # Set up and run
        vm.load_node(node)
        vm.set_user_inputs(inputs)
        markets = vm.scan_market()
    
        # Register VM to store
        register_vm_to_cache(vm)

        record_pine(code, vm)
        return jsonify(vm=vm.ident, markets=markets, server_clock=utctimestamp())

    except Exception as e:
        logger.exception(f'request={request.path}: {request.data}')
        return jsonify(error=traceback.format_exc())

@app.route('/touch-vm', methods=['POST'])
def touch_vm ():
    try:
        vmid = request.json['vmid']
        try:
            get_vm_from_cache(vmid)
            return jsonify(server_clock=utctimestamp())
        except KeyError:
            return jsonify(error='Not found in cache'), 205
    except Exception as e:
        logger.exception(f'request={request.path}: {request.data}')
        return jsonify(error=traceback.format_exc()), 500

@app.route('/boot-vm', methods=['POST'])
def boot_vm ():
    try:
        vmid = request.json['vmid']
        ohlcv = request.json['ohlcv']

        try:
            vm = get_vm_from_cache(vmid)
        except KeyError:
            return jsonify(error='Not found in cache'), 205

        vm.set_ohlcv(ohlcv)
        vm.run()
        vm.set_broker(MirrorBroker())

        return jsonify(server_clock=utctimestamp())

    except Exception as e:
        logger.exception(f'request={request.path}: {request.data}')
        return jsonify(error=traceback.format_exc()), 500

@app.route('/step-vm', methods=['POST'])
def step_vm ():
    try:
        vmid = request.json['vmid']
        broker = request.json['broker']
        ohlcv2 = request.json['ohlcv2']

        try:
            vm = get_vm_from_cache(vmid)
        except KeyError:
            return jsonify(error='Not found in cache'), 205

        vm.broker.update(**broker)
        vm.market.update_ohlcv2(ohlcv2)
        
        actions = vm.step_new()
        return jsonify(actions=actions,
                       server_clock=utctimestamp())

    except Exception as e:
        logger.exception(f'request={request.path}: {request.data}')
        return jsonify(error=traceback.format_exc()), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
