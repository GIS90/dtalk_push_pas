# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    解析项目root目录下的config.yaml文件，使用pyyaml包
    初始化时建议配置默认值，可以避免程序运行配置参数时发生异常
    the run configuration information of the project
    use analyse to the config of yaml formatter
    information:
        - SERVER：项目基础信息配置（*不建议更改*）
          * NAME：程序名称
          * VERSION：版本
          * DEBUG：是否采用Debug模式运行，值有True与False，默认值为True开启Debug模式，处于Debug模式的程序会打印log，建议开启
          * IS_TEST：程序开发调试阶段使用，获取模板数据DingTalk use id是否唯一，如果参数为False模板有重复的ID会报error，否则True则会通过，默认设置为False即可


        - DINGTALK：DingTalk Robot openApi服务端URL设置（***不可以更改***）
          防止DingTalk官网服务端变更地址时使用，接口为ali openApi，变更的可能性极小。
          * BASE_URL：DingTalk服务API根地址
          * TOKEN_URL：获取access token地址


        - ROBOT：DingTalk Robot配置信息（**必须更改**）
          * APPKEY：机器人AppKey
          * APPSECRET：机器人AppSecret
          设置钉钉后台创建的企业内部机器人相关配置，具体创建机器人操作见：http://pygo2.top/articles/32206/


        - LOG：日志信息的配置（*不建议更改*）
          * LOG_DIR：日志信息的存放目录，配置值为相对路径，基于项目root根目录下设置，配置好目录程序会自动进行创建
          * LOG_LEVEL：打印日志级别，有5个级别，默认为debug
            ```
            logger.debug('message')
            logger.info('message')
            logger.warning('message')
            logger.error('message')
            logger.critical('message')
            ```
          * LOG_FORMATTER：打印日志格式，具体格式设置请参照core/logger.py文件操作说明
            ```
            %(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s - %(message)s
            ```
          * LOG_FILENAME_PREFIX：日志文件名称的prefix


        - Template：表格模板配置（*不建议更改*）
         包含FILE、SHEET_INDEX、SHEET_INDEX and so on，具体说明如下：
          * FILE：模板文件名称，目前只支持在template目录存放模板文件，建议文件名称为英文，**只支持.xls格式文件**
          * IS_TITLE：模板文件是否包含表头，默认设置为True包含表头，并且为第一行，如果不提供表头，消息只有数字部分
          * SHEET_INDEX：读取的模板文件sheet索引值，从1,2,3开始算，默认读取第一个
          *  COL_INDEX_DINGTALK_ID：设置DingTalk中员工导出文件中的USER_ID，系统会依据此ID对DingTalk人员进行消息推送，
            根据项目实际情况以及模板进行配置，默认为第一列
          * COL_INDEX_HYLB：配置模板文件DingTalk人员的行员类别列，默认为第二列，程序会匹配此参数与MESSAGE_COL配置参数，依据行员类别进行不同消息体（工资项）的内容推送
            ```
            模板特别说明：
            1、模板文件暂不支持其他目录，只允许在template目录，建议英文命名，并且只支持.xls格式文件
            2、模板文件需要提供表头，并且在第一行
            3、其中，USER_ID不可以为空，如果为空则对此行数据自动过滤不推送消息
            DingTalk User ID获取参考：http://pygo2.top/articles/45420/
            ```


        - MANAGE：DingTalk消息控制配置（*不建议更改*）
          * IS_ADD_IMAGE：推送的消息体是否添加图片显示，默认为空不显示，有需要显示图片的添加图片公网URL地址
          * CONTROL：控制不推送DingTalk消息的人员ID，此ID为DingTalk后台导出的User ID，格式为列表，用英文单引号/双引号括起来，多个用英文逗号分割


        - MESSAGE_COL：DingTalk推送消息体配置（**必须更改**）
          配置采用key: value格式，如果不进行配置删除配置值，程序会对每一个用户发送所属行数据的全部模板内容，示例：E01: [3, 4, 5, 6, 7, 8, 9, 28, 31, 26]
          * key：E01代表用户的类别代号，对应模板文件中的第二列HYLBDH
          * value：[]代表工资项，需要配置用户推送哪些工资项，需要提供模板文件对应的列数（从1，2，3开始），如果为空，则发送全部工资项内容

base_info:
    __version__ = "v.10"
    __author__ = "PyGo"
    __time__ = "2021/11/23"
    __mail__ = "gaoming971366@163.com"

design:

reference urls:

python version:
    python3


Enjoy the good everyday！！!
Life is short, I use python.
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python config.py
# ------------------------------------------------------------
import os
import sys
import yaml
import inspect
import logging

# logging.basicConfig()
logger = logging.getLogger(__name__)


# get root folder, solve is or not frozen of the script
def _get_root_folder():
    if getattr(sys, "frozen", False):
        current_folder = os.path.dirname(os.path.abspath(__file__))
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        current_folder = os.path.abspath(cur_folder)
    return os.path.dirname(current_folder)


