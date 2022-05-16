# -*- coding:utf-8 -*-
import sys,hashlib,json,random,importlib,pymysql,datetime
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
sys.path.append("..")
import config,copy
import time
from tools import utils_database,utils_logging,usefulTools,switch
# from werkzeug.security import generate_password_hash, check_password_hash

"""
主要用来处理一些db上需要处理的问题
"""

dlmis = "dlmis" if config.dbTypeName == "oracle" else ""
dlhist = "dlhist" if config.dbTypeName == "oracle" else ""
dlsys = "dlsys" if config.dbTypeName == "oracle" else ""
umstat = "umstat" if config.dbTypeName == "oracle" else ""
dlmis_ = "dlmis." if config.dbTypeName == "oracle" else ""
dlhist_ = "dlhist." if config.dbTypeName == "oracle" else ""
dlsys_ = "dlsys." if config.dbTypeName == "oracle" else ""
umstat_ = "umstat." if config.dbTypeName == "oracle" else ""

# timestr = time.strftime('%Y%m%d', time.localtime(time.time()))
timestr = time.strftime('%Y%m', time.localtime(time.time()))
event_desc = "web auto test rec - " + timestr + "%"
# print event_desc

#实例化class
usefulTools_instances = usefulTools.userfulToolsFactory()

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)


