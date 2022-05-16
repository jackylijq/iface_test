# -*- coding:utf-8 -*-
"""
ljq 2019-09-16
针对需要鉴权的接口进行鉴权认证
1、不传入token的情况下，查看响应
2、传入的token错误的情况下，查看响应

"""
import unittest,json,random,copy,utils_logging
from test_case.cabinet_client import cabinet_basic_operate
from tools import qy_db_manager,usefulTools
from conf import settings,cabinet_client_constant

#实例化调用的class

basic_operate_instances = cabinet_basic_operate.basic_operate()
qy_db_manager_instances = qy_db_manager.database_operate()
usefulTools_instances = usefulTools.userfulToolsFactory()
iface_list_base = cabinet_client_constant.iface_list_base
iface_param = cabinet_client_constant.iface_param

#定义接口返回数据集
if_response_list = []

class authorization_module(unittest.TestCase):
    # 验证token异常的情况
    def test_token_error(self):
        # 获取接口的返回结果
        print u'进行所有需要鉴权的接口鉴权检查，token错误'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcGVuaWQiOiI3Yjk2OGRmZWFkNTkxMTI4MDU5MWJiZjVjYTZkMTNlYyIsInBob25lIjoiMTgyMTIzNDEyMzQiLCJ1aWQiOiJyOUlQaUNqQUxIRVIiLCJ1c2VyX2lkIjo5MzcyOTAsIndlY2hhdHNfaWQiOjU4MTg4MiwidHlwIjoiYWNjZXNzX3Rva2VuIiwiaWF0IjoxNTY4MDEzOTE0LCJleHAiOjE1NzA2MDU5MTQsImp0aSI6IjR0R1RJOXdqOExNOWZwT0c2dlVBU3AifQ.b9SIHKMAIgTzVt0GnYVfsd8yrZ0Rxo7t87UfZF_UAag'
        pass_number = 0
        failed_number = 0
        message = u'token 解析错误'
        failed_iface_list = []
        for i in range(len(iface_list_base)):
            print u'当前鉴权接口：',iface_list_base[i]['remark'],',url：',iface_list_base[i]['url']
            response_infor_json = basic_operate_instances.basic_iface_request(token,iface_list_base[i],[])
            if response_infor_json['status'] ==401 and response_infor_json['message'] == message:
                pass_number = pass_number + 1
            else:
                failed_number = failed_number + 1
                iface_infor_bak = copy.deepcopy(iface_list_base[i])
                failed_iface_list.append(iface_infor_bak)
        print u'所有失败的接口列表：'
        for i in range(len(failed_iface_list)):
            print str(failed_iface_list[i]).decode('unicode_escape')
        self.assertEqual(failed_number, 0,u'失败数量>0')

    # 验证token为空的情况
    def test_no_token(self):
        # 获取接口的返回结果
        print u'进行所有需要鉴权的接口鉴权检查，当前token为空'
        pass_number = 0
        failed_number = 0
        message = u'token 为空'
        failed_iface_list = []
        for i in range(len(iface_list_base)):
            print u'当前鉴权接口：', iface_list_base[i]['remark'], ',url：', iface_list_base[i]['url']
            response_infor_json = basic_operate_instances.basic_iface_request('test_none', iface_list_base[i], [])
            if response_infor_json['status'] == 401 and response_infor_json['message'] == message:
                pass_number = pass_number + 1
            else:
                failed_number = failed_number + 1
                iface_infor_bak = copy.deepcopy(iface_list_base[i])
                failed_iface_list.append(iface_infor_bak)
        print u'所有失败的接口列表：'
        for i in range(len(failed_iface_list)):
            print str(failed_iface_list[i]).decode('unicode_escape')
        self.assertEqual(failed_number, 0, u'失败数量>0')


