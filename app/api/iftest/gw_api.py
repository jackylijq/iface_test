"""
    主要用来做用例执行的工作，分为2种执行，一种为直接界面测试，不进行结果写入，一种为写入结果
"""
import json, time
from flask import Blueprint, g
from flask import jsonify
from lin.redprint import Redprint
from flask import request
from model import config_assembly
from inward_tackle import etl_compare
from base_frame import standard_api_request
from tools import usefulTools

gwapi = Blueprint("gwapi", __name__)

#实例化class
standard_api_instances = standard_api_request.standard_api()
usefulTools_instances = usefulTools.userfulToolsFactory()
config_assembly_instances = config_assembly.config_assembly()
etl_compare_instances = etl_compare.etl_components()

# 这与真实的情况是一致的，因为一般的情况下，重要的接口需要被保护，重要的消息才需要推送
@gwapi.route('',defaults={'info': None, 'info2': None, 'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@gwapi.route('/method/get',defaults={'info': 'info', 'info2': 'info2', 'info3': 'info3'}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@gwapi.route('/method/post',defaults={'info': None, 'info2': None, 'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@gwapi.route('/method/get/<info>', defaults={'info2': None, 'info3': None},  methods=['POST', 'GET', 'PUT', 'DELETE'])
@gwapi.route('/method/get/<info>/<info2>', defaults={'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@gwapi.route('/method/get/<info>/<info2>/<info3>', methods=['POST', 'GET', 'PUT', 'DELETE'])
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
    # req_header = request.headers.to_list()
    req_header = list(request.headers.environ.keys())
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
    result = {"data": "success", "ip": ipaddress, "path": req_path, "message": '/' + info, "headers": req_header,"post_data":post_data}
    return result, 200, headers

@gwapi.route('/permission/query', methods=['POST'])
def test_return():
    # 定义默认结果：
    result = {'code': 200, 'message': '数据返回', 'data': {}}
    # 获取接口传入的内容
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        print(reason)
        post_data = ''
    result['data'] = post_data
    result = {'code': 401, 'message': '您当前没有访问该服务的权限，请先进行申请', 'data': {}}
    return result

@gwapi.route('/speed/limit', methods=['POST'])
def test_speed():
    # 定义默认结果：
    result = {'code': 200, 'message': '数据返回', 'data': {}}
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        print(reason)
        post_data = ''
    result['data'] = post_data
    result['data']['account_code'] ='WH0181028120'
    result = {'code': 402, 'message': '当日访问已达上限', 'data': {}}
    return result


@gwapi.route('/etlcompare',methods=['POST'])
def etl_compare():
    # test = {"etl2290_id":0,"etl2300_id":0,"check_type":"job/trans"}
    '''
       请求地址：http://ip:port/execute
       请求参数：{"etl2290_id":0,"etl2300_id":0,"check_type":"job"}
       :param path:
       :param args:
       :return:
       '''
    post_data = json.loads(request.data)
    #定义需要检查的key：
    case_key_list = ['etl2290_id', 'etl2300_id', 'check_type','etl2300','etl2290']
    #进行循环检查，是否需要的key都存在，不存在进行异常抛出
    for case_key in case_key_list:
        if case_key in post_data.keys():
            continue
        response_json = {'code': 402, 'message': u'请求参数中缺少字段：%s' % case_key, 'data': []}
        return response_json
    # 先调用数据库替换程序
    if post_data['etl2290'] != '':
        config_assembly_instances.match_config_infor(post_data['etl2290'],'etl2290')
    if post_data['etl2300'] != '':
        config_assembly_instances.match_config_infor(post_data['etl2300'],'etl2300')
    #进行用例执行
    test_result = etl_compare_instances.etl_assembly_compare(post_data)
    return test_result

@gwapi.route('/autodeploy/config/add',methods=['POST'])
def autodeploy_config_add():
    post_data = json.loads(request.data)
    form_data = request.form
    print(post_data)
    return post_data
