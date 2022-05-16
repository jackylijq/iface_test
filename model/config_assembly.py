#coding=utf-8
import os
import sys,json,copy,random,re,importlib,config
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
from tools import usefulTools,mg_db_manager,utils_logging

#实例化 class
usefulTools_instances = usefulTools.userfulToolsFactory()
mg_db_manager_instances = mg_db_manager.database_operate()

class config_assembly():
    #根据传入的config的信息进行db数据更新
    def update_db_config(self,db_config,update_config):
        '''
        :param db_config:
        :return:
        '''
        print(u'需要从数据库中进行查询更新')

    def match_config_infor(self,update_db_infor,config_db_name):
        '''
        "etl2300":{
    	"host": "127.0.0.1",
        "port": 3306,
        "db": "etl2300",
        "user": "root",
        "password": "admin",
        "charset": "utf8"
	} 为传入的 db 内容
        :param update_config:
        :return:
        '''
        #获取数据库列表 key 值
        config_db_keys = list(config.db_list_infor.keys())
        #获取传入的json的keys
        update_db_keys = list(update_db_infor.keys())
        for i in range(len(config.db_list)):
            #根据 config_db_name 和 update_config的 key进行比对，不一致，则继续比对，一致则替换
            if config.db_list[i]['config_db_name'] != config_db_name:
                continue
            #一致先剔除db_type
            if 'db_type' in update_db_keys:
                config.db_list[i]['db_type'] = update_db_infor['db_type']
                # update_db_infor.pop('db_type')
                update_db_keys.pop(5)
            #一致则进行替换
            for db_key in update_db_keys:
                config.db_list[i][config_db_name][db_key] = update_db_infor[db_key]
            break

    # #配置使用的数据库
    # def update_check_db(self,env_config_list):
