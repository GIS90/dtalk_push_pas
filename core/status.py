# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    JSON RESULT

base_info:
    __version__ = "v.10"
    __author__ = "PyGo"
    __time__ = "2021/11/23"
    __mail__ = "gaoming971366@163.com"

usage:
    return Status(
            100,
            "success",
            "成功",
            {}
        )
design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""
import json


class Status(object):
    def __init__(self, status_id: int = 100, status: str = 'success', msg: str = '成功', data=None):
        if data is None:
            data = {}
        self.status_body = {
            "status_id": status_id,
            "status": status,
            "msg": msg,
            "data": data,
        }
        self.data = data
        super(Status, self).__init__()

    def json(self):
        return json.dumps(self.status_body)





