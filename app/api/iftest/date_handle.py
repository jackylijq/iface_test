"""
    主要用来做用例执行的工作，分为2种执行，一种为直接界面测试，不进行结果写入，一种为写入结果
"""
import json,requests,time,config,random
from flask import jsonify
from flask import Blueprint, g
# from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
# from app.validators.forms import BookSearchForm, CreateOrUpdateBookForm
from flask import Flask,request

from base_frame import standard_api_request
from tools import usefulTools,db_manager

datehandle = Blueprint("datehandle", __name__)

#实例化class
standard_api_instances = standard_api_request.standard_api()
usefulTools_instances = usefulTools.userfulToolsFactory()
db_manager_instances = db_manager.database_operate()

# 这与真实的情况是一致的，因为一般的情况下，重要的接口需要被保护，重要的消息才需要推送
@datehandle.route('',defaults={'info': None, 'info2': None, 'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@datehandle.route('/method/get',defaults={'info': 'info', 'info2': 'info2', 'info3': 'info3'}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@datehandle.route('/method/post',defaults={'info': None, 'info2': None, 'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@datehandle.route('/method/get/<info>', defaults={'info2': None, 'info3': None},  methods=['POST', 'GET', 'PUT', 'DELETE'])
@datehandle.route('/method/get/<info>/<info2>', defaults={'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@datehandle.route('/method/get/<info>/<info2>/<info3>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def test_echo(info, info2, info3):
    '''
    测试输出
        ---
        parameters:
          - name: info
            in: body
            type: string
            description: 路径信息
          - name: info2
            in: body
            type: string
            description: 路径信息
          - name: info ...
            in: body
            type: string
            description: 路径信息 ...
        responses:
          200:
            description: 返回该路径下的信息，响应码，请求头
            examples:
              res: {"data": "success", "ip": "MANAGER", "path": "/test/echo", '...': '...'}
    :param info:
    :param info2:
    :param info3:
    :return:
    '''
    # app.logger.info("info: %s, info2: %s, info3: %s" % (str(info), str(info2), str(info3)))
    print("info: %s, info2: %s, info3: %s" % (str(info), str(info2), str(info3)))
    if info is None:
        info = '<NULL>'
    elif info == 'longwait':
        time.sleep(60)
    if info2 is not None:
        info = info + '/' + info2
    if info3 is not None:
        info = info + '/' + info3
    req_header = request.headers.to_list()
    #定义需要去掉的请求头信息
    drop_header = ['Connection','Upgrade-Insecure-Requests','User-Agent','Sec-Fetch-User','Accept','Sec-Fetch-Site','Sec-Fetch-Mode',
                   'Accept-Encoding','Accept-Language','Cache-Control']
    req_header = usefulTools_instances.drop_list_context(req_header,drop_header)
    req_path = request.path
    # 获取接口传入的内容
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        print(reason)
        post_data = ''
    #获取请求IP
    ipaddress = request.remote_addr
    result = jsonify(
        {"data": "success", "ip": ipaddress, "path": req_path, "message": '/' + info, "headers": req_header,"post_data":post_data})
    headers = {"X-Test-Response-Header-1": '111', "X-Test-Response-Header-2": '222'}
    return result, 200, headers

@datehandle.route('/table/create', methods=['POST'])
def table_create():
    '''
    主要目的是做表的插入操作，随机给数据库生成一批表数据,需要传入的参数为：数据库信息，数量，表字段信息
    {'config_db_name':'mysql8','host':'','db':'','table_name':'','field_list':[{'name':'varchar'}],'record_num':0}
    :return:
    '''
    # 定义默认结果：
    result = {'code': 200, 'message': '添加表结构成功', 'data': []}
    # 获取接口传入的内容
    post_data = json.loads(request.data)
    # 定义参数检测
    case_key_list = ['config_db_name', 'host', 'db', 'table_name', 'record_num','field_list']
    args_key_list = post_data.keys()
    for i in range(len(case_key_list)):
        if case_key_list[i] in args_key_list:
            continue
        result['message'] = u'请求参数中缺少字段：%s' % case_key_list[i]
        return result
    #进行config文件的更新
    for i in range(len(config.db_list)):
        if config.db_list[i]['config_db_name'] == post_data['config_db_name']:
            config.db_list[i][post_data['config_db_name']]['host'] = post_data['host']
            config.db_list[i][post_data['config_db_name']]['db'] = post_data['db']
            break
        if i == len(config.db_list) -1:
            result['message'] = u'根据config_db_name：%s,无法找到相关的配置' %post_data['config_db_name']
            return result
    #进行数据插入请求
    for i in range(post_data['record_num']):
        #获取13位时间轴
        db_manager_instances.create_table_date(post_data)
    return result



