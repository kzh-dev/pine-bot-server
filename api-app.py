# coding=utf-8

from datetime import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSON_SORT_KEYS'] = False

#@app.route('/')
#def landing ():
#    return render_template('landing.html')

from pine.base import PineError
from pine.vm.vm import InputScanVM
from pine.vm.step import StepVM
from pine.vm.compile import compile_pine
from pine.market.base import Market, MARKETS, str_to_resolution
import pine.market.bitmex
import pine.market.bitflyer
from pine.broker.mirror import MirrorBroker

import traceback
from collections import OrderedDict

from datetime import datetime, timezone
def utctimestamp ():
    return datetime.now(timezone.utc).timestamp()


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

        # FIXME should consider market recommendation
        default_qty = 1.0
        if vm.meta:
            default_qty = vm.meta.get('default_qty', 1.0)

        params = OrderedDict(
            exchange='BITMEX',
            symbol='XBTUSD',
            resolution=30,
            default_qty=default_qty,
        )
        for i in inputs:
            params[i['title']] = i['defval']

        return jsonify(params=params)

    except Exception as e:
        return jsonify(error=traceback.format_exc())


vm_cache = OrderedDict()
MAX_VM_CACHE_COUNT = 100

@app.route('/init-vm', methods=['POST'])
def init_vm ():
    try:
        code = request.json['code']
        params = request.json['params']

        # resolution
        resolution = str_to_resolution(params['resolution'])
        if resolution not in Market.RESOLUTIONS:
            raise Exception("unusable resolution: {}".format(resolution))
        # Market
        exchange = params['exchange']
        market_cls = MARKETS.get(exchange, None)
        if market_cls is None:
            raise Exception('unusable exchange: {}'.fomrat(exchange))
        market = market_cls(params['symbol'], resolution)

        # compile PINE
        node = compile_pine(code)
        if node is None:
            raise PineError("pine script is empty")

        # VM & broker
        vm = StepVM(market, code)
        vm.set_broker(MirrorBroker())

        # Set up and run
        vm.load_node(node)
        vm.set_user_inputs(params)
        vm.run()
    
        # Register VM to store
        vm_cache[vm.ident] = vm
        while len(vm_cache) > MAX_VM_CACHE_COUNT:
            vm_cache.pop_item()

        return jsonify(vm=vm.ident, clock=vm.clock, next_clock=vm.next_clock,
                       server_clock=int(utctimestamp()))

    except Exception as e:
        # ステータスコードは OK (200)
        return jsonify(error=traceback.format_exc())


@app.route('/step-vm', methods=['POST'])
def step_vm ():
    try:
        vmid = request.json['vm']
        next_clock = request.json['next_clock']
        broker = request.json['broker']

        vm = vm_cache.pop(vmid, None)
        if vm is None:
            return jsonify(error='Not found in cache'), 205
        vm_cache[vmid] = vm

        now = utctimestamp()
        interval = 10
        if next_clock - now > interval:
            return jsonify(server_clock=int(now)), 206

        if vm.next_clock != next_clock:
            raise Exception('out-of-sync: vm={0}, client={1}'.fomrat(vm.next_clock, next_clock))

        vm.broker.update(**broker)
        actions = vm.step_new()
        if actions is None:
            now = utctimestamp()
            return jsonify(server_clock=int(now)), 206

        return jsonify(actions=actions,
                       next_clock=vm.next_clock,
                       server_clock=int(utctimestamp()))

    except Exception as e:
        vm = vm_cache.pop(vmid, None)
        # ステータスコードは RESET
        return jsonify(error=traceback.format_exc()), 205

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
