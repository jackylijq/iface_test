#coding=utf-8
import os
import json,random,urllib,time,copy,hashlib,datetime,sys,importlib,bson
import config
from tools import switch
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
from conf import settings,cabinet_client_constant,constant
from  po import  basic_http_request
from tools import mg_db_manager,usefulTools,switch,db_manager,utils_logging,utils_database
# from model import utils_components
from model import utils
from base_frame import metadata_request
from model import config_assembly

#参数实例化
basic_http_request_instances = basic_http_request.basic_http_request()
db_manager_instances = db_manager.database_operate()
mg_db_manager_instances = mg_db_manager.database_operate()
usefulTools_instances = usefulTools.userfulToolsFactory()
utils_instances = utils.utils_components()
metadata_request_instances = metadata_request.basic_operate()
config_assembly_instances = config_assembly.config_assembly()

basic_headers = {'Content-Type':'application/json','Authorization':''}

class standard_api():
    #获取最基础的header信息,通用获取headers：token、from信息
    def get_headers(self,user_id):
        headers = basic_headers
        # headers['From'] = 'Android'
        # headers['Content-Type'] = 'application/x-www-form-urlencoded'
        if type(user_id) != type(0) and len(user_id) > 10:
            headers['Authorization'] = 'Bearer ' + user_id
            return headers
        if user_id == '':
            return headers
        # headers['From'] = cabinet_client_constant.common_parameter.user_list[int(user_id)]['From']
        headers['Authorization'] = 'Bearer ' + cabinet_client_constant.common_parameter.user_list[int(user_id)]['access_token']
        return headers

    #基础的接口请求服务
    def basic_iface_request(self,request_method,request_url,request_param,headers):
        #进行判断是什么类型的请求,进行数据请求：
        time_compare = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
        Basic_response = 0
        message =  u'请求时间：%s ,接口方法类型：%s' %(time_compare,request_method)
        utils_logging.log(message)
        for method in switch.basic_switch(request_method):
            if method('GET'):
                Basic_response = basic_http_request_instances.basic_get_request(request_url, request_param, headers)
                break
            if method('POST'):
                request_param = json.dumps(request_param)
                Basic_response = basic_http_request_instances.basic_post_request(request_url, request_param, headers)
                break
            if method('PUT'):
                Basic_response = basic_http_request_instances.basic_put_request(request_url, request_param, headers)
            if method('DELETE'):
                request_param = json.dumps(request_param)
                Basic_response = basic_http_request_instances.basic_delete_request(request_url, request_param, headers)
        # Basic_response = basic_http_request_instances.basic_get_request(request_url, request_param, headers)
        if Basic_response == 0:
            message = u'3次接口请求，网络请求异常，返回为0，直接返回为0'
            utils_logging.log(message)
            return 0
        print (Basic_response.text)
        try:
            Basic_response_json = json.loads(Basic_response.text)
            return Basic_response_json
        except Exception as reason:
            return Basic_response.text

    #重新整理测试用例，根据配置进行更新request_url
    def test_case_optimize(self,test_case_list,env_config):
        '''
        主要是重置 request_url,根据url_list_infor列表中的url信息进行更新
        :param test_case_list:
        :param url_list_infor:
        :return:
        '''
        #获取所有url的key 列表
        # url_list_keys = list(url_list_infor.keys())
        for i in range(len(test_case_list)):
            # test_case_infor = test_case_list[i]
            # #循环从url的keys中比对，如果url_key 在request_url中，则进行请求地址叠加
            # for url_key in url_list_keys:
            #     if url_key in test_case_infor['request_url']:
            #         test_case_list[i]['request_url'] = url_list_infor[url_key] + test_case_list[i]['request_url']
            #         break
            if test_case_list[i]['project_mark'] != None:
                test_case_list[i]['request_url'] = env_config['env_host'] +test_case_list[i]['project_mark']+ test_case_list[i]['request_url']
            else:
                test_case_list[i]['request_url'] = env_config['env_host'] + test_case_list[i]['request_url']
        return test_case_list

    #api请求入口
    def api_request_entry(self, case_request):
        '''
        1、根据接口传入的请求字段获取测试用例
        2、根据测试用例中的方法名称，判断是走那种类型的测试：标准API，元数据、运行态等
        3、根据record_db中的值判断是否进行测试结果更新
        :param case_request:{"test_plan":[],"test_module":[],"test_case":[],"record_db":"","branch":""}
        test_plan:测试计划ID，test_module：模块ID，test_case：测试用例ID，record_db：是否进行结果记录，branch：分支版本(test、dev)
        查找case顺序：test_case > test_module > test_plan，任意一个list有值 则直接进行返回
        :return:
        '''
        #定义返回的数据格式
        result_infor = {'code': 200, 'message': 'success', 'result_list': []}
        # 先获取数据库
        # url_list_infor = db_manager_instances.get_url_list(case_request['branch'])
        #获取环境变量
        env_config_list = db_manager_instances.get_env_setting(case_request['branch'])
        #判断环境变量是否为空，为空则返回
        if len(env_config_list) == 0:
            result_infor['code'] = 401
            result_infor['message'] = '环境变量为空'
            return result_infor
        # 从数据库中获取需要执行的用例
        test_case_list = db_manager_instances.pack_case_request(case_request['test_plan'], case_request['test_module'],case_request['test_case'])
        # 判断用例变量是否为空，为空则返回
        if len(test_case_list) == 0:
            result_infor['code'] = 401
            result_infor['message'] = '用例列表为空'
            return result_infor
        #进行请求头重新赋值
        basic_headers['Authorization'] = 'Bearer ' + utils_instances.update_user_token(env_config_list[0]['env_host'])
        #根据test_case_list、url_list 重组测试用例，主要是更新request_url
        test_case_list = self.test_case_optimize(test_case_list,env_config_list[0])
        #循环检查case步骤，判断走什么类型的测试
        for case_id in range(len(test_case_list)):
            test_case_keys = test_case_list[case_id].keys()
            if 'product_name' not in test_case_keys:
                test_result_infor = self.standard_case_excute(test_case_list[case_id],env_config_list)
                result_infor['result_list'].append(test_result_infor)
                continue
            if 'matedata' in test_case_list[case_id]['product_name']:
                test_result_infor = metadata_request_instances.matadata_api_entry(test_case_list[case_id])
                result_infor['result_list'].append(test_result_infor)
                continue
        print (result_infor)
        #调用数据库插入操作，先把结果写入数据库
        self.insert_case_result(result_infor)
        return result_infor

    # api请求入口
    def sigle_case_test(self, test_case_list):
        '''
        单条用例测试
        '''
        # 定义返回的数据格式
        result_infor = {'code': 200, 'message': 'success', 'result_list': []}
        # 获取环境变量
        env_config_list = db_manager_instances.get_env_setting('test')
        # 判断环境变量是否为空，为空则返回
        if len(env_config_list) == 0:
            result_infor['code'] = 401
            result_infor['message'] = '环境变量为空'
            return result_infor
        # 从数据库中获取需要执行的用例
        test_case_list = '(' + ','.join('%s' % id for id in test_case_list) + ')'
        param = [
                {'field_name': 'id', 'filed_concatenation': 'in', 'field_value': test_case_list},
            ]
        case_list = db_manager_instances.get_table_data_sigle(config.test_case_db, 'stand_atom_case_list', 'id', param)
        # 判断用例变量是否为空，为空则返回
        if len(test_case_list) == 0 or len(test_case_list) > 10:
            result_infor['code'] = 401
            result_infor['message'] = '用例列表为空,或是用例数据大于10条'
            return result_infor
        # 进行请求头重新赋值
        basic_headers['Authorization'] = 'Bearer ' + utils_instances.update_user_token(env_config_list[0]['env_host'])
        # 根据test_case_list、url_list 重组测试用例，主要是更新request_url
        case_list = self.test_case_optimize(case_list, env_config_list[0])
        # 循环检查case步骤，判断走什么类型的测试
        for test_case in case_list:
            test_result_infor = self.standard_case_excute(test_case, env_config_list)
            result_infor['result_list'].append(test_result_infor)
            continue
        print(result_infor)
        # 调用数据库更新操作，更新当前用例状态
        self.update_case_status('stand_atom_case_list',result_infor)
        return result_infor

    #更新用例的可执行状态
    def update_case_status(self,table_name,result_infor):
        '''
        从用例结果中获取基础的结果信息，写入到用例列表
        '''
        # 获取接口case执行的结果
        if_case_result_list = result_infor['result_list']
        for case_result in if_case_result_list:
            case_id = int(usefulTools_instances.SubString_handle(case_result['case_id'], '当前测试用例id：', ''))
            # excute_result = '\'' + case_result['test_result'] + '\''
            # excute_result = usefulTools_instances.quoted_string(case_result['test_result'])
            update_field = ['case_status']
            update_value = [case_result['test_result']]
            query_field = ['id']
            query_value = [case_id]
            update_value = usefulTools_instances.quoted_string(update_value)
            db_manager_instances.update_data_db(config.test_case_db,table_name,update_field, update_value, query_field, query_value)



    #把结果插入到数据库中
    def insert_case_result(self,result_infor):
        #先从 fun_case_result 中获取最新的 batch_id
        param = [
                ]
        db_case_result_list = db_manager_instances.get_table_data_sigle(config.zentao['db'], 'fun_case_result', 'id', param,1)
        batch_id = 0 if len(db_case_result_list) == 0 else db_case_result_list[0]['batch_id'] + 1
        #获取接口case执行的结果
        if_case_result_list = result_infor['result_list']
        for case_result in if_case_result_list:
            plan_id = 0
            module_id = 0
            case_id = int(usefulTools_instances.SubString_handle(case_result['case_id'],'当前测试用例id：',''))
            request_url = '\'' + case_result['request_url'] +  '\''
            request_method = '\'' + case_result['request_method'] + '\''
            header = '\'' + json.dumps(case_result['header']) + '\''
            request_param = '\'' + json.dumps(case_result['request_param']) + '\''
            response = '\'' + json.dumps(case_result['response']) + '\''
            excute_result = '\'' + case_result['test_result'] + '\''
            result_message = '\'' + case_result['message'] + '\''
            result_detail = '\'' + json.dumps(case_result['response_check_result']) + '\''
            excute_time = 'NOW()'
            table_name = 'fun_case_result'
            #进行数据库插入操作
            db_manager_instances.insert_data_db(config.zentao['db'],table_name,batch_id,plan_id,module_id,case_id,request_url,request_method,header,
                                                request_param,response,excute_result,result_message,result_detail,excute_time)



    #针对测试结果初始数据进行赋值
    def test_result_init(self,test_result_infor,test_case_infor):
        '''

        :param test_result_infor: {'test_result':'pass','message':'','request_url':'','request_method':'','request_param':'','response':'','response_check_result':{}}
        :param test_case_infor:
        :return:
        '''
        test_result_infor['request_url'] = test_case_infor['request_url']
        test_result_infor['request_method'] = test_case_infor['request_method']
        test_result_infor['request_param'] = test_case_infor['request_param']
        test_result_infor['header'] = test_case_infor['header']
        return test_result_infor

    # 配置使用的数据库
    def update_check_db(self, env_config_list,project_list):
        '''
        把env_config_list 和 project中的数据库配置信息进行合并
        '''
        db_config = {}
        db_config['host'] = env_config_list[0]['db_host'] if project_list[0]['db_host'] ==None else project_list[0]['db_host']
        db_config['port'] = env_config_list[0]['db_port'] if project_list[0]['db_port'] ==None else project_list[0]['db_port']
        db_config['db'] = env_config_list[0]['db_name'] if project_list[0]['db_name'] == None else project_list[0]['db_name']
        db_config['user'] = env_config_list[0]['db_username'] if project_list[0]['db_username'] == None else project_list[0]['db_username']
        db_config['password'] = env_config_list[0]['db_password'] if project_list[0]['db_password'] == None else project_list[0]['db_password']
        db_config['db_type'] = env_config_list[0]['db_type'] if project_list[0]['db_type'] == None else project_list[0]['db_type']
        config_assembly_instances.match_config_infor(db_config,'check_db')
        return db_config

    #标准api请求入口
    def standard_case_excute(self,case_infor,env_config_list):
        '''
        1、定义结果参数，或许会作为全局参数
        2、检查当前用例的json字符串，如果json解析失败，直接返回
        3、配置请求地址（根据当前接口的特殊字段进行配置）、请求参数、进行接口请求
        4、取出需要进行校验的内容，分为四种，不同的校验内容调用不同的方法
        5、结果返回之后，根据返回的内容判断当前用例的结果，pass、failed
        :param case_request:
        :return:
        '''
        #组装请求参数：
        case_id = u'当前测试用例id：%s' %case_infor['id']
        utils_logging.log(case_id)
        test_result_infor = {'test_result':'pass','message':'','case_id':case_id,'request_url':'','request_method':'','request_param':'','response':'','response_check_result':{}}
        #进行用例数据校验，主要是针对json格式进行校验
        test_case_infor = utils_instances.check_jsonData_format(case_infor)
        #如果测试用例中json格式异常，则直接返回，不进行数据请求处理
        if test_case_infor['json_check_result'] == 'false':
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] =  u'json格式校验异常，字段:%s'%test_case_infor['failed_key']
            return test_result_infor

        #进行接口测试结果初始化
        test_result_infor = utils_instances.test_result_init(test_result_infor,test_case_infor)
        #针对参数，尤其是需要赋值的参数进行数据完整性校验
        # test_result_infor = utils_instances.param_intact_check(test_case_infor,test_result_infor)
        # if test_result_infor['test_result'] == 'failed':
        #     return test_result_infor
        # 针对 request_param 参数化进行赋值
        # test_case_infor = utils_instances.request_param_assignment(test_case_infor,['insert_result_check'])
        # 针对赋值完的参数，如果参数中包含db获取失败的情况，则直接返回，不进行数据请求处理
        if test_case_infor['test_result'] == 'failed':
            test_result_infor['test_result'] = test_case_infor['test_result']
            test_result_infor['message'] = test_case_infor['message']
            return test_result_infor
        # 进行接口测试结果 请求数据更新
        test_result_infor = utils_instances.test_result_init(test_result_infor, test_case_infor)
        #组装URL：base_url 为setting中配置的域名/ip + 真实从用例中获取的请求地址
        request_url = test_case_infor['request_url']
        #请求方法：POST\GET\DELETE等
        request_method = test_case_infor['request_method']
        #参数直接从case中获取，需要进行参数的参数化
        request_param = test_case_infor['request_param']
        #请求的header信息，直接从用例获取，后续需要进行参数化，比如token等
        # headers = json.loads(test_case_infor['header'])
        headers = test_case_infor['header']
        headers = dict(basic_headers,**test_case_infor['header'])
        #进行数据准备处理
        if 'prepare_data' in case_infor.keys():
            utils_instances.prepare_db_data(case_infor['prepare_data'],request_param,case_infor)
        #进行接口请求
        Basic_response = self.basic_iface_request(request_method,request_url,request_param,headers)
        test_result_infor['response'] = Basic_response
        # 先对响应结果的格式进行校验：
        test_result_infor = utils_instances.response_layout_check(Basic_response,case_infor['response'],test_result_infor)
        if test_result_infor['test_result'] == 'failed' or int(case_infor['response']['code']) != 200:
            return test_result_infor
        #进行检查库的设置，先获取project信息
        param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': case_infor['project_id']},
        ]
        project_list = db_manager_instances.get_table_data_sigle(config.test_case_db, 'project_list', 'id', param)
        #调用config文件修改
        db_config = self.update_check_db(env_config_list,project_list)
        # 针对 insert_result_check 参数化进行赋值
        # test_case_infor = utils_instances.request_param_assignment(test_case_infor)
        #进行结果校验
        #定义需要检查的内容
        check_detail = {}
        if test_case_infor['result_check'] is None:
            return test_result_infor
        if test_case_infor['result_check']['check_type'] == 'request_param':
            check_detail = request_param
        if test_case_infor['result_check']['check_type'] == 'response':
            check_detail = Basic_response['data']['datasList']
        result_check_data = self.ex_result_check(check_detail, test_case_infor['result_check'],test_result_infor,db_config)
        #获取需要校验的key列表
        compare_key_list = test_case_infor['result_check']
        #循环取出需要校验的内容，进行内容校验，内容校验分为4种类型：query、insert、update、delete
        for key_id in range(len(compare_key_list)):
            #根据key值，从case中获取需要检查的列表
            check_infor = test_case_infor[compare_key_list[key_id]]
            result_check_infor = {}
            result_check_data = {}
            #需要根据不同的类型进行数据获取，插入、查询、更新，对 对应的返回data数据格式不同
            if 'query_result_check' in compare_key_list[key_id]:
                # result_check_data = self.query_result_check(Basic_response, check_infor,case_infor['response'],test_result_infor,compare_key_list[key_id])
                result_check_data = self.ex_result_check(Basic_response, check_infor, case_infor['response'],test_result_infor, compare_key_list[key_id])
            if 'insert_result_check' in compare_key_list[key_id]:
                result_check_data = self.insert_result_check(request_param, Basic_response,check_infor,test_result_infor,compare_key_list[key_id])
            if 'update_result_check' in compare_key_list[key_id]:
                result_check_data = self.update_result_check(Basic_response, check_infor,case_infor['response'],test_result_infor,compare_key_list[key_id])
            if 'delete_result_check' in compare_key_list[key_id]:
                result_check_data = self.delete_result_check(Basic_response, check_infor,case_infor['response'],test_result_infor,compare_key_list[key_id])
            result_check_infor[compare_key_list[key_id]] = result_check_data['response_check_result'][compare_key_list[key_id]]
            test_result_infor['response_check_result'][compare_key_list[key_id]] = result_check_infor[compare_key_list[key_id]]
        #把结果返回到前端
        return test_result_infor

    # 针对响应结果的格式进行校验
    def response_layout_check(self,Basic_response,response_standard,test_result_infor):
        '''
        从接口响应的key中进行比较格式是否相同
        :param Basic_response: 接口响应的内容
        :param response_standard: 测试用例中接口响应的标准格式
        :return:
        '''
        #获取 Basic_response 接口响应的格式
        basic_response_keys = list(Basic_response.keys())
        #获取 response_standard 标准响应的格式
        response_standard_keys = list(response_standard.keys())
        #循环校验 基础结果字段
        for response_key in response_standard_keys:
            if response_key in basic_response_keys:
                continue
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = '接口响应字段：%s在响应内容中未找到' %response_key
            return test_result_infor
        # 循环校验 data中的内容
        basic_response_data_keys = list(Basic_response['data'].keys())
        response_standard_data_keys = list(response_standard['data'].keys())
        # 循环校验 基础结果字段
        for response_data_key in response_standard_data_keys:
            if response_data_key in basic_response_data_keys:
                continue
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = '接口响应字段：%s在响应内容中未找到' %response_data_key
            return test_result_infor
        if 'datasList' not in response_standard_data_keys:
            return test_result_infor
        #获取响应标准字段中 datasList
        response_datasList_keys = list(response_standard['data']['datasList'][0].keys())
        for i in range(len(Basic_response['data']['datasList'])):
            # 获取实际响应内容字段中 datasList
            if_response_datasList_keys = list(Basic_response['data']['datasList'][i].keys())
            #进行 datasList 格式比较
            for response_datasList_key in response_datasList_keys:
                if response_datasList_key in if_response_datasList_keys:
                    continue
                test_result_infor['test_result'] = 'failed'
                test_result_infor['message'] = 'datasList中接口响应字段：%s在响应内容中未找到，当前为返回内容第%s条记录' %(response_datasList_key,str(i+1))
                return test_result_infor
        #进行数据返回
        return test_result_infor

    #插入类型结果校验
    def insert_result_check(self,request_param,Basic_response,check_infor,test_result_infor,check_name):
        '''
        针对插入的结果进行校验，插入的结果分为直接插入、复制插入两种2类型
        :param request_param:
        :param check_infor:
        :param test_result_infor:
        :param check_name:
        :return:
        '''
        #获取check_infor的key列表，根据key中是否包含了copy_result进行分支处理
        check_infor_key_list = list(check_infor.keys())
        if 'copy_result' in check_infor_key_list:
            test_result_infor = self.copy_result_check(request_param,check_infor,test_result_infor,check_name)
            return test_result_infor
        #从check_infor中获取到需要进行比对的key值
        compare_key_list = list(check_infor['field_check'].keys())
        test_result_infor['response_check_result'][check_name] = []
        #从 Basic_response 的data 中提取数据 放入到
        try:
            Basic_response_data_keys = list(Basic_response['data'].keys())
            for response_data_key in Basic_response_data_keys:
                request_param[response_data_key] = Basic_response['data'][response_data_key]
        except Exception as reason:
            utils_logging.log(u'当前返回的data中无数据，不用兼容')
        #重新对 request_param 进行调整，获取需要校验的内容
        request_param_check = utils_instances.request_param_split(request_param,check_infor)
        db_query_result = []
        # 根据不同的数据库类型，进行数据获取
        if check_infor['db_type'] == 'MongoDB':
            db_query_result = mg_db_manager_instances.mg_query_data(check_infor['db_name'],check_infor['query_condition'])
        if len(db_query_result) == 0:
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = u'新增的数据在数据库中未找到'
            return test_result_infor
        datas_diff_infor = self.basic_data_check(compare_key_list,check_infor['field_check'],request_param_check,db_query_result[0])
        #把差异数据回写到测试结果中
        test_result_infor['test_result'] = datas_diff_infor['test_result']
        test_result_infor['response_check_result'][check_name].append(datas_diff_infor)
        test_result_infor['message'] = datas_diff_infor['message']
        return test_result_infor

    # 更新结果校验
    def copy_result_check(self, request_param,check_infor, test_result_infor,check_name):
        '''
        针对复制类型的内容进行校验
        :param Basic_response:
        :param check_infor:
        :param response_standard:
        :param test_result_infor:
        :param check_name:
        :return:
        '''
        test_result_infor['response_check_result'][check_name] = []
        #获取复制前的数据
        query_result_list = utils_instances.get_db_data(check_infor['db_type'],check_infor['db_name'],check_infor['query_condition'])
        #获取复制后的数据
        copy_result_list = utils_instances.get_db_data(check_infor['db_type'],check_infor['db_name'],check_infor['copy_result'])
        #获取不需要比对的key列表
        un_check_list = list(check_infor['field_check'].keys())
        un_check_list.append('_id')
        #如果返回的数据为空，则直接返回失败
        if len(query_result_list) == 0 or len(copy_result_list) == 0:
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = u'复制新增的数据在数据库中未找到'
            return test_result_infor
        #获取数据库中要比较的字段列表
        check_list = list(query_result_list[0].keys())
        #获取复制的请求参数的key信息
        request_param_keys = list(request_param.keys())
        #进行数据比较
        for check_key in check_list:
            datas_diff_infor = {}
            #如果key是在un_check_list 不需要检查的列表中，则继续
            if check_key in un_check_list:
                try:
                    datas_diff_infor['original_' + check_key] = u'原始需要复制的字段信息：%s' % query_result_list[0][check_key]
                    datas_diff_infor['target_' + check_key] = u'数据库中最新一条的记录信息：%s' % copy_result_list[0][check_key]
                    test_result_infor['response_check_result'][check_name].append(datas_diff_infor)
                except Exception as reason:
                    continue
                continue
            #进行数据校验
            if query_result_list[0][check_key] == copy_result_list[0][check_key]:
                continue
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = u'字段值不一样，字段名称：%s,原始值：%s,.........复制之后的值：%s' \
                                           %(check_key,query_result_list[0][check_key],copy_result_list[0][check_key])
            return test_result_infor
        return test_result_infor

    #更新结果校验
    def update_result_check(self,Basic_response,check_infor,response_standard,test_result_infor,check_name):
        '''
        针对更新的内容进行校验
        :param Basic_response:
        :param check_infor:
        :param response_standard:
        :param test_result_infor:
        :param check_name:
        :return:
        '''
        test_result_infor['response_check_result'][check_name] = []
        #获取需要校验的字段：
        update_check_key_list = list(check_infor['field_check'].keys())
        #从数据库进行数据获取
        query_result_list = utils_instances.get_db_data(check_infor['db_type'],check_infor['db_name'],check_infor['query_condition'])
        if len(query_result_list) == 0:
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = u'从数据库中未获取到数据，query_condition=%s'%check_infor['query_condition']
            return test_result_infor
        for update_check_key in update_check_key_list:
            try:
                test_get_key = query_result_list[0][update_check_key]
            except Exception as reason:
                test_result_infor['test_result'] = 'failed'
                test_result_infor['message'] = u'数据库的查询结果中未找到字段：%s' % update_check_key
                return test_result_infor
            datas_diff_infor = {}
            if type(query_result_list[0][update_check_key]) in [int,bson.Int64]:
                check_infor['field_check'][update_check_key] = int(check_infor['field_check'][update_check_key])
            if type(query_result_list[0][update_check_key]) in [list] and type(check_infor['field_check'][update_check_key]) == str:
                check_infor['field_check'][update_check_key] = str(check_infor['field_check'][update_check_key]).split(',')
                if sorted(query_result_list[0][update_check_key]) == sorted(check_infor['field_check'][update_check_key]):
                    continue
            if query_result_list[0][update_check_key] == check_infor['field_check'][update_check_key]:
                continue
            datas_diff_infor['expect_' + update_check_key] = check_infor['field_check'][update_check_key]
            datas_diff_infor['reality_' + update_check_key] = query_result_list[0][update_check_key]
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = u'字段比对失败，比对的字段为：%s'%update_check_key
            test_result_infor['response_check_result'][check_name].append(datas_diff_infor)
            return test_result_infor
        return test_result_infor

    #删除结果校验
    def delete_result_check(self,Basic_response,check_infor,response_standard,test_result_infor,check_name):
        '''
        针对删除的结果进行校验
        :param Basic_response:
        :param check_infor:
        :param response_standard:
        :param test_result_infor:
        :param check_name:
        :return:
        '''
        test_result_infor['response_check_result'][check_name] = []
        datas_diff_infor = {}
        #直接从库中进行数据获取
        query_result_list = utils_instances.get_db_data(check_infor['db_type'],check_infor['db_name'],check_infor['query_condition'])
        if len(query_result_list) == 0:
            return test_result_infor
        test_result_infor['test_result'] = 'failed'
        test_result_infor['message'] = u'删除失败，数据依然存在'
        datas_diff_infor['query_condition'] = str(check_infor['query_condition'])
        test_result_infor['response_check_result'][check_name].append(datas_diff_infor)
        return test_result_infor

    # 查询类型的结果校验：
    def ex_result_check(self, check_detail, check_rules, test_result_infor,db_config):
        '''
        校验字段格式：field_check = {"taskId":"taskid","cnName":"srvcn","enName":"srven"}，左侧为接口响应字段，右侧为数据库查询到的字段
        check_infor = {"check_type":"request_param","check_sql":"select * from ds_phy where ds_id = 123"}
        check_type：request_param/response
        1、先进行check_rules中check_field分析，如果有数据，只针对check_field检查
        2、再判断是请求参数 还是响应数据检查
        :return:
        '''

        # 定义默认的query_result 为空
        db_query_result = []
        #定义数据比较结果
        test_result_infor['result_check_detail'] = {'abnormal_list':[]}
        # 根据不同的数据库类型，进行数据获取
        if db_config['db_type'] =='mysql':
            db_query_result = utils_database.db_query_mysql(check_rules['check_sql'], 'check_db')
        #判断check_field是否为空，不为空只针对check_field检查
        if len(list(check_rules['check_field'].keys())) != 0:
            check_detail = check_rules['check_field']
        #定义需要检查的key
        check_keys = list(check_detail.keys()) if check_rules['check_type'] != 'response' else list(check_detail[0].keys())
        #定义需要比较的key：
        review_keys = list(db_query_result[0].keys())
        #先进行数量比较：
        if check_rules['check_type'] == 'response' and len(check_detail) > len(db_query_result):
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = '接口返回的数量大于数据库查询的数量，接口返回%s,数据库返回%s' %(len(check_detail),len(db_query_result))
            return test_result_infor
        #先进行数组处理，把格式统一处理未数组格式
        check_list = [check_detail] if check_rules['check_type'] != 'response' else check_detail
        #定义数据比较结果
        abnormal_list = []
        #进行数据比对：
        for list_id in range(len(check_list)):
            for check_key in check_keys:
                abnormal_infor = {}
                if check_key not in review_keys:
                    continue
                if check_list[list_id][check_key] == db_query_result[list_id][check_key]:
                    continue
                test_result_infor['test_result'] = 'failed'
                abnormal_infor[check_key + '_if'] = check_list[list_id][check_key]
                abnormal_infor[check_key + '_db'] = db_query_result[list_id][check_key]
                test_result_infor['result_check_detail']['abnormal_list'].append(abnormal_infor)
        return test_result_infor
        # 先进行数量比对,数量不一致，直接返回
        response_check_result = {'check_result': 'pass', 'message': '', 'data': []}
        # 定义数据比对差异列表
        response_check_data_list = []
        # 定义需要比对的数量：
        data_check_num = len(Basic_response['data']['datasList'])
        # 判断 total、pageSize、curPage 是否在返回参数的标准列表中，如果不在，不进行数量校验
        page_list = ['total', 'pageSize', 'curPage']
        response_standard_data_keys = list(response_standard['data'].keys())
        if set(page_list) <= set(response_standard_data_keys):
            if Basic_response['data']['total'] != len(db_query_result):
                test_result_infor['test_result'] = 'failed'
                test_result_infor['message'] = u'接口返回的data数量:%s 与数据库查询到的数量:%s 不一致' % (
                str(Basic_response['data']['total']), len(db_query_result))
            # 设置检查循环数量，根据接口返回的每页数量和总数量进行判断
            data_check_num = Basic_response['data']['pageSize'] if Basic_response['data']['total'] >Basic_response['data']['pageSize'] else Basic_response['data']['total']
            # 根据查询的页数和每页数量来处理db查询到的数据
            for i in range(Basic_response['data']['pageSize'] * (Basic_response['data']['curPage'] - 1)):
                db_query_result.pop(0)
        else:
            if len(Basic_response['data']['datasList']) != data_check_num:
                test_result_infor['test_result'] = 'failed'
                test_result_infor['message'] = u'接口返回的data数量:%s 与数据库查询到的数量:%s 不一致' % (
                str(data_check_num), len(db_query_result))
        # 根据 datasList 是否在 key中进行处理，是否循环检查
        if 'datasList' in response_standard['data'].keys():
            # 获取所有的查询列表
            Basic_response_data_list = Basic_response['data']['datasList']
            # 获取需要比较的字段list
            response_datasList_keys = list(response_standard['data']['datasList'][0].keys())
            test_result_infor['response_check_result'][check_name] = []
            # 循环对数据进行校验：
            for if_data_id in range(data_check_num):
                datas_diff_infor = self.basic_data_check(response_datasList_keys, check_infor['field_check'],
                                                         Basic_response_data_list[if_data_id],
                                                         db_query_result[if_data_id])
                if datas_diff_infor['test_result'] == 'pass':
                    continue
                test_result_infor['test_result'] = datas_diff_infor['test_result']
                test_result_infor['response_check_result'][check_name].append(datas_diff_infor)
            return test_result_infor
        else:
            # 获取需要比对的字段：
            response_datasList_keys = list(response_standard['data'].keys())
            datas_diff_infor = self.basic_data_check(response_datasList_keys, check_infor['field_check'],
                                                     Basic_response['data'], db_query_result[0])
            test_result_infor['test_result'] = datas_diff_infor['test_result']
            test_result_infor['response_check_result'][check_name].append(datas_diff_infor)
            return test_result_infor

    #查询类型的结果校验：
    def query_result_check(self,Basic_response,check_infor,response_standard,test_result_infor,check_name):
        '''
        校验字段格式：field_check = {"taskId":"taskid","cnName":"srvcn","enName":"srven"}，左侧为接口响应字段，右侧为数据库查询到的字段
        1、校验响应结果 与 标准的响应格式 进行比对
        2、循环对每一条的响应结果进行比对
        :return:
        '''

        #定义默认的query_result 为空
        db_query_result = []
        #根据不同的数据库类型，进行数据获取
        if check_infor['db_type'] == 'MongoDB':
            db_query_result = mg_db_manager_instances.mg_query_data(check_infor['db_name'], check_infor['query_condition'])
        # 先进行数量比对,数量不一致，直接返回
        response_check_result = {'check_result': 'pass', 'message': '', 'data': []}
        # 定义数据比对差异列表
        response_check_data_list = []
        #定义需要比对的数量：
        data_check_num = len(Basic_response['data']['datasList'])
        #判断 total、pageSize、curPage 是否在返回参数的标准列表中，如果不在，不进行数量校验
        page_list = ['total','pageSize','curPage']
        response_standard_data_keys = list(response_standard['data'].keys())
        if set(page_list) <= set(response_standard_data_keys):
            if Basic_response['data']['total'] != len(db_query_result):
                test_result_infor['test_result'] = 'failed'
                test_result_infor['message'] = u'接口返回的data数量:%s 与数据库查询到的数量:%s 不一致' % (str(Basic_response['data']['total']), len(db_query_result))
            # 设置检查循环数量，根据接口返回的每页数量和总数量进行判断
            data_check_num = Basic_response['data']['pageSize'] if Basic_response['data']['total'] > Basic_response['data']['pageSize'] else  Basic_response['data']['total']
            #根据查询的页数和每页数量来处理db查询到的数据
            for i in range(Basic_response['data']['pageSize'] * (Basic_response['data']['curPage'] - 1)):
                db_query_result.pop(0)
        else:
            if len(Basic_response['data']['datasList']) != data_check_num:
                test_result_infor['test_result'] = 'failed'
                test_result_infor['message'] = u'接口返回的data数量:%s 与数据库查询到的数量:%s 不一致' % (str(data_check_num), len(db_query_result))
        #根据 datasList 是否在 key中进行处理，是否循环检查
        if 'datasList' in response_standard['data'].keys():
            # 获取所有的查询列表
            Basic_response_data_list = Basic_response['data']['datasList']
            #获取需要比较的字段list
            response_datasList_keys = list(response_standard['data']['datasList'][0].keys())
            test_result_infor['response_check_result'][check_name] = []
            #循环对数据进行校验：
            for if_data_id in range(data_check_num):
                datas_diff_infor = self.basic_data_check(response_datasList_keys,check_infor['field_check'],Basic_response_data_list[if_data_id],db_query_result[if_data_id])
                if datas_diff_infor['test_result'] == 'pass':
                    continue
                test_result_infor['test_result'] = datas_diff_infor['test_result']
                test_result_infor['response_check_result'][check_name].append(datas_diff_infor)
            return test_result_infor
        else:
            #获取需要比对的字段：
            response_datasList_keys = list(response_standard['data'].keys())
            datas_diff_infor = self.basic_data_check(response_datasList_keys, check_infor['field_check'],Basic_response['data'], db_query_result[0])
            test_result_infor['test_result'] = datas_diff_infor['test_result']
            test_result_infor['response_check_result'][check_name].append(datas_diff_infor)
            return test_result_infor


    #基础数据比对，传入需要比对的字段，比对的字段值列表
    def basic_data_check(self,response_datasList_keys,field_check,if_response_data,db_check_data):
        '''
        数据库检查，根据传入需要检查的标准字段、对应差异字段、字段值进行比对
        :param response_datasList_keys: 需要比较的标准字段
        :param field_check: 接口、db字段名差异
        :param if_response_data: 接口返回的数据内容
        :param db_check_data: 数据库查到的内容
        :return:
        '''
        field_check_keys = list(field_check.keys())
        # 定义查询信息，接口返回的数据、数据查询到的数据，不一致的地方
        datas_diff_infor = {'test_result':'pass','message':'','check_list':[]}
        #获取接口响应/请求参数中，所有需要比对的key值
        if_response_data_keys = list(if_response_data.keys())
        #循环对一条数据进行校验
        for response_data_key in response_datasList_keys:
            #先进行校验需要检查的key是否在接口的参数中
            if response_data_key not in if_response_data_keys:
                datas_diff_infor['test_result'] = 'failed'
                datas_diff_infor['message'] = '接口的参数中未找到key：%s' %response_data_key
                return datas_diff_infor
            check_list_infor = {}
            # 获取数据库中的值，为了兼容MongoDB字段不返回的情况，先进行值获取，获取不到直接continue
            db_check_key = response_data_key if response_data_key not in field_check_keys else field_check[response_data_key]
            try:
                db_check_data_value = db_check_data[db_check_key]
            except Exception as reason:
                continue
            # 对数据库查询到的结果进行处理，主要是处理时间轴的问题
            db_check_data_compare = utils_instances.db_timestamp_handle(db_check_data_value)
            #对dtime进行处理，接口返回的内容去掉 -
            if response_data_key == 'dtime':
                if_response_data['dtime'] = str(if_response_data['dtime']).replace('-','')
            #针对数据库为list，请求参数非list情况进行处理
            if type(db_check_data_compare) == list and type(if_response_data[response_data_key]) != list:
                if_response_data[response_data_key] = str(if_response_data[response_data_key]).split(',')
            #如果是list进行重新排序比较
            if type(if_response_data[response_data_key]) == list:
                if sorted(if_response_data[response_data_key]) == sorted(db_check_data[db_check_key]):
                    continue
                else:
                    datas_diff_infor['test_result'] = 'failed'
                    check_list_infor[response_data_key + '_if'] = if_response_data[response_data_key]
                    check_list_infor[db_check_key + '_db'] = db_check_data[db_check_key]
                    datas_diff_infor['check_list'].append(check_list_infor)
                    continue
            #非list数据进行比较
            if if_response_data[response_data_key] == db_check_data_compare:
                continue
            datas_diff_infor['test_result'] = 'failed'
            check_list_infor[response_data_key + '_if'] = if_response_data[response_data_key]
            check_list_infor[db_check_key + '_db'] = db_check_data[db_check_key]
            datas_diff_infor['check_list'].append(check_list_infor)
        return datas_diff_infor





if __name__ == '__main__':
    standard_api_instances = standard_api()
    test = {"test_plan":[1],"test_module":[],"test_case":[1,2,3],"branch":'test'}
    # standard_api_instances.insert_case_result('')
    standard_api_instances.api_request_entry(test)



