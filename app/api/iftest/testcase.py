"""
    主要用来做用例执行的工作，分为2种执行，一种为直接界面测试，不进行结果写入，一种为写入结果
"""
import json,requests,config
from flask import Blueprint, g
from flask import jsonify
# from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
# from app.models.book import Book
# from app.validators.forms import BookSearchForm, CreateOrUpdateBookForm
from flask import Flask,request
from tools import usefulTools,db_manager
from base_frame import standard_api_request

testcase_api = Blueprint("case", __name__)

#实例化class
standard_api_instances = standard_api_request.standard_api()
usefulTools_instances = usefulTools.userfulToolsFactory()
db_manager_instances = db_manager.database_operate()

@testcase_api.route('/execute/sigle', methods=['GET'])
def execute_sigle():
    # 定义默认结果：
    result = {'code': 402, 'message': '更新数据成', 'data': []}
    # 获取接口传入的内容
    post_data = json.loads(request.data)
    # 定义参数检测
    case_key_list = ['test_plan', 'test_module', 'test_case', 'record_db', 'branch']
    args_key_list = post_data.keys()
    for i in range(len(case_key_list)):
        if case_key_list[i] in args_key_list:
            continue
        result['message'] = u'请求参数中缺少字段：%s' % case_key_list[i]
        return result
    test_plan_list = post_data['test_plan']
    test_module_list = post_data['test_module']
    test_case_list = post_data['test_case']
    if len(test_plan_list) == 0 and len(test_module_list) == 0 and len(test_case_list) == 0:
        result['message'] = u'所有参数都为空，无需要执行的用例'
        return result
    test_result = standard_api_instances.api_request_entry(post_data)
    return test_result


@testcase_api.route('/standStom/add', methods=['POST'])
def add_stand_stom_case():
    result = {'code': 200, 'message': '添加用例信息成功', 'data': {}}
    #从接口获取数据
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    #必填参数校验
    param_list = ['iface_id','case_title','case_desc','case_type','header','request_param','response','result_check_sql']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    try:
        insert_id = db_manager_instances.insert_data_byField('case_db','stand_atom_case_list',post_data)
        result['data']['id'] = insert_id
        db_manager_instances.case_iface_update(insert_id,post_data['iface_id'])
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        result['code'] = 401
        return result



@testcase_api.route('/standStom/modify', methods=['POST'])
def update_standStom_case():
    result = {'code': 200, 'message': '更新用例信息成功', 'data': {}}
    # 从接口获取数据
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    # 必填参数校验
    param_list = ['id', 'edit_uid']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    iface_id = post_data['id']
    # 定义查询数据,更新数据
    query_field = ['id']
    query_value = [iface_id]
    update_param_dict = db_manager_instances.pack_update_infor(post_data)
    update_field = update_param_dict['update_field']
    update_field.append('update_time')
    update_value = update_param_dict['update_value']
    update_value.append('NOW()')
    update_value = usefulTools_instances.list_transt_str(update_value)
    update_value = usefulTools_instances.quoted_string(update_value)
    try:
        db_manager_instances.update_data_db('interface_test','stand_atom_case_list',update_field,update_value,query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'更新信息失败，原因：%s' %reason
        result['code'] = 401
        return result

@testcase_api.route('/build/copy', methods=['POST'])
def copy_testcase():
    result = {'code': 200, 'message': '添加用例信息成功', 'data': []}
    #从接口获取数据
    post_data = json.loads(request.data)
    try:
        # 根据project需要的内容进行更新
        case_id = post_data['id']
        copy_infor = {'query_field': 'id', 'query_value': case_id}
        result_db = db_manager_instances.copy_insert('lin_cms','case_list',copy_infor)
        if result_db['result'] == 'pass':
            return result
        else:
            result['message'] = result_db['message']
            return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        return result

@testcase_api.route('/standStom/list', methods=['POST'])
def get_standStom_case_list():
    result = {'code': 200, 'message': '获取用例列表成功', 'data': {'pageSize':0,'curPage':0,'total':0,'datasList':[]}}
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    # 必填参数校验
    param_list = ['curPage','pageSize']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    try:
        param = usefulTools_instances.create_query_condition(post_data)
        data_list = db_manager_instances.query_date_page('lin_cms','stand_atom_case_list','id',param,post_data['curPage'],post_data['pageSize'])
        result['data']['datasList'] = data_list
        result['data']['total'] = db_manager_instances.get_total_size('lin_cms','stand_atom_case_list','id',param)
        result['data']['curPage'] = post_data['curPage']
        result['data']['pageSize'] = post_data['pageSize']
        return result
    except Exception as reason:
        result['message'] = u'获取列表失败，原因：%s' %reason
        result['code'] = 401
        return result

#获取用例详情
@testcase_api.route('/detail', methods=['GET'])
def case_detail():
    result = {'code': 200, 'message': '获取用例详情成功', 'data': {}}
    #从接口获取数据
    # post_data = json.loads(request.data)
    try:
        caseid = request.args.get('caseid', type=int, default=0)
        param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': caseid},
        ]
        data_list = db_manager_instances.get_table_data_sigle('lin_cms','case_list','id',param)
        if len(data_list) == 0:
            result['message'] = '未找到相关用例，用例ID：%s'%caseid
            return result
        result['data'] = data_list[0]
        return result
    except Exception as reason:
        result['message'] = u'获取用例详情失败，原因：%s' %reason
        return result

