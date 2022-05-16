# -*- coding:utf-8 -*-

import urllib.parse,urllib.request,time,requests,json
from time import sleep
from tools import utils_logging


class basic_http_request():
    #判断接口地址是否返回200
    def http_code(self,url):
        code = urllib.request.urlopen(url).getcode()

        return code

    # 基本的post/get请求
    def basic_post_request(self, request_url, request_param, headers):
        message =  u'请求地址：%s' %request_url
        message2 = u'请求参数：%s' %request_param
        utils_logging.log(message)
        utils_logging.log(message2)
        # 定义默认的返回内容为0
        Basic_response = 0
        for i in range(5):
            timestr = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
            try:
                # 创建请求的request
                Basic_response = requests.post(request_url, data=request_param, headers=headers,verify=True,timeout=10)
                message = u'当前接口请求用时： '+ str(Basic_response.elapsed.total_seconds()) + ' s'
                utils_logging.log(message)
                sleep(2)
            except Exception as reason:
                sleep(3)
                message =  u'接口请求超时，请求的url=' + request_url + u'当前时间:'+ timestr
                utils_logging.log(message)
                continue
            return Basic_response
        return 0

    # 基本的post/get请求
    def basic_get_request(self, request_url, request_param, headers):
        interface_data = urllib.parse.urlencode(request_param)
        message = u'请求地址：%s' %request_url
        message2 = u'请求参数：%s' %request_param
        utils_logging.log(message)
        utils_logging.log(message2)
        # 拼接请求url
        interface_get_url = request_url + '?' + interface_data
        #定义默认的返回内容为0
        Basic_response = 0
        for i in range(5):
            timestr = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
            try:
                # 创建请求的request
                # Basic_response = requests.get(request_url, data=json.dumps(request_param), headers=headers,verify=True)
                # Basic_response = requests.get(request_url, data=request_param, headers=headers, verify=True)
                Basic_response = requests.get(interface_get_url, headers=headers, verify=True,timeout=10)
                message =  u'当前接口请求用时： ' + str(Basic_response.elapsed.total_seconds()) + ' s'
                utils_logging.log(message)
                sleep(2)
            except Exception as reason:
                sleep(3)
                message = u'接口请求超时，请求的url=' + request_url + u'当前时间:' + timestr
                utils_logging.log(message)
                continue
            return Basic_response
        return 0

    # 基本的put请求
    def basic_put_request(self, request_url, request_param, headers):
        message = u'请求地址：%s' %request_url
        message2 = u'请求参数：%s' %request_param
        utils_logging.log(message)
        utils_logging.log(message2)
        # 定义默认的返回内容为0
        Basic_response = 0
        interface_data = urllib.parse.urlencode(request_param)
        # 拼接请求url
        interface_get_url = request_url + '?' + interface_data
        for i in range(5):
            timestr = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
            try:
                # 创建请求的request
                Basic_response = requests.put(interface_get_url, headers=headers, verify=True,timeout=5)
                message =  u'当前接口请求用时： ' + str(Basic_response.elapsed.total_seconds()) + ' s'
                utils_logging.log(message)
                sleep(2)
            except Exception as reason:
                sleep(3)
                message = u'接口请求超时，请求的url=' + request_url + u',当前时间:' + timestr
                utils_logging.log(message)
                continue
            return Basic_response
        return 0

    # 基本的delete请求
    def basic_delete_request(self, request_url, request_param, headers):
        message = u'请求地址：%s' %request_url
        message2 = u'请求参数：%s' %request_param
        utils_logging.log(message)
        utils_logging.log(message2)
        # 定义默认的返回内容为0
        Basic_response = 0
        # interface_data = urllib.parse.urlencode(request_param)
        # 拼接请求url
        # interface_get_url = request_url + '?' + interface_data
        for i in range(5):
            timestr = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
            try:
                # 创建请求的request
                # Basic_response = requests.delete(interface_get_url, headers=headers, verify=True,timeout=10)
                Basic_response = requests.delete(request_url, data=request_param, headers=headers, verify=True, timeout=5)
                message =  u'当前接口请求用时： ' + str(Basic_response.elapsed.total_seconds()) + ' s'
                utils_logging.log(message)
                sleep(2)
            except Exception as reason:
                sleep(3)
                message =  u'接口请求超时，请求的url=' + request_url + u',当前时间:' + timestr
                utils_logging.log(message)
                continue
            return Basic_response
        return 0