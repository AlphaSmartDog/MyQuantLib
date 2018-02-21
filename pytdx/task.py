#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 22:52
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : task.py

import pandas as pd
from PyTdx.utils_function_timer import dy_func_timer


@dy_func_timer
def get_stock_data_transaction(con_api, code, market, cal_date):
    idx = [i*2000 for i in range(6)]
    with con_api.connect():
        buffer = []
        for date in cal_date:
            try:
                tmp = [con_api.to_df(con_api.get_history_transaction_data(
                    market, code, s, e, int(date.strftime("%Y%m%d"))))
                       for s, e in zip(idx[:-1], idx[1:])]
                tmp.reverse()
                tmp = pd.concat(tmp, axis=0)
                tmp["date"] = date
                buffer.append(tmp)
            except KeyError:
                print("Stock:{} wrong@{}".format(code, date))

    print("获取股票{}的分笔数据".format(code))
    return pd.concat(buffer, axis=0)
