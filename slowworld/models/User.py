# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/24 下午5:07        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from dataclasses import dataclass

from tornado.gen import coroutine, Return

from slowworld.common.connections import RedisConn
from slowworld.models.model import Model

redis = RedisConn.instance().conn

@dataclass
class User(Model):

    username: str = ""
    password: str = ""
    phone: str = ""
    describe: str = ""


    @coroutine
    def to_doc(self):
        """入库必走"""
        doc = dict()
        assert isinstance(self.username, str)
        doc["username"] = self.username
        assert isinstance(self.password, str)
        doc["password"] = self.password
        assert isinstance(self.phone, str)
        doc["phone"] = self.phone
        assert isinstance(self.describe, str)
        doc["describe"] = self.describe
        raise Return(doc)

    @staticmethod
    def from_doc(doc):
        """转对象"""
        user = User()
        user.id = doc.get("_id")
        user.name = doc.get("name")
        user.vendor_id = doc.get("vendor_id")
        user.type = doc.get("type")
        user.value = doc.get("value")
        user.spec_1 = doc.get("spec_1")
        user.spec_2 = doc.get("spec_2")
        user.note = doc.get("note")
        user.status = doc.get("status")
        user.item_id = doc.get("item_id")
        return user

    @staticmethod
    def pretty_show(doc):
        doc["id"] = str(doc.pop("_id"))
        return doc
