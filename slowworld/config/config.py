# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/11/16 下午9:32        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os

if os.environ.get("DOCKER"):
    # 正式服务器
    APP_HOST = ''
    IS_DEBUG = False
    HOST = os.popen("/sbin/ip route|awk '/default/ { print $3 }'").read().strip('\n')
    # mongodb
    MONGODB_HOST = ""
    MONGODB_HOST_LIST = []
    MONGODB_PORT = 30005
    MONGODB_NAME = 'slowworld'

    # redis
    REDIS_HOST = HOST
    REDIS_PORT = 6440

    # redis集群
    SENTINEL_HOST_LIST = [
                          ]

    # 文件下载地址
    DOWN_URL = ""

    # 第三方地址
    AIMUSIC_URL = ""
    LIVEMUSIC_URL = ""


else:
    # 其他服务器
    APP_HOST = 'http://127.0.0.1:33333'
    IS_DEBUG = True

    # mongodb
    MONGODB_HOST = "127.0.0.1"
    MONGODB_PORT = 27001
    MONGODB_NAME = 'slowworld'

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6440

    # redis集群
    SENTINEL_HOST_LIST = []

    # 文件下载地址
    DOWN_URL = "http://127.0.0.1:6262"

    # 第三方地址
    AIMUSIC_URL = ""
    # LIVEMUSIC_URL = "http://58.87.125.111:55555"
    LIVEMUSIC_URL = ""

class app_config(object):
    salt = '85ca6aa6e8e081400aca6c9c79491475'  # 加盐
    token_salt = "78ETzKX45aYdkL5gEmGeJJFuYh483np2XdTP1o/Vo="
    debug = True

    class qiniu(object):
        access_key = ''
        secret_key = ''
        download_base_image_url = ''
        download_base_mp4_url = ''
