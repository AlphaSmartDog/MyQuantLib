#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/22 20:47
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : pytdx_connect.py

import time
import gc
import pandas as pd
from pytdx.hq import TdxHq_API
from PyTdx.utils import dy_func_timer


@dy_func_timer
def connect_tdx(date, universe, market_dict, path, fix_universe):
    # 修复bug
    new_code = lambda c: "{}.XSHG".format(c) \
        if c[0] == "6" else "{}.XSHE".format(c)

    int_date = int(date.replace("-", ""))
    save_path = path + "\\Date{}.csv".format(int_date)

    idx = [i * 2000 for i in range(6)]
    with TdxHq_API(heartbeat=True, auto_retry=True) as con_api:
        with con_api.connect():
            access = []
            try:
                universe = universe(date)
                universe = list(set(universe).union(fix_universe))
            except:
                universe = fix_universe

            for code in universe:
                gc.collect()  # 小内存使用
                market = market_dict[code[0]]
                tmp = [con_api.to_df(con_api.get_history_transaction_data(
                    market, code, s, e, int_date)) for s, e in zip(idx[:-1], idx[1:])]
                tmp.reverse()
                tmp = pd.concat(tmp, axis=0)
                tmp["date"] = date
                tmp["code"] = new_code(code)
                access.append(tmp)
            access = pd.concat(access, axis=0)
    access.to_csv(save_path, encoding="utf_8_sig")
    print("Level-1逐笔数据@{}".format(date))
    time.sleep(0.5)
    gc.collect()
