# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/11/16 下午9:23        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from __future__ import unicode_literals, print_function, division, absolute_import

import os
from pymongo import MongoClient
from redis import Redis
from motor import MotorClient
from redis.sentinel import Sentinel

from slowworld.config import config
from slowworld.config.config import SENTINEL_HOST_LIST


class MotorConn(object):
    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        assert not hasattr(self.__class__, '_instance'), 'Do not call constructor directly!'
        host = config.MONGODB_HOST
        port = config.MONGODB_PORT
        print("\033[1;30;46m|motor : host %s port %s \033[0m" % (config.MONGODB_HOST, config.MONGODB_PORT))
        db = config.MONGODB_NAME
        self.client = MotorClient(config.MONGODB_HOST_LIST) if os.environ.get("DOCKER") else MotorClient(host=host,
                                                                                                         port=port)
        self.db = self.client[db]
        self.user_coll = self.db['users']
        self.vendor_coll = self.db['vendor']
        self.seq_coll = self.db['seq']
        self.channel_coll = self.db['channel']
        self.cgoods_coll = self.db['cgoods']
        self.fgoods_coll = self.db['fgoods']
        self.worker_coll = self.db['worker']

        self.channel_titles_coll = self.db["channel_titles"]  # 渠道表标题
        self.in_channel_coll = self.db['in_channel']  # 导入的原始渠道订单
        self.out_channel_coll = self.db['out_channel']  # 原始订单里导出的发往厂家的订单
        self.down_channel_coll = self.db['down_channel']  # 生成的可以下下载的给厂家的表格

        self.in_vendor_coll = self.db['in_vendor']  # 导入的原始厂商回单
        self.out_vendor_coll = self.db['out_vendor']  # 厂商回单分到个渠道
        self.down_vendor_coll = self.db['down_vendor']  # 生成的可以下下载的给渠道的表格

        self.music_order_coll = self.db['music_order']  # 生成的可以下下载的给ai的订单

        self.channel_model_coll = self.db['channel_model']  # 渠道模型
        self.vendor_model_coll = self.db['vendor_model']  # 厂商模型
        self.sys_order_coll = self.db['sys_order']  # 系统订单
        self.channel_form_coll = self.db["channel_form"]  # 渠道上传的表单
        self.vendor_form_coll = self.db["vendor_form"]  # 厂商上传的表单
        self.order_statistics_coll = self.db["order_statistics"] # 订单统计


class MongoConn(object):
    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        assert not hasattr(self.__class__, '_instance'), 'Do not call constructor directly!'
        host = config.MONGODB_HOST
        port = config.MONGODB_PORT
        print("\033[1;30;46m|mongo : host %s port %s \033[0m" % (config.MONGODB_HOST, config.MONGODB_PORT))
        db = config.MONGODB_NAME
        self.client = MongoClient(config.MONGODB_HOST_LIST) if os.environ.get("DOCKER") else MongoClient(host=host,
                                                                                                         port=port)
        self.db = self.client[db]
        self.worker_coll = self.db['worker']
        self.seq_coll = self.db['seq']
        self.channel_form_coll = self.db["channel_form"]  # 渠道上传的表单
        self.vendor_form_coll = self.db["vendor_form"]  # 渠道上传的表单
        self.order_statistics_coll = self.db["order_statistics"]  # 订单统计
        self.channel_coll = self.db['channel']
        self.cgoods_coll = self.db['cgoods']
        self.fgoods_coll = self.db['fgoods']


class RedisConn(object):
    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        assert not hasattr(self.__class__, '_instance'), 'Do not call constructor directly!'
        if os.environ.get("DOCKER"):
            self.sentinel = Sentinel(SENTINEL_HOST_LIST,
                                     socket_timeout=0.5)
            self.conn = self.sentinel.master_for('mymaster', socket_timeout=0.5)
        else:
            self.conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
        print("\033[1;30;46m|redis : host %s port %s \033[0m" % (config.REDIS_HOST, config.REDIS_PORT))
