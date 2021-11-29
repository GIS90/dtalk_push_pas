# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    main entry
    消息程序主入口，在运行之前需要完成数据采集与配置修改2个部分。
    1.数据采集
        数据需要存放在template目录下面，文件名称以及内容采用固定方式，统一使用文件模板。
    2.配置
        修改项目root目录下的config.yaml文件，需要修改ROBOT配置下的APPKEY、APPSECRET，具体DingTalk ROBOT的创建、配置请查看
        README.md文件

base_info:
    __version__ = "v.10"
    __author__ = "PyGo"
    __time__ = "2021/11/23"
    __mail__ = "gaoming971366@163.com"

usage:

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


Enjoy the good everyday！！!
Life is short, I use python.

------------------------------------------------
"""
from core.run import start


if __name__ == '__main__':
    # entry
    # default is python, according to the environment to name
    # local pc have python(2.7) and python3(3.7)
    start()

