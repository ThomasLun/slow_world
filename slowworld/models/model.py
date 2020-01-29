# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/24 下午5:08        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import hashlib

from tornado.gen import coroutine, Return

from slowworld.common.connections import MotorConn
from slowworld.config.config import app_config


class Model:

    def __init__(self):
        self.coll = MotorConn.instance()
        self.seq_coll = self.coll.seq_coll

    @classmethod
    def hash_with_salt(cls, item, salt=None):
        """密码加盐"""
        return str(hashlib.md5((salt or app_config.salt) + item).hexdigest())

    @coroutine
    def get_int_id(self, seq_name=None, step=1, start=1):
        """生成int类型自增id"""
        seq_name = self.__class__.__name__.lower() if not seq_name else seq_name

        number = yield self.seq_coll.count_documents({})
        if number == 0:
            yield self.seq_coll.insert_one({})
        seq_list = yield self.seq_coll.find_one({})
        if seq_name not in seq_list:
            yield self.seq_coll.update_one({}, {'$set': {seq_name: start}})
        result = yield self.seq_coll.find_one_and_update({}, {'$inc': {seq_name: step}})
        raise Return(result.get(seq_name, step))


if __name__ == '__main__':
    class Dog(Model):
        pass


    a = Dog()
    a.get_int_id()
    # coll = MotorConn.instance()
    # seq_coll = coll.seq_coll
    # seq_coll.insert_one({})
