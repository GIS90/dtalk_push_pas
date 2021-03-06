# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    main entry
    消息程序主入口，在运行之前需要完成数据采集与处理、配置修改2个部分。
    1.数据采集与修改
        数据需要按照在template目录下面模板文件进行数据采集，文件名称以及内容采用固定方式，统一使用文件模板。
        - DingTalk User ID源于钉钉管理后台
        - 采集其他消息数据
        - 以模板内容为准，形成消息数据
    2.配置
        修改项目root目录下的config.yaml文件，需要修改ROBOT配置下的APPKEY、APPSECRET，
        具体DingTalk ROBOT的创建、配置请查看README.md文件
    完成1&&2内容之后，运行此文件，其他文件内容无须更改

base_info:
    __version__ = "v.10"
    __author__ = "PyGo"
    __time__ = "2021/11/23"
    __mail__ = "gaoming971366@163.com"

usage:
    python main.py
    All parameters from config.yaml

design:
    +------------------------------------------------------+
    | 1.Initialize source data:                            |
    |   - bank staff information data from db              |
    |   - salary data from db or bank (.xls or .xlsx)      |
    +------------------------------------------------------+
              |
              v
    +------------------------------------------------------+
    | 2.modify config file at project root folder          |
    +------------------------------------------------------+
              |
              v
    +------------------------------------------------------+
    | 3.run the main.py script file to send messages       |
    +------------------------------------------------------+
              |
              v
    +------------------------------------------------------+
    | 4.scan log                                           |
    +------------------------------------------------------+

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""
from core.run import start


if __name__ == '__main__':
    # entry
    # default is python, according to the environment to name
    # local pc have python(2.7) and python3(3.7)
    start()

