#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function, unicode_literals

# -*- coding: utf-8 -*-
# 腾讯云短信推送服务
import time
import json
from hashlib import sha256
import random

from tornado import httpclient
from tornado.gen import coroutine, Return
from slowworld.common.connections import MongoConn

SDKAPPID = 0
random_key = random.randint(100000, 999999)
BASE_URL = 'https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid={}&random={}'.format(SDKAPPID, random_key)
VOICE_URL = 'https://cloud.tim.qq.com/v5/tlsvoicesvr/sendcvoice?sdkappid={}&random={}'.format(SDKAPPID, random_key)
NATIONCODE = '86'
VERIFY_TEMP_ID = 254741
VERIFY_TEMP_ID_LOG = 254739
OVERSEA_VERIFY_TEMP_ID = 64123
ACTIVE_TEMP_ID = 51902
SEND_SUCCESS_CODE = 0

mongo_conn = MongoConn.instance()

def gen_sig(phone):
    t = int(time.time())
    sig = sha256('appkey={}&random={}&time={}&mobile={}'.format('', random_key, t, phone)).hexdigest()
    return sig, t

class TXSMS(object):
    @coroutine
    def send(self, phone, zone, tid, params=[]):
        sig, t = gen_sig(phone)
        url = BASE_URL
        body = {
            "tel": {
                "nationcode": zone,
                "mobile": phone,
            },
            "sign": "宁静森林",
            "tpl_id": tid,
            "params": params,
            "sig": sig,
            "time": t,
            "extend": "",
            "ext": ""
        }
        print (body)
        response = yield httpclient.AsyncHTTPClient().fetch(
            url,
            method='POST',
            body=json.dumps(body),
        )
        res = json.loads(response.body)
        # raise Return(res.get("result") == SEND_SUCCESS_CODE)
        raise Return(res)

    @coroutine
    def _send(self, phone, zone, params=''):
        sig, t = gen_sig(phone)
        url = VOICE_URL
        body = {
            "tel": {
                "nationcode": zone,
                "mobile": phone
            },
            "msg": str(params),
            "playtimes": 2,
            "sig": sig,
            "time": t,
            "ext": ""
        }
        response = yield httpclient.AsyncHTTPClient().fetch(
            url,
            method='POST',
            body=json.dumps(body),
        )
        res = json.loads(response.body)
        # raise Return(res.get("result") == SEND_SUCCESS_CODE)
        raise Return(res)


    @coroutine
    def send_code(self, phone, code, zone):
        try:
            cur = mongo_conn.user_coll.find_one({'phone': str(phone)})
        except:
            cur = None
        if zone == "86":
            if cur:
                r = yield self.send(phone, zone, tid=VERIFY_TEMP_ID_LOG, params=[code])
            else:
                r = yield self.send(phone, zone, tid=VERIFY_TEMP_ID, params=[code])
        else:
            r = yield self.send(phone, zone, tid=OVERSEA_VERIFY_TEMP_ID, params=[code])
        raise Return(r)

    @coroutine
    def send_voice(self, phone, code, zone):
        r = yield self._send(phone, zone=zone, params=code)
        raise Return(r)

    @coroutine
    def send_active(self, phone, zone):
        r = yield self.send(phone, zone, tid=ACTIVE_TEMP_ID)
        raise Return(r)


if __name__ == "__main__":
    from tornado import ioloop

    loop = ioloop.IOLoop.instance()


    def done_callback(future):
        print (future.result())
        loop.add_callback(loop.stop)

    t = TXSMS()
    # t.send_code("13020009382", "23423").add_done_callback(done_callback)
    t.send_code("15718835699", "23423").add_done_callback(done_callback)
    loop.start()

