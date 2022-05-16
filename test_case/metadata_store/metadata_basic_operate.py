#coding=utf-8
import os
import sys,json,random,urllib,time,copy,hashlib,datetime,msgpack,base64
from tools import switch
reload(sys)
# sys.setdefaultencoding("utf-8")
from conf import settings,cabinet_client_constant,constant
from  po import  basic_http_request
from tools import qy_db_manager,usefulTools,switch



#参数实例化
basic_http_request_instances = basic_http_request.basic_http_request()
qy_db_manager_instances = qy_db_manager.database_operate()
usefulTools_instances = usefulTools.userfulToolsFactory()

iface_list = cabinet_client_constant.iface_list
iface_param = cabinet_client_constant.iface_param
user_infor = cabinet_client_constant.common_parameter.user_list[settings.cabinet_client_user_id]
web_user_infor = constant.common_parameter.web_user_list[settings.web_user_id]

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
    def basic_iface_request(self,user_infor,iface_infor,params,*args):
        if user_infor == '':
            user_infor = settings.cabinet_client_user_id
        if user_infor == 'test_none':
            user_infor = ''
        headers = self.get_headers(user_infor)
        request_param ={}
        Basic_response = ''
        for i in range(len(args)):
            request_param[params[i]] = args[i]
        request_url = settings.cabinet_client_url + iface_infor['url']
        #进行判断是什么类型的请求,进行数据请求：
        time_compare = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
        print u'请求时间：',time_compare,u'接口方法类型：',iface_infor['method']
        for method in switch.basic_switch(iface_infor['method']):
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
        # Basic_response = basic_http_request_instances.basic_get_request(request_url, request_param, headers)
        if Basic_response == 0:
            print u'3次接口请求，网络请求异常，返回为0，直接返回为0'
            return 0
        print Basic_response.text
        Basic_response_json = json.loads(Basic_response.text)
        return Basic_response_json

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
        print request_param_packb
        print len(request_param_packb)
        print len(json.dumps(request_param))
        request_param_unpackb = msgpack.unpackb(request_param_packb)
        print request_param_unpackb
        request_param_2bin = self.encode(json.dumps(request_param))
        print request_param_2bin
        print len(request_param_2bin)
        request_param_normal = self.decode(request_param_2bin)
        print request_param_normal

        test = 'hello world'
        print bytes(request_param_2bin)

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
        print var
        print type(var)
        var_paccked = msgpack.packb(var)
        test_param_packed = msgpack.packb(test_param)
        print len(test_packed)
        test_unpacked = msgpack.unpackb(test_packed)
        print test_unpacked

        request_url = 'http://192.168.64.142:8086/execute'
        basic_response = basic_http_request_instances.basic_post_request(request_url, var_paccked, {})
        print basic_response.text
        unp = msgpack.unpackb(basic_response.content)
        basic_response_unpackb = msgpack.unpackb(basic_response.text)
        print basic_response_unpackb

    def test_autoParam(self):
        param = {'test':'sql:select * form','cn_name':'cn_random','en_name':'en_random'}
        if param['en_name'] == 'en_random':
            param['en_name'] = 'test_en_name'
        request_param = {'name':'%(en_name)s'}
        request_param = json.dumps(request_param)
        request_param =  request_param %param
        request_param = json.loads(request_param)
        print request_param


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
        print request_param
        #进行接口请求
        basic_response = basic_http_request_instances.basic_post_request(request_url, request_param_packed, {})
        #进行数据解析
        basic_response_unpackb = msgpack.unpackb(basic_response.content)
        print basic_response_unpackb

    #标准api请求入口
    def matadata_api_entry(self, case_infor):
        '''
        1、{"test_plan":[],"test_module":[],"test_case":[],"record_db":""} 根据接口传入的请求字段获取测试用例
        2、根据测试用例中的方法名称，判断是走那种类型的测试：标准API，元数据、运行态等
        3、根据record_db中的值判断是否进行测试结果更新
        :param case_request:
        :return:
        '''
        # 从数据库中获取需要执行的用例
        for interface_name in switch.basic_switch(case_infor['interface_name']):
            if interface_name('matedata_table_create'):
                test_result_infor = self.matedata_table_create()


if __name__ == '__main__':
    basic_operate_instances = basic_operate()
    collist = [{'collist_item':{"coltype":"INT","colname":"age","length":10,"ifprikey":0,"restrict":0}},
               {'collist_item': {"coltype": "INT", "colname": "age", "length": 10, "ifprikey": 0, "restrict": 0}},]
    indexlist = [{'indexlist_item':{"name":"nihao","index":"age|name"}}]
    # basic_operate_instances.db_table_create(collist,indexlist)
    basic_operate_instances.test_2bdecode()