@testcase_api.route('/param/add', methods=['POST'])
def add_case_param():
    result = {'code': 200, 'message': '添加参数信息成功', 'data': {}}
    # 从接口获取数据
    post_data = json.loads(request.data)
    #必填参数校验
    param_list = ['case_id','param_name','param_desc','param_value','ram_field_name','edit_uid']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    try:
        insert_id = db_manager_instances.insert_data_byField('lin_cms','case_parameter_list',post_data)
        result['data']['id'] = insert_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        result['code'] = 401
        return result

@testcase_api.route('/param/modify', methods=['POST'])
def update_case_param():
    result = {'code': 200, 'message': '更新参数信息成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    # 必填参数校验
    param_list = ['id']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    param_id = post_data['id']
    # 定义查询数据,更新数据
    query_field = ['id']
    query_value = [param_id]
    update_param_dict = db_manager_instances.pack_update_infor(post_data)
    update_field = update_param_dict['update_field']
    update_field.append('update_time')
    update_value = update_param_dict['update_value']
    update_value.append('NOW()')
    update_value = usefulTools_instances.list_transt_str(update_value)
    update_value = usefulTools_instances.quoted_string(update_value)
    try:
        db_manager_instances.update_data_db('lin_cms','case_parameter_list',update_field,update_value,query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'更新接口信息失败，原因：%s' %reason
        print(result['message'])
        return result

@testcase_api.route('/param/list', methods=['GET'])
def param_list():
    result = {'code': 200, 'message': '获取参数列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #从接口获取数据
    post_data = json.loads(request.data)
    # 必填参数校验
    param_list = ['id']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    try:
        interface_id = request.args.get('interface_id', type=int, default=0)
        param = [
            {'field_name': 'interface_id', 'filed_concatenation': '=', 'field_value': interface_id},
        ]
        data_list = db_manager_instances.get_table_data_sigle('lin_cms','case_parameter','id',param)
        result['data']['datasList'] = data_list
        result['data']['total'] = db_manager_instances.get_total_size('lin_cms','case_parameter','id',param)
        return result
    except Exception as reason:
        result['message'] = u'获取参数列表失败，原因：%s' %reason
        return result

@testcase_api.route('/param/detail', methods=['POST'])
def param_datail():
    result = {'code': 200, 'message': '获取参数列表成功', 'data': {}}
    # 从接口获取数据
    post_data = json.loads(request.data)
    # 必填参数校验
    param_list = ['id']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    try:
        param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': post_data['id']},
        ]
        data_list = db_manager_instances.get_table_data_sigle('lin_cms','case_parameter_list','id',param)
        result['data'] = data_list[0] if len(data_list) >0 else []
        return result
    except Exception as reason:
        result['message'] = u'获取参数列表失败，原因：%s' %reason
        result['code'] = 401
        return result

@testcase_api.route('/scene/add', methods=['POST'])
#增加场景用例
def add_scene_case():
    result = {'code': 200, 'message': '添加场景用例成功', 'data': {}}
    # 从接口获取数据
    post_data = json.loads(request.data)
    #必填参数校验
    param_list = ['project_id','caseGroupID','case_title','case_type','case_type_main','case_type_sub','atomCaseInfo','caseTag','edit_uid']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    try:
        insert_id = db_manager_instances.insert_data_byField('lin_cms','scene_case_list',post_data)
        result['data']['id'] = insert_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        result['code'] = 401
        return result

@testcase_api.route('/scene/modify', methods=['POST'])
def update_scene_case():
    result = {'code': 200, 'message': '更新信息成功', 'data': {}}
    #从接口获取数据
    post_data = json.loads(request.data)
    # 必填参数校验
    param_list = ['id']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    param_id = post_data['id']
    # 定义查询数据,更新数据
    query_field = ['id']
    query_value = [param_id]
    update_param_dict = db_manager_instances.pack_update_infor(post_data)
    update_field = update_param_dict['update_field']
    update_field.append('update_time')
    update_value = update_param_dict['update_value']
    update_value.append('NOW()')
    update_value = usefulTools_instances.list_transt_str(update_value)
    update_value = usefulTools_instances.quoted_string(update_value)
    try:
        db_manager_instances.update_data_db('lin_cms','scene_case_list',update_field,update_value,query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'更新信息失败，原因：%s' %reason
        print(result['message'])
        return result

@testcase_api.route('/scene/list', methods=['POST'])
def scene_case_list():
    result = {'code': 200, 'message': '获取列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #从接口获取数据
    post_data = json.loads(request.data)
    # 必填参数校验
    param_list = ['curPage','pageSize']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    try:
        param = usefulTools_instances.create_query_condition(post_data)
        data_list = db_manager_instances.query_date_page('lin_cms','scene_case_list','id',param,post_data['curPage'],post_data['pageSize'])
        result['data']['datasList'] = data_list
        result['data']['total'] = db_manager_instances.get_total_size('lin_cms','scene_case_list','id',param)
        result['data']['curPage'] = post_data['curPage']
        result['data']['pageSize'] = post_data['pageSize']
        return result
    except Exception as reason:
        result['message'] = u'获取列表失败，原因：%s' %reason
        result['code'] = 401
        return result

@testcase_api.route('/scene/result/list', methods=['POST'])
def scene_case_result_list():
    result = {'code': 200, 'message': '获取列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #从接口获取数据
    post_data = {}
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    # 必填参数校验
    param_list = ['curPage','pageSize','batch_id']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    try:
        param = usefulTools_instances.create_query_condition(post_data)
        data_list = db_manager_instances.query_date_page('lin_cms','scene_case_result','id',param,post_data['curPage'],post_data['pageSize'])
        result['data']['datasList'] = data_list
        result['data']['total'] = db_manager_instances.get_total_size('lin_cms','scene_case_result','id',param)
        result['data']['curPage'] = post_data['curPage']
        result['data']['pageSize'] = post_data['pageSize']
        return result
    except Exception as reason:
        result['message'] = u'获取列表失败，原因：%s' %reason
        result['code'] = 401
        return result

@testcase_api.route('/atom/result/list', methods=['POST'])
def atom_case_result_list():
    result = {'code': 200, 'message': '获取列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #从接口获取数据
    post_data = {}
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    # 必填参数校验
    param_list = ['curPage','pageSize','batch_id','scene_id']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    try:
        param = usefulTools_instances.create_query_condition(post_data)
        data_list = db_manager_instances.query_date_page('lin_cms','atom_case_result','id',param,post_data['curPage'],post_data['pageSize'])
        result['data']['datasList'] = data_list
        result['data']['total'] = db_manager_instances.get_total_size('lin_cms','atom_case_result','id',param)
        result['data']['curPage'] = post_data['curPage']
        result['data']['pageSize'] = post_data['pageSize']
        return result
    except Exception as reason:
        result['message'] = u'获取列表失败，原因：%s' %reason
        result['code'] = 401
        return result

@testcase_api.route('/group/add', methods=['POST'])
#增加场景用例
def add_case_group():
    result = {'code': 200, 'message': '添加分组成功', 'data': {}}
    # 从接口获取数据
    post_data = {}
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    #必填参数校验
    param_list = ['project_id','group_type','group_name','edit_uid']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    try:
        insert_id = db_manager_instances.insert_data_byField('lin_cms','case_group',post_data)
        result['data']['id'] = insert_id
        return result
    except Exception as reason:
        result['message'] = u'添加失败，原因：%s' %reason
        result['code'] = 401
        return result

@testcase_api.route('/group/modify', methods=['POST'])
def update_case_group():
    result = {'code': 200, 'message': '更新信息成功', 'data': {}}
    #从接口获取数据
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    # 必填参数校验
    param_list = ['id','group_name']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    #根据project需要的内容进行更新
    param_id = post_data['id']
    # 定义查询数据,更新数据
    query_field = ['id']
    query_value = [param_id]
    update_param_dict = db_manager_instances.pack_update_infor(post_data)
    update_field = update_param_dict['update_field']
    update_field.append('update_time')
    update_value = update_param_dict['update_value']
    update_value.append('NOW()')
    update_value = usefulTools_instances.list_transt_str(update_value)
    update_value = usefulTools_instances.quoted_string(update_value)
    try:
        db_manager_instances.update_data_db('lin_cms','case_group',update_field,update_value,query_field,query_value)
        return result
    except Exception as reason:
        result['message'] = u'更新信息失败，原因：%s' %reason
        result['code'] = 401
        print(result['message'])
        return result

@testcase_api.route('/group/list', methods=['POST'])
def get_group_list():
    result = {'code': 200, 'message': '获取列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #从接口获取数据
    post_data = {}
    try:
        post_data = json.loads(request.data)
    except Exception as reason:
        result['code'] = 401
        result['data'] = {}
        result['message'] = u'传入参数非json格式，无法解析'
        return result
    # 必填参数校验
    param_list = ['project_id']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    try:
        param = usefulTools_instances.create_query_condition(post_data)
        data_list = db_manager_instances.query_date_page('lin_cms','case_group','id',param)
        result['data']['datasList'] = data_list
        result['data']['total'] = len(data_list)
        return result
    except Exception as reason:
        result['message'] = u'获取列表失败，原因：%s' %reason
        result['code'] = 401
        return result


@testcase_api.route('/statistics/list', methods=['GET'])
def statistics_list():
    result = {'code': 200, 'message': '获取参数列表成功', 'data': {'curPage': 0, 'pageSize': 0, 'total': 0, 'datasList': []}}
    #从接口获取数据
    # post_data = json.loads(request.data)
    try:
        project_id = request.args.get('project_id', type=int, default=0)
        group_id = request.args.get('group_id', type=int, default=0)
        page_num = request.args.get('curPage', type=int, default=0)
        page_size = request.args.get('pageSize', type=int, default=0)
        # project_id = post_data['project_id']
        # group_id = post_data['group_id']
        # page_num = post_data['curPage']
        # page_size = post_data['pageSize']
        data_list = db_manager_instances.case_statistics_list('lin_cms',project_id,group_id,page_num,page_size)
        total = db_manager_instances.get_total_size('lin_cms','case_list')
        result['data']['datasList'] = data_list
        result['data']['curPage'] = page_num
        result['data']['pageSize'] = page_size
        result['data']['total'] = total
        return result
    except Exception as reason:
        result['message'] = u'获取参数列表失败，原因：%s' %reason
        return result
