# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2020/1/9 下午1:55        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import random
from faker import Faker
fake = Faker("zh_CN")
from slowworld.common.connections import MotorConn, MongoConn


motor_cli = MotorConn().instance()
mongo_cli = MongoConn().instance()


def create_order_statistics(num):
    statistics_list = []
    for i in range(num):
        statistics_dict = {"channel_id": str(random.randint(1,2)),
                           "cgoods_id": random.choice(['5e16ef5174aa3479a0688720', '5e16ef6374aa3479a0688721']),
                           "create_time":int(fake.postcode()),
                           "c_goods_name": "电视机",
                           "f_goods_name"
                           "value": 100,
                           "spec_1": "大号",
                           "spec_2": "红色",
                           "vendor_id": str(random.randint(1,2)),
                           "s_order_id":fake.country_code(),
                           "status":str(random.randint(0,1)),
                           "group_price": 200,
                           "bro_percent": 30,
                           "supply_price": 70,
                           "pay_way": str(random.randint(0,1)),
                           "f_goods_id": random.choice(['5e16ef9474aa3479a0688722', '5e16ef9f74aa3479a0688723']),
                           "Real_income":100,
                           }


        statistics_list.append(statistics_dict)

    motor_cli.order_statistics_coll.insert_many(statistics_list)

def find_statistics():
    a = mongo_cli.order_statistics_coll.aggregate([
        {'$match':{}}
    ])
    print([x for x in a])


if __name__ == '__main__':
    create_order_statistics(20)
    # find_statistics()