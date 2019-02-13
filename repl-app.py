from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def landing ():
    return render_template('landing.html')

from pine.base import PineError
from pine.vm.vm import InputScanVM
from pine.vm.plot import PlotVM
from pine.vm.compile import compile_pine
from pine.market.base import Market
from pine.market.bitmex import BitMexMarket
from pine.broker.base import Broker

def convert_to_form (spec):
    return spec

import sys, traceback

@app.route('/evaluate', methods=['POST'])
def evaluate ():
    code = request.form['code']
    try:
        node = compile_pine(code)
        # Exract input
        vm = InputScanVM(Market())
        vm.load_node(node)
        inputs = vm.run()
        pine_title = vm.title
        forms = [convert_to_form(i) for i in inputs]
        return render_template('input_forms.html', title=pine_title, forms=forms, code=code)

    except PineError as e:
        return render_template('evaluate_error.html', error=str(e))
    except Exception as e:
        tb = traceback.format_exception(*sys.exc_info())
        return render_template('evaluate_error_exception.html', error=e, tb=tb)

@app.route('/run', methods=['POST'])
def run ():
    symbol = 'BITMEX:XBTUSD'
    code = ''
    resolution = None
    inputs = {}
    indicator_pane = 1
    for k in request.form:
        if k == 'code':
            code = request.form[k]
        elif k == 'symbol':
            symbol = request.form[symbol]
        elif k == 'resolution':
            resolution = request.form.get(k, type=int)
        else:
            inputs[k] = request.form[k]

    try:
        # FIXME parse again
        node = compile_pine(code)

        # Run
        market, symbol_ = symbol.split(':')
        market = BitMexMarket(symbol_, resolution)
        vm = PlotVM(market)
        vm.load_node(node)
        vm.set_user_inputs(inputs)
        vm.set_broker(Broker())
        vm.run()

        if vm.overlay:
            indicator_pane = 0

        html = _make_chart(market, vm.outputs, indicator_pane)
        return html
    except PineError as e:
        return render_template('evaluate_error.html', error=str(e))
    except Exception as e:
        tb = traceback.format_exception(*sys.exc_info())
        return render_template('evaluate_error_exception.html', error=e, tb=tb)


import time, requests
from collections import OrderedDict
import pandas as pd
from chart_creator import ChartCreator as cc

import math
def _make_non_na (timestamps, series):
    ts = []
    srs = []
    for t, v in zip(timestamps, series):
        if math.isnan(v):
            continue
        ts.append(t)
        srs.append(v)
    return (ts, srs)

def _make_chart (market, plots, indicator_pane):
    file_path = "chart.html" 

    # OHLCVデータ取得
    df = market.ohlcv_df()

    # チャート初期化
    cc.initialize()

    # メインチャート(ax:0)設定
    cc.add_subchart(ax=0, label="Price", grid=True)

    # ローソクバー設定(OHLCV)
    cc.set_ohlcv_df(df)

    if indicator_pane != 0:
        cc.add_subchart(ax=indicator_pane, grid=True)

    ts = df['unixtime'].values

    for plot in plots:
        title = plot['title']
        series = plot['series']

        typ = plot.get('type', 'line')
        color = plot.get('color', 'blue')
        width = plot.get('width', 1)

        if typ == 'line':
            t, s = _make_non_na(ts, series)
            if t:
                cc.set_line(t, s,
                            ax=indicator_pane, color=color, width=width, name=title)
        elif typ == 'band':
            t, s = _make_non_na(ts, series)
            alpha = plot.get('alpha', 0.5)
            ymin = min(s)
            ymax = max(s)
            ymin = ymin - (ymax - ymin) * 0.5
            if t:
                cc.set_band(t, s, [ymin] * len(series),
                            ax=indicator_pane, up_color=color, edge_width=width, alpha=alpha, name=title)
        elif typ == 'bar':
            t, s = _make_non_na(ts, series)
            if t:
                cc.set_bar(t, s, ax=indicator_pane, color=color, name=title)
        elif typ == 'hline':
            cc.set_line([ts[0], ts[-1]], [series, series],
                        ax=indicator_pane, color=color, width=width, name=title)
        elif typ == 'marker':
            t, s = _make_non_na(ts, series)
            if t:
                cc.set_marker(t, s,
                            ax=indicator_pane, color=color, size=width*10, mark=plot['mark'], name=title)
        elif typ == 'fill':
            series2 = plot['series2']
            alpha = plot.get('alpha', 0.5)
            ts_ = ts
            if type(series) == float:
                ts_ = [ts[0], ts[-1]]
                series = [series, series]
                series2 = [series2, series2]
            cc.set_band(ts_, series2, series,
                        ax=indicator_pane, up_color=color, alpha=alpha, name=title)
                        

    # SMA計算
    #sma = df["close"].rolling(window=14, min_periods=1).mean()

    # メインチャートにSMA設定
    #cc.set_line(df["unixtime"].values, sma, ax=0, color="blue", width=1.0, name="SMA")

    # MACD計算
    #ema12 = df["close"].ewm(span=12).mean()
    #ema26 = df["close"].ewm(span=26).mean()
    #macd = ema12 - ema26
    #signal = macd.ewm(span=9).mean()
    #hist = macd - signal

    # MACDサブチャート(ax:1)追加
    #cc.add_subchart(ax=1, label="MACD", grid=True)

    # MACD設定
    #cc.set_line(df["unixtime"].values, macd, ax=1, color="red", width=1.0, name="MACD")
    #cc.set_line(df["unixtime"].values, signal, ax=1, color="cyan", width=1.0, name="Signal")
    #cc.set_bar(df["unixtime"].values, hist, ax=1, color="orange", name="Hist")

    # チャート生成
    return cc.create_chart(file_path, chart_mode="html")


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(port)
    app.run(port=port)
