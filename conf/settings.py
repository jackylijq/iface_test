# -*- coding: utf-8 -*-

""""
Self_Laundering_Procedure_ifURL：测试服务端的主url地址
user_id：用于测试的访问用户ID，根据user_id可以从constant获取用户的基础信息：token、from、user_id、phone等
wechat_micro_user_id：用于测试小程序部分的特殊的用户ID
new_user_id：用于测试新用户功能的ID

这些ID都可以做动态调整
"""

import sys,time,os
from tools import usefulTools
from conf import constant

module = 'dev'

usefulTools_instances = usefulTools.userfulToolsFactory()

#请求地址
base_url = 'http://10.10.64.21:8001'


# 定义系统常用的一些变量值
path_dir = os.path.dirname(__file__)
path_base_dir = os.path.dirname(path_dir)
base_dir = sys.path[0]

cookie_file = usefulTools_instances.update_file_path_deal(path_dir) + '/cookie.txt'
test_case_file = ''

def get_pic_file_path():
    relative_address = usefulTools_instances.creat_dir(path_base_dir + '/Result/')
    pic_file_path = base_dir + '/Result/' + relative_address
    return pic_file_path

class interface_config():
    print (u'interface_config 初始化')
    test_name = 'test_name form settings'
