#coding=utf-8
import os
import sys,json,random,urllib,time,copy,hashlib,datetime,msgpack,base64,importlib,config
from tools import switch
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
from conf import settings,cabinet_client_constant,constant
from  po import  basic_http_request
from tools import db_manager,usefulTools,switch,utils_logging
from model import utils



#参数实例化
basic_http_request_instances = basic_http_request.basic_http_request()
db_manager_instances = db_manager.database_operate()
usefulTools_instances = usefulTools.userfulToolsFactory()

iface_list = cabinet_client_constant.iface_list
iface_param = cabinet_client_constant.iface_param
utils_components_instances = utils.utils_components()

basic_headers = {'Content-Type':'application/json','Authorization':''}

class basic_operate():
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
        # 进行判断是什么类型的请求,进行数据请求：
        time_compare = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
        Basic_response = 0
        message = u'请求时间：%s ,接口方法类型：%s' % (time_compare, request_method)
        utils_logging.log(message)
        for method in switch.basic_switch(request_method):
            if method('GET'):
                Basic_response = basic_http_request_instances.basic_get_request(request_url, request_param, headers)
            if method('POST'):
                request_param = json.dumps(request_param)
                Basic_response = basic_http_request_instances.basic_post_request(request_url, request_param, headers)
            if method('PUT'):
                Basic_response = basic_http_request_instances.basic_put_request(request_url, request_param, headers)
            if method('DELETE'):
                request_param = json.dumps(request_param)
                Basic_response = basic_http_request_instances.basic_delete_request(request_url, request_param, headers)
        if Basic_response == 0:
            print (u'3次接口请求，网络请求异常，返回为0，直接返回为0')
            return 0
        # print (Basic_response.text)
        # Basic_response_json = json.loads(Basic_response.text)
        # return Basic_response_json
        return Basic_response


    def encode(self,msg_str):
        return ' '.join([bin(ord(c)).replace('0b', '') for c in msg_str])

    def decode(self,msg_str):
        return ''.join([chr(i) for i in [int(b, 2) for b in msg_str.split(' ')]])

    def test_mysql(self):
        time_now = int(time.time())
        request_param = {'version':1,'dataType':8,'product':1,'subDataType':22,'timestamp':time_now,'nodeId':11,'clusterid':'11','workNum':'1111','status':1,'outTime':200,'processid':'1111'}
        request_param['dsid'] = 1
        request_param['schema'] = ''
        request_param['table'] = 'ddd'
        request_param['num'] = 3

        request_param_packb = msgpack.packb(request_param)
        print (request_param_packb)
        print (len(request_param_packb))
        print (len(json.dumps(request_param)))
        request_param_unpackb = msgpack.unpackb(request_param_packb)
        print (request_param_unpackb)
        request_param_2bin = self.encode(json.dumps(request_param))
        print (request_param_2bin)
        print (len(request_param_2bin))
        request_param_normal = self.decode(request_param_2bin)
        print (request_param_normal)

        test = 'hello world'
        print (bytes(request_param_2bin))

    def test_2bdecode(self):
        test = {
                  "configHead": {
                    "outTime": 200,
                    "processid": "1111",
                    "status": 1,
                    "workNum": "1111"
                  },
                  "generalContent": {
                    "mapList": [
                      {
                        "dbtype": "23",
                        "driver": "org.postgresql.Driver",
                        "dsid": "3",
                        "passwd": "root",
                        "user": "postgres",
                        "url": "jdbc:postgresql://10.10.64.23:5432/dft"
                      }
                    ]
                  },
                  "pubBase": {
                    "clusterid": "11",
                    "dataType": 8,
                    "nodeId": 11,
                    "product": 1,
                    "subDataType": 17,
                    "timestamp": 1577412630159,
                    "version": 1
                  }
                }
        test_pubBase = (1, 8, 242, 25, 12345678, 13, 7)
        test_configHead = (u'opid123', u'12', 7, 60)
        test_mapList = ({u'optype': u'1', u'para': u'{"collist":[{"coltype":"INT","colname":"id","length":10,"ifprikey":"1","restrict":"0"},{"coltype":"INT","colname":"age","length":10,"ifprikey":0,"restrict":0},{"coltype":"VARCHAR","colname":"name","length":128,"ifprikey":0,"restrict":0}],"indexlist":[{"name":"nihao","index":"age|name"}],"type":0}', u'dbtype': u'18', u'tablename': u'test1', u'dsid': u'1', u'schema': u'sql_test'},)
        test_param = (test_pubBase,test_configHead,test_mapList)
        test_packed = msgpack.packb(test)
        with open('data.txt', 'wb') as f1:
            msgpack.dump(test, f1)
            # rs = msgpack.packb(test)
            # f1.write(rs)
        with open('test.msg', 'rb') as f2:
            var = msgpack.load(f2, use_list=False, encoding='utf-8')
        print (var)
        print (type(var))
        var_paccked = msgpack.packb(var)
        test_param_packed = msgpack.packb(test_param)
        print (len(test_packed))
        test_unpacked = msgpack.unpackb(test_packed)
        print (test_unpacked)

        request_url = 'http://192.168.64.142:8086/execute'
        basic_response = basic_http_request_instances.basic_post_request(request_url, var_paccked, {})
        print (basic_response.text)
        unp = msgpack.unpackb(basic_response.content)
        basic_response_unpackb = msgpack.unpackb(basic_response.text)
        print (basic_response_unpackb)

    def test_autoParam(self):
        param = {'test':'sql:select * form','cn_name':'cn_random','en_name':'en_random'}
        if param['en_name'] == 'en_random':
            param['en_name'] = 'test_en_name'
        request_param = {'name':'%(en_name)s'}
        request_param = json.dumps(request_param)
        request_param =  request_param %param
        request_param = json.loads(request_param)
        print (request_param)


    #元数据表操作，基础方法
    def matedata_table_create(self,collist,indexlist):
        #请求接口信息
        request_url = 'http://192.168.64.142:8086/execute'
        #常量- 数据小类
        subDataType = {'query_schemas':17,'table_operate':25}
        #常量--disd，数据库相关已配置好的数据
        dsid = {'sql_test':1,'TONGTECH':2,'public':3,'TONG':5}
        #配置基础的base
        request_base = (1, 8, 242, subDataType['query_schemas'], 12345678, 13, 7)
        #配置基础的head
        request_head = (u'opid123', u'12', 7, 60)
        # collist 数据库字段相关数据
        request_content_item_collist = {"coltype":"","colname":"","length":0,"ifprikey":0,"restrict":""}
        #indexlist 主键相关的数据
        request_content_item_indexlist = {"name":"nihao","index":"age|name"}
        #collist 、indexlist 定义空列表，用于接收item数据
        request_content_item_collist_list = []
        request_content_item_indexlist_list = []
        for collist_id in range(len(collist)):
            request_content_item_collist_list.append(collist[collist_id]['collist_item'])
        for indexlist_id in range(len(indexlist)):
            request_content_item_indexlist_list.append(indexlist[indexlist_id]['indexlist_item'])
        #配置基础的库表操作规则
        request_content_item_param = {"collist":request_content_item_collist_list,"indexlist":request_content_item_indexlist_list,"type":0}
        #定义库表基础信息
        request_content_item = {'dsid':dsid['sql_test'],'schema':'sql_test','tablename':'test1','optype':1,'param':request_content_item_param}
        #定义库表操作列表
        request_content = (request_content_item,)
        #定义请求接口的原始内容
        request_param = (request_base,request_head,request_content)
        #针对原始内容进行 msgpack打包操作
        request_param_packed = msgpack.packb(request_param)
        print (request_param)
        #进行接口请求
        basic_response = basic_http_request_instances.basic_post_request(request_url, request_param_packed, {})
        #进行数据解析
        basic_response_unpackb = msgpack.unpackb(basic_response.content)
        print (basic_response_unpackb)

    # 元数据表操作，基础方法
    def infrastructure_basic_operate(self,case_infor):
        '''
        1、定义结果参数，或许会作为全局参数
        2、检查当前用例的json字符串，如果json解析失败，直接返回
        3、配置请求地址（根据当前接口的特殊字段进行配置）、请求参数、进行接口请求
        4、取出需要进行校验的内容，分为四种，不同的校验内容调用不同的方法
        5、结果返回之后，根据返回的内容判断当前用例的结果，pass、failed
        collist 新增表--字段信息：[{"coltype": "", "colname": "", "length": 0, "ifprikey": 0, "restrict": ""},]
        indexlist 新增表--主键信息：[{"name": "nihao", "index": "age|name"},]
        addlist 修改表--新增字段信息：[{"coltype": "", "colname": "", "length": 0, "ifprikey": 0, "restrict": ""},]
        droplist 修改表--删除字段信息：[{"colname":""}]
        alterlist 修改表--修改的字段信息：[{"coltype": "", "colname": "", "length": 0, "ifprikey": 0, "restrict": ""},]
        request_base (version、data_type、product、sub_data_type、timestamp、nodeId、clusterid)
        request_head：(workNum、processid、status、outTime)
        :param case_request:
        :return:
        '''
        # 组装请求参数：
        test_result_infor = {'test_result': 'pass', 'message': '', 'request_url': '', 'request_method': '',
                             'request_param': '', 'response': '', 'check_data': []}
        # 进行用例数据校验，主要是针对json格式进行校验
        test_case_infor = utils_components_instances.check_jsonData_format(case_infor)
        # 如果测试用例中json格式异常，则直接返回，不进行数据请求处理
        if test_case_infor['json_check_result'] == 'false':
            test_result_infor['test_result'] = 'failed'
            test_result_infor['message'] = u'json格式校验异常，字段：%s' % test_case_infor['failed_key']
            return test_result_infor
        # 进行接口测试结果初始化
        test_result_infor = utils_components_instances.test_result_init(test_result_infor, test_case_infor)
        # 组装请求参数--组装URL：base_url 为setting中配置的域名/ip + 真实从用例中获取的请求地址
        request_url = test_case_infor['request_url']
        # 请求方法：POST\GET\DELETE等
        request_method = test_case_infor['request_method']
        # 参数直接从case中获取，需要进行参数的参数化
        request_param_init = test_case_infor['request_param']
        # 请求的header信息，直接从用例获取，后续需要进行参数化，比如token等
        headers = test_case_infor['header']

        #定义表结构需要的一些常量
        col_param = {'collist':[],'indexlist':[],'addlist':[],'droplist':[],'alterlist':[]}
        #每次进行表结构创建的时候，给一些默认的列信息，为更新和删除做准备
        col_param['collist'] = [
            {"colname": "col_modify_01", "coltype": "INT", "length": 5, "ifprikey": 0, "restrict": 0},
            {"colname": "col_modify_02", "coltype": "INT", "length": 5, "ifprikey": 0, "restrict": 0},
            {"colname": "col_modify_03", "coltype": "INT", "length": 5, "ifprikey": 0, "restrict": 0},
            {"colname": "col_drop_01", "coltype": "INT", "length": 5, "ifprikey": 0, "restrict": 0},
            {"colname": "col_drop_02", "coltype": "INT", "length": 5, "ifprikey": 0, "restrict": 0},
            {"colname": "col_drop_03", "coltype": "INT", "length": 5, "ifprikey": 0, "restrict": 0},
        ]
        #从数据库中获取当前用例的基础配置对象
        operate_infor = test_case_infor['operate_infor']
        matedata_param = [
            {'field_name': 'db_type_name', 'filed_concatenation': '=', 'field_value': '\''+operate_infor['db_type_name']+'\''},
            {'field_name': 'op_type_name', 'filed_concatenation': '=','field_value': '\'' + operate_infor['op_type_name'] + '\''},
        ]
        matedata_list = db_manager_instances.get_table_data_sigle(config.test_case_db,'matedata_config','id',matedata_param)
        matedata_infor = matedata_list[0]
        #配置元数据基本信息--配置基础的base
        timestamp = usefulTools_instances.get_time_stamp13()
        request_base = (matedata_infor['version'], matedata_infor['data_type'], matedata_infor['product'],
                        matedata_infor['sub_data_type'], timestamp, matedata_infor['nodeId'], matedata_infor['clusterid'])
        # 配置基础的head
        request_head = (matedata_infor['workNum'], matedata_infor['processid'], matedata_infor['status'], matedata_infor['outTime'])

        #循环给col_param 进行赋值，把需要操作的列的数据进行赋值
        col_param_keys = list(col_param.keys())
        test_case_keys = list(test_case_infor.keys())
        for col_keys_id in range(len(col_param_keys)):
            for case_keys_id in range(len(test_case_keys)):
                if col_param_keys[col_keys_id] in test_case_keys[case_keys_id]:
                    col_param[col_param_keys[col_keys_id]].append(test_case_infor[test_case_keys[case_keys_id]])
        print(col_param)
        #optype、tablename、schema、dsid 进行赋值
        optype = matedata_infor['op_type']
        tablename_random = 'add_table_'+str(time.strftime('%Y%m%d', time.localtime(time.time())))+'_'+str(random.randint(101,10001))
        #根据需要修改和删除的数量进行获取表名
        # tablename_list = db_manager_instances.get_table_name(operate_infor['db_type'],matedata_infor['schema'],'add_table_')
        tablename_exist = db_manager_instances.get_modify_drop_table(len(col_param['alterlist']),len(col_param['droplist']),operate_infor['db_type'],matedata_infor['schema'])
        tablename = tablename_random if operate_infor['tablename'] != '' else tablename_exist
        schema = matedata_infor['schema']
        dsid = matedata_infor['dsid']
        #定义 request_param_init 赋值的参数信息
        request_param_value = {'optype': optype, 'tablename': tablename, 'schema': schema,'dsid':dsid,'collist':col_param['collist'],'indexlist':col_param['indexlist'],
                               'addlist': col_param['addlist'],'droplist':col_param['droplist'],'alterlist':col_param['alterlist'],}
        #进行 request_param_init 的重新赋值
        request_param_init = json.dumps(request_param_init) %request_param_value
        #重新进行json格式化，并赋值给 request_param
        request_content = utils_components_instances.request_param_json(request_param_init)

        # 定义请求接口的原始内容
        request_param = (request_base, request_head, request_content)
        test_result_infor['request_param'] = request_param

        # # 测试结果比对
        # response_check_result = self.infrastructure_data_check(test_result_infor,operate_infor, request_content)
        # return response_check_result

        #请求参数赋值给结果数据
        test_result_infor = utils_components_instances.test_result_init(test_result_infor, test_case_infor)
        # 针对原始内容进行 msgpack打包操作
        request_param_packed = msgpack.packb(request_param)
        print (request_param)
        #针对打包的内容进行还原，查看数据
        request_param_unpacked = msgpack.unpackb(request_param_packed)
        print (request_param_unpacked)
        # 进行接口请求
        basic_response = self.basic_iface_request(request_method,request_url,request_param_packed,headers)
        # 进行数据解析
        basic_response_unpackb = msgpack.unpackb(basic_response.content)
        print (basic_response_unpackb)
        #进行数据比对，添加、修改、删除的一次性进行比对
        response_check_result = self.infrastructure_data_check(test_result_infor,operate_infor,request_content)
        return response_check_result


    #表结构操作基础数据比对
    def infrastructure_data_check(self,test_result_infor,operate_infor,request_content):
        print ('test')
        #定义数据对比的结果
        # response_check_result = {'test_result': 'pass', 'message': '','check_data':[]}
        response_check_result = test_result_infor
        #先获取所有的
        request_content_param = request_content['param']
        # 获取param中key list ，进行循环格式化
        request_content_param_keys = list(request_content_param.keys())
        check_failed_num = 0
        for param_key_id in range(len(request_content_param_keys)):
            #定义比对结果
            check_data_infor = {'check_type': request_content_param_keys[param_key_id], 'data_list': {}}
            # check_data_infor['data_list'] = {'collist':[],'indexlist':[],'addlist':[],'alterlist':[],'droplist':[]}
            #获取每个key的value值
            request_content_param_value = request_content_param[request_content_param_keys[param_key_id]]
            #如果当前为索引信息，则调用索引检查
            if request_content_param_keys[param_key_id] == 'indexlist':
                check_data_infor['data_list']['indexlist'] = self.data_check_index(operate_infor,request_content,request_content_param_value)
                check_failed_num = len(check_data_infor['data_list']['indexlist']) + check_failed_num
            # 如果当前为 droplist 信息，则调用drop 检查
            if request_content_param_keys[param_key_id] == 'droplist':
                check_data_infor['data_list']['droplist'] = self.data_check_dropCol(operate_infor,request_content,request_content_param_value)
                check_failed_num = len(check_data_infor['data_list']['droplist']) + check_failed_num
            # 如果当前为 col 操作 信息，则调用 col 检查
            if request_content_param_keys[param_key_id] not in ['indexlist','droplist']:
                check_data_infor['data_list'][request_content_param_keys[param_key_id]] = self.data_check_col(operate_infor, request_content,request_content_param_value)
                check_failed_num = len(check_data_infor['data_list'][request_content_param_keys[param_key_id]]) + check_failed_num
            #把检查价格加入到总的结果列表中
            response_check_result['check_data'].append(check_data_infor)
        #汇总总的结果列表，来判断当前用例是通过还是失败，根据 check_failed_num 的数量进行判断
        if check_failed_num > 0:
            response_check_result['test_result'] = 'failed'
        return response_check_result

    #index 索引校验方法
    def data_check_index(self,operate_infor,request_content,request_content_param_value):
        check_result_list = []
        for index_id in range(len(request_content_param_value)):
            # 从请求参数中获取列信息
            request_index_infor = request_content_param_value[index_id]
            # 定义表差异信息
            index_list_infor = {'db_type_name': operate_infor['db_type_name'], 'schema': request_content['schema'],'tablename': request_content['tablename'], 'index_name': request_index_infor['name'],'message': ''}
            request_index_list = str(request_index_infor['index']).split('|')
            for i in range(len(request_index_list)):
                # 从数据库中获取索引信息
                db_index_infor = db_manager_instances.get_index_infor(operate_infor['db_type'],request_content['schema'],request_content['tablename'],request_index_infor['name'],request_index_list[i])
                if len(db_index_infor) == 0:
                    index_list_infor['message'] = u'索引字段：' + request_index_list[i] + u' 不存在'
                    check_result_list.append(index_list_infor)
                    continue
        return check_result_list

    #表结构：删除 col 校验：
    def data_check_dropCol(self, operate_infor, request_content, request_content_param_value):
        '''
        :param operate_infor:链接的数据库信息
        :param request_content: 操作表的时候的请求信息
        :param request_content_param_value: list，当前需要校验的已删除的列信息[{"colname":""}]
        :return:
        '''
        check_result_list = []
        for param_id in range(len(request_content_param_value)):
            # 从请求参数中获取列信息
            request_col_infor = request_content_param_value[param_id]
            # 定义表差异信息
            col_list_infor = {'db_type_name': operate_infor['db_type_name'], 'schema': request_content['schema'],'tablename': request_content['tablename'], 'colname': request_col_infor['colname'],'message': ''}
            # 根据列名从数据库中进行获取
            db_col_infor = db_manager_instances.get_table_structure(operate_infor['db_type'], request_content['schema'],request_content['tablename'],request_col_infor['colname'])
            if len(db_col_infor) > 0:
                col_list_infor['message'] = u'字段：' + request_col_infor['colname'] + u' 未drop成功'
                check_result_list.append(col_list_infor)
        return check_result_list


    #表结构 新增、修改col 校验
    def data_check_col(self,operate_infor,request_content,request_content_param_value):
        '''
        :param operate_infor: 链接的数据库信息
        :param request_content: 操作表的时候的请求信息
        :param request_content_param_value: list,当前添加、修改的列表信息[{"coltype": "", "colname": "", "length": 0, "ifprikey": 0, "restrict": ""},]
        :return:
        '''
        check_result_list = []
        for param_id in range(len(request_content_param_value)):
            # 从请求参数中获取列信息
            request_col_infor = request_content_param_value[param_id]
            # 定义表差异信息
            col_list_infor = {'db_type_name': operate_infor['db_type_name'], 'schema': request_content['schema'],'tablename': request_content['tablename'], 'colname': request_col_infor['colname'],'message': ''}
            # 根据列名从数据库中进行获取
            db_col_infor = db_manager_instances.get_table_structure(operate_infor['db_type'], request_content['schema'],request_content['tablename'],request_col_infor['colname'])
            if len(db_col_infor) == 0:
                col_list_infor['message'] = u'字段：' + request_col_infor['colname'] + u'不存在，未添加成功'
                check_result_list.append(col_list_infor)
                continue
            # 字段存在的情况下，进行类型、长度、主键的对比
            db_col_length = usefulTools_instances.SubString_handle(db_col_infor[0]['COLUMN_TYPE'], '(', ')')
            if request_col_infor['length'] != db_col_length:
                col_list_infor['message'] = u'字段：' + request_col_infor['colname'] + u'长度不正确,RQ:' + str(request_col_infor['length']) + u',DB:' + str(db_col_length)
                check_result_list.append(col_list_infor)
                continue
            # 字段类型校验
            if request_col_infor['coltype'] != db_col_infor[0]['DATA_TYPE']:
                col_list_infor['message'] = u'字段：' + request_col_infor['colname'] + u'类型不正确,RQ:' + str(request_col_infor['coltype']) + u',DB:' + str(db_col_infor[0]['DATA_TYPE'])
                check_result_list.append(col_list_infor)
                continue
            # 主键校验
            if request_col_infor['ifprikey'] == 1 and db_col_infor[0]['COLUMN_TYPE'] is None:
                col_list_infor['message'] = u'字段：' + request_col_infor['colname'] + u'主键信息不正确,数据库未非主键'
                check_result_list.append(col_list_infor)
                continue
        return check_result_list





    #元数据api请求入口
    def matadata_api_entry(self, case_infor):
        '''
        1、{"test_plan":[],"test_module":[],"test_case":[],"record_db":""} 根据接口传入的请求字段获取测试用例
        2、根据测试用例中的方法名称，判断是走那种类型的测试：标准API，元数据、运行态等
        3、根据record_db中的值判断是否进行测试结果更新
        :param case_request:
        :return:
        '''
        # 从数据库中获取需要执行的用例
        for interface_name in switch.basic_switch(case_infor['product_name']):
            if interface_name('matedata_infrastructure'):
                test_result_infor = self.infrastructure_basic_operate(case_infor)
                return test_result_infor
            if interface_name('matedata_table_create'):
                test_result_infor = self.matedata_table_create()



if __name__ == '__main__':
    basic_operate_instances = basic_operate()
    collist = [{'collist_item':{"colname":"age","coltype":"INT","length":10,"ifprikey":0,"restrict":0}},
               {'collist_item': {"coltype": "INT", "colname": "age", "length": 10, "ifprikey": 0, "restrict": 0}},]
    indexlist = [{'indexlist_item':{"name":"nihao","index":"age|name"}}]
    # basic_operate_instances.db_table_create(collist,indexlist)
    basic_operate_instances.test_2bdecode()




