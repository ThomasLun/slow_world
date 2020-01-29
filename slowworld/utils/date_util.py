# -*- coding: utf-8 -*-
from time import strptime, mktime
from datetime import datetime, time, date
import time

def get_today():
    return datetime.today()


def date_format(d):
    return '-'.join(['%d' % d.year, '%02d' % d.month, '%02d' % d.day]) \
        if isinstance(d, datetime) or isinstance(d, date) else ''


# 标准的时间书格式
def time_format(t):
    return ':'.join(['%02d' % t.hour, '%02d' % t.minute, '%02d' % t.second]) \
        if isinstance(t, datetime) or isinstance(t, time) else ''


# 标准的日期与时间输出格式
def datetime_format(dt):
    if isinstance(dt, datetime):
        return ' '.join([date_format(dt.date()), time_format(dt.time())])
    elif isinstance(dt, date):
        return date_format(dt)
    elif isinstance(dt, time):
        return time_format(dt)
    else:
        return dt


def timestamp_to_datetime(ts):
    return datetime.fromtimestamp(ts)


def timestamp_to_str(ts):
    return datetime_format(datetime.fromtimestamp(ts))


def str_to_timestamp(str_time):
    """年-月-日 --> 时间戳"""
    tuple_time = strptime(str(str_time), "%Y-%m-%d")
    return mktime(tuple_time)

def format_time(time_sj):
    # 时间戳转换正常时间
    data_sj = time.localtime(time_sj)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S",data_sj)
    return time_str

def format_time_simple(time_sj):
    # 文件名专用
    data_sj = time.localtime(time_sj)
    time_str = time.strftime("%Y-%m-%d-%H:%M:%S", data_sj)
    return time_str

if __name__ == '__main__':
    print(format_time_simple(1577688949))