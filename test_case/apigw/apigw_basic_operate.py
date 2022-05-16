#coding=utf-8
import os
import sys,json,random,urllib,time,copy,hashlib,datetime,msgpack,base64,importlib
from tools import switch
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
from conf import settings,cabinet_client_constant,constant,apigw_constant
from  po import  basic_http_request
from tools import qy_db_manager,usefulTools,switch



#参数实例化
basic_http_request_instances = basic_http_request.basic_http_request()
qy_db_manager_instances = qy_db_manager.database_operate()
usefulTools_instances = usefulTools.userfulToolsFactory()

iface_list = apigw_constant.iface_list
iface_param = apigw_constant.iface_param

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
        headers = {}
        # headers = self.get_headers(user_infor)
        request_param ={}
        Basic_response = ''
        for i in range(len(args)):
            request_param[params[i]] = args[i]
        request_url = settings.cabinet_client_url + iface_infor['url']
        #进行判断是什么类型的请求,进行数据请求：
        time_compare = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
        message =  u'请求时间：',time_compare,u'接口方法类型：',iface_infor['method']
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
            message =  u'3次接口请求，网络请求异常，返回为0，直接返回为0'
            return 0
        message =  Basic_response.text
        Basic_response_json = json.loads(Basic_response.text)
        return Basic_response_json



if __name__ == '__main__':
    basic_operate_instances = basic_operate()
    # basic_operate_instances.basic_iface_request('',iface_list.totalsec,iface_param.totalsec,'2019-06-01','2020-06-05',2,1,'dtime',-1)
    test_dict = {'taskid':'%(taskid)s','test_id':123,'taskid_new':'%(taskid)s','same':{'taskid':'%(abc)s'}}
    test_new = {"db_type": "MongoDB", "db_name": "gwconf", "query_condition": "db.gw_service.find({'taskid':'%(taskid)s'})", "field_check": {"taskid": "%{taskid}s", "actiontype": 2, "srvcn": "\u670d\u52a11", "deptid": 1, "domainid": 1, "srvkeywd": "xxx", "priority": 5, "sertype": 0, "srvclass": "xxx", "srvtag": "\u6807\u7b7e1,\u6807\u7b7e3", "appsysid": 1, "oid": "/dir", "dataupdate": 1, "validbefore": 111, "sharetype": 1, "sharecond": "xxx", "opentype": 1, "srvdes": "xxx", "applyannex": 1, "ifcors": 1, "allow_origins": "*", "allow_origin_regex": "xxx", "allow_methods": "get,post", "allow_headers": "xxx", "allow_credentials": "xxx", "exposed_headers": "xxx", "max_age": 1, "srvhost": "192.168.0.1,192.168.0.2", "weight": 1, "srvtimeout": 1000, "srvreadtimeout": 1000, "srvrlkey": "xxx", "spid": 4, "statustimetype": 1, "statustime": "2019-12-11 10:56:50", "offtype": 1, "revokeremark": "xxx", "oplist": [{"opid": "adduser", "opcn": "\u589e\u52a0\u5de5\u5355\u5c65\u5386", "des": "\u8fd9\u662f\u589e\u52a0\u5de5\u5355\u5c65\u5386\u64cd\u4f5c", "dataformat": 0, "method": "", "protocol": "", "excode": "", "succresult": "", "failresult": "", "sysresult": ""}, {"opid": "adduser", "opcn": "\u7f16\u8f91\u5de5\u5355\u5c65\u5386", "des": "\u8fd9\u662f\u589e\u52a0\u5de5\u5355\u5c65\u5386\u64cd\u4f5c", "dataformat": 0, "method": "", "protocol": "", "excode": "", "succresult": "", "failresult": "", "sysresult": ""}], "oamfilefist": [{"filename": "\u6d4b\u8bd5\u6587\u4ef6", "filepath": "http://localhsot"}], "errcodelist": [{"code": "500", "cn": "\u670d\u52a1\u5668\u9519\u8bef", "en": "server error"}]}}
    param = {'taskid':123}
    param_new = {'spid': 1, 'taskid': 17}
    list_a = ['test1','test3','test5']
    list_b = ['test5','test1']
    print(set(list_b) <= set(list_a))
    test_str = json.dumps(test_dict) %param
    str_new = json.dumps(test_new) %param_new
    print(test_str)



