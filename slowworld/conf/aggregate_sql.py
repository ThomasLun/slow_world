# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2020/1/9 下午6:04        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

# 渠道统计
CHANNEL_STATISTICS_SQL = {"$group":
                              {"_id": {"channel_id": "$channel_id", "f_goods_id": "$f_goods_id", 'status': '$status',
                                       "pay_way": "$pay_way"},
                               'count': {"$sum": 1},
                               'ghjs': {"$sum": '$supply_price'},
                               'ysk': {"$sum": '$group_price'},
                               'sjsr': {"$sum": '$Real_income'}
                               }

                          }, {"$project": {'channel_id': '$_id.channel_id', 'f_goods_id': '$_id.f_goods_id',
                                           'status': '$_id.status',
                                           'pay_way': '$_id.pay_way', 'count': 1, 'ghjs': 1, 'ysk': 1, 'sjsr': 1,
                                           '_id': 0,
                                           "keys": {"$concat": ['$_id.channel_id', '$_id.f_goods_id', '$_id.pay_way',
                                                                '$_id.status']}}}, {
                             "$sort": {"channel_id": 1, "f_goods_id": 1}}
