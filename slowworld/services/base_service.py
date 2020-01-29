# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/24 下午2:15        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import time

from tornado.gen import coroutine

from slowworld.common.connections import MotorConn, RedisConn


class BaseService(object):
    def __init__(self, services):
        self.motor_conn = MotorConn.instance()
        self.redis_conn = RedisConn.instance().conn
        self.db = None
        self.services = services

    def save(self, data):
        self.db.insert(data)

    def delete(self, query):
        self.db.update(query, {"$set": {"delete_at": True, "update_time": time.time()}})

    def update(self, query, data):
        self.db.update(query, data)

    def find_one(self, query):
        return self.db.find_one(query)

    def find_many(self, args, page, size, sort=(('_id', 1),)):
        # 获取所有上线和未上线
        def str_id(x):
            x["id"] = str(x["_id"])
            x.pop("_id")
            return x

        query = {'status': {"$ne": -1}}
        query.update(args)
        if page:
            page = int(page)
        if size:
            size = int(size)
        result_list = self.db.find(query).skip(page * size).sort(sort).limit(size)
        total = self.db.find(query).count()
        result_list = map(str_id, result_list)
        return [x for x in result_list], total

    @coroutine
    def is_only_key(self, coll, query):
        if coll == "channel_titles":
            motor_coll = self.motor_conn.channel_titles_coll
        elif coll == "channel_model":
            motor_coll = self.motor_conn.channel_model_coll
        elif coll == "fgoods":
            motor_coll = self.motor_conn.fgoods_coll
        result = yield motor_coll.find_one(query)
        return False if result else True