class database_operate():
    #获取授权相关的案件列表
    #根据需要获取 schema 中表名
    def get_table_name(self,db_type,db_name,table_condition):
        sql = ''
        if db_type == 'mysql':
            sql = "SELECT table_name FROM information_schema.TABLES WHERE TABLE_SCHEMA = %(TABLE_SCHEMA)s AND TABLE_NAME like '&&%(table_condition)s&&'"
        param = {'TABLE_SCHEMA':'\''+db_name+'\'','table_condition':table_condition}
        query_result = utils_database.db_query_all_dict(sql % param, db_name)
        result = query_result if query_result is not None else []
        print (result)
        return result

    #获取表结构信息
    def get_table_structure(self,db_type,db_name,table_name,column_condition):
        sql = ''
        if db_type == 'mysql':
            # sql = "SELECT TABLE_NAME AS 'table_name',COLUMN_NAME AS 'columnName',COLUMN_COMMENT AS 'columnComment',IS_NULLABLE AS 'nullable',DATA_TYPE AS 'dataType',CHARACTER_MAXIMUM_LENGTH AS 'strLength',NUMERIC_PRECISION AS 'numLength',NUMERIC_SCALE AS 'numBit' FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = %(TABLE_SCHEMA)s AND TABLE_NAME = '%(table_name)s' and COLUMN_NAME like '&&%(column_condition)s&&'"
            sql = "select TABLE_NAME, COLUMN_NAME, COLUMN_TYPE,DATA_TYPE,COLUMN_KEY,CHARACTER_MAXIMUM_LENGTH AS 'strLength' from information_schema.columns where TABLE_SCHEMA = %(TABLE_SCHEMA)s AND TABLE_NAME = '%(table_name)s' and COLUMN_NAME like '&&%(column_condition)s&&'"
        param = {'TABLE_SCHEMA':'\''+db_name+'\'','table_name':table_name,'column_condition':column_condition}
        query_result = utils_database.db_query_all_dict(sql % param, db_name)
        result = query_result if query_result is not None else []
        print (result)
        return result

    #获取表的索引信息
    def get_index_infor(self,db_type,db_name,table_name,index_name,index_condition):
        sql = ''
        if db_type == 'mysql':
            sql = "SHOW INDEX FROM %(table_name)s WHERE Non_unique=1 AND Key_name = '%(index_name)s' AND Column_name = '&&%(index_condition)s&&'"
        param = {'TABLE_SCHEMA': '\'' + db_name + '\'', 'table_name': table_name, 'index_name': index_name,'index_condition': index_condition}
        query_result = utils_database.db_query_all_dict(sql % param, db_name)
        result = query_result if query_result is not None else []
        print (result)
        return result

    #根据需要修改和删除的数量进行获取表名
    def get_modify_drop_table(self,modify_num,drop_num,db_type,db_name):
        #根据传入的需要修改、删除的数量，如果都为0，则直接返回为空
        if modify_num == 0 and drop_num == 0:
            return ''
        #获取到所有的测试中添加的表
        table_name_list = self.get_table_name(db_type,db_name,'add_table_')
        #循环从表中获取可删除、可更新的字段数量，进行比对
        for i in range(len(table_name_list)):
            col_modify_list = self.get_table_structure(db_type,db_name,table_name_list[i]['table_name'],'col_modify')
            col_drop_list = self.get_table_structure(db_type, db_name, table_name_list[i]['table_name'], 'col_drop')
            if len(col_modify_list) >= modify_num and len(col_drop_list) >= drop_num:
                return table_name_list[i]['table_name']
        return ''

    # 单表获取数据，
    def get_table_data_sigle(self, db_name, table_name, sort_type, param_list, limit=None):
        result = []
        # sql = "SELECT * FROM %(db_name)s.%(table_name)s t "
        sql = "SELECT * FROM %(table_name)s t "
        sql_order = "ORDER BY t.%(sort_type)s DESC"
        sql_limit = "LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'WHERE' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + str(param_list[i]['field_value']) + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        param = {'db_name': db_name, 'table_name': table_name, 'sort_type': sort_type}
        # sql = sql + sql_order + sql_limit
        sql = sql + sql_order
        if limit is not None:
            sql = sql + sql_limit
        # print sql
        result = utils_database.db_query_all_dict(sql % param, db_name)
        if result == None:
            result = []
        return result

    # 单表获取数据，
    def query_date_page(self, db_name, table_name, sort_type, param_list, page_num=0,page_size=10):
        result = []
        sql = "SELECT * FROM %(db_name)s.%(table_name)s t "
        sql_order = "ORDER BY t.%(sort_type)s DESC"
        sql_limit = "LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'WHERE' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            field_value = '\'' + str(param_list[i]['field_value']) + '\'' if type(param_list[i]['field_value']) == str else str(param_list[i]['field_value'])
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + field_value + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        param = {'db_name': db_name, 'table_name': table_name, 'sort_type': sort_type}
        # sql = sql + sql_order + sql_limit
        sql = sql + sql_order
        if page_num != 0 and page_size != 0:
            sql = sql + ' LIMIT %s,%s;' %((page_num-1)*page_size,page_size)
        result = utils_database.db_query_all_dict(sql % param, db_name)
        if result == None:
            result = []
        for result_id in range(len(result)):
            result_item_keys = list(result[result_id].keys())
            for key in result_item_keys:
                try:
                    result[result_id][key] = json.loads(result[result_id][key])
                except Exception as reason:
                    continue
        return result

    # 单表获取数据，
    def query_date_single(self, config_db_name, table_name, sort_type, param_list, page_num=0, page_size=500):
        result = []
        sql = "SELECT * FROM %(db_name)s.%(table_name)s t "
        sql_order = "ORDER BY t.%(sort_type)s DESC"
        sql_limit = "LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'WHERE' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            field_value = '\'' + str(param_list[i]['field_value']) + '\'' if type(param_list[i]['field_value']) == str else str(param_list[i]['field_value'])
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + field_value + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        param = {'db_name': config_db_name, 'table_name': table_name, 'sort_type': sort_type}
        # sql = sql + sql_order + sql_limit
        sql = sql + sql_order
        if page_num != 0 and page_size != 0:
            sql = sql + ' LIMIT %s,%s;' % ((page_num - 1) * page_size, page_size)
        result = utils_database.db_query_mysql(sql % param, config_db_name)
        if result == None:
            result = []
        for result_id in range(len(result)):
            result_item_keys = list(result[result_id].keys())
            for key in result_item_keys:
                try:
                    result[result_id][key] = json.loads(result[result_id][key])
                except Exception as reason:
                    continue
        return result

    #获取所有的配置表信息，组装请求的url
    def get_url_list(self,branch):
        param = [
            {'field_name': 'branch', 'filed_concatenation': '=', 'field_value': '\''+branch+'\''},
        ]
        #从system_config获取数据，以product_mark为key，product_address为value，组成字典表，供后续使用
        sysConfig_list = self.get_table_data_sigle(config.test_case_db, 'system_config', 'id', param)
        url_infor = {}
        for i in range(len(sysConfig_list)):
            url_infor[sysConfig_list[i]['product_mark']] = sysConfig_list[i]['product_address']
        return url_infor

    # 获取环境变量
    def get_env_setting(self, branch):
        param = [
            {'field_name': 'branch', 'filed_concatenation': '=', 'field_value': '\'' + branch + '\''},
        ]
        # 从system_config获取数据，以product_mark为key，product_address为value，组成字典表，供后续使用
        env_setting_list = self.get_table_data_sigle(config.test_case_db, 'env_setting', 'id', param)
        return env_setting_list



    #根据需要测试的用例组装字典表
    def pack_case_request(self,test_plan_list,test_module_list,test_case_list):
        #如果case列表不为空，则直接根据case列表进行数据获取
        case_status = usefulTools_instances.quoted_string('pass')
        if len(test_case_list) != 0:
            # case_list = self.case_data_handle(test_case_list)
            test_case_list = '('+','.join('%s' % id for id in test_case_list)+')'
            param = [
                {'field_name': 'id', 'filed_concatenation': 'in', 'field_value': test_case_list},
                {'field_name': 'case_status', 'filed_concatenation': '=', 'field_value': case_status},
            ]
            case_list = self.get_table_data_sigle(config.test_case_db, 'stand_atom_case_list', 'id', param)
            return case_list
        #如果case列表为空，检查test_module_list 是否为空
        if len(test_module_list) != 0:
            for module_id in range(len(test_module_list)):
                param = [
                    {'field_name': 'module', 'filed_concatenation': '=', 'field_value': test_module_list[module_id]},
                ]
                case_infor = self.get_table_data_sigle(config.test_case_db, 'stand_atom_case_list', 'id', param)
                for case_id in range(len(case_infor)):
                    test_case_list.append(case_infor[case_id]['id'])
            case_list = self.case_data_handle(test_case_list)
            return case_list
        #如果case_list,module_list都为空的情况：
        if len(test_plan_list) != 0:
            for plan_id in range(len(test_plan_list)):
                param = [
                    {'field_name': 'task', 'filed_concatenation': '=', 'field_value': test_plan_list[plan_id]},
                ]
                case_infor = self.get_table_data_sigle(config.test_case_db, 'stand_atom_case_list', 'id', param)
                for case_id in range(len(case_infor)):
                    test_case_list.append(case_infor[case_id]['case'])
            case_list = self.case_data_handle(test_case_list)
            return case_list

    #处理case数据
    def case_data_handle(self,test_case_list):
        case_list = []
        execute_case_list = []
        compare_keyWord = 'check'
        print (u'处理case数据')
        for case_id in range(len(test_case_list)):
            case_param = [
                {'field_name': 'case', 'filed_concatenation': '=', 'field_value': test_case_list[case_id]},
            ]
            case_infor = self.get_table_data_sigle(config.test_case_db, 'zt_casestep', 'id', case_param)
            case_list.append(case_infor)
        print (len(case_list))
        for case_list_id in range(len(case_list)):
            case_infor = case_list[case_list_id]
            execute_case_infor = {'case_id':case_list[case_list_id][0]['case']}
            case_version = case_infor[0]['version']
            compare_key_list = []
            for i in range(len(case_infor)):
                if case_infor[i]['version'] != case_version:
                    break
                request_key = case_infor[i]['desc']
                request_value = str(case_infor[i]['expect']).replace('&quot;','"').replace('\r','').replace('\n','')
                if request_key == 'query_result_check':
                    request_value = self.deal_value_marks(request_key,request_value)
                if request_key == 'header':
                    request_value = str(request_value).replace('\'','"')
                #如果有多条结果检查，则需要校验当前key是否已在字典表，在的情况下，加个随机数进去
                execute_case_keys = execute_case_infor.keys()
                if request_key in execute_case_keys:
                    request_key = request_key + '_' + str(random.randint(100,999))
                #把需要校验的内容放入到 compare_key_list 中，后续所有需要校验的都从这里进行取值
                if compare_keyWord in request_key:
                    compare_key_list.append(request_key)
                execute_case_infor[request_key] = request_value
            execute_case_infor['compare_key_list'] = compare_key_list
            execute_case_list.append(execute_case_infor)
        return execute_case_list

    #处理value中包含 ""的情况
    def deal_value_marks(self,request_key,request_value):
        if request_key == 'query_result_check':
            request_value = request_value.replace('\'','"').replace(',}','}')
            value_original = usefulTools_instances.SubString_handle(request_value,'"query_condition":"','","field_check"')
            value_target = value_original.replace('\\"','"').replace('"','\\"')
            request_value_target = str(request_value).replace(value_original,value_target)
            # request_value_target = json.loads(request_value_target)
            return request_value_target

    #写入测试结果到 fun_case_result
    def insert_data_db(self,db_name,table_name,*args):
        basic_sql = 'INSERT INTO %(table_name)s VALUES (0,'
        basic_param = {'table_name': table_name}
        for i in range(len(args)):
            sql_last = ',' if i < len(args) - 1 else ''
            basic_sql = basic_sql + str(args[i]) + sql_last
        basic_sql = basic_sql + ')'
        print(basic_sql %basic_param)
        # 进行数据库操作
        utils_database.sysBusiness_db_update(basic_sql % basic_param,db_name)

    #创建表结构,主要针对创建多个表结构，post请求调用
    def create_table_date(self,post_data):
        base_sql = """
                    create table %(table_name)s(
                    id int not null,
                    name VARCHAR(10),
                    age int,
                    address VARCHAR(20),
                    create_time DATE)
                """
        # 重新对字段进行修改
        if len(post_data['field_list']) > 0:
            base_sql = base_sql[:-18] + ','
            for field_list_item in post_data['field_list']:
                field_infor = list(field_list_item.keys())[0] + ' ' + list(field_list_item.values())[0]
                field_infor_end = ',' if list(field_list_item.values())[0] == 'int' else '(124),'
                base_sql = base_sql + '\n                    ' + field_infor + field_infor_end
            base_sql = base_sql[:-1] + ')'
        #重新随机生成表名
        table_name = post_data['table_name'] + usefulTools_instances.ranstr(5)
        table_name = table_name + str(usefulTools_instances.get_time_stamp13())[5:] + '_' + str(random.randint(1000, 9999))
        param = {'table_name': table_name}
        # print(base_sql %param)
        utils_database.update_database(base_sql %param,post_data['config_db_name'])


