#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/22 16:38
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : run_level1_win.py

import os
from functools import partial
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from pytdx.params import TDXParams
from PyTdx.pytdx_connect import connect_tdx
from PyTdx.utils_ts import TsUniverse, TsCal
from PyTdx.utils import dy_path


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
    jq_universe = pd.read_csv("jq_securities_20180222.csv").iloc[:, 0].tolist()
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


















