# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/24 下午4:49        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from schema import Optional, Use
from tornado.gen import coroutine

from slowworld.api import BaseHandler


class UserHandler(BaseHandler):
    # 子商品
    def __init__(self, application, request, **kwargs):
        super(UserHandler, self).__init__(application, request, **kwargs)

    @coroutine
    def create(self):
        args = yield self.validate({
            'phone': Use(str),
            'password': Use(str),
            'username': Use(str),
            'describe': Use(str),
        }, self.get_all_arguments())

        if args.get("error"):
            self.write(args)
        else:
            yield self.cgoods_service.save(args)
            self.write_norm(0, "创建子商品成功!")

    @coroutine
    def delete(self):
        args = yield self.validate({
            'id': Use(str)
        }, self.get_all_arguments())

        if args.get("error"):
            self.write(args)
        else:
            yield self.cgoods_service.delete(args)
            self.write_norm(0, "删除子商品成功!")

    @coroutine
    def update(self):
        args = yield self.validate({
            "id": Use(str),
            Optional('vendor_id'): Use(int),
            Optional('name'): Use(str),
            Optional('type'): Use(int),
            Optional('value'): Use(int),
            Optional('spec_1'): Use(str),
            Optional('spec_2'): Use(str),
            Optional('note'): Use(str),
            Optional('status'): Use(int),
            Optional('item_id'): Use(str),
        }, self.get_all_arguments())
        if args.get("error"):
            self.write(args)
        else:
            self.process_query(args)
            yield self.cgoods_service.update_one(args)
            self.write_norm(0, "修改子商品成功!")

    @coroutine
    def index(self):
        """列表展示"""
        args = yield self.validate({
            "page": Use(int),
            "size": Use(int),
            "status": Use(int),
            Optional('vendor_id'): Use(int),
        }
            , self.get_all_arguments())

        if args.get("error"):
            self.write(args)
        else:
            query = {} if args["status"] == 2 else {"status": args["status"]}
            query.update({"vendor_id": args.get("vendor_id")}) if args.get("vendor_id") else None
            result_list, total = yield self.cgoods_service.find_many(query, args["page"], args["size"])
            self.write_norm(0, "请求列表成功!", **{"list": result_list, "total": total})
