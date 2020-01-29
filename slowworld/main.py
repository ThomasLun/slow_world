# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/11/16 下午9:20        
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



import sys
import logging
import multiprocessing
import tornado
import tornado.ioloop
import tornado.web
import tornado.log
from tornado.options import options, define

from slowworld.api import *
from slowworld.common.connections import MotorConn, RedisConn
from slowworld.config import config
from slowworld.services import Services

aipiano_route = [
    (r"/404", NotFoundHandler),
    # 子商品
    (r'/v1/user/create', UserHandler, dict(action=UserHandler.create)),

]


class ApiApplication(tornado.web.Application):
    def __init__(self):
        super(ApiApplication, self).__init__(
            handlers=aipiano_route,
            **dict(
                default_handler_class=NotFoundHandler,
                debug=config.IS_DEBUG,
                cookie_secret='xxx',
                serve_traceback=False
            )
        )
        self.colls = MotorConn.instance()
        self.redis = RedisConn.instance().conn
        self.services = Services.instance()


def run(port):
    app = ApiApplication()
    app.port = port
    app.listen(int(port))
    logging.info('Listening on port: {}'.format(port))
    tornado.ioloop.IOLoop.instance().start()


def main():
    define('port', default=33333, type=str, help='run at port')
    tornado.options.parse_command_line()
    if not any([x.startswith('--logging=') for x in sys.argv]):
        level = logging.INFO if config.IS_DEBUG else logging.WARNING
        logging.getLogger().setLevel(level)
        tornado.log.app_log.setLevel(level)
        tornado.log.gen_log.setLevel(level)
        tornado.log.access_log.setLevel(level)

    port = options.port if len(sys.argv) == 1 else int(sys.argv[1])
    print("\033[1;30;46m|running in %s:\033[0m" % port)
    if str(port).isdigit():
        run(port)
    else:
        first_port, count = map(int, port.split('+'))
        for p in range(first_port, first_port + count):
            multiprocessing.Process(target=run, args=(p,)).start()


if __name__ == '__main__':
    main()
