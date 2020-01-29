#! /usr/env/bin python
# -*- coding: utf-8 -*-
from tornado.gen import Return
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPClient
from tornado import gen
import requests
import json
import urllib
from slowworld.conf.sms_config import SMS_APP_KEY, SMS_APP_KEY1, SEND_SMS_URL1,VERIFY_URL3, VERIFY_URL4, VERIFY_URL1, VERIFY_URL2
class MobSMS:
    """版本要求：
    http://www.mob.com/#/index
    发送短信：
        https://api.sms.mob.com/sms/sendmsg
    验证短信：
        1、IOS version 9 以下：https://api.sms.mob.com/sms/verify（适用验证来自SMSSDK1.2.0版本 IOS发送的验证码）
        2、IOS version 9 以上、Android： https://web.sms.mob.com/sms/verify（适用验证来SMSSDK1.3.0以上版本发送的验证码）
        3、如果开启服务端发送，验证时需用：https://api.sms.mob.com/sms/checkcode）（适用验证来自服务端发送的验证码）
    """
    def __init__(self, verify_type=3):
        self.appkey = SMS_APP_KEY
        self.send_url = SEND_SMS_URL1
        if verify_type == 3:
            # 采用服务端发送验证码，需要这个验证
            self.verify_url = VERIFY_URL3
        elif verify_type == 1:
            # IOS version 9版本通过这个验证
            self.verify_url = VERIFY_URL1
        elif verify_type == 4:
            self.appkey = SMS_APP_KEY1
            self.verify_url = VERIFY_URL4
        else:
            # version 9 以上版本 IOS和安卓都通过这个验证
            self.verify_url = VERIFY_URL2

    def __call__(self, *args, **kwargs):
        return self

    def verify_sms_code(self, zone, phone, code, debug=False):
        if debug:
            # return 200
            return True

        data = {'appkey': self.appkey, 'phone': phone, 'zone': zone, 'code': code}
        req = requests.post(self.verify_url, data=data, verify=False, timeout=5)
        if req.status_code == 200:
            j = req.json()
            result = j.get('status', 500)
            if int(result) == 200:
                return True
            else:
                return False
        else:
            # return 500
            return False

    @gen.coroutine
    def verify_asyn_code(self, zone, phone, code, debug=False):
        if debug:
            raise gen.Return(True)
        data = {'appkey': self.appkey, 'phone': phone, 'zone': zone, 'code': code}
        request = HTTPRequest(self.verify_url, method="POST", body=urllib.urlencode(data), validate_cert=False)
        httpClient = AsyncHTTPClient()
        try:
            response = yield httpClient.fetch(request)
        except Exception as e:
            results = False
        else:
            if response.code == 200:
                body = json.loads(response.body)
                if int(body['status']) == 200:
                    results = True
                else:
                    results = False
            else:
                results = False
        raise gen.Return(results)

    @gen.coroutine
    def send_sns(self, zone, phone):
        body = {"appkey": self.appkey, "zone": zone, "phone": phone}
        request = HTTPRequest(self.send_url, method="POST", body=urllib.urlencode(body), validate_cert=False)
        httpClient = AsyncHTTPClient()
        try:
            response = yield httpClient.fetch(request)
            if json.loads(response.body).get("status") != 200:
                raise Return()
        except Exception as e:
            raise gen.Return(dict(result=0))
        raise gen.Return(dict(result=1))

    def send_sns_sync(self, zone, phone):
        body = {"appkey": self.appkey, "zone": zone, "phone": phone}
        request = HTTPRequest(self.send_url, method="POST", body=urllib.urlencode(body), validate_cert=False)
        httpClient = HTTPClient()
        try:
            response = httpClient.fetch(request)
            if json.loads(response.body).get("status") == 200:
                return dict(result=1)
            else:
                print(response.body)
                return dict(result=0)
        except Exception as e:
            return dict(result=0)



if __name__ == '__main__':
    pass
    # mobsms = MobSMS(4)
    # print mobsms.verify_sms_code(86, 15232815600, 5825)
    # print mobsms.send_sns_sync('86', '15232815600')