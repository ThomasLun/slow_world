# -*- coding: utf-8 -*-
import time
from bson import ObjectId
from slowworld.common.connections import MongoConn

MongoConn_s = MongoConn.instance()
pay_order = MongoConn_s.order_coll.find({"pay_status": 9})
# pay_uid = MongoConn_s.order_coll.find({}).distinct('uid')
pay_uid = MongoConn_s.order_coll.find({"pay_status": 9}).distinct('uid')

# 当前的时间
now = int(time.time())
timeArray = time.localtime(now)
new_Time_y = time.strftime("%Y", timeArray)
new_Time_m = time.strftime("%m", timeArray)


def pay_operation_year_good():
    """
    所有用户的交易的商品
    :return:
    """
    for pay_order_list in pay_order:
        pay_time_list = pay_order_list.get('pay_time')
        time_num_list = time.localtime(pay_time_list)
        Style_Time_pay_y = time.strftime("%Y", time_num_list)
        if Style_Time_pay_y == new_Time_y:
            # Style_Time_pay_m = time.strftime("%m", time_num_list)
            goods_pay = pay_order_list.get('goods')
            order_id = pay_order_list.get("_id")
            yield goods_pay, order_id


pay_good_year_time = pay_operation_year_good()


def pay_good_price():
    """
    全年总消费
    :return: good_year_price 全年金额
             good_month_prices 月消费
    """

    good_year_prices = []
    good_year_prices_1 = []
    good_year_prices_2 = []
    good_year_prices_3 = []
    good_year_prices_4 = []
    good_year_prices_5 = []
    good_year_prices_6 = []
    good_year_prices_7 = []
    good_year_prices_8 = []
    good_year_prices_9 = []
    good_year_prices_10 = []
    good_year_prices_11 = []
    good_year_prices_12 = []
    for pay_good_year_id in pay_good_year_time:
        pay_good_year = MongoConn_s.goods_coll.find_one({"_id": ObjectId(str(pay_good_year_id[0][0]))})
        pay_good_year_price_s = pay_good_year.get("price") / 100
        good_year_prices.append(pay_good_year_price_s)
        pay_time_m = MongoConn_s.order_coll.find_one({"_id": pay_good_year_id[1]})
        time_num_list = time.localtime(pay_time_m.get("pay_time"))
        Time_pay_m = time.strftime("%m", time_num_list)
        if Time_pay_m == '01':
            good_year_prices_1.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '02':
            good_year_prices_2.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '03':
            good_year_prices_3.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '04':
            good_year_prices_4.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '05':
            good_year_prices_5.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '06':
            good_year_prices_6.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '07':
            good_year_prices_7.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '08':
            good_year_prices_8.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '09':
            good_year_prices_9.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '10':
            good_year_prices_10.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '11':
            good_year_prices_11.append(int(pay_good_year.get("price") / 100))
        elif Time_pay_m == '12':
            good_year_prices_12.append(int(pay_good_year.get("price") / 100))
    good_month_prices = [

        sum(good_year_prices_1),
        sum(good_year_prices_2),
        sum(good_year_prices_3),
        sum(good_year_prices_4),
        sum(good_year_prices_5),
        sum(good_year_prices_6),
        sum(good_year_prices_7),
        sum(good_year_prices_8),
        sum(good_year_prices_9),
        sum(good_year_prices_10),
        sum(good_year_prices_11),
        sum(good_year_prices_12)
    ]

    good_year_price = sum(good_year_prices)
    return good_year_price, good_month_prices


def pay_good_number():
    """
    每年用户交易的个数
    :return: par_year_num 年
             pay_month_num 月
     """
    pay_year_num = []
    pay_month_num_1 = []
    pay_month_num_2 = []
    pay_month_num_3 = []
    pay_month_num_4 = []
    pay_month_num_5 = []
    pay_month_num_6 = []
    pay_month_num_7 = []
    pay_month_num_8 = []
    pay_month_num_9 = []
    pay_month_num_10 = []
    pay_month_num_11 = []
    pay_month_num_12 = []

    for pay_order_list in pay_uid:
        pay_time_list = MongoConn_s.order_coll.find_one({"uid": pay_order_list}).get("pay_time")
        time_num_list = time.localtime(pay_time_list)
        Style_Time_pay_y = time.strftime("%Y", time_num_list)
        Style_Time_pay_m = time.strftime("%m", time_num_list)
        if Style_Time_pay_y == new_Time_y:
            pay_year_num.append(Style_Time_pay_y)
            if Style_Time_pay_m == '01':
                pay_month_num_1.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '02':
                pay_month_num_2.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '03':
                pay_month_num_3.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '04':
                pay_month_num_4.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '05':
                pay_month_num_5.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '06':
                pay_month_num_6.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '07':
                pay_month_num_7.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '08':
                pay_month_num_8.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '09':
                pay_month_num_9.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '10':
                pay_month_num_10.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '11':
                pay_month_num_11.append(Style_Time_pay_m)
            elif Style_Time_pay_m == '12':
                pay_month_num_12.append(Style_Time_pay_m)
    pay_month_num = [
        len(pay_month_num_1),
        len(pay_month_num_2),
        len(pay_month_num_3),
        len(pay_month_num_4),
        len(pay_month_num_5),
        len(pay_month_num_6),
        len(pay_month_num_7),
        len(pay_month_num_8),
        len(pay_month_num_9),
        len(pay_month_num_10),
        len(pay_month_num_11),
        len(pay_month_num_12)
    ]
    par_year_num = len(pay_year_num)
    return par_year_num, pay_month_num
