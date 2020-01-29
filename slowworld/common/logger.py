# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/11/17 上午12:15        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

from __future__ import unicode_literals
from future.builtins import str

import os
import logging
import logging.handlers


import colorlog
import datetime
import log4mongo.handlers

from slowworld.config import config


class MongoFormatter(logging.Formatter):
    DEFAULT_PROPERTIES = logging.LogRecord(
        '', '', '', '', '', '', '', '').__dict__.keys()

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        document = {
            'timestamp': datetime.datetime.utcnow(),
            'level': record.levelname,
            'thread': record.thread,
            'threadName': record.threadName,
            'message': record.getMessage(),
            'loggerName': record.name,
            'fileName': record.pathname,
            'module': record.module,
            'method': record.funcName,
            'lineNumber': record.lineno
        }
        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })
        # Standard document decorated with extra contextual information
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(
                set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        return document


def init_logger():
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s.%(msecs)03d %(levelname)-8s %(name)-20s %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers[0].setFormatter(formatter)

    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=os.path.join(os.path.dirname(__file__), '../../logs/log.txt'))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d %(levelname)-8s %(name)-20s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    ))
    logger.addHandler(file_handler)

    mongo_handler = log4mongo.handlers.MongoHandler(host=config.MONGODB_HOST, port=config.MONGODB_PORT)
    mongo_handler.setLevel(logging.DEBUG)
    mongo_handler.setFormatter(MongoFormatter())
    logger.addHandler(mongo_handler)

    logger.info('Logger has been initialized.')