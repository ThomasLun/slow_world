# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/24 下午2:00        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import copy
import json

import tornado.web
from schema import Schema, SchemaMissingKeyError, SchemaError, SchemaUnexpectedTypeError
from tornado.gen import coroutine, Return

from slowworld.common.errors import LostError, WrongError


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        if False:
            from slowworld.main import ApiApplication
            self.application = ApiApplication()
        self._all_arguments = None
        self.colls = self.application.colls
        self.redis = self.application.redis
        self._services = self.application.services
        self.cgoods_service = self._services.cgoods_service

    def initialize(self, action=None, extra_args=None, *args, **kwargs):
        self.action = action.__name__ if callable(action) else action
        self.extra_args = extra_args or {}
        super(BaseHandler, self).initialize()

    def prepare(self):
        super(BaseHandler, self).prepare()
        args = {k.lower(): v for (k, v) in self.request.headers.items() if k.lower() in [
            'uid', 'token', 'god', 'version', 'platform']}
        args.update({k: tornado.web.RequestHandler.get_argument(self, k) for k in self.request.arguments})
        try:
            self.request.body and args.update(json.loads(self.request.body))
        except ValueError:
            pass
        args.update(self.extra_args)
        self._all_arguments = args

    def delete(self, *args, **kwargs):
        return super(BaseHandler, self).delete(*args, **kwargs) if not self.action else getattr(self, self.action)(
            *args, **kwargs)

    def get(self, *args, **kwargs):
        return super(BaseHandler, self).get(*args, **kwargs) if not self.action else getattr(self, self.action)(
            *args, **kwargs)

    def put(self, *args, **kwargs):
        return super(BaseHandler, self).put(*args, **kwargs) if not self.action else getattr(self, self.action)(
            *args, **kwargs)

    def patch(self, *args, **kwargs):
        return super(BaseHandler, self).patch(*args, **kwargs) if not self.action else getattr(self, self.action)(
            *args, **kwargs)

    def post(self, *args, **kwargs):
        return super(BaseHandler, self).post(*args, **kwargs) if not self.action else getattr(self, self.action)(
            *args, **kwargs)

    def write_norm(self, code=0, msg="error", **data):

        self.write({"error": code, "msg": msg, "data": data})

    def set_default_headers(self):
        """
        设置HTTP响应公共头，支持跨域访问
        :return:
        """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, PUT')
        self.set_header('Access-Control-Allow-Headers', 'content-type, token, uid, god')

    def options(self, *args, **kwargs):
        """
        响应OPTIONS请求，以支持跨域
        :param args:
        :param kwargs:
        :return:
        """
        self.write({})

    _ARG_DEFAULT = object()

    def get_all_arguments(self, exclude_empty=False):
        if exclude_empty:
            return {k: v for (k, v) in self._all_arguments.items() if v not in ['', None]}
        return self._all_arguments

    def get_argument(self, name, default=_ARG_DEFAULT, strip=True):
        arg = self.get_all_arguments().get(name, None)
        if arg is None:
            if default is self._ARG_DEFAULT:
                raise tornado.web.MissingArgumentError(name)
            return default
        return arg

    @staticmethod
    def process_query(query):
        data = copy.deepcopy(query)
        for k, v in query.items():
            if (not v) and (v != 0): data.pop(k)
        return data

    # @classmethod
    @coroutine
    def validate(self, rules, data):
        dic = {}
        for (k, v) in rules.items():
            real_k = k if isinstance(k, str) else k._schema
            try:
                dic.update(Schema({k: v}).validate({real_k: data[real_k]} if real_k in data else {}))
            except SchemaMissingKeyError:
                raise Return(LostError(k).error)
            except SchemaError as e:
                raise Return(WrongError(real_k, v).error)
        raise Return(dic)
