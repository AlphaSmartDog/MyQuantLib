"""@author: Young
@license: (C) Copyright 2013-2018
@contact: aidabloc@163.com
@file: dy_calendar.py
@time: 2018/1/28 14:10
日历API
"""
import tushare as ts
import numpy as np
import pandas as pd
from datetime import timedelta
from datetime import datetime
from pandas.tseries.offsets import WeekOfMonth


class CalendarDates(object):
    START_DATE = '2009-01-01'
    END_DATE = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    def __init__(self):
        self.cal_dates = self._get_ts_cal()
        self.index_dates = self._get_index_cal()
        # 交叉验证日历
        self._get_cross(self.cal_dates, self.index_dates)
        # 日历 月末日
        self.months = self.index_dates.resample("1m").last().index.strftime("%Y-%m")

    def _get_ts_cal(self):
        # 获取tushare 交易日历
        cal_dates = ts.trade_cal()
        cal_dates.set_index("calendarDate", inplace=True)
        cal_dates.index = pd.to_datetime(cal_dates.index)
        cal_dates = cal_dates.loc[self.START_DATE: self.END_DATE]
        return cal_dates

    def _get_index_cal(self):
        # 获取上证指数
        index_dates = ts.get_k_data('000001', index=True,
                                    start=self.START_DATE, end=self.END_DATE)
        index_dates.set_index("date", inplace=True)
        index_dates["isOpen"] = int(1)
        index_dates = index_dates["isOpen"]
        index_dates.index = pd.to_datetime(index_dates.index)
        return index_dates

    def _get_cross(self, cal_dates, index_dates):
        # 交叉验证交易日历
        cross = pd.concat([cal_dates.loc[cal_dates["isOpen"] == 1], index_dates], axis=1)
        cross.columns = ["cal", "index"]
        cross["cross"] = cross.iloc[:, 0] - cross.iloc[:, 1]
        cross["cross"].fillna(999)  # 针对可能存在的nan
        print("交易日历交叉验证:{}".format(cross["cross"].sum() == 0))
        print("交易日历{} : {}共{}个交易日".format(
            self.START_DATE, self.END_DATE, cross.shape[0]))

    def get_cal_01(self, week, weekday):
        """返回每月第week周weekday日"""
        wom = WeekOfMonth(week=week-1, weekday=weekday-1)
        return pd.date_range(self.START_DATE, self.END_DATE, freq=wom)

    def get_cal_02(self, week, weekday):
        """返回每月第week周weekday日(含)后第一个交易日"""
        wom_dates = self.get_cal_01(week, weekday)
        buffer = []
        for day in wom_dates:
            if self.cal_dates.loc[day][0] == 1:
                buffer.append(day)
            else:
                while True:
                    if day >= self.index_dates.index[-1]:
                        break
                    # 时间后延
                    day += timedelta(1)
                    if self.cal_dates.loc[day][0] == 1:
                        buffer.append(day)
                        break
        return pd.to_datetime(buffer)

    def get_cal_03(self, week, weekday):
        """返回每月第week周weekday日(含)后第一个前连续交易日,
        即，返回第一个T-1，T 均为交易日的月份日历"""
        wom_dates = self.get_cal_01(week, weekday)
        buffer = []
        for day in wom_dates:
            pre_day = day + timedelta(-1)
            if self.cal_dates.loc[pre_day:day].sum()[0] == 2:
                buffer.append(day)
            else:
                while True:
                    if day >= self.index_dates.index[-1]:
                        break
                    # 时间后延
                    day += timedelta(1)
                    pre_day = day + timedelta(-1)
                    if self.cal_dates.loc[pre_day:day].sum()[0] == 2:
                        buffer.append(day)
                        break
        return pd.to_datetime(buffer)

    def get_cal_04(self, week, weekday):
        """返回每月第week周weekday日(含)后第一个前后连续交易日,
        即，返回第一个T-1，T，T+1 均为交易日的月份日历"""
        wom_dates = self.get_cal_01(week, weekday)
        buffer = []
        for day in wom_dates:
            pre_day = day + timedelta(-1)
            next_day = day + timedelta(1)
            if self.cal_dates.loc[pre_day:next_day].sum()[0] == 3:
                buffer.append(day)
            else:
                while True:
                    if day >= self.index_dates.index[-1]:
                        break
                    # 时间后延
                    day += timedelta(1)
                    pre_day = day + timedelta(-1)
                    next_day = day + timedelta(1)
                    if self.cal_dates.loc[pre_day:next_day].sum()[0] == 3:
                        buffer.append(day)
                        break
        return pd.to_datetime(buffer)

    def get_cal_05(self, week, weekday):
        """返回每月第week周weekday日(含)后第一个前后连续交易日,
        即，返回第一个T-1，T，T+1, T+2 均为交易日的月份日历"""
        wom_dates = self.get_cal_01(week, weekday)
        buffer = []
        for day in wom_dates:
            pre_day = day + timedelta(-1)
            next_day = day + timedelta(2)
            if self.cal_dates.loc[pre_day:next_day].sum()[0] == 4:
                buffer.append(day)
            else:
                while True:
                    if day >= self.index_dates.index[-1]:
                        break
                    # 时间后延
                    day += timedelta(1)
                    pre_day = day + timedelta(-1)
                    next_day = day + timedelta(2)
                    if self.cal_dates.loc[pre_day:next_day].sum()[0] == 4:
                        buffer.append(day)
                        break
        return pd.to_datetime(buffer)

    def get_count_01(self):
        """返回自然月每月交易日计数"""
        count = self.index_dates.resample("1m").sum()
        count.index = count.index.strftime("%Y-%m")
        return count

    def get_count_02(self, dates):
        """返回修正划分每月交易日计数"""
        cache = []
        for s, e in zip(dates[:-1], dates[1:]):
            count = self.index_dates.loc[s:e].sum()
            cache.append([s, e, count])
        cache = pd.DataFrame(cache)
        cache.columns = ["start_date", "end_date", "count"]
        cache.index = cache.start_date
        cache.index = cache.index.strftime("%Y-%m")
        cache.index.name = "month"
        return cache

    def get_th_date(self, k):
        """返回每月第k个交易日, 从1开始"""
        buffer = []
        k = k - 1
        for i in self.months:
            m = self.index_dates.loc[i]
            try:
                day = m.index[k]
            except:
                day = np.nan
            buffer.append(day)
        return pd.to_datetime(buffer)

    @staticmethod
    def get_date(date, k=1):
        """获取间隔k日日期"""
        return (date + timedelta(days=k)).strftime("%Y-%m-%d")

    def get_date_cal(self, date, k=1):
        """获取交易日历间隔k日日期"""
        cal_index = self.index_dates.cumsum()
        cursor = cal_index.loc[date] + k
        date = self.index_dates.index[cursor]
        return date.strftime("%Y-%m-%d")