# get config file
def _get_config():
    return os.path.join(_get_root_folder(), 'config.yaml')


# default log dir
def __get_log_dir():
    return os.path.join(_get_root_folder(), 'log')


"""
default config
"""
# SERVER
NAME = 'DTALK_SEND_PAS'
VERSION = '1.0.0'
DEBUG = False
IS_TEST = False

# DINGTALK
DTALK_BASE_URL = 'https://oapi.dingtalk.com/'
DTALK_TOKEN_URL = 'gettoken'

# ROBOT
ROBOT_APPKEY = 'dingsxsbv4swnn17bf3d'
ROBOT_APPSECRET = 'bn48xUE0feFcA0S9L2QS3TA7Gqp9J2-yrZR0baOQyxoY-aQI9rhLYetQDiZ0oWgj'

# LOG
LOG_DIR = __get_log_dir()
LOG_LEVEL = "debug"
LOG_FORMATTER = "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s - %(message)s"
LOG_FILENAME_PREFIX = 'dtalk_send_pas'

# TEMPLATE
TEMPLATE_FILE = 'DingTalk_Bank_Salary.xls'
TEMPLATE_IS_TITLE = True
TEMPLATE_SHEET_INDEX = 1
TEMPLATE_COL_INDEX_DINGTALK_ID = 1
TEMPLATE_COL_INDEX_HYLB = 2

# MANAGE:
MANAGE_CONTROL = []
MANAGE_IS_ADD_IMAGE = ''

# MESSAGE_COL
MESSAGE_COL = {}


"""
enrty: initializate config
"""
logger.info('Start initializing configuration...')
_config_file = _get_config()
if not os.path.exists(_config_file) or not os.path.isfile(_config_file):
    logger.critical('====== config file is not exist, exit ======')
    sys.exit(1)

with open(_config_file, 'r', encoding='utf-8') as f:
    _config_info = yaml.safe_load(f)
    if not _config_info:
        logger.critical('====== config file is unavail, exit ======')
        sys.exit(1)

    # SERVER
    NAME = _config_info['SERVER']['NAME'] or NAME
    VERSION = _config_info['SERVER']['VERSION'] or VERSION
    DEBUG = _config_info['SERVER']['DEBUG'] or DEBUG
    IS_TEST = _config_info['SERVER']['IS_TEST'] or IS_TEST

    # DINGTALK
    DTALK_BASE_URL = _config_info['DINGTALK']['BASE_URL'] or DTALK_BASE_URL
    DTALK_TOKEN_URL = _config_info['DINGTALK']['TOKEN_URL'] or DTALK_TOKEN_URL

    # ROBOT
    ROBOT_APPKEY = _config_info['ROBOT']['APPKEY'] or ROBOT_APPKEY
    ROBOT_APPSECRET = _config_info['ROBOT']['APPSECRET'] or ROBOT_APPSECRET

    # LOG
    if _config_info['LOG']['LOG_DIR']:
        LOG_DIR = os.path.join(_get_root_folder(), _config_info['LOG']['LOG_DIR'])
    else:
        LOG_DIR = LOG_DIR
    if not os.path.exists(LOG_DIR):
        logger.critical('====== log dir is not exist, create %s... ======' % LOG_DIR)
        os.makedirs(LOG_DIR)
    LOG_LEVEL = _config_info['LOG']['LOG_LEVEL'] or LOG_LEVEL
    LOG_FORMATTER = _config_info['LOG']['LOG_FORMATTER'] or LOG_FORMATTER
    LOG_FILENAME_PREFIX = _config_info['LOG']['LOG_FILENAME_PREFIX'] or LOG_FILENAME_PREFIX

    # TEMPLATE
    TEMPLATE_FILE = _config_info['TEMPLATE']['FILE'] or TEMPLATE_FILE
    TEMPLATE_IS_TITLE = _config_info['TEMPLATE']['IS_TITLE'] or TEMPLATE_IS_TITLE
    TEMPLATE_SHEET_INDEX = _config_info['TEMPLATE']['SHEET_INDEX'] or TEMPLATE_SHEET_INDEX
    TEMPLATE_COL_INDEX_DINGTALK_ID = _config_info['TEMPLATE']['COL_INDEX_DINGTALK_ID'] or TEMPLATE_COL_INDEX_DINGTALK_ID
    TEMPLATE_COL_INDEX_HYLB = _config_info['TEMPLATE']['COL_INDEX_HYLB'] or TEMPLATE_COL_INDEX_HYLB

    # MANAGE
    MANAGE_CONTROL = _config_info['MANAGE']['CONTROL'] or MANAGE_CONTROL
    MANAGE_IS_ADD_IMAGE = _config_info['MANAGE']['IS_ADD_IMAGE'] or MANAGE_IS_ADD_IMAGE

    # MESSAGE
    MESSAGE_COL = _config_info['MESSAGE_COL']


logger.info('End initializing configuration...')