# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    单例模式
    用于其他类继承使用

base_info:
    __version__ = "v.10"
    __author__ = "PyGo"
    __time__ = "2021/11/23"
    __mail__ = "gaoming971366@163.com"

usage:
    from base_class import BaseClass
    class DemoClass(BaseClass)

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""
import threading


class BaseClass(object):

    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        super(BaseClass, self).__init__()
        self.init_run()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with BaseClass._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    def init_run(self):
        pass