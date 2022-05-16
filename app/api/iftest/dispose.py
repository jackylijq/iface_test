"""
    主要用来做用例执行的工作，分为2种执行，一种为直接界面测试，不进行结果写入，一种为写入结果
"""
import json,requests,time
from flask import jsonify
from flask import Blueprint, g
# from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
# from app.validators.forms import BookSearchForm, CreateOrUpdateBookForm
from flask import Flask,request

from base_frame import standard_api_request
from tools import usefulTools,db_manager

dispose = Blueprint("dispose", __name__)

#实例化class
standard_api_instances = standard_api_request.standard_api()
usefulTools_instances = usefulTools.userfulToolsFactory()
db_manager_instances = db_manager.database_operate()

# 这与真实的情况是一致的，因为一般的情况下，重要的接口需要被保护，重要的消息才需要推送
@dispose.route('',defaults={'info': None, 'info2': None, 'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@dispose.route('/method/get',defaults={'info': 'info', 'info2': 'info2', 'info3': 'info3'}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@dispose.route('/method/post',defaults={'info': None, 'info2': None, 'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@dispose.route('/method/get/<info>', defaults={'info2': None, 'info3': None},  methods=['POST', 'GET', 'PUT', 'DELETE'])
@dispose.route('/method/get/<info>/<info2>', defaults={'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@dispose.route('/method/get/<info>/<info2>/<info3>', methods=['POST', 'GET', 'PUT', 'DELETE'])
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

#环境变量添加
@dispose.route('/env/add', methods=['POST'])
def add_env():
    # 定义默认结果：
    result = {'code': 200, 'message': '添加环境变量成功', 'data': {}}
    # 从接口获取数据
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    # 必填参数校验
    param_list = ['env_name', 'env_host', 'edit_uid']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    # 根据project需要的内容进行更新
    try:
        insert_id = db_manager_instances.insert_data_byField('lin_cms', 'env_setting', post_data)
        result['data']['id'] = insert_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' % reason
        result['code'] = 401
        return result

#环境变量修改
@dispose.route('/env/modify', methods=['POST'])
def update_env():
    result = {'code': 200, 'message': '更新环境设置信息成功', 'data': {}}
    #从接口获取数据
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    # 必填参数校验
    param_list = ['id']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    id = post_data['id']
    # 定义查询数据,更新数据
    query_field = ['id']
    query_value = [id]
    update_param_dict = db_manager_instances.pack_update_infor(post_data)
    update_field = update_param_dict['update_field']
    update_field.append('update_time')
    update_value = update_param_dict['update_value']
    update_value.append('NOW()')
    update_value = usefulTools_instances.list_transt_str(update_value)
    update_value = usefulTools_instances.quoted_string(update_value)
    try:
        db_manager_instances.update_data_db('lin_cms','env_setting',update_field,update_value,query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'更新环境设置信息失败，原因：%s' %reason
        return result

#获取环境变量列表
@dispose.route('/env/list', methods=['GET'])
def env_list():
    result = {'code': 200, 'message': '获取环境变量列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #从接口获取数据
    # post_data = json.loads(request.data)
    # interface_id = request.args.get('interface_id',type = int,default = 0)
    try:
        param = [
        ]
        data_list = db_manager_instances.get_table_data_sigle('lin_cms','env_setting','id',param)
        result['data']['datasList'] = data_list
        result['data']['total'] = len(data_list)
        return result
    except Exception as reason:
        result['message'] = u'获取环境变量列表失败，原因：%s' %reason
        return result

#设置默认环境变量
@dispose.route('/favorite/add', methods=['POST'])
def add_env_favorite():
    # 定义默认结果：
    result = {'code': 200, 'message': '设置默认成功', 'data': {}}
    # 从接口获取数据
    post_data = json.loads(request.data)
    try:
        # 根据project需要的内容进行更新
        user_id = post_data['user_id']
        env_id = post_data['env_id']
        param = [
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_id},
        ]
        #从数据库中获取数据
        data_list = db_manager_instances.get_table_data_sigle('lin_cms', 'env_favorite', 'id', param)
        if len(data_list) == 0:
            db_manager_instances.interface_data_insert('lin_cms', 'env_favorite', user_id, env_id, 'NOW()')
            return result
        #进行数据更新：
        query_field = ['user_id']
        query_value = [user_id]
        update_field = ['env_id']
        update_value = [env_id]
        db_manager_instances.update_data_db('lin_cms', 'env_favorite', update_field, update_value, query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'设置默认失败，原因：%s' % reason
        return result

@dispose.route('/user/favorite', methods=['GET'])
def get_user_favorite_infor():
    result = {'code': 200, 'message': '获取数据成功', 'data': {}}
    #从接口获取数据
    # post_data = json.loads(request.data)
    try:
        user_id = request.args.get('user_id', type=int, default=0)
        param = [
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_id},
        ]
        data_list = db_manager_instances.get_table_data_sigle('lin_cms','case_list','id',param)
        if len(data_list) == 0:
            result['message'] = '未获取到数据，用户ID：%s'%user_id
            return result
        result['data'] = data_list[0]
        return result
    except Exception as reason:
        result['message'] = u'获取用例详情失败，原因：%s' %reason
        return result
