# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/26 上午9:51        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from __future__ import unicode_literals, absolute_import
import site

try:
    import i_am_kidding_pycharm  # For suppress pycharm's import warning
except ImportError:
    i_am_kidding_pycharm = None
finally:
    site.addsitedir("../")  # For absolute import

from hotqueue import HotQueue

from slowworld.common.cache import HOTQUEUE_KEY
from slowworld.conf import worker_type
from slowworld.config import config

queue = HotQueue(HOTQUEUE_KEY, host=config.REDIS_HOST, port=config.REDIS_PORT)


@queue.worker
def job_worker(data):
    print(data.get("type"))

    if not isinstance(data, dict):
        return
    if not data.get("type"):
        return
    result = True
    lines = 0



if __name__ == '__main__':
    print("\033[1;30;46m|worker is start ! \033[0m")
    job_worker()
