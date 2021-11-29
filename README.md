## 简介

基于Python语言研发，调用DingTalk（钉钉）Robot OpenApi实现钉钉机器人自动化推动绩效工资明细到钉钉用户。

目前，程序处于***v1.0.0***版本研发阶段，具体功能如下：
- Robot自动化推送DingTalk消息
- 日志记录（初次运行项目会自动创建）
- 参数配置
- 模板配置（DingTalk User ID、消息内容）

v1.1.0预研发功能：
- fix v1.0.0 bug
- 优化参数配置，预加入DingTalk消息体配置
- 打包制作.exe文件或者一键式部署（具体部署方式以发布版本功能为准）

> ### 效果图

<img src="http://pygo2.top/images/result.jpg" width = "350" height = "450" alt="图片名称" align=center />

> ### 项目架构

- 开发语言：***Python3.7***
- 研发工具：Pycharm CE

程序可运行于Linux、Windows、MacOS等不同系统上，git clone之后进行修改配置，可在此基础上可进行二次开发。

> ### 目录说明

程序中的配置信息提取到root目录下config.yaml配置文件，将运行代码封装core核心目录中，对外只暴露程序入口，有兴趣或者想了解源码的依据目录说明进行源代码查看。

* ***core***   
  程序的核心运行代码：  
    1. **run** 程序运行的逻辑代码
    1. **base_class** 单例模式 
    3. **config** 配置解析
    4. **ding_api** 钉钉Robot openApi的封装
    5. **excel_lib** Excel操作类
    6. **logger** 程序日志
    7. **status** Method Response json封装类
    8. **utils** 通用静态方法
* log   
  日志存放目录，***git clone***之后，初次运行会自动创建log目录，以config.yaml配置为准，名称采用FILENAME_PREFIX + YY-mm-dd.log命名，具体配置请参考config.yaml中的LOG，不建议更改。
* package   
  dingtalk.zip：DingTalk openApi离线包   
  官方下载地址：https://developers.dingtalk.com/document/resourcedownload/download-server-sdk/title-12y-g4g-zn2?pnamespace=robots   
  建议使用官网的***新版服务端SDK***，除了Python SDK还有Java、C#、GO、PHP等，当前主流的开发语言SDK包都提供了。
  
* ***template***   
  存放DingTalk模板配置文件，目前程序**只支持.xls格式的模板**，文件中包含推送消息的用户以及内容，具体template配置相关请查下下个章节配置说明，模板格式如下：
  
| USER_ID  | HYLBDH | 统计日期 | 机构名称 | 行员代号 | 行员名称 | 行员类别 | 行员岗位 | 工资项1 | 工资项2 | 工资项N | 实发绩效工资 |
| :-----------: | :-----------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| 032511245938821831  | E01 | 20210930 | 测试部 | 100001 | mingliang.gao1 | 支行行长 | 支行行长 | 100 | 500 | -80 | 520 |
| manager2730  | E02 | 20210930 | 研发部 | 100002 | mingliang.gao2 | 支行行长 | 支行行长 | 100 | 500 | -80 | 520 |
    
* main.py   
  程序入口
* config.yaml  
  配置文件
* requirements.txt
  程序包版本
  
> ### 配置说明

- SERVER：项目基础信息配置（*不建议更改*）  
  * NAME：程序名称
  * VERSION：版本信息   
  * DEBUG：是否采用Debug模式运行，值有True与False，默认值为True开启Debug模式，处于Debug模式的程序会打印log，建议开启
  * IS_TEST：程序开发调试阶段使用，获取模板数据DingTalk use id是否唯一，如果参数为False模板有重复的ID会报error，否则True则会通过，默认设置为False即可


- DINGTALK：DingTalk Robot openApi服务端URL设置（***不可以更改***）  
  防止DingTalk官网服务端变更地址时使用，接口为ali openApi，变更的可能性极小。
  * BASE_URL：DingTalk服务API根地址
  * TOKEN_URL：获取access token地址，DingTalk所有的OpenApi操作均需要认证，access token是二次对接的第一步
    

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
    

## 部署策略

这部分介绍项目的环境搭建、运行，帮助开发者把项目跑起来，具体的测试部分需要用户自行创建测试数据进行测试。

> ### 环境搭建

项目是用Python语言开发，而且需要在有网的PC/服务器上进行环境搭建，除了在安装包的时候可以实现一键式包安装，主要原因在于程序调用了DingTalk Robot OpenApi，需要联网把数据推送给ali服务。  
第一要素：<font style="color: red; font-size: 1.5rem; font-style: italic;">网络</font>

1. Pyhton环境  
Python官网下载地址：https://www.python.org/downloads/  
依据系统进行版本下载，建议下载安装Python3.7或者以上的版本，本程序是基于3.7进行开发。  
安装没什么特别说明的，安装完之后记得把Python加入到系统Path。