#.....................
    #接口数据写入
    def interface_data_insert(self,config_db_name,table_name,*args):
        basic_sql = 'INSERT INTO %(table_name)s VALUES (0,'
        basic_param = {'table_name': table_name}
        for i in range(len(args)):
            sql_last = ',' if i < len(args) - 1 else ''
            insert_value = args[i]
            if type(insert_value) == list:
                insert_value = ','.join('%s' % id for id in insert_value)
                # insert_value = usefulTools_instances.quoted_string(insert_value) if insert_value == '' else insert_value
                insert_value = insert_value.replace('\'','"')
                insert_value = usefulTools_instances.quoted_string(insert_value)
                basic_sql = basic_sql + str(insert_value) + sql_last
                continue
            if insert_value== 'NOW()':
                basic_sql = basic_sql + str(insert_value) + sql_last
                continue
            if type(insert_value) == dict:
                insert_value = json.dumps(insert_value,ensure_ascii=False)
                # basic_sql = basic_sql + str(insert_value) + sql_last
            if type(insert_value) == str:
                insert_value = usefulTools_instances.quoted_string(insert_value)
                basic_sql = basic_sql + str(insert_value) + sql_last
                continue
            basic_sql = basic_sql + str(insert_value) + sql_last
        basic_sql = basic_sql + ')'
        print(basic_sql %basic_param)
        # 进行数据库操作
        insert_id = utils_database.update_database(basic_sql % basic_param,config_db_name)
        return insert_id

    #根据插入的字段名称进行数据插入
    def insert_data_byField(self,config_db_name,table_name,data_json):
        #获取每个json的key
        data_json_keys = list(data_json.keys())
        basic_insert_value = ''
        #设置基础的插入语句
        basic_sql = 'INSERT INTO %(table_name)s (%(field_list)s) VALUES (%(basic_insert_value)s)'
        #组装需要插入的字段和字段值
        field_list = ''
        for i in range(len(data_json_keys)):
            #设置sql最后 一位为空，否则加入 ,
            sql_last = ',' if i < len(data_json_keys) - 1 else ''
            #需要插入的字段组装
            field_list = field_list + data_json_keys[i] + sql_last
            #需要插入的字段的值进行组装
            insert_value = data_json[data_json_keys[i]]
            if type(insert_value) == list:
                insert_value = ','.join('%s' % id for id in insert_value)
                # insert_value = usefulTools_instances.quoted_string(insert_value) if insert_value == '' else insert_value
                insert_value = insert_value.replace('\'','"')
                insert_value = usefulTools_instances.quoted_string(insert_value)
                basic_insert_value = basic_insert_value + str(insert_value) + sql_last
                continue
            if insert_value== 'NOW()':
                basic_insert_value = basic_insert_value + str(insert_value) + sql_last
                continue
            if type(insert_value) == dict:
                insert_value = json.dumps(insert_value,ensure_ascii=False)
                # basic_sql = basic_sql + str(insert_value) + sql_last
            if type(insert_value) == str:
                insert_value = usefulTools_instances.quoted_string(insert_value)
                basic_insert_value = basic_insert_value + str(insert_value) + sql_last
                continue
            basic_insert_value = basic_insert_value + str(insert_value) + sql_last
        field_list = field_list + ',update_time'
        basic_insert_value = basic_insert_value + ',NOW()'
        basic_param = {'table_name': table_name, 'field_list': field_list, 'basic_insert_value': basic_insert_value}
        # print(basic_sql %basic_param)
        insert_id = utils_database.update_database(basic_sql % basic_param, config_db_name)
        return insert_id

    #处理接口更新数据
    def case_iface_update(self,case_id,iface_id):
        '''
        需要把iface_list 表中的部分数据copy到用例表中
        '''
        # 定义查询数据,更新数据
        query_field = ['id']
        query_value = [case_id]
        # 进行接口数据更新
        update_field = ['project_id', 'iface_name', 'request_method', 'request_url', 'req_body','res_body']
        update_value = []
        # 获取接口列表
        param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': iface_id},
        ]
        iface_list = self.query_date_page(config.test_case_db, 'iface_list', 'id', param)
        #重组更新的数据
        for i in range(len(update_field)):
            update_value.append(iface_list[0][update_field[i]])
        update_value = usefulTools_instances.quoted_string(update_value)
        #进行数据更新--接口的数据copy到用例中
        self.update_data_db('case_db', 'stand_atom_case_list', update_field, update_value, query_field, query_value)
        #进行project数据更新到用例中
        # 获取项目数据
        update_field = ['project_mark']
        param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': iface_list[0]['project_id']},
        ]
        project_list = self.query_date_page(config.test_case_db, 'project_list', 'id', param)
        # 重组更新的数据
        if project_list[0]['project_mark'] ==None:
            return 0
        update_value = [project_list[0]['project_mark']]
        update_value = usefulTools_instances.quoted_string(update_value)
        self.update_data_db('case_db', 'stand_atom_case_list', update_field, update_value, query_field,query_value)
        return 0

    #复制插入
    def copy_insert(self,config_db_name,table_name,copy_infor):
        '''
        copy_infor 为需要复制的信息，包含查询字段，查询的值:{'query_field':'id','query_value':1}
        :param config_db_name:
        :param table_name:
        :param copy_infor:
        :return:
        '''
        result = {'result':'pass','message':''}
        # copy_infor = {'query_field':'id','query_value':1}
        param = [{'field_name': copy_infor['query_field'], 'filed_concatenation': '=', 'field_value': copy_infor['query_value']}]
        copy_data_list = self.get_table_data_sigle(config_db_name,table_name,'id',param)
        if len(copy_data_list) == 0:
            result['result'] = 'failed'
            result['message'] = u'根据条件未查询到数据'
            return result
        #获取需要插入的数据
        copy_date_infor = copy_data_list[0]
        #生成插入语句
        basic_sql = 'INSERT INTO %(table_name)s VALUES (0,'
        basic_param = {'table_name': table_name}
        insert_keys = list(copy_date_infor.keys())
        for i in range(len(insert_keys)):
            sql_last = ',' if i < len(insert_keys) - 1 else ''
            if insert_keys[i] == copy_infor['query_field']:
                continue
            insert_value = copy_date_infor[insert_keys[i]]
            insert_value = usefulTools_instances.quoted_string(insert_value)
            basic_sql = basic_sql + str(insert_value) + sql_last
        basic_sql = basic_sql + ')'
        print(basic_sql % basic_param)
        # 进行数据库操作
        utils_database.update_database(basic_sql % basic_param, config_db_name)
        return result


    # 数据更新
    def update_data_db(self, config_db_name, table_name, update_field, update_value, query_field, query_value):
        basic_sql = 'UPDATE %(table_name)s SET '
        basic_param = {'table_name': table_name}
        # 更新设置字段
        for i in range(len(update_field)):
            sql_last = ',' if i < len(update_field) - 1 else ''
            basic_sql = basic_sql + str(update_field[i]) + '=' + str(update_value[i]) + sql_last
        basic_sql = basic_sql + ' where '
        # 更新查询字段
        for j in range(len(query_field)):
            sql_last = ' and ' if j < len(query_field) - 1 else ''
            basic_sql = basic_sql + str(query_field[j]) + '=' + str(query_value[j]) + sql_last
        # print(basic_sql % basic_param)
        # 进行数据库操作
        update_id = utils_database.update_database(basic_sql % basic_param,config_db_name)
        return update_id

    #根据传入的参数组装更新列表
    def pack_update_infor(self,update_param):
        update_dict = {'update_field':[],'update_value':[]}
        #获取所有的key值
        update_param_keys = list(update_param.keys())
        for i in range(len(update_param_keys)):
            if update_param_keys[i] == 'id':
                continue
            update_dict['update_field'].append(update_param_keys[i])
            update_dict['update_value'].append(update_param[update_param_keys[i]])
        print(update_dict)
        return update_dict

    #获取接口传参获取用例列表
    def get_case_list(self,db_name,table_name,post_data):
        param = [
            {'field_name': 'interface_id', 'filed_concatenation': '=', 'field_value': post_data['interface_id']},
        ]
        if post_data['case_title'] != '':
            query_condition_add = {'field_name': 'case_title', 'filed_concatenation': 'like', 'field_value': '\'&&'+post_data['case_title']+'&&\''}
            param.append(query_condition_add)
        if post_data['case_desc'] != '':
            query_condition_add = {'field_name': 'case_desc', 'filed_concatenation': 'like', 'field_value': '\'&&'+post_data['case_desc']+'&&\''}
            param.append(query_condition_add)
        if post_data['case_type'] != '':
            query_condition_add = {'field_name': 'case_type', 'filed_concatenation': '=', 'field_value': '\''+post_data['case_type']+'\''}
            param.append(query_condition_add)
        #获取分页数据
        page_num = post_data['curPage']
        page_size = post_data['pageSize']
        #从system_config获取数据，以product_mark为key，product_address为value，组成字典表，供后续使用
        data_list = self.query_date_page(db_name, table_name, 'id', param,page_num,page_size)
        for i in range(len(data_list)):
            data_list[i].pop('request_param_base')
            data_list[i].pop('response_base')
            data_list[i].pop('request_param')
            data_list[i].pop('response')
            data_list[i].pop('header')
            data_list[i].pop('insert_result_check')
            data_list[i].pop('query_result_check')
            data_list[i].pop('query_result_check_1')
            data_list[i].pop('query_result_check_2')
        return data_list

    #获取用例的统计数据
    def case_statistics_list(self,db_name,project_id,group_id,page_num,page_size):
        #设置接口查询条件
        interface_sql = 'SELECT id as iface_id,title,path FROM interface_list t where t.project_id =%s ' %project_id
        if group_id != 0:
            interface_sql = interface_sql + 'and t.group_id =%s ' %group_id
        interface_sql = interface_sql + 'LIMIT %s,%s' %(page_num,page_size)
        #进行接口查询
        iface_list = utils_database.db_query_all_dict(interface_sql, db_name)
        if len(iface_list) == 0:
            return iface_list
        #设置用例查询条件
        case_sql_down = "SELECT COUNT(case_title) as case_num,interface_id FROM case_list WHERE case_status = 'down' GROUP BY interface_id;"
        case_sql_smoke = "SELECT COUNT(case_title) as smoke_case_num,interface_id FROM case_list WHERE case_status = 'down' and case_type = 'smoking' GROUP BY interface_id;"
        case_down_list = utils_database.db_query_all_dict(case_sql_down, db_name)
        case_smoke_list = utils_database.db_query_all_dict(case_sql_smoke, db_name)
        #设置结果查询条件
        pass_sql = "SELECT COUNT(excute_result) as pass_num,iface_id from fun_case_result where excute_result = 'pass' GROUP BY iface_id;"
        failed_sql = "SELECT COUNT(excute_result) as failed_num,iface_id from fun_case_result where excute_result = 'failed' GROUP BY iface_id;"
        pass_list = utils_database.db_query_all_dict(pass_sql, db_name)
        failed_list = utils_database.db_query_all_dict(failed_sql, db_name)
        #重组接口统计的列表
        for i in range(len(iface_list)):
            for down_id in range(len(case_down_list)):
                iface_list[i]['case_num'] = 0
                if case_down_list[down_id]['interface_id'] == iface_list[i]['iface_id']:
                    iface_list[i]['case_num'] = case_down_list[down_id]['case_num']
                    break
            for smoke_id in range(len(case_smoke_list)):
                iface_list[i]['smoke_case_num'] = 0
                if case_smoke_list[smoke_id]['interface_id'] == iface_list[i]['iface_id']:
                    iface_list[i]['smoke_case_num'] = case_smoke_list[smoke_id]['smoke_case_num']
                    break
            for pass_id in range(len(pass_list)):
                iface_list[i]['pass_num'] = 0
                if pass_list[pass_id]['iface_id'] == iface_list[i]['iface_id']:
                    iface_list[i]['pass_num'] = pass_list[pass_id]['pass_num']
                    break
            for failed_id in range(len(failed_list)):
                iface_list[i]['failed_num'] = 0
                if failed_list[failed_id]['iface_id'] == iface_list[i]['iface_id']:
                    iface_list[i]['failed_num'] = failed_list[failed_id]['failed_num']
                    break
        print(iface_list)
        return iface_list

    #查询表容量
    def get_total_size(self,db_name, table_name, sort_type, param_list):
        #定义查询的基础sql
        sql = "SELECT COUNT(*) FROM %(db_name)s.%(table_name)s t "
        #定义查询的where条件内容
        if len(param_list) > 0:
            sql = sql + 'WHERE' + ' '
        for i in range(len(param_list)):
            field_value = '\'' + str(param_list[i]['field_value']) + '\'' if type(param_list[i]['field_value']) == str else str(param_list[i]['field_value'])
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + field_value + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        param = {'db_name': db_name, 'table_name': table_name, 'sort_type': sort_type}
        total_list = utils_database.db_query_all_dict(sql % param, db_name)
        if total_list == None:
            return 0
        return total_list[0]['COUNT(*)']





if __name__ == '__main__':
    print ("utils test")
    database_operate_instances = database_operate()
    # database_operate_instances.get_total_size('lin_cms','lin_file12')
    # database_operate_instances.pack_case_request([4,1],[],[5])
    # database_operate_instances.get_table_structure('mysql',config.test_case_db,'matedata_config','db_type')
    # db_infor = {'config_db_name':'oracle_tong','host':'10.10.64.46','db':'lijq','table_name':'test','field_list':[{'test':'varchar'}],'record_num':0}
    # database_operate_instances.create_table_date(db_infor)
    # database_operate_instances.interface_data_insert('lin_cms','project','test2','desc',1,'','NOW()')
    # database_operate_instances.interface_data_insert('lin_cms','interface_group',1,'test_group','test_group_desc',2,'aaa','NOW()')
    # database_operate_instances.pack_update_infor(db_infor)
    # database_operate_instances.query_date_page('lin_cms','test_json','id',[])
    database_operate_instances.insert_data_byField('lin_cms','test_json',{'test_str':'123','test_json':{'t01':123,'t02':'特殊'}})



