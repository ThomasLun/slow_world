# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/24 下午4:51        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import json

from bson import ObjectId

from slowworld.common.cache import USER_INFO
from slowworld.models.User import User
from slowworld.services.base_service import BaseService
from tornado.gen import coroutine, Return


class UserService(BaseService):
    def __init__(self, services):
        super(UserService, self).__init__(services)
        self.cgoods_coll = self.motor_conn.cgoods_coll

    @coroutine
    def save(self, data):
        data = yield User(**data).to_doc()
        result = yield self.cgoods_coll.insert_one(data)
        _id = str(result.inserted_id)
        data.pop("_id")
        self.redis_conn.hset(USER_INFO,_id,json.dumps(data))

    @coroutine
    def delete(self, query):
        yield self.cgoods_coll.update_one({"_id": ObjectId(query.get("id"))}, {"$set": {"status": -1}})
        self.redis_conn.hdel(USER_INFO,query.get("id"))

    @coroutine
    def update_one(self, args):
        self.redis_conn.hdel(USER_INFO, args.get("id"))
        yield self.cgoods_coll.update_one({"_id": ObjectId(args.pop("id"))}, {"$set": args})
    @coroutine
    def find_many(self, query, page, size, sort=(('_id', 1),)):
        # 获取所有上线和未上线
        result_list = self.cgoods_coll.find(query).skip(page * size).sort(sort).limit(size)
        result_list = yield result_list.to_list(length=100)
        total = yield self.cgoods_coll.count_documents(query)
        return [User.pretty_show(x) for x in result_list], total

    @coroutine
    def find_one(self, query):
        data = yield self.cgoods_coll.find_one(query)
        return User.pretty_show(data)

    @coroutine
    def find_all(self, query):
        result_list = self.cgoods_coll.find(query)
        result_list = yield result_list.to_list(length=100)
        return [User.pretty_show(x) for x in result_list]

    @coroutine
    def find_by_id(self, id):
        data = self.redis_conn.hget(USER_INFO, id)
        if data:
            return json.loads(data)
        else:
            data = yield self.cgoods_coll.find_one({"_id":ObjectId(id)})
            data.pop("_id")
            self.redis_conn.hset(USER_INFO, id, json.dumps(data))
            return data
