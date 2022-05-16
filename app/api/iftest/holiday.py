"""
    主要用来做用例执行的工作，分为2种执行，一种为直接界面测试，不进行结果写入，一种为写入结果
"""
import json, time
from flask import jsonify
from flask import Blueprint, g
from lin.redprint import Redprint
from flask import request
from model import config_assembly
from inward_tackle import etl_compare
from base_frame import standard_api_request
from tools import usefulTools

holiday = Blueprint("holiday", __name__)

#实例化class
standard_api_instances = standard_api_request.standard_api()
usefulTools_instances = usefulTools.userfulToolsFactory()
config_assembly_instances = config_assembly.config_assembly()
etl_compare_instances = etl_compare.etl_components()

festival_day = ['20210101','20210102','20210103','20210403','20210404','20210405','20210612','20210613','20210614',
                '20210919','20210920','20210921',]
weekend = ['20210109','20210110','20210116','20210117','20210123','20210124','20210130','20210131','20210206','20210221',
           '20210227','20210228','20210306','20210307','20210313','20210314','20210320','20210321','20210327','20210328',
           '20210410','20210411','20210417','20210418','20210424','20210509','20210515','20210516','20210522','20210523',
           '20210529','20210530','20210605','20210606','20210619','20210620','20210626','20210627','20210703','20210704',
           '20210710','20210711','20210717','20210718','20210724','20210725','20210731','20210801','20210807','20210808',
           '20210815','20210815','20210821','20210822','20210828','20210829','20210904','20210905','20210911','20210912',
           '20210925','20211010','20211016','20211017','20211023','20211024','20211030','20211031','20211107','20211107',
           '20211113','20211114','20211120','20211121','20211127','20211128',]
long_leave_spring = ['20210211','20210212','20210213','20210214','20210215','20210216','20210217',]
national_day = ['20211001','20211002','20211003','20211004','20211005','20211006','20211007',]
may_day = ['20210501','20210502','20210503','20210504','20210505',]


# 这与真实的情况是一致的，因为一般的情况下，重要的接口需要被保护，重要的消息才需要推送
@holiday.route('',defaults={'info': None, 'info2': None, 'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@holiday.route('/method/get',defaults={'info': 'info', 'info2': 'info2', 'info3': 'info3'}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@holiday.route('/method/post',defaults={'info': None, 'info2': None, 'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@holiday.route('/method/get/<info>', defaults={'info2': None, 'info3': None},  methods=['POST', 'GET', 'PUT', 'DELETE'])
@holiday.route('/method/get/<info>/<info2>', defaults={'info3': None}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@holiday.route('/method/get/<info>/<info2>/<info3>', methods=['POST', 'GET', 'PUT', 'DELETE'])
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

@holiday.route('/permission/query', methods=['POST'])
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

@holiday.route('/speed/limit', methods=['POST'])
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


@holiday.route('/etlcompare',methods=['POST'])
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

@holiday.route('/autodeploy/config/add',methods=['POST'])
def autodeploy_config_add():
    post_data = json.loads(request.data)
    form_data = request.form
    print(post_data)
    return post_data

@holiday.route('/judge',methods=['POST','GET'])
def holiday_weekend():
    result = {'code': 200, 'message': '获取成功'}
    post_data = {}
    if request.method == 'POST':
        try:
            post_data = json.loads(request.data)
        except Exception as reason:
            result['code'] = 401
            result['message'] = u'传入参数非json格式，无法解析'
            return result
    if request.method == 'GET':
        try:
            datestr = request.args.get('datestr', type=str, default=0)
            post_data['datestr'] = datestr
        except Exception as reason:
            result['code'] = 401
            result['message'] = u'无法解析到传入的参数：datestr'
            return result
    # 必填参数校验
    param_list = ['datestr']
    param_check_result = usefulTools_instances.check_param_exist(param_list, post_data)
    if len(param_check_result) > 0:
        result['code'] = 401
        result['message'] = u'必填参数：%s 为空' % param_check_result
        return result
    if type(post_data['datestr']) != str or len(post_data['datestr']) != 8:
        result['code'] = 401
        result['message'] = u'参数datestr未传入，或是传入的格式不正确，传入的格式应该为字符串格式：20210101'
        return result
    if post_data['datestr'] in weekend:
        result[post_data['datestr']] = '2'
        result['holidayType'] = 'weekend'
    elif post_data['datestr'] in festival_day:
        result[post_data['datestr']] = '3'
        result['holidayType'] = 'festival_day'
    elif post_data['datestr'] in long_leave_spring:
        result[post_data['datestr']] = '7'
        result['holidayType'] = 'spring'
    elif post_data['datestr'] in national_day:
        result[post_data['datestr']] = '7'
        result['holidayType'] = 'national_day'
    elif post_data['datestr'] in may_day:
        result[post_data['datestr']] = '5'
        result['holidayType'] = 'may_day'
    else:
        result[post_data['datestr']] = '0'
        result['holidayType'] = 'workDay'
    return result
