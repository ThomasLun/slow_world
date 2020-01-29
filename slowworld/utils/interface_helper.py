# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/11/16 下午10:32
# @Author  : LpL
# @Email   : peilun2050@gmail.com
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import functools
import random
from collections import OrderedDict

from tornado import gen

from slowworld.utils.date_util import str_to_timestamp




def des_page_size(method):
    """
    分页装饰器
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        page, size = int(self.get_argument('page', 0)), int(self.get_argument('size', 15))
        return method(self, page, size, *args, **kwargs)

    return wrapper


def des_chk_version(method):
    """
    版本装饰器
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # version = self.get_argument('version', '1.0')
        version = '1.0'
        return method(self, version, *args, **kwargs)

    return wrapper

