# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/11/16 下午11:01        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

ERRORS_MAP = {
    # 基础error
    404: "页面不存在，请访问/v1/查看帮助",

}


class BaseError(BaseException):
    def __init__(self, code, Message, data=None):
        super(BaseError, self).__init__()
        self.error = {"error": code, "msg": Message, "data": data}


class LostError(BaseError):
    def __init__(self, arg):
        super(LostError, self).__init__(1012, "缺少参数:%s" % arg)


class WrongError(BaseError):
    def __init__(self, arg, msg):
        super(WrongError, self).__init__(1009, "参数:%s:应该是类型%s" % (arg, msg))


if __name__ == '__main__':
    error = LostError("dog").error
    print(error)
