#coding=utf-8
import os
import sys,json,random,urllib,time,copy,hashlib,datetime,msgpack,base64
from tools import switch
reload(sys)
# sys.setdefaultencoding("utf-8")
from gmssl import sm3,func
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

    #测试sm3
    def test_sm3(self):
        y = sm3.sm3_hash(func.bytes_to_list(b"abc"))
        print y







if __name__ == '__main__':
    basic_operate_instances = basic_operate()
    basic_operate_instances.test_sm3()



