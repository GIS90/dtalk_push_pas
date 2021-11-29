# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    record  system information
    level: debug, info, warning, error, critical
    
    CRITICAL 50
    ERROR 40
    WARNING 30
    INFO 20
    DEBUG 10
    

usage:
    from app.utils.logger import logger
    
    logger.debug('message')
    logger.info('message')
    logger.warning('message')
    logger.error('message')
    logger.critical('message')
    
    
formatter：
    %(levelno)s：打印日志级别的数值。

    %(levelname)s：打印日志级别的名称。
    
    %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]。
    
    %(filename)s：打印当前执行程序名。
    
    %(funcName)s：打印日志的当前函数。
    
    %(lineno)d：打印日志的当前行号。
    
    %(asctime)s：打印日志的时间。
    
    %(thread)d：打印线程ID。
    
    %(threadName)s：打印线程名称。
    
    %(process)d：打印进程ID。
    
    %(processName)s：打印线程名称。
    
    %(module)s：打印模块名称。
    
    %(message)s：打印日志信息。


base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/1/15"
    __mail__ = "mingliang.gao@163.com"
    

remarks:
    everyone file allow to import and to use
------------------------------------------------
"""
import datetime
import inspect
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from core.config import LOG_DIR, LOG_LEVEL, LOG_FORMATTER, LOG_FILENAME_PREFIX

LEVEL = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


logger = logging.getLogger(__name__)


# get current folder, solve is or not frozen of the script
def _get_log_folder():
    if getattr(sys, "frozen", False):
        current_folder = os.path.dirname(os.path.abspath(__file__))
    else:
        current_folder = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    return os.path.join(os.path.dirname(current_folder), 'log')


def _get_now(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strftime(datetime.datetime.now(), format)


logdir = LOG_DIR
level = LOG_LEVEL
formatter = LOG_FORMATTER
filename_prefix = LOG_FILENAME_PREFIX


if not logdir:
    logdir = _get_log_folder()
if not os.path.exists(logdir):
    try:
        os.makedirs(logdir)
        logger.critical('====== log dir is not exist, create: %s ======' % logdir)
    except:
        logger.critical('====== log dir is not exist and create failure, exist: %s ======' % logdir)
        sys.exit(1)
if not level:
    level = 'debug'
# 格式
if not formatter:
    formatter = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s - %(message)s'
formatter = logging.Formatter(formatter,
                              datefmt='%Y/%m/%d %H:%M:%S')

log_level = LEVEL.get(level)
logger.setLevel(level=log_level)


# 定义一个RotatingFileHandler，最多备份10个日志文件，每个日志文件最大10M
log_name = filename_prefix + '_' + _get_now(format="%Y-%m-%d") \
    if filename_prefix and filename_prefix != '-' else _get_now(format="%Y-%m-%d")
log_file = os.path.join(logdir, (log_name + '.log'))
file_handler = RotatingFileHandler(log_file,
                                   mode='a',
                                   maxBytes=10*1024*1024,
                                   backupCount=10,
                                   encoding='utf-8')
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# 控制台
stream_handler = logging.StreamHandler()
stream_handler.setLevel(log_level)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
