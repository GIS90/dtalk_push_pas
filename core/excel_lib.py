# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    excel operation lib
    对excel表格数据进行读写操作，此程序目前不涉及写操作，之开发了对表格的读取操作，支持.xls、.xlsx
    注意要点：
        不管是win还是linux，文件的路径统一采用/，示例：
        f = 'E:/python3/dtalk_send_pas/template/demo.xls'
        避免\t等特殊在win操作系统下的转义，导致文件不可用

base_info:
    __version__ = "v.10"
    __author__ = "PyGo"
    __time__ = "2021/11/23"
    __mail__ = "gaoming971366@163.com"

usage:
    excel_lib = ExcelLib()
    f = 'E:/python3/dtalk_send_pas/template/demojhh哈哈哈哈.xls'
    res = excel_lib.read(read_file=f)
    print(res)

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""
import json
import os
import xlrd
from typing import List, Tuple
from core.status import Status
from core.base_class import BaseClass
from core.logger import logger as LOG
from core.config import DEBUG


class ExcelLib(BaseClass):
    """
    excel operate class
    """
    def __init__(self):
        if DEBUG:
            LOG.debug("ExcelLib class start initialize.")

    def read(self, read_file: str, sheet: int = 0, rows: List = [], columns: List = [], **kwargs) -> json:
        """
        read excel data
        :param read_file: excel文件abs全路径
        :param sheet: 读取的sheet数，从0开始，default value is 0
        :param rows: 读取数据的rows行列表，如果为空，默认读取全部行
        :param columns: 读取数据的columns列列表，如果为空，默认读取全部列
        :param kwargs: 读取excel数据的其他参数配置
            request_title: 读取的表格是否包含title行，默认是true（bool类型）
            response_title: 返回的数据是否包含title说明，默认是true（bool类型）

        :return: dict result
        """
        if DEBUG:
            LOG.debug("ExcelLib read file: %s" % read_file)

        if not read_file or not os.path.exists(read_file) \
                or not os.path.isfile(read_file):
            return Status(
                206,
                'failure',
                '读取的excel数据不存在',
                {}
            ).status_body
        request_title = False if kwargs.get('request_title') is False else True
        # 数据读取开始的行数
        start_row = 1 if request_title else 0
        response_title = False if kwargs.get('response_title') is False else True
        excel_object = xlrd.open_workbook(filename=read_file)
        excel_sheet_names = excel_object.sheet_names()
        if not sheet:
            sheet = 0
        if sheet > len(excel_sheet_names) or sheet < 0:
            return Status(
                203,
                'failure',
                '读取的sheet页不存在',
                {}
            ).status_body
        excel_sheet = excel_object.sheet_by_index(sheet)
        new_rows = list()
        if rows:
            for r in rows:
                try:
                    new_rows.append(int(r))
                except:
                    pass
        new_cols = list()
        if columns:
            for c in columns:
                try:
                    new_cols.append(int(c))
                except:
                    pass

        read_rows = new_rows if new_rows else range(start_row, excel_sheet.nrows, 1)
        read_cols = new_cols if new_cols else range(0, excel_sheet.ncols, 1)
        # 读取表头
        resp_header = list()
        if response_title and request_title:
            for col in read_cols:
                if col < 0: continue
                if not excel_sheet.cell_value(0, col) or excel_sheet.cell_value(0, col) in resp_header:
                    return Status(
                        301,
                        'failure',
                        'Please ensure title is unique or exist: %s' % excel_sheet.cell_value(0, col),
                        {}
                    ).status_body
                resp_header.append(excel_sheet.cell_value(0, col))
        # 读取表数据
        resp_data = list()
        for row in read_rows:
            if not row: continue
            _d = list()
            for col in read_cols:
                if col < 0: continue
                _d.append(excel_sheet.cell_value(row, col))
            if _d: resp_data.append(_d)
        return Status(
            100,
            'success',
            '成功',
            {'header': resp_header, 'data': resp_data}
        ).status_body
