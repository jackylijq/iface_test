#coding=utf-8
import os
import sys,json,copy,random,re,importlib,config
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
from tools import usefulTools,mg_db_manager,utils_logging

#实例化 class
usefulTools_instances = usefulTools.userfulToolsFactory()
mg_db_manager_instances = mg_db_manager.database_operate()

#获取参数化的正则
param_mark_pattern = "%(.*?)s"

class case_handle():
    def test_check(self,type,str):
        ReportSuccessful = ""
        if ReportSuccessful.decode("utf-8")in str:
            return True
        else:
            return False
    #获取原子用例
    # 根据需要测试的用例组装字典表
    def pack_case_request(self, test_plan_list, test_module_list, test_case_list):
        # 如果case列表不为空，则直接根据case列表进行数据获取
        if len(test_case_list) != 0:
            case_list = self.case_data_handle(test_case_list)
            return case_list
        # 如果case列表为空，检查test_module_list 是否为空
        if len(test_module_list) != 0:
            for module_id in range(len(test_module_list)):
                param = [
                    {'field_name': 'module', 'filed_concatenation': '=','field_value': test_module_list[module_id]},
                ]
                case_infor = self.get_table_data_sigle(config.test_case_db, 'zt_case', 'id', param)
                for case_id in range(len(case_infor)):
                    test_case_list.append(case_infor[case_id]['id'])
            case_list = self.case_data_handle(test_case_list)
            return case_list
        # 如果case_list,module_list都为空的情况：
        if len(test_plan_list) != 0:
            for plan_id in range(len(test_plan_list)):
                param = [
                    {'field_name': 'task', 'filed_concatenation': '=', 'field_value': test_plan_list[plan_id]},
                ]
                case_infor = self.get_table_data_sigle(config.test_case_db, 'zt_testrun', 'id', param)
                for case_id in range(len(case_infor)):
                    test_case_list.append(case_infor[case_id]['case'])
            case_list = self.case_data_handle(test_case_list)
            return case_list

    # 处理case数据
    def case_data_handle(self, test_case_list):
        case_list = []
        execute_case_list = []
        compare_keyWord = 'check'
        print(u'处理case数据')
        for case_id in range(len(test_case_list)):
            case_param = [
                {'field_name': 'case', 'filed_concatenation': '=', 'field_value': test_case_list[case_id]},
            ]
            case_infor = self.get_table_data_sigle(config.test_case_db, 'zt_casestep', 'id', case_param)
            case_list.append(case_infor)
        print(len(case_list))
        for case_list_id in range(len(case_list)):
            case_infor = case_list[case_list_id]
            execute_case_infor = {'case_id': case_list[case_list_id][0]['case']}
            case_version = case_infor[0]['version']
            compare_key_list = []
            for i in range(len(case_infor)):
                if case_infor[i]['version'] != case_version:
                    break
                request_key = case_infor[i]['desc']
                request_value = str(case_infor[i]['expect']).replace('&quot;', '"').replace('\r', '').replace('\n','')
                if request_key == 'query_result_check':
                    request_value = self.deal_value_marks(request_key, request_value)
                if request_key == 'header':
                    request_value = str(request_value).replace('\'', '"')
                # 如果有多条结果检查，则需要校验当前key是否已在字典表，在的情况下，加个随机数进去
                execute_case_keys = execute_case_infor.keys()
                if request_key in execute_case_keys:
                    request_key = request_key + '_' + str(random.randint(100, 999))
                # 把需要校验的内容放入到 compare_key_list 中，后续所有需要校验的都从这里进行取值
                if compare_keyWord in request_key:
                    compare_key_list.append(request_key)
                execute_case_infor[request_key] = request_value
            execute_case_infor['compare_key_list'] = compare_key_list
            execute_case_list.append(execute_case_infor)
        return execute_case_list




if __name__ == '__main__':
    test = case_handle()
    # test.db_timestamp_handle('123')
    test_re = re.findall(param_mark_pattern,"%(dtime)sssss%(dtime1)ssss")
    print (test_re)
    # test.create_stringEN_random('测试'.decode('utf-8'))
    test.db_timestamp_handle(1582700632503)




