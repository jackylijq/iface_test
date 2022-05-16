# -*- coding:utf-8 -*-
import sys,importlib,bson
importlib.reload(sys)
sys.path.append("..")
import config,time,copy,json,random
from tools import utils_logging,utils_database,usefulTools,switch
from conf import factory_sorting_constant
import pymongo

usefulTools_instances = usefulTools.userfulToolsFactory()

"""
主要用来处理一些db上需要处理的问题
"""

wechat_api = "wechat_api" if config.dbTypeName == "wechat_api" else ""
dlhist = "dlhist" if config.dbTypeName == "oracle" else ""
dlsys = "dlsys" if config.dbTypeName == "oracle" else ""
umstat = "umstat" if config.dbTypeName == "oracle" else ""
dlmis_ = "dlmis." if config.dbTypeName == "oracle" else ""
dlhist_ = "dlhist." if config.dbTypeName == "oracle" else ""
dlsys_ = "dlsys." if config.dbTypeName == "oracle" else ""
umstat_ = "umstat." if config.dbTypeName == "oracle" else ""

timestr = time.strftime('%Y%m', time.localtime(time.time()))
event_desc = "web auto test rec - " + timestr + "%"
# print event_desc
db_type = ['wechat_api']

class database_operate():
    def drop_special_character(self,str_source):
        str_target = str(str_source).replace('\\','').replace('u\'','').replace('u"','').replace('\'','').replace('"','')
        return str_target

    #拆分find的内容
    def split_find_condition(self,find_str):
        '''
        find_str 会是 query、projection 的组合
        :param find_str:{status:2,status:2},{tag:1}
        :return:
        '''
        # 定义返回的格式
        find_condition = {'query':{},'projection':{}}
        if find_str == '{}' or find_str == '':
            return find_condition
        find_condition_keys = ['query','projection']
        find_condition_list = []
        # find_str = str(find_str).replace('\\','').replace('u\'','').replace('u"','').replace('\'','')
        find_str = str(find_str).replace('\\','').replace('\'','"')
        #统计当前的字符串中一个有多少个 { , 根据{ 进行拆分
        dict_start_str = '{'
        for i in range(find_str.count('{')):
            #获取字典表结束符}之前的内容
            dict_str = usefulTools_instances.SubString_handle(find_str,dict_start_str,'}')
            #计算字典表的 { } 数量是不是一致的
            dict_start_num = (dict_start_str + dict_str + '}').count('{')
            dict_end_num = (dict_start_str + dict_str + '}').count('}')
            #如果数量一致，则加入到 find_condition_list，并把相关字符串去掉
            if dict_start_num == dict_end_num:
                find_condition_list.append(dict_start_str + dict_str + '}')
                find_str = usefulTools_instances.SubString_handle(find_str,(dict_start_str + dict_str + '},'),'')
                dict_start_str = '{'
            else:
                dict_start_str = dict_start_str + dict_str + '}'
            #需要查找的字符串为空的情况下，结束循环
            if find_str == '':
                break
        #进行 query、 projection 的字典表重新构建
        for condition_id in range(len(find_condition_list)):
            condition_infor = find_condition_list[condition_id]
            #兼容查询条件为空的情况
            if condition_infor == '{}':
                continue
            try:
                find_condition[find_condition_keys[condition_id]] = json.loads(condition_infor)
                continue
            except Exception as reason:
                pass
            dict_start_str = '{'
            for i in range(str(condition_infor).count('{')):
                condition_key = usefulTools_instances.SubString_handle(condition_infor,dict_start_str,':')

                condition_key_str = condition_key if '"' in condition_key else '"'+condition_key+'"'
                condition_infor = condition_infor if '"' in condition_key else str(condition_infor).replace(condition_key,condition_key_str,1)
                dict_start_str = dict_start_str + condition_key_str + usefulTools_instances.SubString_handle(condition_infor,condition_key_str,'{')+'{'
            dict_start_str = '{'
            for j in range(str(condition_infor).count(':')):
                condition_key = usefulTools_instances.SubString_handle(condition_infor, dict_start_str, ':')
                if condition_key == '':
                    find_condition[find_condition_keys[condition_id]] = json.loads(condition_infor)
                    break
                condition_key_str = condition_key if '"' in condition_key else '"' + condition_key + '"'
                condition_infor = condition_infor if '"' in condition_key else str(condition_infor).replace(condition_key, condition_key_str)
                dict_start_str = dict_start_str + condition_key_str + usefulTools_instances.SubString_handle(condition_infor, condition_key_str, ',')+','
            find_condition[find_condition_keys[condition_id]] = json.loads(condition_infor)
        return find_condition



    #基础查询接口
    def mg_query_data(self,db_name,query_condition):
        '''
        db_name 需要查询的表名
        query_condition：查询条件，MongoDB 为dict格式的查询条件
        eg:
        sql = {"srvcn":"测试"}
        result = utils_database.mongodb_db_query(sql,'gwconf','gw_service')
        for i in result:
            print(i)
        print 'test'
        :param db_name:
        :param query_condition:格式db.gw_service_sub.find({status:22},{taskid:1}).sort({ inserttime:-1 }).limit(1)，需要进行格式拆解
        :return:
        '''
        #拆解表名出来
        table_name = usefulTools_instances.SubString_handle(query_condition, 'db.', '.find')
        #拆解查询条件出来
        # query_sql = {}
        # query_sql_list = usefulTools_instances.SubString_handle(query_condition,'find(',')').replace('$or','"$or"').replace('\'','"')
        find_condition = self.split_find_condition(usefulTools_instances.SubString_handle(query_condition,'find(',')'))
        #获取连表查询的条件
        pipeline = usefulTools_instances.SubString_handle(query_condition,'aggregate(',')')
        #如果条件为空，则直接传入空字符串进行处理，如果不为空，处理为字典表进行传入
        pipeline = '' if pipeline == '' else {'pipeline':pipeline}
        pipeline_condition = self.split_find_condition(pipeline)
        #pipeline_condition 根据pipeline是否为空进行分开处理
        pipeline_condition = [] if pipeline == '' else pipeline_condition['query']['pipeline']
        #拆卸排序条件
        sort_list = []
        query_sort_list = usefulTools_instances.SubString_handle(query_condition,'sort(',')').replace('{','').replace('}','')
        if query_sort_list != '':
            query_sort_list = str(query_sort_list).split(',')
            for sort_id in range(len(query_sort_list)):
                query_sort_key = usefulTools_instances.SubString_handle(str(query_sort_list[sort_id]),'',':')
                query_sort_value = usefulTools_instances.SubString_handle(str(query_sort_list[sort_id]), ':', '')
                sort_infor = (usefulTools_instances.drop_special_character(query_sort_key),int(query_sort_value))
                sort_list.append(sort_infor)
        limit = 0
        #拆卸limit条件
        limit_infor = usefulTools_instances.SubString_handle(query_condition,'limit(',')')
        limit = 0 if limit_infor == '' else int(limit_infor)
        query_result = utils_database.mongodb_db_query(db_name, table_name, find_condition['query'],find_condition['projection'], sort_list, limit,pipeline_condition)
        return query_result

    def test(self):
        # from pymongo import MongoClient
        # conn = pymongo.MongoClient('mongodb://admin:iftest@10.10.64.46:27017/')
        conn = pymongo.MongoClient('mongodb://10.10.64.23:27017/')
        # conn = pymongo.MongoClient('58.49.40.146', 27017)

        sql = {'$or':[{'taskid':4},{'status':0}]}
        query = {"status": 2}
        projection = {"tag":1}
        sort = [("inserttime", -1)]
        query_list = [query,projection,sort,1]
        db = conn.gwconf
        collection = db.gw_astask_A
        # test = my_set.find({"srvcn":"测试"}).sort([("sertype",-1)]).limit(1)
        # test = my_set.find({'status':0}).sort([("inserttime", -1)]).limit(2)
        test = collection.find({}, projection=[], sort=[('inserttime', 1)], limit=10)
        # test = collection.find({}, projection={}, sort=[('inserttime', 1)], limit=10)
        # test = utils_database.mongodb_db_query('gwconf','gw_service_lv',{'taskid':13,'oappsysId':None},{},[('inserttime', -1)],10,[])
        for i in test:
            print (i)
        print('down')

    #数据库 初始化，根据字段类型继续数据插入
    def prepare_data(self,db_name,table_name,field_infor):
        '''
        1、从表中先查到一条数据
        2、根据数据的格式进行自动随机填充，对部分查询的字段按照传入的值进行赋值
        :param db_name:
        :param table_name:
        :param field_infor:
        :return:
        '''
        query_list = utils_database.mongodb_db_query(db_name,table_name,{},[],[('_id',-1)],1)
        #获取当前table所有的字段（已存在数据的）
        table_field_list = list(query_list[0].keys())
        #获取传入的参数中包含的字段
        exist_field_list = field_infor.keys()
        #定义部分常量字段
        timestamp = usefulTools_instances.get_time_stamp13()
        dtime = usefulTools_instances.make_strftime('YYYY-MM-DD',0,'').replace('-','')
        static_field_list = ['_class']
        special_field = {'inserttime':timestamp,'dtime':dtime,'updatetime':timestamp,'subtime':timestamp}
        for table_field in table_field_list:
            if table_field == '_id':
                continue
            if table_field in exist_field_list:
                continue
            if table_field in static_field_list:
                field_infor[table_field] = query_list[0][table_field]
                continue
            if table_field in special_field.keys():
                field_infor[table_field] = special_field[table_field]
                continue
            if type(query_list[0][table_field]) == int:
                field_infor[table_field] = random.randint(101,999)
                continue
            if type(query_list[0][table_field]) == str:
                field_infor[table_field] = table_field + str(random.randint(101,999))
                continue
            if type(query_list[0][table_field]) == list:
                field_infor[table_field] = [table_field + str(random.randint(101,999)),table_field + str(random.randint(101,999))]
                continue
            if type(query_list[0][table_field])._type_marker == 18:
                field_infor[table_field] = usefulTools_instances.get_time_stamp13()
                continue
        print(field_infor)
        utils_database.mongodb_db_insert(db_name,table_name,field_infor)

    #根据表获取表结构
    def get_collection_field(self,table_name):
        query_condition = 'db.%s.find({}).limit(20)' %table_name
        #从表中获取数据
        data_list = self.mg_query_data(config.MongoDB['db'],query_condition)
        #如果数据为0，则返回空
        if len(data_list) == 0:
            return []
        #获取字段信息
        field_list = list(data_list[0].keys())
        #循环比较字段数量
        for i in range(len(data_list)):
            key_list = list(data_list[i].keys())
            if len(key_list) > len(field_list):
                field_list = key_list
        print(field_list)
        return field_list


