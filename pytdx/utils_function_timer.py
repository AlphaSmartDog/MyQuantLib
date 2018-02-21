#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 22:53
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : utils_function_timer.py

import time
from functools import wraps


# 函数时间计数器
def dy_func_timer(function):
    @wraps(function)
    def wraps_timer(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print("Function: %s ---- %s" %(function.__name__, str(end - start)))
        return result
    return wraps_timer


if __name__ == "__main__":
    import numpy as np

    @dy_func_timer
    def test_timer():
        return np.sort(np.random.normal(size=np.int(1e6)))

    test_timer()




