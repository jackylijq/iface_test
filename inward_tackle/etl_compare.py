#coding=utf-8
import os
import sys,json,copy,random,re,importlib,config
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
from tools import usefulTools,mg_db_manager,utils_logging,db_manager

#实例化 class
usefulTools_instances = usefulTools.userfulToolsFactory()
mg_db_manager_instances = mg_db_manager.database_operate()
db_manager_instances = db_manager.database_operate()

etl2290_jobentry_infor = {}
etl2300_jobentry_infor = {}
etl2290_step_infor = {}
etl2300_step_infor = {}

#获取参数化的正则
param_mark_pattern = "%(.*?)s"

class etl_components():

    #进行数据比对
    def etl_assembly_compare(self,post_data):
        '''
        test_result =  {'code': 200, 'message': 'success', 'result_infor':{}}
        :return:
        '''
        etl2290_id = post_data['etl2290_id']
        etl2300_id = post_data['etl2300_id']
        check_type = post_data['check_type']
        # 定义返回的结果
        test_result = {'code': 200, 'message': 'success', 'result_infor': {}}
        if check_type == 'job':
            test_result = self.etl_job_compare(etl2290_id,etl2300_id,test_result)
        if check_type == 'trans':
            test_result = self.etl_trans_compare(etl2290_id,etl2300_id,test_result)
        return test_result

    #定义任务组件对比
    def etl_job_compare(self,etl2290_id,etl2300_id,result_infor):
        '''

        :param etl2290_id:
        :param etl2300_id:
        :return:
        '''
        global etl2290_jobentry_infor,etl2300_jobentry_infor
        #根据ID先进行任务组件jobentry的获取
        etl2290_jobentry_infor = self.get_jobentry_2300(config.etl2290['db'], etl2290_id)
        etl2300_jobentry_infor = self.get_jobentry_2300(config.etl2300['db'], etl2300_id)
        # 获取r_jobentry_attribute
        etl2290_jobentry_attribute_list = self.get_jobentry_attribute_2300(config.etl2290['db'], etl2290_id,etl2290_jobentry_infor)
        etl2300_jobentry_attribute_list = self.get_jobentry_attribute_2300(config.etl2300['db'], etl2300_id,etl2300_jobentry_infor)
        #进行jobentry_attribute比对
        result_infor = self.job_hop_compare(etl2290_id, etl2300_id,result_infor)
        result_infor = self.job_attribute_compare(etl2290_id, etl2300_id,result_infor)
        result_infor = self.jobentry_attribute_compare(etl2290_jobentry_attribute_list,etl2300_jobentry_attribute_list,result_infor)
        return result_infor

    # 定义组件流程对比方法
    def etl_trans_compare(self, etl2290_id, etl2300_id, result_infor):
        '''
        :param etl2290_id:
        :param etl2300_id:
        :return:
        '''
        global etl2290_step_infor, etl2300_step_infor
        # 根据ID先进行任务组件jobentry的获取
        etl2290_step_infor = self.get_trans_step(config.etl2290['db'], etl2290_id)
        etl2300_step_infor = self.get_trans_step(config.etl2300['db'], etl2300_id)
        # 进行jobentry_attribute比对
        result_infor = self.trans_hop_compare(etl2290_id, etl2300_id, result_infor)
        result_infor = self.trans_attribute_compare(etl2290_id, etl2300_id, result_infor)
        result_infor = self.step_attribute_compare(etl2290_id, etl2300_id, result_infor)
        return result_infor


    #获取组件--任务组件的基础信息，形成字典表
    def get_jobentry(self,db_name,id_job):
        jobentry_infor = {}
        param = [{'field_name': 'ID_JOB', 'filed_concatenation': '=', 'field_value': id_job},]
        table_name = 'r_jobentry'
        jobentry_list = db_manager_instances.get_table_data_sigle(db_name,table_name,'ID_JOB',param)
        for jobentry in jobentry_list:
            jobentry_infor[str(jobentry['ID_JOBENTRY'])] = jobentry['NAME']
        print(jobentry_infor)
        return jobentry_infor

    # 获取组件--任务组件的基础信息，形成字典表
    def get_jobentry_2300(self, db_name, id_job):
        jobentry_infor = {}
        param = [{'field_name': 'ID_JOB', 'filed_concatenation': '=', 'field_value': id_job}, ]
        table_name = 'r_jobentry'
        jobentry_list = db_manager_instances.get_table_data_sigle(db_name, table_name.upper(), 'ID_JOB', param)
        for jobentry in jobentry_list:
            jobentry_infor[str(jobentry['ID_JOBENTRY'])] = jobentry['NAME']
        print(jobentry_infor)
        return jobentry_infor

    #获取 r_jobentry_attribute 数据
    def get_jobentry_attribute(self,db_name,id_job,jobentry_infor):
        param = [{'field_name': 'ID_JOB', 'filed_concatenation': '=', 'field_value': id_job}, ]
        table_name = 'r_jobentry_attribute'
        if '2300' in db_name:
            table_name = table_name.upper()
        jobentry_attribute_list = db_manager_instances.get_table_data_sigle(db_name,table_name,'ID_JOB',param)
        for i in range(len(jobentry_attribute_list)):
            jobentry_attribute_list[i].pop('ID_JOBENTRY_ATTRIBUTE')
            jobentry_attribute_list[i].pop('ID_JOB')
            jobentry_attribute_list[i]['ID_JOBENTRY'] = jobentry_infor[str(jobentry_attribute_list[i]['ID_JOBENTRY'])]
            jobentry_attribute_list[i]['VALUE_NUM'] = 0 if jobentry_attribute_list[i]['VALUE_NUM'] is None else jobentry_attribute_list[i]['VALUE_NUM']
        print(jobentry_attribute_list)
        return jobentry_attribute_list

    # 获取 r_jobentry_attribute 数据
    def get_jobentry_attribute_2300(self, db_name, id_job, jobentry_infor):
        param = [{'field_name': 'ID_JOB', 'filed_concatenation': '=', 'field_value': id_job}, ]
        table_name = 'r_jobentry_attribute'
        jobentry_attribute_list = db_manager_instances.get_table_data_sigle(db_name, table_name.upper(), 'ID_JOB', param)
        for i in range(len(jobentry_attribute_list)):
            jobentry_attribute_list[i].pop('ID_JOBENTRY_ATTRIBUTE')
            jobentry_attribute_list[i].pop('ID_JOB')
            jobentry_attribute_list[i].pop('VALUE_NUM')
            jobentry_attribute_list[i]['ID_JOBENTRY'] = jobentry_infor[
                str(jobentry_attribute_list[i]['ID_JOBENTRY'])]
            # jobentry_attribute_list[i]['VALUE_NUM'] = 0 if jobentry_attribute_list[i]['VALUE_NUM'] is None else \
            # jobentry_attribute_list[i]['VALUE_NUM']
        print(jobentry_attribute_list)
        return jobentry_attribute_list

    #进行 jobentry_attribute 数据比对
    def jobentry_attribute_compare(self,etl2290_jobentry_attribute_list,etl2300_jobentry_attribute_list,test_result):
        #定义结果信息
        test_result['result_infor']['jobentry_attribute'] = {}
        test_result['result_infor']['jobentry_attribute']['num'] = ''
        test_result['result_infor']['jobentry_attribute']['different'] = []
        #进行数量上的比对
        if len(etl2290_jobentry_attribute_list) != len(etl2300_jobentry_attribute_list):
            test_result['result_infor']['jobentry_attribute']['num'] = u'etl2290:%s..,etl2300:%s' %(len(etl2290_jobentry_attribute_list),len(etl2300_jobentry_attribute_list))
        #定义已检查的idlist
        check_id_list = []
        #进行数据比对
        for etl2290_jobentry_attribute in etl2290_jobentry_attribute_list:
            if etl2290_jobentry_attribute['VALUE_STR'] is None or etl2290_jobentry_attribute['VALUE_STR'] in ['','N']:
                continue
            check_flag = 'NO'
            for i in range(len(etl2300_jobentry_attribute_list)):
                if i in check_id_list:
                    continue
                if etl2290_jobentry_attribute['ID_JOBENTRY'] != etl2300_jobentry_attribute_list[i]['ID_JOBENTRY']:
                    continue
                if etl2290_jobentry_attribute['CODE'] != etl2300_jobentry_attribute_list[i]['CODE']:
                    continue
                check_flag = 'YES'
                check_id_list.append(i)
                if etl2290_jobentry_attribute == etl2300_jobentry_attribute_list[i]:
                    break
                different = {'etl2290': etl2290_jobentry_attribute,'etl2300': etl2300_jobentry_attribute_list[i]}
                test_result['result_infor']['jobentry_attribute']['different'].append(different)
            if check_flag == 'NO':
                different = {'etl2290': etl2290_jobentry_attribute, 'etl2300': ''}
                test_result['result_infor']['jobentry_attribute']['different'].append(different)
        return test_result

    #删除字段的通用方法：
    def delete_dict_field(self,source_list,field_list):
        '''
        根据field_list 删除列表中包含的字段
        :param source_list:
        :param field_list:
        :return:
        '''
        for field_name in field_list:
            for i in range(len(source_list)):
                source_list[i].pop(field_name)
        return source_list


    #进行 job_attribute 比对
    def job_attribute_compare(self,etl2290_id,etl2300_id,test_result):
        # 定义结果信息
        test_result['result_infor']['job_attribute'] = {}
        test_result['result_infor']['job_attribute']['num'] = ''
        test_result['result_infor']['job_attribute']['different'] = []
        #获取job_attribute信息
        etl2290_param = [{'field_name': 'ID_JOB', 'filed_concatenation': '=', 'field_value': etl2290_id}, ]
        etl2300_param = [{'field_name': 'ID_JOB', 'filed_concatenation': '=', 'field_value': etl2300_id}, ]
        table_name = 'r_job_attribute'
        #获取数据
        etl2290_job_attribute_list = db_manager_instances.get_table_data_sigle(config.etl2290['db'],table_name.upper(),'ID_JOB',etl2290_param)
        etl2300_job_attribute_list = db_manager_instances.get_table_data_sigle(config.etl2300['db'],table_name.upper(),'ID_JOB',etl2300_param)
        #先进行数量比对
        # 进行数量上的比对
        if len(etl2290_job_attribute_list) != len(etl2300_job_attribute_list):
            test_result['result_infor']['job_attribute']['num'] = u'etl2290:%s..,etl2300:%s' % (len(etl2290_job_attribute_list), len(etl2300_job_attribute_list))
        # 定义已检查的idlist
        check_id_list = []
        pop_field_list = ['ID_JOB_ATTRIBUTE','ID_JOB','VALUE_NUM']
        etl2290_job_attribute_list = self.delete_dict_field(etl2290_job_attribute_list,pop_field_list)
        etl2300_job_attribute_list = self.delete_dict_field(etl2300_job_attribute_list,pop_field_list)
        for i in range(len(etl2290_job_attribute_list)):
            if etl2290_job_attribute_list[i]['VALUE_STR'] is None or etl2290_job_attribute_list[i]['VALUE_STR'] in ['','N']:
                continue
            check_flag = 'NO'
            for j in range(len(etl2300_job_attribute_list)):
                if j in check_id_list:
                    continue
                # etl2300_job_attribute_list[j]['VALUE_NUM'] = 0 if etl2300_job_attribute_list[j]['VALUE_NUM'] is None else etl2300_job_attribute_list[j]['VALUE_NUM']
                if etl2290_job_attribute_list[i]['CODE'] != etl2300_job_attribute_list[j]['CODE']:
                    continue
                check_flag = 'YES'
                check_id_list.append(j)
                if etl2290_job_attribute_list[i] == etl2300_job_attribute_list[j]:
                    continue
                different = {'etl2290': etl2290_job_attribute_list[i], 'etl2300': etl2300_job_attribute_list[j]}
                test_result['result_infor']['job_attribute']['different'].append(different)
            if check_flag == 'NO':
                different = {'etl2290': etl2290_job_attribute_list[i], 'etl2300': ''}
                test_result['result_infor']['job_attribute']['different'].append(different)
        return test_result

    #基础数据替换 jobentry_infor
    def jobentry_date_replace(self,source_list,field_list,jobentry_infor):
        for field_name in field_list:
            for i in range(len(source_list)):
                source_list[i][field_name] = jobentry_infor[str(source_list[i][field_name])]
        return source_list

    # job_hop 检查
    def job_hop_compare(self,etl2290_id,etl2300_id,test_result):
        '''
        {'40':'开始'}
        :param etl2290_id:
        :param etl2300_id:
        :param etl2290_jobentry_infor:
        :param test_result:
        :return:
        '''
        # 定义结果信息
        test_result['result_infor']['job_hop'] = {}
        test_result['result_infor']['job_hop']['num'] = ''
        test_result['result_infor']['job_hop']['different'] = []
        # 获取job_attribute信息
        etl2290_param = [{'field_name': 'ID_JOB', 'filed_concatenation': '=', 'field_value': etl2290_id}, ]
        etl2300_param = [{'field_name': 'ID_JOB', 'filed_concatenation': '=', 'field_value': etl2300_id}, ]
        table_name = 'r_job_hop'
        # 获取数据
        etl2290_list = db_manager_instances.get_table_data_sigle(config.etl2290['db'], table_name.upper(), 'ID_JOB', etl2290_param)
        etl2300_list = db_manager_instances.get_table_data_sigle(config.etl2300['db'], table_name.upper(), 'ID_JOB', etl2300_param)
        # 进行数量上的比对
        if len(etl2290_list) != len(etl2300_list):
            test_result['result_infor']['job_hop']['num'] = u'etl2290:%s..,etl2300:%s' % (len(etl2290_list), len(etl2300_list))
        cycle_num = min(len(etl2290_list), len(etl2300_list))
        # 定义已检查的idlist
        check_id_list = []
        pop_field_list = ['ID_JOB_HOP', 'ID_JOB']
        replace_field_list = ['ID_JOBENTRY_COPY_FROM','ID_JOBENTRY_COPY_TO']
        #重新进行数量整理
        etl2290_list = self.delete_dict_field(etl2290_list,pop_field_list)
        etl2290_list = self.jobentry_date_replace(etl2290_list,replace_field_list,etl2290_jobentry_infor)
        etl2300_list = self.delete_dict_field(etl2300_list,pop_field_list)
        etl2300_list = self.jobentry_date_replace(etl2300_list,replace_field_list,etl2300_jobentry_infor)
        #进行数据比对
        for i in range(len(etl2290_list)):
            if i >= cycle_num:
                different = {'etl2290': etl2290_list[i], 'etl2300': ''}
                test_result['result_infor']['job_hop']['different'].append(different)
                continue
            if etl2290_list[i] == etl2300_list[i]:
                continue
            different = {'etl2290': etl2290_list[i], 'etl2300': etl2300_list[i]}
            test_result['result_infor']['job_hop']['different'].append(different)
        return test_result

    #从 r_step 中获取步骤，并进行参数化
    def get_trans_step(self,db_name,trans_id):
        trans_step_infor = {}
        param = [{'field_name': 'ID_TRANSFORMATION', 'filed_concatenation': '=', 'field_value': trans_id}, ]
        table_name = 'r_step'
        trans_step_list = db_manager_instances.get_table_data_sigle(db_name, table_name.upper(), 'ID_TRANSFORMATION', param)
        if len(trans_step_list) == 0:
            return trans_step_infor
        for trans_step in trans_step_list:
            trans_step_infor[str(trans_step['ID_STEP'])] = trans_step['NAME']
        print(trans_step_infor)
        return trans_step_infor

    #进行 r_trans_hop 数据重置
    def trans_hop_reset(self,db_name,trans_id,trans_step_infor):
        param = [{'field_name': 'ID_TRANSFORMATION', 'filed_concatenation': '=', 'field_value': trans_id}, ]
        table_name = 'r_trans_hop'
        trans_hop_list = db_manager_instances.get_table_data_sigle(db_name, table_name.upper(), 'ID_TRANSFORMATION',param)
        if len(trans_hop_list) == 0:
            return trans_hop_list
        for i in range(len(trans_hop_list)):
            trans_hop_list[i].pop('ID_TRANS_HOP')
            trans_hop_list[i].pop('ID_TRANSFORMATION')
            trans_hop_list[i]['ID_STEP_FROM'] = trans_step_infor[str(trans_hop_list[i]['ID_STEP_FROM'])]
            trans_hop_list[i]['ID_STEP_TO'] = trans_step_infor[str(trans_hop_list[i]['ID_STEP_TO'])]
        print(trans_hop_list)
        return trans_hop_list

    #进行 r_trans_hop 数据比较
    def trans_hop_compare(self,etl2290_id,etl2300_id,test_result):
        ''''''
        # 定义结果信息
        test_result['result_infor']['trans_hop'] = {}
        test_result['result_infor']['trans_hop']['num'] = ''
        test_result['result_infor']['trans_hop']['different'] = []
        #获取表数据
        etl2290_list = self.trans_hop_reset(config.etl2290['db'],etl2290_id,etl2290_step_infor)
        etl2300_list = self.trans_hop_reset(config.etl2300['db'],etl2300_id, etl2300_step_infor)
        #进行数据比较
        # 进行数量上的比对
        if len(etl2290_list) != len(etl2300_list):
            test_result['result_infor']['trans_hop']['num'] = u'etl2290:%s..,etl2300:%s' % (len(etl2290_list), len(etl2300_list))
        cycle_num = min(len(etl2290_list), len(etl2300_list))
        # 进行数据比对
        for i in range(len(etl2290_list)):
            if i >= cycle_num:
                different = {'etl2290': etl2290_list[i], 'etl2300': ''}
                test_result['result_infor']['trans_hop']['different'].append(different)
                continue
            if etl2290_list[i] == etl2300_list[i]:
                continue
            different = {'etl2290': etl2290_list[i], 'etl2300': etl2300_list[i]}
            test_result['result_infor']['trans_hop']['different'].append(different)
        return test_result

    #进行 job_attribute 比对
    def trans_attribute_compare(self,etl2290_id,etl2300_id,test_result):
        # 定义结果信息
        test_result['result_infor']['trans_attribute'] = {}
        test_result['result_infor']['trans_attribute']['num'] = ''
        test_result['result_infor']['trans_attribute']['different'] = []
        #获取job_attribute信息
        etl2290_param = [{'field_name': 'ID_TRANSFORMATION', 'filed_concatenation': '=', 'field_value': etl2290_id}, ]
        etl2300_param = [{'field_name': 'ID_TRANSFORMATION', 'filed_concatenation': '=', 'field_value': etl2300_id}, ]
        table_name = 'r_trans_attribute'
        #获取数据
        etl2290_list = db_manager_instances.get_table_data_sigle(config.etl2290['db'],table_name.upper(),'ID_TRANSFORMATION',etl2290_param)
        etl2300_list = db_manager_instances.get_table_data_sigle(config.etl2300['db'],table_name.upper(),'ID_TRANSFORMATION',etl2300_param)
        #先进行数量比对
        # 进行数量上的比对
        if len(etl2290_list) != len(etl2300_list):
            test_result['result_infor']['trans_attribute']['num'] = u'etl2290:%s..,etl2300:%s' % (len(etl2290_list), len(etl2300_list))
        # 定义已检查的idlist
        check_id_list = []
        pop_field_list = ['ID_TRANSFORMATION','ID_TRANS_ATTRIBUTE','VALUE_NUM']
        etl2290_list = self.delete_dict_field(etl2290_list,pop_field_list)
        etl2300_list = self.delete_dict_field(etl2300_list,pop_field_list)
        for i in range(len(etl2290_list)):
            if etl2290_list[i]['VALUE_STR'] is None or etl2290_list[i]['VALUE_STR'] in ['','N']:
                continue
            # if etl2290_list[i]['VALUE_NUM'] is None:
            #     etl2290_list[i]['VALUE_NUM'] = 0
            check_flag = 'NO'
            for j in range(len(etl2300_list)):
                if j in check_id_list:
                    continue
                #进行VALUE_NUM的重置，确保不会因为null值导致失败
                # etl2300_list[j]['VALUE_NUM'] = 0 if etl2300_list[j]['VALUE_NUM'] is None else etl2300_list[j]['VALUE_NUM']
                #进行code比对，如果不相等，则循环下一个，已对比的会放入check_id_list中，不再进行比对
                if etl2290_list[i]['CODE'] != etl2300_list[j]['CODE']:
                    continue
                check_flag = 'YES'
                check_id_list.append(j)
                if etl2290_list[i] == etl2300_list[j]:
                    continue
                different = {'etl2290': etl2290_list[i], 'etl2300': etl2300_list[j]}
                test_result['result_infor']['trans_attribute']['different'].append(different)
            if check_flag == 'NO':
                different = {'etl2290': etl2290_list[i], 'etl2300': ''}
                test_result['result_infor']['trans_attribute']['different'].append(different)
        return test_result

    #进行 r_step_attribute 数据比对
    def step_attribute_compare(self,etl2290_id,etl2300_id,test_result):
        #定义结果信息
        test_result['result_infor']['step_attribute'] = {}
        test_result['result_infor']['step_attribute']['num'] = ''
        test_result['result_infor']['step_attribute']['different'] = []
        # 获取 r_step_attribute 信息
        etl2290_param = [{'field_name': 'ID_TRANSFORMATION', 'filed_concatenation': '=', 'field_value': etl2290_id}, ]
        etl2300_param = [{'field_name': 'ID_TRANSFORMATION', 'filed_concatenation': '=', 'field_value': etl2300_id}, ]
        table_name = 'r_step_attribute'
        # 获取数据
        etl2290_list = db_manager_instances.get_table_data_sigle(config.etl2290['db'], table_name.upper(), 'ID_TRANSFORMATION',etl2290_param)
        etl2300_list = db_manager_instances.get_table_data_sigle(config.etl2300['db'], table_name.upper(), 'ID_TRANSFORMATION',etl2300_param)
        # 定义已检查的idlist
        check_id_list = []
        pop_field_list = ['ID_TRANSFORMATION', 'ID_STEP_ATTRIBUTE','VALUE_NUM']
        etl2290_list = self.delete_dict_field(etl2290_list, pop_field_list)
        etl2300_list = self.delete_dict_field(etl2300_list, pop_field_list)
        #进行数据替换
        replace_field_list = ['ID_STEP']
        etl2290_list = self.jobentry_date_replace(etl2290_list,replace_field_list,etl2290_step_infor)
        etl2300_list = self.jobentry_date_replace(etl2300_list,replace_field_list,etl2300_step_infor)

        #进行数量上的比对
        if len(etl2290_list) != len(etl2300_list):
            test_result['result_infor']['step_attribute']['num'] = u'etl2290:%s..,etl2300:%s' %(len(etl2290_list),len(etl2300_list))
        #定义已检查的idlist
        check_id_list = []
        #进行数据比对
        for etl2290_step_attribute in etl2290_list:
            if etl2290_step_attribute['VALUE_STR'] is None or etl2290_step_attribute['VALUE_STR'] in ['','N']:
                continue
            check_flag = 'NO'
            for i in range(len(etl2300_list)):
                if i in check_id_list:
                    continue
                # 进行VALUE_NUM的重置，确保不会因为null值导致失败
                # etl2300_list[i]['VALUE_NUM'] = 0 if etl2300_list[i]['VALUE_NUM'] is None else etl2300_list[i]['VALUE_NUM']
                #进行 ID_STEP 内容比对，不一致则进行下一个，一致则进行code比对
                if etl2290_step_attribute['ID_STEP'] != etl2300_list[i]['ID_STEP']:
                    continue
                if etl2290_step_attribute['CODE'] != etl2300_list[i]['CODE']:
                    continue
                #在 ID_STEP 和 code 完全一致的情况下，对整条数据进行比对
                check_flag = 'YES'
                check_id_list.append(i)
                if etl2290_step_attribute == etl2300_list[i]:
                    break
                different = {'etl2290': etl2290_step_attribute,'etl2300': etl2300_list[i]}
                test_result['result_infor']['step_attribute']['different'].append(different)
            if check_flag == 'NO':
                different = {'etl2290': etl2290_step_attribute, 'etl2300': ''}
                test_result['result_infor']['step_attribute']['different'].append(different)
        return test_result


if __name__ == '__main__':
    test = etl_components()
    # test.db_timestamp_handle('123')
    test_re = re.findall(param_mark_pattern,"%(dtime)sssss%(dtime1)ssss")
    print (test_re)
    # test.create_stringEN_random('测试'.decode('utf-8'))
    # jobentry_infor = test.get_jobentry(config.etl2300['db'],8)
    # test.get_jobentry_attribute(config.etl2300['db'],8,jobentry_infor)
    test.etl_assembly_compare({"etl2290_id":1,"etl2300_id":1,"check_type":"job"})




