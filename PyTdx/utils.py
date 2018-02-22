#!/iQuant/MyQuantLib
# -*- coding: utf-8 -*-
# @Time    : 2018/2/22 14:30
# @Author  : Aries
# @Email   : aidabloc@163.com
# @File       : utils.py
import os
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


# 检查创建tdx逐笔数据存储文件夹
def dy_path():
    #当前文件的路径
    path = os.getcwd()
    # 去除首位空格
    path = path.strip()
    path = path + "\\Tdx_Level_1"
    # 判断路径是否存在
    is_exists = os.path.exists(path)

    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录
        #  创建目录操作函数
        os.makedirs(path)
    else:
        pass
    return path


if __name__ == "__main__":
    import numpy as np

    @dy_func_timer
    def test_timer():
        return np.sort(np.random.normal(size=np.int(1e6)))

    test_timer()