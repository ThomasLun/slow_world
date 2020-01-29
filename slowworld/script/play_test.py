# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/26 上午10:11        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import copy
import os

from slowworld.worker import queue




def process_query(query):
    print(query)
    data = copy.deepcopy(query)
    for k, v in query.items():
        if (not v) and (v != 0): data.pop(k)
    return data



if __name__ == '__main__':
    # put_files()
    # print(os.path.abspath("data") )
    a = {"a":"","b":1}
    b = process_query(a)
    print(b)