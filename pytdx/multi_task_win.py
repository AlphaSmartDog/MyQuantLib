#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/22 0:26
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : multi_task_win.py

import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from pytdx.hq import TdxHq_API
from utils import market_dict
from utils_ts import TsUniverse, CalendarVer01
from single import get_stock_data_transaction

cal_dates = CalendarVer01()()
universe = TsUniverse()(cal_dates[-1])
codes = np.array_split(universe, 8)


def tasking(codes):
    api = TdxHq_API(heartbeat=True)
    for code in codes.tolist():
        time.sleep(1)
        market = market_dict[code[0]]
        stk_data = get_stock_data_transaction(api, code, market, cal_dates)
        stk_data.to_csv("data/stk_{}.csv".format(code))
        # stk_data.to_hdf("data/stk_{}.h5".format(code), "stock", complevel=9)
        time.sleep(1)


if __name__ == "__main__":
    codes = np.array_split(universe, 8)
    with ProcessPoolExecutor(max_workers=8) as executor:
        executor.map(tasking, codes)