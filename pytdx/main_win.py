#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/22 16:38
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : main_win.py

import os
import time
import gc
from functools import partial
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from PyTdx.utils_ts import TsUniverse, TsCal
from PyTdx.utils import dy_func_timer, dy_path


@dy_func_timer
def connect_tdx(date, universe, market_dict, path, fix_universe):
    int_date = int(date.replace("-", ""))
    save_path = path + "\\Date{}.csv".format(int_date)

    idx = [i * 2000 for i in range(6)]
    with TdxHq_API(heartbeat=True, auto_retry=True) as con_api:
        with con_api.connect():
            access = []
            try:
                universe = universe(date)
                universe = list(set(universe).union(jq_universe))
            except:
                universe = fix_universe

            for code in universe:
                market = market_dict[code[0]]
                tmp = [con_api.to_df(con_api.get_history_transaction_data(
                    market, code, s, e, int_date)) for s, e in zip(idx[:-1], idx[1:])]
                tmp.reverse()
                tmp = pd.concat(tmp, axis=0)
                tmp["date"] = date
                tmp["code"] = code
                access.append(tmp)
            access = pd.concat(access, axis=0)
    access.to_csv(save_path, encoding="utf_8_sig")
    print("Level-1逐笔数据@{}".format(date))
    time.sleep(0.5)
    gc.collect()


if __name__ == "__main__":
    # 证券代码交易所(沪深)分类
    market_dict = {
        "0": TDXParams.MARKET_SZ,
        "3": TDXParams.MARKET_SZ,
        "6": TDXParams.MARKET_SH
    }
    universe = TsUniverse()
    path = dy_path()

    # joinquant 数据库提取股票池
    jq_universe = pd.read_csv("securities_20180222.csv").iloc[:, 0].tolist()
    jq_universe = [i[:6] for i in jq_universe]

    task = partial(connect_tdx, universe=universe,
                   market_dict=market_dict, path=path, fix_universe=jq_universe)

    # 消除已存在截面数据
    ts_cal = TsCal()()
    exists_cal = ["{}-{}-{}".format(
        i[4:8], i[8:10], i[10:12]) for i in os.listdir(path)]
    cal_dates = list(set(ts_cal).difference(set(exists_cal)))
    cal_dates.sort()

    with ProcessPoolExecutor(max_workers=16) as executor:
        executor.map(task, cal_dates)
        executor.shutdown(True)


















