#coding=utf-8
import os
import sys,json,copy,random,re,importlib,urllib
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
from tools import usefulTools,mg_db_manager,utils_logging
from  po import  basic_http_request
# from base_frame.standard_api_request import basic_headers

#实例化 class
usefulTools_instances = usefulTools.userfulToolsFactory()
mg_db_manager_instances = mg_db_manager.database_operate()
#参数实例化
basic_http_request_instances = basic_http_request.basic_http_request()

#获取参数化的正则
param_mark_pattern = "%(.*?)s"

class utils_components():
    def test_check(self,type,str):
        ReportSuccessful = ""
        if ReportSuccessful.decode("utf-8")in str:
            return True
        else:
            return False

    def db_timestamp_handle(self,db_param):
        '''
        这个方法主要是用来处理数据库中查询到的参数，目前无法判断是否为时间字段，只能根据当前的类型、长度等进行判断
        如果当前参数可以转换为int类型，并且int类型的值大于1000000000000
        :param db_param:
        :return:
        '''
        if type(db_param) == 'str' or type(db_param) == list:
            return db_param
        try:
            db_param_int = int(db_param)
            if db_param_int > 1000000000000:
                db_param_time = usefulTools_instances.strftime_standard(db_param)
                return db_param_time
            else:
                return db_param
        except:
            return db_param

    #针对传入的json串做详细的格式校验：
    def check_jsonData_format(self,check_data):
        '''
        主要是针对测试用例的各个vale进行类型和格式校验，对于json格式的需要转换
        1、先获取所有的key
        2、再根据key获取value，校验value的值
        :param json_data:
        :return:
        '''
        #定义不检查的列表
        uncheck_list = ['product_name','request_url','request_method','compare_key_list','case_id']
        #定义要检查的json格式的字段
        check_list = ['header', 'response', 'request_param','result_check']
        #获取所有的json key值
        json_data_keys = list(check_data.keys())
        #循环获取value，判断value的类型，如果不是dict，则进行转
        for i in range(len(json_data_keys)):
            #如果key不在检查列表，则跳过
            if json_data_keys[i] not in check_list:
                continue
            #如果当前key的值为none，则跳过
            if check_data[json_data_keys[i]] == None:
                continue
            if type(check_data[json_data_keys[i]]) == type({}):
                continue
            else:
                try:
                    if 'query_condition' in check_data[json_data_keys[i]]:
                        # query_condition = ''
                        copy_result = ''
                        check_data[json_data_keys[i]] = str(check_data[json_data_keys[i]]).replace(' ','')
                        #根据是否为check类型，区分query_condition获取方式
                        if 'copy_result' in check_data[json_data_keys[i]]:
                            query_condition = usefulTools_instances.SubString_handle(check_data[json_data_keys[i]],'"query_condition":"','","copy_result"')
                            copy_result = usefulTools_instances.SubString_handle(check_data[json_data_keys[i]],'"copy_result":"','","field_check"')
                        elif 'result_check' in json_data_keys[i]:
                            query_condition = usefulTools_instances.SubString_handle(check_data[json_data_keys[i]],'"query_condition":"','","field_check"')
                        else:
                            query_condition = usefulTools_instances.SubString_handle(check_data[json_data_keys[i]], '"query_condition":"','"}')
                        check_data[json_data_keys[i]] = str(check_data[json_data_keys[i]]).replace(query_condition,'').replace(copy_result,'')
                        check_data[json_data_keys[i]] = json.loads(check_data[json_data_keys[i]])
                        query_condition = query_condition.replace(' ','')
                        check_data[json_data_keys[i]]['query_condition'] = query_condition
                        if copy_result != '':
                            check_data[json_data_keys[i]]['copy_result'] = copy_result
                    else:
                        check_data[json_data_keys[i]] = json.loads(check_data[json_data_keys[i]])
                except Exception as reason:
                    #转换失败的情况下进行异常捕获，设置结果为false
                    check_data['json_check_result'] = 'false'
                    check_data['failed_key'] = json_data_keys[i]
                    return check_data
        check_data['json_check_result'] = 'true'
        check_data['failed_key'] = ''
        check_data['test_result'] = 'pass'
        return check_data

    #把请求的参数进行json格式化
    def request_param_json(self,request):
        '''
        1、先把request_param进行格式化
        2、再把param中的内容先进行序列号，然后再循环进行格式化
        :param request_param:
        :return:
        '''
        request_json = json.loads(request)
        request_json_return = copy.deepcopy(request_json)
        request_param = request_json['param']
        #获取param中key list ，进行循环格式化
        request_param_keys = list(request_param.keys())
        for param_key_id in range(len(request_param_keys)):
            #先把原始列表中的 [] u ' 等字符串替换为需要的值，再根据 }, 转换str 为 list
            request_param_value = str(request_param[request_param_keys[param_key_id]]).replace('[','').replace(']','').replace('u\'','').replace('\'','"').split('},')
            #清空相关列表的值，为赋值进行准备
            request_json_return['param'][request_param_keys[param_key_id]] = []
            for param_id in range(len(request_param_value)):
                #根据列表的内容进行添加 } 处理
                request_param_value_item = request_param_value[param_id]
                if param_id < len(request_param_value) - 1:
                    request_param_value_item = request_param_value_item + '}'
                #赋值给 request_json_return
                request_json_return['param'][request_param_keys[param_key_id]].append(json.loads(request_param_value_item))
        return request_json_return

    #随机生成中文名称
    def create_stringCN_random(self,name_key=''):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)
        val = random.randint(0x4e00, 0x9fbf)
        name = chr(101)
        name = str(name_key) + '测试' + str(random.randint(101,999))
        return name

    # 随机生成英文名称
    def create_stringEN_random(self, name_key=''):
        name = str(name_key) + 'test' + str(random.randint(101, 999))
        return name

    #数据库参数化赋值
    def db_param_assignment(self,db_condition):
        '''
        db_condition 根据 db_type 不同选择不同的处理方法
        :param db_condition:{
                            "db_type":"MongoDB",
                            "db_name":"gwconf",
                            "query_condition":"db.gw_service.find({"status":93,"taskid":1}).sort({"taskid":-1 }).limit(1)"
                        }
        :return:
        '''
        db_result = 0
        query_result = []
        if db_condition['db_type'] == 'MongoDB':
            query_result = mg_db_manager_instances.mg_query_data(db_condition['db_name'],db_condition['query_condition'])
        if db_condition['db_type'] == 'mysql':
            query_result = mg_db_manager_instances.mg_query_data(db_condition['db_name'],db_condition['query_condition'])
        #针对查询的结果进行拆解
        if len(query_result) == 0:
            return query_result
        #针对查询到的字段，如果字段为1个，直接使用字段值进行返回，如果字段为多个，略却_id不要，然后获取第一个
        query_result_keys = query_result[0].keys()
        for result_key in query_result_keys:
            if result_key == '_id':
                continue
            db_result = query_result[0][result_key]
            return db_result

    #检查参数的完整性，主要是检查数据库参数
    def param_intact_check(self,test_case_infor,test_result_infor):
        # 先进行不需要的内容删除
        test_case_infor.pop('json_check_result')
        test_case_infor.pop('failed_key')
        # 定义不检查的列表
        uncheck_list = ['product_name', 'request_url', 'request_method', 'compare_key_list', 'case_id', 'response','header']
        db_key_list = ['db_type', 'db_name', 'query_condition']
        # 获取请求参数所有的key值
        test_case_keys = test_case_infor.keys()
        # 循环检查key是否需要进行参数化
        for param_key in test_case_keys:
            # 如果value为json，则直接返回
            if param_key in uncheck_list:
                continue
            # 循环进行参数的内容正常性检查
            if 'query_condition' in test_case_infor[param_key].keys():
                # 检查value中的内容是否全面，数据库类型的必须包含db_name,db_type,query_condition
                for db_key in db_key_list:
                    if db_key in test_case_infor[param_key].keys():
                        continue
                    test_result_infor['test_result'] = 'failed'
                    test_result_infor['message'] = u'参数数据异常，%s中缺少%s信息' % (param_key, db_key)
                    return test_result_infor
        return test_result_infor


    #请求参数 request_param 进行参数赋值
    def request_param_assignment(self,test_case_infor,unassignment_list=[]):
        # 定义不检查的列表
        uncheck_list = ['product_name', 'request_url', 'request_method', 'compare_key_list', 'case_id','response','header','test_result']
        #不需要进行初始化的keys
        assignment_list = []
        # unassignment_list = unassignment_list if unassignment_list else []
        #获取请求参数所有的key值
        test_case_keys = test_case_infor.keys()
        param_value = {}
        #循环检查key是否需要进行参数化,需要则加入列表
        for param_key in test_case_keys:
            #如果value为json，则直接返回
            if param_key in uncheck_list:
                continue
            #计算 value 中 %**s 的数量
            param_mark_num = len(re.findall(param_mark_pattern,str(test_case_infor[param_key])))
            #如果 request_param_key_value 中 不包含 %***s 则进行返回
            if param_mark_num == 0:
                continue
            assignment_list.append(param_key)
        #把 request_param、prepare_data 加入到不检查列表
        uncheck_list.append('request_param')
        uncheck_list.append('prepare_data')
        param_init_infor = {}
        #进行参数初始化赋值
        for param_key in test_case_keys:
            if param_key in uncheck_list or 'result_check' in param_key:
                continue
            #获取参数是否需要其他参数初始化赋值
            param_init_infor[param_key] = usefulTools_instances.SubString_handle_mutil(str(test_case_infor[param_key]),'%(',')s')

        #获取初始化需要的key列表
        param_init_keys = list(param_init_infor.keys())
        for i in range(100):
            #如果param_init_keys 与 param_value 中key值一致，则退出循环
            if sorted(list(param_value.keys())) == sorted(param_init_keys):
                break
            for param_key in param_init_keys:
                if param_key in param_value.keys():
                    continue
                if set(param_init_infor[param_key]) > set(list(param_value.keys())):
                    continue
                if 'query_condition' in test_case_infor[param_key].keys():
                    test_case_infor[param_key]['query_condition'] = test_case_infor[param_key]['query_condition'] %param_value
                #检查 变量 的value中是否包含 method 的key，不包含，则为数据库查询
                if 'method' not in test_case_infor[param_key].keys():
                    param_value[param_key] = self.db_param_assignment(test_case_infor[param_key])
                    # if param_value[param_key] == [] or param_value[param_key] ==None:
                    #     param_value[param_key] = ''
                    if param_value[param_key] == [] or param_value[param_key] ==None:
                        test_case_infor['test_result'] = 'failed'
                        test_case_infor['message'] = u'请求参数赋值异常，字段：%s，获取到的值为空或是None' %param_key
                        return test_case_infor
                    continue
                if test_case_infor[param_key]['method'] == 'make_strftime':
                    param_value[param_key] = usefulTools_instances.make_strftime(test_case_infor[param_key]['time_format'],test_case_infor[param_key]['days'],'')
                    continue
                if test_case_infor[param_key]['method'] == 'create_stringEN_random':
                    param_value[param_key] = self.create_stringEN_random(test_case_infor[param_key]['key_word'])
                    continue
                if test_case_infor[param_key]['method'] == 'create_stringCN_random':
                    param_value[param_key] = self.create_stringCN_random(test_case_infor[param_key]['key_word'])
                    continue
        #针对 unassignment_list 中的 insert_result_check 是否包含 copy_result 进行判断
        if unassignment_list and 'insert_result_check' in test_case_keys:
            unassignment_list = [] if 'copy_result' in test_case_infor['insert_result_check'].keys() else unassignment_list
        #返回给测试请求
        for case_key in assignment_list:
            if case_key in unassignment_list:
                continue
            test_case_infor[case_key] = json.dumps(test_case_infor[case_key]) %param_value
            test_case_infor[case_key] = json.loads(test_case_infor[case_key])
        test_case_infor['test_result'] = 'pass'
        #对参数进行为空的校验：

        return test_case_infor

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

    #根据传入的参数进行数据准备
    def prepare_db_data(self,prepare_data_infor,request_param,test_case_infor):
        '''
        :param prepare_data_infor: {"db_type":"","db_name":"","table_name":"","field_check":""}
        :param request_param 请求接口的参数信息
        :return:
        '''
        dtime = ''
        if 'dtime' in test_case_infor.keys():
            dtime = usefulTools_instances.make_strftime(test_case_infor['dtime']['time_format'],test_case_infor['dtime']['days'],test_case_infor['dtime']['week'])
        #获取基础数据
        db_name = prepare_data_infor['db_name']
        table_name = prepare_data_infor['table_name']
        field_check = prepare_data_infor['field_check']
        #根据不同的数据库类型，进行数据插入
        if prepare_data_infor['db_type'] == 'MongoDB':
            db_insert_dict = {}
            field_check_keys = list(field_check.keys())
            for field_check_key in field_check_keys:
                if field_check_key == 'dtime':
                    db_insert_dict['dtime'] = dtime.replace('-','')
                    continue
                db_insert_dict[field_check[field_check_key]] = request_param[field_check_key]
            #调用数据库初始化功能
            mg_db_manager_instances.prepare_data(db_name,table_name,db_insert_dict)

    # 针对响应结果的格式进行校验
    def response_layout_check(self,Basic_response,response_standard,test_result_infor):
        '''
        从接口响应的key中进行比较格式是否相同
        :param Basic_response: 接口响应的内容
        :param response_standard: 测试用例中接口响应的标准格式
        :return:
        '''
        # 对请求结果连通性校验
        if Basic_response in [0,'']:
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = u'5次请求接口失败'
            return test_result_infor
        #获取 Basic_response 接口响应的格式
        basic_response_keys = []
        try:
            basic_response_keys = list(Basic_response.keys())
        except Exception as reason:
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = '接口响应内容非json格式，请检查响应内容'
            test_result_infor['response'] = Basic_response
            return test_result_infor
        #针对响应的code进行校验：
        if Basic_response['code'] != response_standard['code']:
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = '接口响应code与用例中标注的code不一致，接口：%s,用例：%s' %(Basic_response['code'],response_standard['code'])
            test_result_infor['response'] = Basic_response
            return test_result_infor
        #如果code不等于200，直接返回
        if int(response_standard['code']) != 200:
            return test_result_infor
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
        basic_response_data_keys = list(Basic_response['data'].keys()) if type(Basic_response['data']) == dict else []
        response_standard_data_keys = list(response_standard['data'].keys()) if type(response_standard['data']) == dict else []
        if len(response_standard_data_keys) == 0:
            return test_result_infor
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
                test_result_infor['message'] = 'datasList中接口响应字段：%s在响应内容中未找到，当前为返回内容第%s条记录' %(response_datasList_key,str(i))
                return test_result_infor
        #进行数据返回
        return test_result_infor

    # 针对request_param进行拆分，拆分成需要的字典表
    def request_param_split(self, request_param, check_infor):
        '''

        :param request_param:
        :param check_infor:
        :return:
        '''
        request_param_check = {}
        # 根据需要校验的参数，把 request_param 进行拆分
        request_param_keys = list(request_param.keys())
        for param_key in request_param_keys:
            # 如果在 param_key 在 field_check 中则直接加入
            if param_key in check_infor['field_check'].keys():
                request_param_check[param_key] = request_param[param_key]
                continue
            if type(request_param[param_key]) == list and len(request_param[param_key]) > 0:
                for i in range(len(request_param[param_key])):
                    if type(request_param[param_key][i]) != dict:
                        continue
                    second_keys_list = list(request_param[param_key][i].keys())
                    for key_name in second_keys_list:
                        if key_name in check_infor['field_check'].keys():
                            request_param_check[param_key] = request_param[param_key]
                            continue
        return request_param_check

    #针对不同的类型进行数据库数据的获取
    def get_db_data(self,db_type,db_name,query_condition):
        '''
        根据不同的 db_type 请求不同的数据库操作的底层方法
        :param db_type:
        :param db_name:
        :param query_condition:
        :return:
        '''
        db_query_result = []
        if db_type == 'MongoDB':
            db_query_result = mg_db_manager_instances.mg_query_data(db_name,query_condition)
        return db_query_result

    #更新用户token：
    def update_user_token(self,env_url,username='admin',password = '123456'):
        '''
        更新用户token，用户传入用户名，密码。根据用户的生成，不传，则使用默认的admin
        lijq/MocHIZBbB%2BdPwVZTXKd3vA%3D%3D
        admin/r2imGoYRb98oZFBwU2ytvQ==
        '''
        password = 'r2imGoYRb98oZFBwU2ytvQ=='
        token_url = '/auth/oauth/token'
        request_param = {'username':username,'password':password,'grant_type':'password','scope':'server'}
        request_param = urllib.parse.urlencode(request_param)
        token_header = {'Authorization':'Basic dGVzdDp0ZXN0'}
        request_url = env_url + token_url + '?' + request_param
        #请求登录接口，获取token
        token_infor = basic_http_request_instances.basic_post_request(request_url, {}, token_header)
        #重新进行赋值
        # basic_headers['Authorization'] = 'Bear ' + token_infor['access_token']
        token_infor = json.loads(token_infor.text)
        return token_infor['access_token']



if __name__ == '__main__':
    test = utils_components()
    # test.db_timestamp_handle('123')
    test_re = re.findall(param_mark_pattern,"%(dtime)sssss%(dtime1)ssss")
    print (test_re)
    # test.create_stringEN_random('测试'.decode('utf-8'))
    test.db_timestamp_handle(1582700632503)




