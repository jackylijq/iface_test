#encoding:utf-8

import sys, importlib,json
from flask import Flask,request
from time import sleep
from base_frame import  standard_api_request
from inward_tackle import etl_compare

importlib.reload(sys)

#实例化class
standard_api_request_instances = standard_api_request.standard_api()
etl_compare_instances = etl_compare.etl_components()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/buildInterface/<string:task_id>',methods=['POST'])
def create_app(task_id):
  if task_id == "b06815c5078b99fa83da57b04bd8c25bd8cfef4b" :
      post_headers =  request.headers
      # message =  request.form
      post_data = json.loads(request.data)
      # message =  request.form['app_name']
      # message =  request.form['version']
      # message =  request.form['hashcode']
      # app_name=request.form['app_name']
      # version = request.form['version']
      # hashcode =request.form['hashcode']
      # #os.environ['app_name']=str(app_name)
      # #os.environ['version']=str(version)
      # #os.environ['hashcode']=str(hashcode)
      # doshell = 'python /home/jenkins/ci_build/auto_build/git_module.py %s %s %s' %(app_name,version,hashcode)
      # status,output=subprocess.check_output(doshell)
      # message =  output
      test_response = {'code': 401, 'message': u'所有参数都为空，无需要执行的用例', 'data': []}
      return test_response
      # return "脚本完毕"

@app.route('/execute',methods=['POST'])
def case_excute():
    '''
       请求地址：http://ip:port/execute
       请求参数：{"test_plan":[1],"test_module":[],"test_case":[],"record_db":"","branch":"dev"} 四个参数都不为空的时候执行用例，执行顺序 依照plan、module、case的方式进行执行
       :param path:
       :param args:
       :return:
       '''
    post_data = json.loads(request.data)
    #定义需要检查的key：
    case_key_list = ['test_plan', 'test_module', 'test_case', 'record_db', 'branch']
    #进行循环检查，是否需要的key都存在，不存在进行异常抛出
    for case_key in case_key_list:
        if case_key in post_data.keys():
            continue
        response_json = {'code': 402, 'message': u'请求参数中缺少字段：%s' % case_key, 'data': []}
        return response_json
    #检查需要执行的用例是否都为空
    if post_data['test_plan'] == post_data['test_module'] == post_data['test_case'] == []:
        response_json = {'code': 401, 'message': u'所有参数plan、module、case都为空，无需要执行的用例', 'data': []}
        return response_json
    #进行用例执行
    test_result = standard_api_request_instances.api_request_entry(post_data)
    return test_result

@app.route('/etlcompare',methods=['POST'])
def etl_compare():
    # test = {"etl2290_id":0,"etl2300_id":0,"check_type":"job"}
    '''
       请求地址：http://ip:port/execute
       请求参数：{"etl2290_id":0,"etl2300_id":0,"check_type":"job"}
       :param path:
       :param args:
       :return:
       '''
    post_data = json.loads(request.data)
    #定义需要检查的key：
    case_key_list = ['etl2290_id', 'etl2300_id', 'check_type']
    #进行循环检查，是否需要的key都存在，不存在进行异常抛出
    for case_key in case_key_list:
        if case_key in post_data.keys():
            continue
        response_json = {'code': 402, 'message': u'请求参数中缺少字段：%s' % case_key, 'data': []}
        return response_json
    #进行用例执行
    test_result = etl_compare_instances.etl_assembly_compare(post_data)
    return test_result


@app.route('/test_thread',methods=['POST'])
def test_thread():
    print('进行thread测试')
    for i in range(10):
        print(u'当前id=%s' % i)
        sleep(5)
    test_response = {'code': 401, 'message': u'所有参数都为空，无需要执行的用例', 'data': []}
    return test_response



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=82,
        debug=True
    )
