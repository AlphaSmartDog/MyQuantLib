#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/22 0:29
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : utils_dict.py
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from PyTdx.utils_univers import DyUniverse
from PyTdx.utils_cal import DyCal
from PyTdx.task import get_stock_data_transaction

# 证券代码交易所(沪深)分类
market_dict = {
    "0": TDXParams.MARKET_SZ,
    "3": TDXParams.MARKET_SZ,
    "6": TDXParams.MARKET_SH
}


cal_dates = DyCal()()
universe = DyUniverse(cal_dates[-1])







