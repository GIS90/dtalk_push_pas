# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the all collection of daily tools and methods
    main:
        path
        make dir
        date && time
        ......

base_info:
    __version__ = "v.10"
    __author__ = "PyGo"
    __time__ = "2021/11/23"
    __mail__ = "gaoming971366@163.com"

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.
------------------------------------------------
"""
import os
import sys
import inspect
import hashlib
import time
import platform
from datetime import datetime
from functools import wraps


def get_cur_folder():
    """
    get current folder, solve is or not frozen of the script
    :return: the file current folder
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(__file__))
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        return os.path.abspath(cur_folder)


def get_root_folder():
    """
    get root folder
    """
    return os.path.dirname(get_cur_folder())


def get_template_folder():
    """
    get template folder
    """
    return os.path.join(get_root_folder(), 'template')


def get_log_folder():
    """
    get log folder
    """
    return os.path.join(get_root_folder(), 'log')


def md5(v):
    """
    # md5加密
    :param v: value
    :return: md5 value
    """
    if isinstance(v, str):
        v = v.encode('utf-8')
    return hashlib.md5(v).hexdigest()


def s2d(s, fmt="%Y-%m-%d %H:%M:%S"):
    """
    # 字符串转日期
    :param s: string type time
    :param fmt: transfer to formatter
    :return: datetime type time
    """
    return datetime.strptime(s, fmt)


def d2s(d, fmt="%Y-%m-%d %H:%M:%S"):
    """
    # 日期转字符串
    :param d: datetime type time
    :param fmt: transfer to formatter
    :return: string type time
    """
    return d.strftime(fmt)


def d2ts(d):
    """
    # 日期转ts
    :param d: datetime type parameter
    :return: time.time type
    """
    return time.mktime(d.timetuple())


def s2ts(s, format="%Y-%m-%d %H:%M:%S"):
    """
    # 字符串转ts
    :param s: sting type parameter
    :return: time.time type
    """
    d = s2d(s, format)
    return d2ts(d)


def dura_date(d1, d2, need_d=False):
    """
    # get datetime1 and datatime difference 时间差
    :param d1: datetime parameter 1
    :param d2: datetime parameter 2
    :param need_d: is or not need hours, minutes, seconds
    :return: result 1: seconds
    result 2: hours, minutes, seconds
    """
    if type(d1) is str:
        d1 = s2d(d1)
    if type(d2) is str:
        d2 = s2d(d2)
    d = d2 - d1
    if need_d is False:
        seconds = d.seconds
        mins = seconds / 60.00
        hours = mins / 60.00
        return seconds, mins, hours
    return d


def get_now_time():
    """
    # 获取当前时间
    :return: to return the now of datetime type
    """
    return datetime.now()


def get_now_date():
    """
    # 获取当前日期
    :return: to return the now of date type
    """
    return datetime.now().date()


def get_now(format="%Y-%m-%d %H:%M:%S"):
    """
    # 获取当前时间str
    :return: to return the now of string type
    """
    return d2s(datetime.now(), format)


def get_week_day(date):
    """
    # 获取weekday
    :param date: date
    :return: week
    """
    weekdaylist = ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天')
    weekday = weekdaylist[date.weekday()]
    return weekday


# 计时器
def timeer(fn):
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        start = datetime.now()
        res = fn(*args, **kwargs)
        end = datetime.now()
        print('@timeer %s is run: %s' % (fn.__name__, (end - start).seconds))
        return res

    return _wrapper


def mk_dirs(path):
    """
    # mdkirs folder 建立文件夹（递归）
    :param path: to make folder path
    :return: path
    """
    os.makedirs(path)
    return path


def get_base_dir():
    """
    # 获取项目base目录（deploy）
    :return: deploy base path
    """
    return os.path.dirname(get_cur_folder())


def get_deicle(x, y):
    """
    # 保留小数
    :param x: value
    :param y: point decimal
    :return:
    """
    if not x:
        return None
    if x.find('.') > 0:
        return round(x, y)
    return int(x)


def get_month_list():
    """
    static method
    # 获取月份list
    :return: list data
    """
    return [u'1月', u'2月', u'3月', u'4月', u'5月', u'6月',
            u'7月', u'8月', u'9月', u'10月', u'11月', u'12月']


def get_os_type():
    """
    static method
    # 获取当前运行系统时win or linux
    :return:string
    """
    return 'windows' if platform.system().lower() == 'windows' else 'linux'