if __name__ == '__main__':
    print ("utils test")
    database_operate_instances = database_operate()
    print(type(bson.Int64))
    # utils_database.mongodb_db_query('gwconf', 'gw_service_tag', [], [],[])
    # database_operate_instances.test()
    sql = "db.alarm_his.find({}).limit(100)"
    database_operate_instances.get_collection_field('alarm_his')
    sql = "db.gw_service.find({$or:[{'approvalstatus':-1},{'approvalstatus':11}]},{sertype:1,srvcn: 1}).sort({ _id:-1,srvcn: 1 }).limit(2)"
    # sql = "db.gw_service_tag.find({status:2},{tag:1}).sort({ inserttime:-1 }).limit(1)"
    # sql = "db.gw_service_tag.find({'tag':'%(tag)s'})"
    sql = "db.gw_service.find({$or:[{'approvalstatus':-1},{'approvalstatus':11}]}).sort({_id: -1 }).limit(2)"

    find = "{$or:[{approvalstatusaaa:-1,approvalstatuccc:-1},{'approvalstatusbbb':11}]},{tag:1}"
    param = {'tag':'test'}
    pipeline = '[{$lookup:{from:\\"gw_service\\",localField:\\"tag\\",foreignField:\\"srvtag\\",as:\\"tag_docs\\"}},{$lookup:{from:\\"gw_service\\",localField:\\"tag\\",foreignField:\\"srvtag\\",as:\\"tag_docs\\"}}]'
    pipeline_dict = {'pipeline':pipeline}
    # database_operate_instances.split_find_condition(pipeline_dict)
    test_query = "db.gw_service_sub.find({status:0},{taskid:1}).sort({ taskid:-1 }).limit(1)"
    # database_operate_instances.test()
    database_operate_instances.mg_query_data('gwconf',test_query %param)
    # database_operate_instances.prepare_data('gwconf','gw_dassubstatus_W',{"xiid" : 123,"xiname" : "部门A","deptid" : 111,"deptname" : "部门B"})

