# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    main entry
    RC 0: 程序正常退出
       1: 程序异常退出
base_info:
    __version__ = "v.10"
    __author__ = "PyGo"
    __time__ = "2021/11/25"
    __mail__ = "gaoming971366@163.com"

usage:

design:

reference urls:

python version:
    python3


Enjoy the good everyday！！!
Life is short, I use python.

------------------------------------------------
"""
import sys
import json
import os.path
import time
import random

from core.ding_api import DingApi
from core.utils import timeer, get_template_folder, get_os_type, get_now
from core.config import TEMPLATE_FILE, TEMPLATE_IS_TITLE, TEMPLATE_SHEET_INDEX, \
    TEMPLATE_COL_INDEX_DINGTALK_ID, TEMPLATE_COL_INDEX_HYLB, MESSAGE_COL, IS_TEST,\
    MANAGE_IS_ADD_IMAGE, MANAGE_CONTROL, MANAGE_TITLE, DK_INTERVAL
from core.logger import logger as LOG
from core.excel_lib import ExcelLib


def __message_format_col() -> dict:
    """
    返回格式化后的行员类别message列
    配置文件是按1，2，3，4开始的列
    代码处理是按0，1，2，3开始，需要进行处理
    """
    res = dict()
    if not MESSAGE_COL:
        return res

    for key, value in MESSAGE_COL.items():
        if not key: continue
        if key in res.keys():
            raise ValueError("Please check MESSAGE_COL configuration: %s is repeat." % key)
        res[key] = [x-1 for x in value]
    else:
        return res


def get_excel_data(excel_file: str, sheet_index: int = 0) -> json:
    """
    获取源数据，主要操作有2步:
        第一获取excel表格数据
        第二对数据进行格式化，形成key: value格式，依据HYLBDH配置的列表进行格式化
    """
    is_title = True if TEMPLATE_IS_TITLE else False
    if get_os_type() == 'windows':  # 判断系统类型，如果为win把template模板路径进行\替换/
        excel_file = excel_file.replace('\\', '/')
    excel_lib = ExcelLib()
    json_res = excel_lib.read(read_file=excel_file, sheet=sheet_index,
                              request_title=is_title, response_title=is_title)
    if json_res.get('status_id') != 100:
        raise Exception("Read template file data occur error: %s" % json_res.get('msg'))

    ret_data = dict()
    titles = json_res.get('data').get('header')
    message_col = __message_format_col()
    for _d in json_res.get('data').get('data'):
        if not _d: continue
        dtalk_user_id = _d[TEMPLATE_COL_INDEX_DINGTALK_ID - 1]
        if not dtalk_user_id: continue
        hylb = _d[TEMPLATE_COL_INDEX_HYLB - 1] or ''
        _unit = dict()
        _hy_message_col = message_col.get(hylb) if message_col.get(hylb) \
            else range(0, len(_d), 1)
        for col in _hy_message_col:
            if col < 0: raise IndexError("Format excel data is error: %s %s index out of range" % (hylb, col))
            if not titles[col] and not _d[col]: continue
            _unit[titles[col]] = _d[col]
        if dtalk_user_id in ret_data.keys() and not IS_TEST:
            raise ValueError("Format excel data is error: %s is repeat." % dtalk_user_id)
        ret_data[dtalk_user_id] = _unit
    return ret_data


def __format_message_json(content: dict) -> dict:
    """
    格式化推送的信息，string -> json
    获取config是否添加额外的图片
    后续定制专门的markdown信息，待开发TODO
    DingTalk 消息格式：
        {
            "title": "2021-12绩效明细",
            "text": "#### 2021-11绩效明细  \n  - 个人存款绩效：278  \n  - 贷款绩效：278  \n  - 部门履职绩效：278  \n  - 合规履职绩效：278  \n  - 存款下降扣发：278  \n  - ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)"
        }
    支持markdown语法
    \n代表换行，建议\n前后分别加2个空格
    参考：https://developers.dingtalk.com/document/app/message-types-and-data-format

    名称          类型          是否必填          示例值          描述
    msgtype      String        是               markdown      消息类型，Markdown类型为：markdown。
                                                              消息链接跳转，请参考消息链接说明。
    title        String        是               测试标题        首屏会话透出的展示内容。
    text         String        是               测试内容        markdown格式的消息，建议500字符以内。
    """
    title = MANAGE_TITLE if MANAGE_TITLE else '%s月薪资明细' % get_now(format="%Y-%m")
    text = '### %s' % title
    if MANAGE_IS_ADD_IMAGE:
        text += '  \n  - ![](%s)' % MANAGE_IS_ADD_IMAGE
    for _k, _v in content.items():
        if not _k and not _v: continue
        # TODO 只有数值型才为空才设置0
        if not _v:
            _v = 0
        if isinstance(_v, float):
            _v = round(_v, 2)
        text += '  \n  - %s: %s' % (_k, _v)
    ding_msg = {
        "title": '%s    详情...' % title,
        "text": text,
    }
    return ding_msg


def run():
    """
    Detailed logic code
    no need parameters, all from config file
    """
    # check template file and refer parameters
    excel_file = os.path.join(get_template_folder(), TEMPLATE_FILE)
    if not excel_file or not os.path.exists(excel_file) \
            or not os.path.isfile(excel_file):
        raise FileExistsError("Template file is not exist, please check.")
    try:
        # xlrd读取excel数据时，sheet index是从0,1,2,3...开始算
        sheet_index = int(TEMPLATE_SHEET_INDEX) - 1
    except:
        sheet_index = 0
    excel_data = get_excel_data(excel_file=excel_file, sheet_index=sheet_index)
    if not excel_data:
        raise ValueError("Template file not found data, please check.")

    # DingTalk push message
    dtalk_lib = DingApi()
    if not dtalk_lib.is_avail():
        raise Exception("DingTalk not found access token, please check configuration or try again later.")
    success_list = list()
    failure_list = list()
    for k, v in excel_data.items():
        if not k or not v or k in MANAGE_CONTROL: continue
        res = dtalk_lib.robot2send(__format_message_json(v), k)
        success_list.append(k) if res.get('status_id') == 100 else failure_list.append(k)
        LOG.info('%s: %s' % (k, res.get('msg')))
        if DK_INTERVAL > 0:
            time.sleep(random.uniform(0.1, DK_INTERVAL))
    else:
        LOG.info('Success list[%s]: %s' % (len(success_list), ', '.join(success_list)))
        LOG.info('Failure list[%s]: %s' % (len(failure_list), ', '.join(failure_list)))


@timeer
def start() -> None:
    """
    real main entry
    """
    RC = 1
    run()
    try:
        RC = 0
    except Exception as e:
        LOG.error(e)
    sys.exit(RC)
