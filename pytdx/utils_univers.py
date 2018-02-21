#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 23:47
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : utils_univers.py
import tushare as ts
from datetime import datetime
from PyTdx.utils_function_timer import dy_func_timer


class DyUniverse(object):
    def __init__(self):
        pass

    @staticmethod
    @dy_func_timer
    def tushare_universe(date=None):
        if date is not None:
            universe = ts.get_stock_basics(date)
            universe = universe.index.tolist()
            universe.sort()
            print("日期:{}股票数目:{}".format(date, len(universe)))
            return universe
        else:
            date = datetime.today().strftime("%Y-%m-%d")
            universe = ts.get_stock_basics(date).index.tolist()
            universe.sort()
            print("日期:{}股票数目:{}".format(date, len(universe)))
            return universe

    def __call__(self, date,*args, **kwargs):
        return self.tushare_universe(date)


if __name__ == "__main__":
    universe = DyUniverse()("2017-12-29")
    print(universe)

