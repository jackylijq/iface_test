"""
    主要用来做用例执行的工作，分为2种执行，一种为直接界面测试，不进行结果写入，一种为写入结果
"""
import json,requests,time,config
from flask import Blueprint, g
from flask import jsonify
# from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
# from app.validators.forms import BookSearchForm, CreateOrUpdateBookForm
from flask import Flask,request

from base_frame import standard_api_request
from tools import usefulTools,db_manager

interface = Blueprint("interface", __name__)

#实例化class
standard_api_instances = standard_api_request.standard_api()
usefulTools_instances = usefulTools.userfulToolsFactory()
db_manager_instances = db_manager.database_operate()

@interface.route('/projectLine/add', methods=['POST'])
def add_project_line():
    result = {'code': 200, 'message': '添加产品线成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    #根据project需要的内容进行更新
    pline_name = post_data['pline_name']
    pline_desc = post_data['pline_desc']
    edit_uid = post_data['edit_uid']
    member = post_data['member']
    try:
        insert_id = db_manager_instances.interface_data_insert('lin_cms','project_line',pline_name,pline_desc,edit_uid,member,'NOW()')
        result['data']['id'] = insert_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        return result

@interface.route('/projectLine/modify', methods=['POST'])
def update_project_line():
    result = {'code': 200, 'message': '更新产品线成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    #根据project需要的内容进行更新
    try:
        # 根据project需要的内容进行更新
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
        update_id = db_manager_instances.update_data_db('lin_cms','project_line',update_field,update_value,query_field,query_value)
        # result['data']['id'] = update_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        return result

@interface.route('/projectLine/list', methods=['GET'])
def project_line_list():
    result = {'code': 200, 'message': '获取产品线列表成功', 'data': {'curPage':0,'pageSize':0,'total':0,'datasList':[]}}
    try:
        param = []
        data_list = db_manager_instances.get_table_data_sigle('lin_cms','project_line','id',param)
        result['data']['datasList'] = data_list
        result['data']['total'] = len(data_list)
        return result
    except Exception as reason:
        result['message'] = u'获取用例详情失败，原因：%s' %reason
        result['code'] = 401
        return result

@interface.route('/project/add', methods=['POST'])
def add_project():
    result = {'code': 200, 'message': '添加产品成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    #根据project需要的内容进行更新
    project_line_id = post_data['project_line_id']
    pro_name = post_data['pro_name']
    pro_desc = post_data['pro_desc']
    edit_uid = post_data['edit_uid']
    member = post_data['member']
    try:
        insert_id = db_manager_instances.interface_data_insert('lin_cms','project',project_line_id,pro_name,pro_desc,edit_uid,member,'NOW()')
        result['data']['id'] = insert_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        return result

@interface.route('/project/modify', methods=['POST'])
def update_project():
    result = {'code': 200, 'message': '更新产品成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    #根据project需要的内容进行更新
    try:
        # 根据project需要的内容进行更新
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
        db_manager_instances.update_data_db('lin_cms','project',update_field,update_value,query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        return result

@interface.route('/project/list', methods=['POST'])
def project_list():
    result = {'code': 200, 'message': '获取产品列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #获取get参数
    # plineid = request.args.get('plineid',type = int,default = 0)
    plineid = 0
    try:
        post_data = json.loads(request.data)
        plineid = post_data['project_line_id']
    except Exception as reason:
        print(reason)
    param = []
    if plineid > 0:
        param.append({'field_name': 'project_line_id', 'filed_concatenation': '=', 'field_value': plineid})
    try:
        # param = [
        #     {'field_name': 'project_line_id', 'filed_concatenation': '=', 'field_value': plineid},
        # ]
        data_list = db_manager_instances.get_table_data_sigle(config.test_case_db,'project_list','id',param)
        result['data']['datasList'] = data_list
        result['total'] = len(data_list)
        return result
    except Exception as reason:
        result['message'] = u'获取用例详情失败，原因：%s' %reason
        return result

@interface.route('/group/add', methods=['POST'])
def add_group():
    result = {'code': 200, 'message': '添加分组成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    #根据project需要的内容进行更新
    project_id = post_data['project_id']
    group_name = post_data['group_name']
    group_desc = post_data['group_desc']
    edit_uid = post_data['edit_uid']
    member = post_data['member']
    try:
        insert_id = db_manager_instances.interface_data_insert('lin_cms','interface_group',project_id,group_name,group_desc,edit_uid,member,'NOW()')
        result['data']['id'] = insert_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        return result

@interface.route('/group/modify', methods=['POST'])
def update_group():
    result = {'code': 200, 'message': '更新分组成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    #根据project需要的内容进行更新
    try:
        # 根据project需要的内容进行更新
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
        db_manager_instances.update_data_db('lin_cms','interface_group',update_field,update_value,query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'更新失败，原因：%s' %reason
        return result

@interface.route('/group/list', methods=['POST'])
def group_list():
    result = {'code': 200, 'message': '获取分组列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #获取get请求参数
    # pid = request.args.get('pid',type = int,default = 0)
    # 从接口获取数据
    post_data = {}
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    param_list = ['project_id']
    param_check_result = usefulTools_instances.check_param_exist(param_list,post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' %param_check_result
        return result
    try:
        param = [
            {'field_name': 'project_id', 'filed_concatenation': '=', 'field_value': post_data['project_id']},
        ]
        data_list = db_manager_instances.query_date_page(config.test_case_db, 'iface_group', 'id', param)
        result['data']['datasList'] = data_list
        result['total'] = len(data_list)
        return result
    except Exception as reason:
        result['message'] = u'获取分组列表失败，原因：%s' % reason
        result['code'] = 401
        return result

@interface.route('/iface/add', methods=['POST'])
def add_interface():
    result = {'code': 200, 'message': '添加接口信息成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    #根据project需要的内容进行更新
    project_id = post_data['project_id']
    group_id = post_data['group_id']
    method = post_data['method']
    title = post_data['title']
    desc = post_data['desc']
    path = post_data['path']
    req_headers = post_data['req_headers']
    req_params = post_data['req_params']
    req_body_type = 'json'
    req_body = post_data['req_body']
    res_body_type = 'json'
    res_body = post_data['res_body']
    query_path = ''
    edit_uid = post_data['edit_uid']
    req_query = post_data['req_query']
    try:
        insert_id = db_manager_instances.interface_data_insert('lin_cms','interface_list',project_id,group_id,method,title,desc,path,
                                                   req_headers,req_query,req_params,req_body_type,req_body,res_body_type,res_body,query_path,edit_uid,'NOW()')
        result['data'][id] = insert_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        return result

@interface.route('/iface/update/', methods=['POST'])
def update_interface():
    result = {'code': 200, 'message': '更新接口信息成功', 'data': []}
    #从接口获取数据
    post_data = json.loads(request.data)
    #根据project需要的内容进行更新
    iface_id = post_data['id']
    project_id = post_data['project_id']
    group_id = post_data['group_id']
    method = post_data['method']
    title = post_data['title']
    iface_desc = post_data['desc']
    path = post_data['path']
    req_headers = post_data['req_headers']
    req_params = post_data['req_params']
    req_body_type = 'json'
    req_body = post_data['req_body']
    res_body_type = 'json'
    res_body = post_data['res_body']
    query_path = ''
    edit_uid = post_data['edit_uid']
    req_query = post_data['req_query']
    # 定义查询数据,更新数据
    query_field = ['id']
    query_value = [iface_id]
    update_field = ['project_id', 'group_id', 'method', 'title', 'iface_desc', 'path','req_headers','req_query','req_params',
                    'req_body_type','req_body','res_body_type','res_body','query_path','edit_uid','update_time']
    update_value = [project_id, group_id, method, title, iface_desc, path,req_headers, req_query,
                    req_params, req_body_type,req_body,res_body_type,res_body,query_path,edit_uid,'NOW()']
    update_value = usefulTools_instances.list_transt_str(update_value)
    update_value = usefulTools_instances.quoted_string(update_value)
    try:
        db_manager_instances.update_data_db('lin_cms','interface_list',update_field,update_value,query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'更新接口信息失败，原因：%s' %reason
        return result

@interface.route('/iface/list', methods=['POST'])
def iface_list():
    result = {'code': 200, 'message': '获取分组列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #获取参数：
    # project_id =  request.args.get("project_id",type = int,default = 0)
    # group_id =  request.args.get("group_id",type = int,default = 0)
    # 从接口获取数据
    post_data = {}
    pid = 0
    group_id = 0
    try:
        post_data = json.loads(request.data)
        pid = post_data['project_id']
        group_id = post_data['group_id']
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    try:
        param = []
        if pid != 0:
            param_add = {'field_name': 'project_id', 'filed_concatenation': '=', 'field_value': post_data['project_id']}
            param.append(param_add)
        if group_id != 0:
            param_add = {'field_name': 'group_id', 'filed_concatenation': '=', 'field_value': post_data['group_id']}
            param.append(param_add)
        data_list = db_manager_instances.get_table_data_sigle(config.test_case_db, 'iface_list', 'id', param)
        for i in range(len(data_list)):
            data_list[i].pop('res_body')
            data_list[i].pop('req_body')
            data_list[i].pop('req_headers')
            data_list[i].pop('req_query')
        result['data']['datasList'] = data_list
        result['total'] = len(data_list)
        return result
    except Exception as reason:
        result['message'] = u'获取分组列表失败，原因：%s' % reason
        return result
