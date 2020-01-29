# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/12/3 下午2:28        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import hashlib

from slowworld.conf.config import YOUZAN_SECRECT


def get_int(num):
    #转化int
    if num and (not isinstance(num,int)):
        try:
            return int(num)
        except:
            return num



def youzan_sign(client_id, entity):
    """有赞sign生成"""
    m5 = hashlib.md5()
    client_id = str(client_id, encoding='utf-8') if not isinstance(client_id,str) else client_id
    entity = str(entity, encoding='utf-8') if not isinstance(entity,str) else entity
    m5.update("".join([client_id, entity, YOUZAN_SECRECT]).encode("utf-8"))
    c = m5.hexdigest()
    return c

if __name__ == '__main__':
    a = youzan_sign("aa", b'{"msg":"%7B%22delivery_order')
    print(a)