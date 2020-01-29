# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/24 下午2:00        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from slowworld.api.base_handler import BaseHandler
from slowworld.common.errors import ERRORS_MAP


class NotFoundHandler(BaseHandler):
    def write_error(self, status_code, **kwargs):
        self.set_status(404)
        self.write({"msg": ERRORS_MAP.get(404), "error": 404, "data": None})
