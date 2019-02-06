# -*- coding: utf-8 -*-
import os, time
from webcolors import rgb_to_name, name_to_rgb
import numpy as np
import pandas as pd
import pandas.tseries.offsets as offsets

import matplotlib # pip install matplotlib
matplotlib.use("Agg")
import mpl_finance as mpf # pip install mpl_finance
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import plotly # pip install plotly
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot
from plotly.offline.offline import _plot_html

#=================================================================
#【ChartCreator】
# Code and documentation copyright 2018 Nagi
#=================================================================
class ChartCreator(object):

    # 設定情報
    settings = {
        "fig_size"   : [12, 8],         # 画像サイズ(横, 縦)
        "fig_dpi"    : 100,             # 画像解像度(DPI)
        "frontcolor" : "DimGray",       # 前景色(文字etc.)
        "backcolor"  : "#FAFAFA",       # 背景色
        "title"      : "chart",         # タイトル文字
        "title_size" : 16,              # タイトル文字サイズ
        "label_size" : 8,               # ラベルサイズ(X/Y見出しetc.)
        "bar"   : {
            "up_color"   : "#53B987",   # 陽線色(ローソク)
            "down_color" : "#EB4D5C",   # 陰線色(ローソク)
        },
        "volume_bar" : True,            # 出来高表示
        "xaxis" : {
            "grid"   : True,            # X軸グリッド表示
        },
        "legend"     : "Top",           # 凡例表示("Top"/"Bottom"/None)
    }

    # OHLCV DataFrame(columns=["unixtime", "open", "high", "low", "close", "volume"])
    __df_ohlcv = pd.DataFrame([], columns=["unixtime", "open", "high", "low", "close", "volume"])
    __start_x  = 0
    __end_x    = 0
    __tick_x   = 0

    # サブチャート
    __subcharts = {0 : {"grid" : True, "label" : "y"}}

    # インジケータ
    __indicators = []

    # Marker Map
    __markers = {
        "." : 0,  "," : 0,  "o" : 0,  "*" : 17,
        "v" : 6,  "^" : 5,  "<" : 7,  ">" : 8,
        "1" : 6,  "2" : 5,  "3" : 7,  "4" : 8,
        "8" : 16, "s" : 1,  "p" : 13, "x" : 4,
        "h" : 14, "H" : 14, "+" : 3,
        "D" : 2,  "d" : 23
    }

    #---------------------------------------------------------------------
    # 初期化
    # チャートレイアウト, OHLCV, indicators etc.全て初期状態にクリア
    #---------------------------------------------------------------------
    @classmethod
    def initialize(cls):
        cls.settings = {
            "fig_size"   : [12, 8],         # 画像サイズ(横, 縦)
            "fig_dpi"    : 100,             # 画像解像度(DPI)
            "frontcolor" : "DimGray",       # 前景色(文字etc.)
            "backcolor"  : "#FAFAFA",       # 背景色
            "title"      : "chart",         # タイトル
            "title_size" : 16,              # タイトル文字サイズ
            "label_size" : 8,               # ラベルサイズ(X/Y見出しetc.)
            "bar"   : {
                "up_color"   : "#53B987",   # 陽線色(ローソク)
                "down_color" : "#EB4D5C",   # 陰線色(ローソク)
            },
            "volume_bar" : True,            # 出来高表示
            "xaxis" : {
                "grid"   : True,            # X軸グリッド表示
            },
            "legend"     : "Top",           # 凡例表示("Top"/"Bottom"/None)
        }
        cls.__df_ohlcv = pd.DataFrame([], columns=["unixtime", "open", "high", "low", "close", "volume"])
        cls.__start_x  = 0
        cls.__end_x    = 0
        cls.__tick_x   = 0
        cls.__subcharts  = {0 : {"grid" : True, "label" : "y"}}
        cls.__indicators = []

    #---------------------------------------------------------------------
    # データクリア
    # OHLCV, indicatorsのみクリア
    # チャートレイアウトなどは保持
    #---------------------------------------------------------------------
    @classmethod
    def clear(cls):
        cls.__df_ohlcv = pd.DataFrame([], columns=["unixtime", "open", "high", "low", "close", "volume"])
        cls.__start_x  = 0
        cls.__end_x    = 0
        cls.__tick_x   = 0
        cls.__indicators = []

    #---------------------------------------------------------------------
    # サブチャート追加
    # [重要] indicatorを設定する前にサブチャート追加をしておく必要がある
    #---------------------------------------------------------------------
    # [@param]
    #     ax     0:メインチャート, 1～:サブチャート
    #     label  Y軸見出し
    #     grid   Y軸方向のグリッドON/OFF
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def add_subchart(cls, ax=1, label="y", grid=True):
        if ax in cls.__subcharts.keys():
            cls.__subcharts[ax]["grid"] = grid
            cls.__subcharts[ax]["label"] = label
        else:
            cls.__subcharts[ax] = {"grid":grid, "label":label}

    #---------------------------------------------------------------------
    # OHLCV設定(DataFrame)
    # ローソク足として表示するOHLCVデータをDataFrameで設定する
    # [重要] timestampはUnixTime(秒)にすること
    #---------------------------------------------------------------------
    # [@param]
    #     df_ohlcv  DataFrame([UnixTime, open, high, low, close, volume])
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_ohlcv_df(cls, df_ohlcv):
        if "unixtime" not in df_ohlcv.keys() or len(df_ohlcv.index) < 2:
            return
        ts = df_ohlcv["unixtime"].values
        if ts[0] < ts[-1]:
            cls.__df_ohlcv = df_ohlcv.copy()
        else:
            cls.__df_ohlcv = df_ohlcv.copy().iloc[::-1]
        cls.__df_ohlcv.reset_index(drop=True, inplace=True)

        cls.__tick_x  = cls.__df_ohlcv["unixtime"].iloc[1] - cls.__df_ohlcv["unixtime"].iloc[0]
        cls.__start_x = cls.__df_ohlcv["unixtime"].iloc[0]
        cls.__end_x   = cls.__df_ohlcv["unixtime"].iloc[-1]

    #---------------------------------------------------------------------
    # OHLCV設定(List)
    # ローソク足として表示するOHLCVデータをListで設定する
    # [重要] timestampはUnixTime(秒)にすること
    #---------------------------------------------------------------------
    # [@param]
    #     lst_ohlcv  List([UnixTime, open, high, low, close, volume])
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_ohlcv_lst(cls, lst_ohlcv):
        if len(lst_ohlcv) < 2 or len(lst_ohlcv[0]) < 6:
            return
        if lst_ohlcv[0][0] < lst_ohlcv[-1][0]:
            ohlcv = lst_ohlcv.copy()
        else:
            ohlcv = lst_ohlcv.copy()[::-1]
        cls.__df_ohlcv = pd.DataFrame(ohlcv,
            columns=["unixtime", "open", "high", "low", "close", "volume"])

        cls.__tick_x  = cls.__df_ohlcv["unixtime"].iloc[1] - cls.__df_ohlcv["unixtime"].iloc[0]
        cls.__start_x = cls.__df_ohlcv["unixtime"].iloc[0]
        cls.__end_x   = cls.__df_ohlcv["unixtime"].iloc[-1]

    #---------------------------------------------------------------------
    # LINE設定
    #---------------------------------------------------------------------
    # [@param]
    #     lst_utime  X値リスト(UnixTime(秒))
    #     lst_plot   Y値リスト
    #     ax         描画するチャート番号
    #     color      線色
    #     width      線幅
    #     name       名前(plotlyホバー表示名)
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_line(cls, lst_utime, lst_plot, ax=0, color="black", width=1.0, name=""):
        if ax not in cls.__subcharts.keys():
            return
        if len(lst_utime) < 2 or len(lst_plot) < 2:
            return
        if lst_utime[0] < lst_utime[-1]:
            np_ut = np.array(lst_utime)
            np_pl = np.array(lst_plot)
        else:
            np_ut = np.array(lst_utime[::-1])
            np_pl = np.array(lst_plot[::-1])

        cls.__indicators += [{
            "ax"       : ax,
            "type"     : "line",
            "unixtime" : np_ut,
            "plot"     : np_pl,
            "color"    : color,
            "width"    : width,
            "name"     : name,
        }]

    #---------------------------------------------------------------------
    # HLINE設定(水平線)
    #---------------------------------------------------------------------
    # [@param]
    #     plot       水平線の値
    #     ax         描画するチャート番号
    #     color      線色
    #     width      線幅
    #     name       名前(plotlyホバー表示名)
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_hline(cls, plot, ax=0, color="black", width=1.0, name=""):
        if ax not in cls.__subcharts.keys():
            return
        cls.__indicators += [{
            "ax"       : ax,
            "type"     : "line",
            "unixtime" : np.array([]),
            "plot"     : np.array([plot, plot]),
            "color"    : color,
            "width"    : width,
            "name"     : name,
        }]

    #---------------------------------------------------------------------
    # VLINE設定(垂直線)
    #---------------------------------------------------------------------
    # [@param]
    #     utime      垂直線のUnixTime
    #     ax         描画するチャート番号
    #     color      線色
    #     width      線幅
    #     name       名前(plotlyホバー表示名)
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_vline(cls, utime, ax=0, color="black", width=1.0, name=""):
        if ax not in cls.__subcharts.keys():
            return
        cls.__indicators += [{
            "ax"       : ax,
            "type"     : "line",
            "unixtime" : np.array([utime, utime]),
            "plot"     : np.array([]),
            "color"    : color,
            "width"    : width,
            "name"     : name,
        }]

    #---------------------------------------------------------------------
    # BAND設定
    #---------------------------------------------------------------------
    # [@param]
    #     lst_utime  X値リスト(UnixTime(秒))
    #     lst_plot1  Y値リスト1
    #     lst_plot2  Y値リスト2
    #     ax         描画するチャート番号
    #     up_color   plot1 > plot2の時の塗り色
    #     down_color plot1 < plot2の時の塗り色
    #     alpha      透過率
    #     edge_width 線幅
    #     edge_color 線色
    #     name       名前(plotlyホバー表示名)
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_band(cls, lst_utime, lst_plot1, lst_plot2, ax=0, up_color="blue", down_color="red", alpha=0.5, edge_width=0.5, edge_color="black", name=""):
        if ax not in cls.__subcharts.keys():
            return
        if len(lst_utime) < 2 or len(lst_plot1) < 2 or len(lst_plot2) < 2:
            return
        if lst_utime[0] < lst_utime[-1]:
            np_ut = np.array(lst_utime)
            np_pl1 = np.array(lst_plot1)
            np_pl2 = np.array(lst_plot2)
        else:
            np_ut = np.array(lst_utime[::-1])
            np_pl1 = np.array(lst_plot1[::-1])
            np_pl2 = np.array(lst_plot2[::-1])

        cls.__indicators += [{
            "ax"         : ax,
            "type"       : "band",
            "unixtime"   : np_ut,
            "plot1"      : np_pl1,
            "plot2"      : np_pl2,
            "up_color"   : up_color,
            "down_color" : down_color,
            "alpha"      : alpha,
            "edge_width" : edge_width,
            "edge_color" : edge_color,
            "name"       : name,
        }]

    #---------------------------------------------------------------------
    # BAR設定
    #---------------------------------------------------------------------
    # [@param]
    #     lst_utime  X値リスト(UnixTime(秒))
    #     lst_plot   Y値リスト
    #     ax         描画するチャート番号
    #     color      バー色
    #     name       名前(plotlyホバー表示名)
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_bar(cls, lst_utime, lst_plot, ax=0, color="red", name=""):
        if ax not in cls.__subcharts.keys():
            return
        if len(lst_utime) < 2 or len(lst_plot) < 2:
            return
        if lst_utime[0] < lst_utime[-1]:
            np_ut = np.array(lst_utime)
            np_pl = np.array(lst_plot)
        else:
            np_ut = np.array(lst_utime[::-1])
            np_pl = np.array(lst_plot[::-1])

        cls.__indicators += [{
            "ax"       : ax,
            "type"     : "bar",
            "unixtime" : np_ut,
            "plot"     : np_pl,
            "color"    : color,
            "name"     : name,
        }]

    #---------------------------------------------------------------------
    # MARK設定
    #---------------------------------------------------------------------
    # [@param]
    #     lst_utime  X値リスト(UnixTime(秒))
    #     lst_plot   Y値リスト
    #     ax         描画するチャート番号
    #     color      マーク色
    #     size       マークサイズ
    #     mark       マーク種類(使用できるmark種類は以下を参照)
    #                (http://ailaby.com/plot_marker/)
    #     name       名前(plotlyホバー表示名)
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_marker(cls, lst_utime, lst_plot, ax=0, color="black", size=20.0, mark="*", name=""):
        if ax not in cls.__subcharts.keys():
            return
        if len(lst_utime) < 2 or len(lst_plot) < 2:
            return
        if lst_utime[0] < lst_utime[-1]:
            np_ut = np.array(lst_utime)
            np_pl = np.array(lst_plot)
        else:
            np_ut = np.array(lst_utime[::-1])
            np_pl = np.array(lst_plot[::-1])

        cls.__indicators += [{
            "ax"       : ax,
            "type"     : "mark",
            "unixtime" : np_ut,
            "plot"     : np_pl,
            "color"    : color,
            "size"     : size,
            "mark"     : mark,
            "name"     : name,
        }]

    #---------------------------------------------------------------------
    # OHLCV設定
    #---------------------------------------------------------------------
    # [@param]
    #     df_ohlcv   OHLCV DataFrame(メインチャートと同じ期間であること)
    #     ax         描画するチャート番号
    #     vol_bar    出来高バーを表示(True:表示, False:非表示)
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def set_sub_ohlcv(cls, df_ohlcv, ax=1, vol_bar=True):
        if ax not in cls.__subcharts.keys():
            return
        if len(df_ohlcv.index) != len(cls.__df_ohlcv.index):
            return
        if df_ohlcv.unixtime.values[0] > df_ohlcv.unixtime.values[-1]:
            df_ohlcv = df_ohlcv.iloc[::-1]

        cls.__indicators += [{
            "ax"       : ax,
            "type"     : "ohlcv",
            "ohlcv"    : df_ohlcv,
            "vol_bar"  : vol_bar,
        }]

    #---------------------------------------------------------------------
    # BOARD設定
    #---------------------------------------------------------------------
    # [@param]
    #     lst_utime       UnixTime(秒)リスト([UnixTime1, UnixTime2, ...])
    #     lst_bids        UnixTime(秒)毎のbidsリスト(bids形式は下記参照)
    #     lst_asks        UnixTime(秒)毎のasksリスト(asks形式は下記参照)
    #     ax              描画するチャート番号
    #     line_width      best bid/ask 線幅
    #     hover_count     ホバーに表示する板件数(bids/asksそれぞれ)
    #     highlight_size  ホバーの板情報で指定値以上のsizeを強調表示する
    #     bid_line_color  best bid 線色
    #     ask_line_color  best ask 線色
    #     bid_hover_color bids ホバー背景色
    #     ask_hover_color asks ホバー背景色
    #     highlight_color ホバーテキスト強調表示色
    # [return]
    #---------------------------------------------------------------------
    # [bids/asks形式]
    #   bids/asksの2次元リスト形式は以下の2パターンどちらでも可能
    #   ・パターン1 (priceとsizeリストの配列)
    #       bids/asks = [
    #         [price1, size1],
    #         [price2, size2],
    #                :
    #       ]
    #   ・パターン2 (priceリストとsizeリストの配列)
    #       bids/asks = [
    #         [price1, price2, price3, ...],
    #         [size1, size2, size3, ...],
    #       ]
    #
    #   ・UnixTime(秒)毎のbids/asksリスト(要素数はlst_utimeと同数であること)
    #     lst_bids = [bids1, bids2, bids3, ...]
    #     lst_asks = [asks1, asks2, asks3, ...]
    #---------------------------------------------------------------------
    @classmethod
    def set_board(cls, lst_utime, lst_bids, lst_asks, ax=0,
                  line_width=1.0, hover_count=20, highlight_size=1000000,
                  bid_line_color="blue", ask_line_color="red",
                  bid_hover_color="lightcyan", ask_hover_color="lavenderblush",
                  highlight_color="red"):
        if ax not in cls.__subcharts.keys():
            return
        if len(lst_utime) < 2:
            return
        if len(lst_utime) != len(lst_bids) or len(lst_utime) != len(lst_asks):
            return
        if lst_utime[0] > lst_utime[-1]:
            lst_utime = lst_utime[::-1]
            lst_bids = lst_bids[::-1]
            lst_asks = lst_asks[::-1]

        lst_best_bid = []
        lst_best_ask = []
        lst_bids_hover = []
        lst_asks_hover = []
        for i in range(len(lst_utime)):
            # bids DataFrame作成＆ソート
            if len(lst_bids[i]) == 2:
                # [[price1,price2,...], [size1,size2,...]]
                df_bids = pd.DataFrame([[bid[0],bid[1]] for bid in zip(lst_bids[i][0], lst_bids[i][1])],
                                       columns=["price", "size"])
            elif len(lst_bids[i][0]) == 2:
                # [[price1,size1], [price2,size2],...]
                df_bids = pd.DataFrame(lst_bids[i],
                                       columns=["price", "size"])
            df_bids.set_index(["price"], inplace=True)
            df_bids.sort_index(ascending=False, inplace=True)

            # asks DataFrame作成＆ソート
            if len(lst_asks[i]) == 2:
                # [[price1,price2,...], [size1,size2,...]]
                df_asks = pd.DataFrame([[ask[0],ask[1]] for ask in zip(lst_asks[i][0], lst_asks[i][1])],
                                       columns=["price", "size"])
            elif len(lst_asks[i][0]) == 2:
                # [[price1,size1], [price2,size2],...]
                df_asks = pd.DataFrame(lst_asks[i],
                                       columns=["price", "size"])
            df_asks.set_index(["price"], inplace=True)
            df_asks.sort_index(ascending=True, inplace=True)

            # best bid/ask list格納
            lst_best_bid.append(df_bids.index[0])
            lst_best_ask.append(df_asks.index[0])

            # hover表示板件数取得
            cnt = min(hover_count, len(df_bids.index))

            # bids/asksを表示件数にトリミング
            df_bids = df_bids.iloc[:cnt]
            df_asks = df_asks.iloc[:cnt]

            # hover表示並び用にasksを反転
            df_asks = df_asks.iloc[::-1]

            bids_price = df_bids.index
            bids_size  = df_bids["size"].values
            asks_price = df_asks.index
            asks_size  = df_asks["size"].values

            # hoverテキスト作成
            bids_hover = ""
            asks_hover = "[  price ] [  size  ]"
            for j in range(cnt):
                # 改行タグ
                if len(bids_hover) > 0:
                    bids_hover += "<br>"
                if len(asks_hover) > 0:
                    asks_hover += "<br>"

                # 板の行テキスト
                bid_text = "{:>10,} {:>10,}".format(bids_price[j], bids_size[j])
                ask_text = "{:>10,} {:>10,}".format(asks_price[j], asks_size[j])

                # sizeがhighlight_sizeを超えている場合、強調表示
                # bids
                if highlight_size <= bids_size[j]:
                    bids_hover += '<b><i><span style="color: ' + cls.color_to_hex(highlight_color) + ';">'
                    bids_hover += bid_text + "</span></i></b>"
                else:
                    bids_hover += bid_text
                # asks
                if highlight_size <= asks_size[j]:
                    asks_hover += '<b><i><span style="color: ' + cls.color_to_hex(highlight_color) + ';">'
                    asks_hover += ask_text + "</span></i></b>"
                else:
                    asks_hover += ask_text

            # bids/asks hover list格納
            lst_bids_hover.append(bids_hover)
            lst_asks_hover.append(asks_hover)

        cls.__indicators += [{
            "ax"              : ax,
            "type"            : "board",
            "unixtime"        : np.array(lst_utime),
            "best_bid"        : np.array(lst_best_bid),
            "best_ask"        : np.array(lst_best_ask),
            "hover_bids"      : lst_bids_hover,
            "hover_asks"      : lst_asks_hover,
            "line_width"      : line_width,
            "bid_line_color"  : bid_line_color,
            "ask_line_color"  : ask_line_color,
            "bid_hover_color" : bid_hover_color,
            "ask_hover_color" : ask_hover_color,
        }]

    #---------------------------------------------------------------------
    # チャート生成
    #---------------------------------------------------------------------
    # [@param]
    #     path          作成したチャート画像ファイル保存パス
    #     chart_mode    "png":matplotlib, "html":plotly
    # [return]
    #---------------------------------------------------------------------
    @classmethod
    def create_chart(cls, path, chart_mode="png"):
        if cls.__df_ohlcv is None or len(cls.__df_ohlcv.index) < 2:
            return
        if cls.__start_x == 0 or cls.__end_x == 0 or cls.__tick_x == 0:
            return
        if 0 not in cls.__subcharts.keys():
            return

        # ディレクトリ存在チェック
        #dir_path = os.path.dirname(path)
        #if not os.path.exists(dir_path):
        #    os.makedirs(dir_path)

        # chart_modeと拡張子チェック
        ext = os.path.splitext(path)[1][1:]
        if chart_mode == "png" and chart_mode == ext:
            # matplotlibでpngチャート生成
            cls.__create_chart_mpl(path)

        elif chart_mode == "html" and chart_mode == ext:
            # plotlyでhtmlチャート生成
            return cls.__create_chart_plt(path)

    #---------------------------------------------------------------------
    # matplotlibチャート生成
    #---------------------------------------------------------------------
    @classmethod
    def __create_chart_mpl(cls, path):
        keys = [*cls.__subcharts]
        keys.sort()
        # ローソクサブチャート検索
        ohlcv_sub = [indi["ax"] for indi in cls.__indicators if indi["type"] == "ohlcv"]
        GridSpec = 0
        for key in keys:
            if key == 0:
                GridSpec += 3
            elif key in ohlcv_sub:
                GridSpec += 2
            else:
                GridSpec += 1
        #GridSpec = len(keys) + 2

        # datetime列
        cls.__df_ohlcv["date"] = pd.to_datetime(cls.__df_ohlcv["unixtime"], unit="s")
        cls.__df_ohlcv["date"] += offsets.Hour(9)

        # チャート余白(左右)を除去
        matplotlib.rcParams["axes.xmargin"] = 0
        matplotlib.rcParams["axes.ymargin"] = 0

        # 描画領域を作成
        # Figure(図全体)
        fig = plt.figure(figsize=(cls.settings["fig_size"][0],
                                  cls.settings["fig_size"][1]), # 領域サイズ
                         dpi    =cls.settings["fig_dpi"]) # 解像度
        fig.autofmt_xdate() # x軸のオートフォーマット
        # チャート配置割り
        gs = gridspec.GridSpec(GridSpec, 1)
        #plt.subplots_adjust(top=0.92, bottom=0.06, right=0.95, wspace=0.0, hspace=0.0)
        plt.subplots_adjust(wspace=0.0, hspace=0.0) # グラフ間余白

        # ax0:メインチャート
        ax0 = plt.subplot(gs[0:3, 0])
        ax0.set_title(cls.settings["title"], loc="center", fontsize=cls.settings["title_size"], color=cls.settings["frontcolor"], fontdict={"verticalalignment": "bottom", "fontweight": 600})
        #ax0.set_aspect("equal", adjustable="box") # 縦横比
        ax0.patch.set_facecolor(cls.settings["backcolor"]) # 背景色
        ax0.set_axisbelow(True)                # グリッドがプロットした点や線の下に隠れる
        ax0.xaxis.grid(cls.settings["xaxis"]["grid"], which="major", linestyle="dotted", color=cls.settings["frontcolor"]) # x軸に垂直なグリッドメソッド
        ax0.yaxis.grid(cls.__subcharts[0]["grid"], which="major", linestyle="dotted", color=cls.settings["frontcolor"]) # y軸に垂直なグリッドメソッド
        ax0.tick_params(axis="y", labelsize=cls.settings["label_size"], labelcolor=cls.settings["frontcolor"], color=cls.settings["frontcolor"])
        ax0.set_ylabel(cls.__subcharts[0]["label"], fontsize=cls.settings["label_size"], color=cls.settings["frontcolor"])     # yラベル設定
        ax0.set_xlim(-1, len(cls.__df_ohlcv["date"]))   # x軸の範囲
        if keys[-1] == 0:
            ax0.tick_params(axis="x", labelsize=cls.settings["label_size"], labelcolor=cls.settings["frontcolor"], color=cls.settings["frontcolor"])
        else:
            ax0.tick_params(labelbottom=False, bottom=False)         # x軸非表示

        y_min = cls.__df_ohlcv["low"].min()
        y_max = cls.__df_ohlcv["high"].max()
        y_margin = (y_max - y_min) * 0.05
        y_min -= y_margin
        y_max += y_margin
        if cls.settings["volume_bar"]:
            # ローソク足を上側75%に収める
            y_min = y_min - (y_max - y_min) / 4

        # ローソク足描画
        mpf.candlestick2_ohlc(ax0,
                              opens     = cls.__df_ohlcv["open"], # 始値
                              highs     = cls.__df_ohlcv["high"], # 高値
                              lows      = cls.__df_ohlcv["low"],  # 安値
                              closes    = cls.__df_ohlcv["close"],# 終値
                              width     = 0.8,                    # バー横幅
                              colorup   = cls.settings["bar"]["up_color"],   # 陽線色
                              colordown = cls.settings["bar"]["down_color"]) # 陰線色
        # 出来高bar
        if cls.settings["volume_bar"]:
            # ax0_1:メインチャートに出来高を重ねる
            ax0_1 = ax0.twinx()
            # 出来高チャートは下側25%に収める
            ax0_1.set_ylim([0, cls.__df_ohlcv["volume"].max() * 4])
            ax0_1.tick_params(axis="y", labelsize=cls.settings["label_size"], labelcolor=cls.settings["frontcolor"], color=cls.settings["frontcolor"])
            ax0_1.set_ylabel("Volume", fontsize=cls.settings["label_size"], color=cls.settings["frontcolor"])     # yラベル設定
            # 出来高描画
            mpf.volume_overlay(ax0_1,
                               opens     = cls.__df_ohlcv["open"],
                               closes    = cls.__df_ohlcv["close"],
                               volumes   = cls.__df_ohlcv["volume"],
                               width     = 1.0,
                               colorup   = cls.settings["bar"]["up_color"],   # 陽線色
                               colordown = cls.settings["bar"]["down_color"], # 陰線色
                               alpha     = 0.5)
        # axe dictionry
        axes = {keys[0] : [ax0, y_min, y_max]}

        # サブチャート生成
        gs_from = 3
        for key in keys:
            if key == 0:
                continue
            # ax:サブチャート
            if key in ohlcv_sub:
                gs_range = 2
            else:
                gs_range = 1
            ax = plt.subplot(gs[gs_from:gs_from+gs_range, 0], sharex=ax0)
            #ax.set_aspect("equal", adjustable="box") # 縦横比
            ax.patch.set_facecolor(cls.settings["backcolor"]) # 背景色
            ax.set_axisbelow(True)                # グリッドがプロットした点や線の下に隠れる
            ax.xaxis.grid(cls.settings["xaxis"]["grid"], which="major", linestyle="dotted", color=cls.settings["frontcolor"]) # x軸に垂直なグリッドメソッド
            ax.yaxis.grid(cls.__subcharts[key]["grid"], which="major", linestyle="dotted", color=cls.settings["frontcolor"]) # y軸に垂直なグリッドメソッド
            ax.tick_params(axis="y", labelsize=cls.settings["label_size"], labelcolor=cls.settings["frontcolor"], color=cls.settings["frontcolor"])
            ax.set_ylabel(cls.__subcharts[key]["label"], fontsize=cls.settings["label_size"], color=cls.settings["frontcolor"])     # yラベル設定
            if keys[-1] == key:
                ax.tick_params(axis="x", labelsize=cls.settings["label_size"], labelcolor=cls.settings["frontcolor"], color=cls.settings["frontcolor"])
            else:
                ax.tick_params(labelbottom=False, bottom=False)         # x軸非表示
            axes[key] = [ax, 999999999, -999999999]
            gs_from += gs_range

        # candle bars
        bars = (cls.__end_x - cls.__start_x) / cls.__tick_x
        # 最初の区切り目盛りのインデックス
        unit_x = int(bars / 10) # X軸目盛り区切り間隔
        if cls.__tick_x < 60:
            xtick0 = (unit_x - cls.__df_ohlcv["date"][0].second % unit_x)
            time_format = "%m/%d %H:%M:%S"
        elif cls.__tick_x < 3600:
            xtick0 = (unit_x - cls.__df_ohlcv["date"][0].minute % unit_x)
            time_format = "%m/%d %H:%M"
        elif cls.__tick_x < 86400:
            xtick0 = (unit_x - cls.__df_ohlcv["date"][0].hour % unit_x)
            time_format = "%m/%d %H:%M"
        else:
            xtick0 = (unit_x - cls.__df_ohlcv["date"][0].day % unit_x)
            time_format = "%y/%m/%d"
        # 区切り間隔からX軸目盛設定
        plt.xticks(range(xtick0, len(cls.__df_ohlcv["date"]), unit_x), # 位置配列
                   [x.strftime(time_format) for x in cls.__df_ohlcv["date"]][xtick0::unit_x]) # ラベル配列

        # インジケータ
        for indi in cls.__indicators:
            ax = axes[indi["ax"]][0]
            if indi["type"] != "ohlcv":
                np_x = (indi["unixtime"] - cls.__start_x) / cls.__tick_x
            y_min = 999999999
            y_max = -999999999
            if indi["type"] == "line":
                if len(indi["plot"]) > 0:
                    y_min = indi["plot"].min()
                    y_max = indi["plot"].max()
                if len(indi["unixtime"]) == 0:
                    ax.hlines(y=indi["plot"][0], xmin=0, xmax=bars, color=indi["color"], linewidth=indi["width"])
                elif len(indi["plot"]) == 0:
                    ax.vlines(x=np_x[0], ymin=-999999999, ymax=999999999, color=indi["color"], linewidth=indi["width"])
                else:
                    ax.plot(np_x, indi["plot"], color=indi["color"], linewidth=indi["width"])

            elif indi["type"] == "band":
                y_min = min([indi["plot1"].min(), indi["plot2"].min()])
                y_max = max([indi["plot1"].max(), indi["plot2"].max()])
                if indi["up_color"] == indi["down_color"]:
                    ax.fill_between(np_x, indi["plot1"], indi["plot2"], facecolor=indi["up_color"], alpha=indi["alpha"], interpolate=True)
                else:
                    ax.fill_between(np_x, indi["plot1"], indi["plot2"], where=indi["plot1"] >= indi["plot2"],
                             facecolor=indi["up_color"], alpha=indi["alpha"], interpolate=True)
                    ax.fill_between(np_x, indi["plot1"], indi["plot2"], where=indi["plot1"] <= indi["plot2"],
                             facecolor=indi["down_color"], alpha=indi["alpha"], interpolate=True)
                if indi["edge_width"] > 0.0:
                    ax.plot(np_x, indi["plot1"], np_x, indi["plot2"], color=indi["edge_color"], linewidth=indi["edge_width"])

            elif indi["type"] == "bar":
                y_min = indi["plot"].min()
                y_max = indi["plot"].max()
                ax.bar(np_x, indi["plot"], color=indi["color"])

            elif indi["type"] == "mark":
                y_min = indi["plot"].min()
                y_max = indi["plot"].max()
                ax.scatter(np_x, indi["plot"], marker=indi["mark"], s=indi["size"], c=indi["color"])

            elif indi["type"] == "ohlcv":
                y_min = indi["ohlcv"]["low"].min()
                y_max = indi["ohlcv"]["high"].max()
                if indi["vol_bar"]:
                    # ローソク足を上側75%に収める
                    y_min = y_min - (y_max - y_min) / 4
                # ローソク足描画
                mpf.candlestick2_ohlc(ax,
                                      opens     = indi["ohlcv"]["open"], # 始値
                                      highs     = indi["ohlcv"]["high"], # 高値
                                      lows      = indi["ohlcv"]["low"],  # 安値
                                      closes    = indi["ohlcv"]["close"],# 終値
                                      width     = 0.8,                   # バー横幅
                                      colorup   = cls.settings["bar"]["up_color"],   # 陽線色
                                      colordown = cls.settings["bar"]["down_color"]) # 陰線色
                # 出来高bar
                if indi["vol_bar"]:
                    # ax0_1:メインチャートに出来高を重ねる
                    ax_1 = ax.twinx()
                    # 出来高チャートは下側25%に収める
                    ax_1.set_ylim([0, indi["ohlcv"]["volume"].max() * 4])
                    ax_1.tick_params(axis="y", labelsize=cls.settings["label_size"], labelcolor=cls.settings["frontcolor"], color=cls.settings["frontcolor"])
                    ax_1.set_ylabel("Volume", fontsize=cls.settings["label_size"], color=cls.settings["frontcolor"])     # yラベル設定
                    # 出来高描画
                    mpf.volume_overlay(ax_1,
                                       opens     = indi["ohlcv"]["open"],
                                       closes    = indi["ohlcv"]["close"],
                                       volumes   = indi["ohlcv"]["volume"],
                                       width     = 1.0,
                                       colorup   = cls.settings["bar"]["up_color"],   # 陽線色
                                       colordown = cls.settings["bar"]["down_color"], # 陰線色
                                       alpha     = 0.5)

            elif indi["type"] == "board":
                y_min = min([indi["best_bid"].min(), indi["best_ask"].min()])
                y_max = max([indi["best_bid"].max(), indi["best_ask"].max()])
                if indi["line_width"] > 0.0:
                    ax.plot(np_x, indi["best_bid"], color=indi["bid_line_color"], linewidth=indi["line_width"])
                    ax.plot(np_x, indi["best_ask"], color=indi["ask_line_color"], linewidth=indi["line_width"])

            y_margin = (y_max - y_min) * 0.05
            if axes[indi["ax"]][1] > y_min - y_margin:
                axes[indi["ax"]][1] = y_min - y_margin
            if axes[indi["ax"]][2] < y_max + y_margin:
                axes[indi["ax"]][2] = y_max + y_margin

        # Y軸調整
        for ax in axes.values():
            ax[0].set_ylim(ax[1], ax[2])

        # pngファイル出力
        plt.savefig(path, dpi=cls.settings["fig_dpi"], bbox_inches="tight", pad_inches=0.2, transparent=False)
        plt.close()

    #---------------------------------------------------------------------
    # plotlyチャート生成
    #---------------------------------------------------------------------
    @classmethod
    def __create_chart_plt(cls, path):
        # Plotlyバージョン確認
        #print("Plotly version:{}".format(plotly.__version__))
        ver_str = plotly.__version__.replace(".", "")
        plotly_version = int(ver_str) if len(ver_str) > 0 else 0

        keys = [*cls.__subcharts]
        keys.sort()
        # ローソクサブチャート検索
        ohlcv_sub = [indi["ax"] for indi in cls.__indicators if indi["type"] == "ohlcv"]
        vol_sub = [indi["ax"] for indi in cls.__indicators if indi["type"] == "ohlcv" and indi["vol_bar"]]
        GridSpec = 0
        for key in keys:
            if key == 0:
                GridSpec += 3
            elif key in ohlcv_sub:
                GridSpec += 2
            else:
                GridSpec += 1
        unit = 1.0 / GridSpec

        # DatetimeIndex設定
        cls.__df_ohlcv["datetime"] = pd.to_datetime(cls.__df_ohlcv["unixtime"], unit="s")
        cls.__df_ohlcv.set_index("datetime", inplace=True)
        cls.__df_ohlcv.index = cls.__df_ohlcv.index.tz_localize("UTC")
        cls.__df_ohlcv.index = cls.__df_ohlcv.index.tz_convert("Asia/Tokyo")
        cls.__df_ohlcv.index = cls.__df_ohlcv.index.tz_localize(None) # plotlyはtimezoneを考慮しないため、日付表示用にJSTをlocalize
        #print(cls.__df_ohlcv.index[-1])

        # X軸 日付フォーマット
        if cls.__tick_x < 60:
            time_format = "%m/%d %H:%M:%S"
        elif cls.__tick_x < 3600:
            time_format = "%m/%d %H:%M"
        elif cls.__tick_x < 86400:
            time_format = "%m/%d %H:%M"
        else:
            time_format = "%y/%m/%d"

        # ローソクチャートY値範囲
        y_min = cls.__df_ohlcv.low.min()
        y_max = cls.__df_ohlcv.high.max()
        y_margin = (y_max - y_min) * 0.05
        y_min -= y_margin
        y_max += y_margin
        if cls.settings["volume_bar"]:
            # ローソク足を上側75%に収める
            y_min = y_min - (y_max - y_min) / 4

        # Figure生成
        if cls.settings["volume_bar"]:
            row_num = len(keys) + 1 + len(vol_sub)
        else:
            row_num = len(keys)
        #row_num = len(keys)+1 if cls.settings["volume_bar"] else len(keys)
        fig = tools.make_subplots(rows=row_num, cols=1, shared_xaxes=True, vertical_spacing = 0.0)

        # 凡例レイアウト
        if cls.settings["legend"] == "Top":
            legend_param = dict(
                orientation = "h",
                xanchor     = "center",
                yanchor     = "bottom",
                x           = 0.5,
                y           = 0.95,
                #traceorder = "grouped",
                #font = dict(
                #    family= "sans-serif",
                #    size  = 12,
                #    color = "#000",
                #),
                #bgcolor    = "#E2E2E2",
                #bordercolor= "#FFFFFF",
                #borderwidth= 2,
            )
        elif cls.settings["legend"] == "Bottom":
            legend_param = dict(
                orientation = "h",
                xanchor     = "center",
                yanchor     = "top",
                x           = 0.5,
                y           = -0.1,
            )
        else:
            legend_param = None

        # チャートレイアウト生成
        add_size = 2
        # titlefont属性が3.4.2よりも上位バージョンで廃止されたため
        if plotly_version <= 342:
            fig["layout"].update(
                title       = "<b>"+cls.settings["title"]+"</b>",
                titlefont   = dict(family="arial, sans-selif", color=cls.settings["frontcolor"], size=cls.settings["title_size"]+add_size),
                width       = cls.settings["fig_size"][0] * cls.settings["fig_dpi"],
                height      = cls.settings["fig_size"][1] * cls.settings["fig_dpi"],
                margin      = dict(l=50, r=50, t=30, b=30),
                font        = dict(family="arial, sans-selif", color=cls.settings["frontcolor"], size=cls.settings["label_size"]+add_size),
                plot_bgcolor= cls.settings["backcolor"],
                showlegend  = (cls.settings["legend"] is not None),
                legend      = legend_param,
                #bargap      = 0.0,
            )
        else:
            fig["layout"].update(
                title       = "<b>" + cls.settings["title"] + "</b>",
                width       = cls.settings["fig_size"][0] * cls.settings["fig_dpi"],
                height      = cls.settings["fig_size"][1] * cls.settings["fig_dpi"],
                margin      = dict(l=50, r=50, t=30, b=30),
                font        = dict(family="arial, sans-selif", color=cls.settings["frontcolor"], size=cls.settings["label_size"]+add_size),
                plot_bgcolor= cls.settings["backcolor"],
                showlegend  = (cls.settings["legend"] is not None),
                legend      = legend_param,
                #bargap      = 0.0,
            )

        # プロットエリアの枠線
        # Shapes生成
        shapes = []
        fill_color = None
        cur_domain = 1.0
        for ax in keys:
            if ax in ohlcv_sub:
                domain_range = 2
            else:
                domain_range = 1

            if ax == 0:
                y1 = 1.0
                cur_domain -= unit * 3
                y0 = cur_domain
            elif ax < max(keys):
                y1 = cur_domain
                cur_domain -= unit * domain_range
                y0 = cur_domain
            else:
                y1 = cur_domain
                y0 = 0.0
            shapes += [
                dict(
                    type      = "rect",
                    xref      = "paper",
                    yref      = "paper",
                    x0        = 0.0,
                    x1        = 1.0,
                    y0        = y0,
                    y1        = y1,
                    fillcolor = cls.get_reverse_color(fill_color, alpha=0.03),
                    line      = dict(
                        color = cls.settings["frontcolor"],
                        width = 2.0,
                    ),
                )
            ]
            #fill_color = cls.settings["backcolor"] if fill_color is None else None
        fig["layout"]["shapes"] = shapes

        fig["layout"]["hovermode"] = "x" # "x", "y", "closest"

        # xaxis
        fig["layout"]["xaxis1"].update(
            tickformat     = time_format,
            #showline       = True,
            #linecolor      = cls.settings["frontcolor"],
            #linewidth      = 2,
            #mirror         = True,
            showgrid       = cls.settings["xaxis"]["grid"],
            gridcolor      = cls.settings["frontcolor"],
            tickfont       = dict(family="arial, sans-selif", size=cls.settings["label_size"]+add_size),
            tickcolor      = cls.settings["frontcolor"],
            showspikes     = True,
            spikecolor     = cls.settings["frontcolor"],
            spikethickness = 1.5,
            spikedash      = "solid",         # "solid", "dot", "dash", "longdash", "dashdot", or "longdashdot"
            spikemode      = "toaxis+across", # "toaxis", "across", "toaxis+across", "toaxis+across+marker"
            spikesnap      = "data",          # "data", "cursor"
            rangeslider    = dict(visible=True, thickness=0.05)
        )

        # yaxis
        map_y_ax = {}
        i = 1
        cur_domain = 1.0
        for ax in keys:
            if ax in ohlcv_sub:
                domain_range = 2
            else:
                domain_range = 1

            if ax == 0:
                y_domain = [cur_domain - unit * 3, 1.0]
                # メインチャート(ローソク足)
                fig["layout"]["yaxis" + str(i)].update(
                    title          = cls.__subcharts[ax]["label"],
                    domain         = y_domain,
                    showticklabels = True,
                    #showline       = True,
                    #linecolor      = cls.settings["frontcolor"],
                    #linewidth      = 2,
                    #mirror         = True,
                    showgrid       = cls.__subcharts[ax]["grid"],
                    gridcolor      = cls.settings["frontcolor"],
                    tickfont       = dict(family="arial, sans-selif", size=cls.settings["label_size"]+add_size),
                    tickcolor      = cls.settings["frontcolor"],
                    anchor         = "x1",
                    showspikes     = True,
                    spikecolor     = cls.settings["frontcolor"],
                    spikethickness = 1.5,
                    spikedash      = "solid",         # "solid", "dot", "dash", "longdash", "dashdot", or "longdashdot"
                    spikemode      = "toaxis+across", # "toaxis", "across", "toaxis+across", "toaxis+across+marker"
                    spikesnap      = "data",          # "data", "cursor"
                    autorange      = True,
                    fixedrange     = False,
                )
                map_y_ax[ax] = [i, y_min, y_max]
                i += 1
                if cls.settings["volume_bar"]:
                    # メインチャート(出来高)
                    fig["layout"]["yaxis" + str(i)].update(
                        title          = "Volume",
                        domain         = y_domain,
                        showticklabels = True,
                        #showline       = True,
                        #linecolor      = cls.settings["frontcolor"],
                        #linewidth      = 2,
                        #mirror         = True,
                        showgrid       = False,
                        tickfont       = dict(family="arial, sans-selif", size=cls.settings["label_size"]+add_size),
                        tickcolor      = cls.settings["frontcolor"],
                        range          = [0, cls.__df_ohlcv.volume.max() * 4], # 出来高チャートは下側25%に収める
                        overlaying     = "y" + str(i-1),
                        side           = "right",
                        anchor         = "x1",
                        showspikes     = True,
                        spikecolor     = cls.settings["frontcolor"],
                        spikethickness = 1.5,
                        spikedash      = "solid",         # "solid", "dot", "dash", "longdash", "dashdot", or "longdashdot"
                        spikemode      = "toaxis+across", # "toaxis", "across", "toaxis+across", "toaxis+across+marker"
                        spikesnap      = "data",          # "data", "cursor"
                    )
                    i += 1
                cur_domain -= unit*3
            else:
                if ax == max(keys):
                    y_domain = [0.0, cur_domain]
                else:
                    y_domain = [cur_domain - unit * domain_range, cur_domain]
                # サブチャート
                fig["layout"]["yaxis" + str(i)].update(
                    title          = cls.__subcharts[ax]["label"],
                    domain         = y_domain,
                    showticklabels = True,
                    #showline       = True,
                    #linecolor      = cls.settings["frontcolor"],
                    #linewidth      = 2,
                    #mirror         = True,
                    showgrid       = cls.__subcharts[ax]["grid"],
                    gridcolor      = cls.settings["frontcolor"],
                    tickfont       = dict(family="arial, sans-selif", size=cls.settings["label_size"]+add_size),
                    tickcolor      = cls.settings["frontcolor"],
                    anchor         = "x1",
                    showspikes     = True,
                    spikecolor     = cls.settings["frontcolor"],
                    spikethickness = 1.5,
                    spikedash      = "solid",         # "solid", "dot", "dash", "longdash", "dashdot", or "longdashdot"
                    spikemode      = "toaxis+across", # "toaxis", "across", "toaxis+across", "toaxis+across+marker"
                    spikesnap      = "data",          # "data", "cursor"
                    autorange      = True,
                    fixedrange     = False,
                )
                map_y_ax[ax] = [i, 999999999, -999999999]
                i += 1
                if ax in ohlcv_sub and ax in vol_sub:
                    # ローソクサブチャート検索
                    ohlcv = [indi["ohlcv"] for indi in cls.__indicators if indi["type"] == "ohlcv" and indi["ax"] == ax]
                    # サブチャート(出来高)
                    fig["layout"]["yaxis" + str(i)].update(
                        title          = "Volume",
                        domain         = y_domain,
                        showticklabels = True,
                        #showline       = True,
                        #linecolor      = cls.settings["frontcolor"],
                        #linewidth      = 2,
                        #mirror         = True,
                        showgrid       = False,
                        tickfont       = dict(family="arial, sans-selif", size=cls.settings["label_size"]+add_size),
                        tickcolor      = cls.settings["frontcolor"],
                        range          = [0, ohlcv[0].volume.max() * 4], # 出来高チャートは下側25%に収める
                        overlaying     = "y" + str(i-1),
                        side           = "right",
                        anchor         = "x1",
                        showspikes     = True,
                        spikecolor     = cls.settings["frontcolor"],
                        spikethickness = 1.5,
                        spikedash      = "solid",         # "solid", "dot", "dash", "longdash", "dashdot", or "longdashdot"
                        spikemode      = "toaxis+across", # "toaxis", "across", "toaxis+across", "toaxis+across+marker"
                        spikesnap      = "data",          # "data", "cursor"
                    )
                    i += 1
                cur_domain -= unit * domain_range

        # データ生成
        # ローソクチャート設定
        fig.append_trace(
            go.Candlestick(
                open  = cls.__df_ohlcv.open,
                high  = cls.__df_ohlcv.high,
                low   = cls.__df_ohlcv.low,
                close = cls.__df_ohlcv.close,
                x     = cls.__df_ohlcv.index,
                name  = "OHLC",
                increasing=dict(line=dict(color=cls.settings["bar"]["up_color"])),  # 陽線色
                decreasing=dict(line=dict(color=cls.settings["bar"]["down_color"])) # 陰線色
            ),
            map_y_ax[0][0], 1)

        # 出来高設定
        if cls.settings["volume_bar"]:
            colors = np.where(cls.__df_ohlcv.close.diff() > 0,
                              cls.settings["bar"]["up_color"],
                              cls.settings["bar"]["down_color"])
            fig.append_trace(
                go.Bar(
                    x      = cls.__df_ohlcv.index,
                    y      = cls.__df_ohlcv.volume,
                    marker = dict(color=colors),
                    name   = "Volume"
                ),
                map_y_ax[0][0]+1, 1)

        # インジケータ
        for indi in cls.__indicators:
            # DatetimeIndex変換
            if indi["type"] == "ohlcv":
                df = indi["ohlcv"]
                df["datetime"] = pd.to_datetime(df["unixtime"], unit="s")
            else:
                df = pd.DataFrame([])
                df["datetime"] = pd.to_datetime(indi["unixtime"], unit="s")
            df.set_index("datetime", inplace=True)
            df.index = df.index.tz_localize("UTC")
            df.index = df.index.tz_convert("Asia/Tokyo")
            df.index = df.index.tz_localize(None) # plotlyはtimezoneを考慮しないため、日付表示用にJSTをlocalize
            np_x = df.index

            # Y値範囲計算用
            y_min = 999999999
            y_max = -999999999
            ax = map_y_ax[indi["ax"]]

            # LINE
            if indi["type"] == "line":
                if len(indi["plot"]) > 0:
                    y_min = indi["plot"].min()
                    y_max = indi["plot"].max()
                data_x = []
                data_y = []
                if len(indi["unixtime"]) == 0:
                    data_x = [np_x[0], np_x[-1]]
                    data_y = [indi["plot"][0], indi["plot"][0]]
                elif len(indi["plot"]) == 0:
                    data_x = [np_x[0], np_x[0]]
                    data_y = [-999999999, 999999999]
                else:
                    data_x = np_x
                    data_y = indi["plot"]
                fig.append_trace(
                    go.Scatter(
                        x         = data_x,
                        y         = data_y,
                        mode      = "lines",
                        line      = dict(width=indi["width"]),
                        marker    = dict(color=indi["color"]),
                        name      = indi["name"],
                    ),
                    ax[0], 1)

            # BAND
            elif indi["type"] == "band":
                y_min = min([indi["plot1"].min(), indi["plot2"].min()])
                y_max = max([indi["plot1"].max(), indi["plot2"].max()])
                fig.append_trace(
                    go.Scatter(
                        x         = np_x,
                        y         = indi["plot1"],
                        fill      = None,
                        mode      = "lines",
                        line      = dict(width=indi["edge_width"], color=indi["edge_color"]),
                        name      = indi["name"] + "_1",
                    ),
                    ax[0], 1)
                fig.append_trace(
                    go.Scatter(
                        x         = np_x,
                        y         = indi["plot2"],
                        fill      = "tonexty",
                        fillcolor = cls.color_to_rgba(indi["up_color"], indi["alpha"]),
                        mode      = "lines",
                        line      = dict(width=indi["edge_width"], color=indi["edge_color"]),
                        name      = indi["name"] + "_2",
                    ),
                    ax[0], 1)

            # BAR
            elif indi["type"] == "bar":
                y_min = indi["plot"].min()
                y_max = indi["plot"].max()
                fig.append_trace(
                    go.Bar(
                        x         = np_x,
                        y         = indi["plot"],
                        marker    = dict(color=indi["color"]),
                        opacity   = 1.0,
                        name      = indi["name"],
                    ),
                    ax[0], 1)

            # MARK
            elif indi["type"] == "mark":
                y_min = indi["plot"].min()
                y_max = indi["plot"].max()
                if indi["mark"] in cls.__markers.keys():
                    mark = cls.__markers[indi["mark"]]
                else:
                    mark = 0
                fig.append_trace(
                    go.Scatter(
                        x         = np_x,
                        y         = indi["plot"],
                        mode      = "markers",
                        marker    = dict(color=indi["color"], size=indi["size"] / 3.0, symbol=mark),
                        opacity   = 1.0,
                        name      = indi["name"],
                    ),
                    ax[0], 1)

            # OHLCV
            elif indi["type"] == "ohlcv":
                y_min = df.low.min()
                y_max = df.high.max()
                # ローソクチャート設定
                fig.append_trace(
                    go.Candlestick(
                        open  = df.open,
                        high  = df.high,
                        low   = df.low,
                        close = df.close,
                        x     = df.index,
                        name  = "OHLC",
                        increasing=dict(line=dict(color=cls.settings["bar"]["up_color"])),  # 陽線色
                        decreasing=dict(line=dict(color=cls.settings["bar"]["down_color"])) # 陰線色
                    ),
                    ax[0], 1)
                # 出来高設定
                if indi["vol_bar"]:
                    colors = np.where(df.close.diff() > 0,
                                      cls.settings["bar"]["up_color"],
                                      cls.settings["bar"]["down_color"])
                    fig.append_trace(
                        go.Bar(
                            x      = df.index,
                            y      = df.volume,
                            marker = dict(color=colors),
                            name   = "Volume"
                        ),
                        ax[0]+1, 1)

            # BOARD
            elif indi["type"] == "board":
                y_min = min([indi["best_bid"].min(), indi["best_ask"].min()])
                y_max = max([indi["best_bid"].max(), indi["best_ask"].max()])

                fig.append_trace(
                    go.Scatter(
                        x          = np_x,
                        y          = indi["best_bid"],
                        mode       = "lines",
                        line       = dict(width=indi["line_width"]),
                        marker     = dict(color=indi["bid_line_color"]),
                        text       = indi["hover_bids"],
                        hoverinfo  = "text",
                        hoverlabel = dict(
                                        bgcolor=cls.color_to_rgba(indi["bid_hover_color"], 0.8),
                                        font=dict(family="Courier New", size=12)),
                    ),
                    ax[0], 1)
                fig.append_trace(
                    go.Scatter(
                        x         = np_x,
                        y         = indi["best_ask"],
                        mode      = "lines",
                        line      = dict(width=indi["line_width"]),
                        marker    = dict(color=indi["ask_line_color"]),
                        text      = indi["hover_asks"],
                        hoverinfo = "text",
                        hoverlabel = dict(
                                        bgcolor=cls.color_to_rgba(indi["ask_hover_color"], 0.8),
                                        font=dict(family="Courier New", size=12)),
                    ),
                    ax[0], 1)

            # Y値範囲調整
            y_margin = (y_max - y_min) * 0.05
            if ax[1] > y_min - y_margin:
                ax[1] = y_min - y_margin
            if ax[2] < y_max + y_margin:
                ax[2] = y_max + y_margin

        # Y値範囲設定
        for value in map_y_ax.values():
            fig["layout"]["yaxis" + str(value[0])].update(
                range = [value[1], value[2]]
            )

        # htmlファイル出力
        show_link=True
        link_text="Export to plot.ly"
        validate=True
        config = {
            "scrollZoom": True,
            "displayModeBar": True,
        }
        plot_html, plotdivid, width, height = _plot_html(
                figure_or_data=fig, config=config, validate=validate,
                default_width="100%", default_height="100%", global_requirejs=False)
        return plot_html

        html_string = '''
        <html>
            <head>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            </head>
            <body>
                ''' + plot_html + '''
            </body>
        </html>'''

        with open(path, "w") as f:
            f.write(html_string)

        # htmlファイル出力
        #plot(fig, filename=path, auto_open=False)

        # DatetimeIndexリセット
        cls.__df_ohlcv.reset_index(drop=True, inplace=True)
        for indi in cls.__indicators:
            if indi["type"] == "ohlcv":
                indi["ohlcv"].reset_index(drop=True, inplace=True)


    #---------------------------------------------------------------------
    # 色変換
    #---------------------------------------------------------------------
    # HEX -> RGB
    @classmethod
    def hex_to_rgb(cls, value):
        value = value.lstrip("#")
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    # RGB -> HEX
    @classmethod
    def rgb_to_hex(cls, rgb):
        return "#%02x%02x%02x" % rgb

    # (HEX or name) & alpha -> RGBA_STR
    @classmethod
    def color_to_rgba(cls, color, alpha=1.0):
        if len(color) < 1:
            return None
        if color[0] == "#":
            rgb = cls.hex_to_rgb(color)
        else:
            rgb = name_to_rgb(color)
        if rgb is None:
            return None
        ret = "rgba("
        for c in rgb:
            ret += str(c) + ","
        ret += str(alpha) + ")"
        return ret

    @classmethod
    def color_to_hex(cls, color):
        if len(color) < 1:
            return None
        if color[0] == "#":
            return color
        else:
            rgb = name_to_rgb(color)
        if rgb is None:
            return None
        return "#%02x%02x%02x" % rgb

    # 反対色取得
    @classmethod
    def get_reverse_color(cls, color, alpha=1.0):
        if color is None or len(color) < 1:
            return None
        if color[0] == "#":
            rgb = cls.hex_to_rgb(color)
        else:
            rgb = name_to_rgb(color)
        if rgb is None:
            return None

        val = 255
        ret = "rgba("
        for c in rgb:
            ret += str(val-c) + ","
        ret += str(alpha) + ")"
        return ret

    # 補色取得
    @classmethod
    def get_complementary_color(cls, color, alpha=1.0):
        if color is None or len(color) < 1:
            return None
        if color[0] == "#":
            rgb = cls.hex_to_rgb(color)
        else:
            rgb = name_to_rgb(color)
        if rgb is None:
            return None

        val = min(rgb) + max(rgb)
        ret = "rgba("
        for c in rgb:
            ret += str(val-c) + ","
        ret += str(alpha) + ")"
        return ret