2. 包安装  
Python安装完之后，会自动安装***pip***包管理工具，对包进行管理、安装、卸载等操作。  
对于初学者不需要进行***pip***源配置，毕竟默认源下载时候需要***fanqiang***，很慢，后期熟悉Python之后再进行更改源更改，自行***baidu***一下，本程序的具体包安装见下一主题包说明，先讲述包安装：    
    ```
    cd dtalk_push_pas
    pip install -r requirements.txt
    ```
    第一句命令：控制台进入到项目root目录打  
    第二句命令：批量包安装


3. git项目     
    ```
    git clone git@github.com:GIS90/dtalk_push_pas.git
    或者
    git clone https://github.com/GIS90/dtalk_push_pas.git
    ```
    如果出现git命令找不到情况，***baidu***自行安装git命令。

4. Pycharm CE安装  
Pycharm是编写Python代码的IDE，跟IDEA、WebStorm等都是jetbrains生成的，虽然各种IDE国内都有破解版的，但是对于Pycharm还是比较友好的的，因为有社区版本，虽然功能不如专业版，但是***free***啊，白嫖不香吗，哈哈哈。  
安装Pycharm部分略，安装完之后需要配置一下IDE使用的Python，选择刚安装的就行，具体安装、配置请自行***baidu***，不明白的也可以留言、发邮件。

5. 配置更改  
安装完Python与git clone项目之后，需要对项目root根目录下的config.yaml进行配置，主要配置内容：  
   - ROBOT：配置机器人的APPKEY、APPSECRET，具体怎么创建、查看机器人在**上面**或者**README.md末尾**有相关链接说明
   - MESSAGE_COL：需要配置所属的行员类别与对应的工资项（消息内容），格式：key: [列1, 列2, 列3..., 列n]
   - MANAGE：关于消息题是否显示图片以及钉钉不发送用户控制列表  
其他配置不建议更改，具体配置相关的说明请自行查阅配置说明章节。

6. 配置模板  
   - 模板文件建议英文命名，必须包含表头，并且表头在模板第一行（表头可中文）
   - 模板文件内容第一列是DingTalk（钉钉）导出的User ID，具体怎么导出员工User ID同样上面有链接，**README.md末尾**也有
   - 模板文件内容第二列定义的是行员类别，是KHDX_HYLB中的LBDH（类别代号）
   - 其他列内容就是PAS绩效系统导出的其他相关展示信息，行员代号、机构名称、工资项1、工资项2、工资项N、合计，需要展示什么内容在MESSAGE_COL进行配置

7. 运行  
完成上述1-5操作之后，在Pycharm中进行启动，打开root目录下的main.py文件，右键 > Run 'main.py'，
也可以使用快捷键：ctrl+shift+R。

> ### 包说明

执行下列***pip***命令进行一键式包安装。
```
pip install -r requirements.txt
```
其中requirements.txt为项目运行所需要的包，已固定版本，重要包简要说明：
- alibabacloud-credentials、 alibabacloud-dingtalk、alibabacloud-endpoint-util、alibabacloud-openapi-util、alibabacloud-tea、alibabacloud-tea-openapi、alibabacloud-tea-util：DingTalk Robot OpenApi服务，ali提供的SDK
- PyYAML：yaml格式配置文件解析
- requests：Http协议请求
- xlrd：Excel的读操作

DingTalk Robot OpenApi SDK离线安装：
- 解压package目录下的dingtalk.zip
- 进入到解压目录
- 打开控制台（Windows：cmd，Macos：item2，Linux：terminal）
- 执行：***python setup.py install***
- 安装完之后，***pip list***查看

***pip***常用命令：  
```
# 安装（最新版）
pip install xxx
# 安装（具体版本）
pip install xxx==1.0
# 批量安装
pip install -r requirements.txt

# 卸载
pip uninstall xxx

# 列表
pip list/freeze
```

> ### 测试

建议注册一个企业单位钉钉，随便先创建一个单位即可，添加一些测试人员。  
***Now, start your test***

## 其他

> ### 学习参考

* MarkDown官网语法：http://markdown.p2hp.com/basic-syntax/
* DingTalk机器人SDK包：https://developers.dingtalk.com/document/resourcedownload/download-server-sdk/title-12y-g4g-zn2?pnamespace=robots
* Pycharm CE下载地址：https://www.jetbrains.com/pycharm/download/#section=windows
* DingTalk Robot创建与权限开通：http://pygo2.top/articles/32206/
* DingTalk User ID获取参考：http://pygo2.top/articles/45420/

> ### chrome插件推荐

* Lifetime Free VPN：VPN（神器）
* JSON Viewer：JSON数据格式化
* 沙拉查词：划词
* Extension Manager：扩展管理器
* Vue.js devtools：VUE

安装插件需要连接VPN，如果没有VPN，推荐大家使用  
fotiaoqiang：https://www.jiayouyashanghai.com/cn/?a=dnxe2  
安装完上述插件之后在卸载

> ### 联系方式

* ***Github:*** https://github.com/GIS90
* ***Email:*** gaoming971366@163.com
* ***Blog:*** http://pygo2.top
* ***WeChat:*** PyGo90


**Enjoy the good everyday！！!**  
**Life is short, I use python.**
