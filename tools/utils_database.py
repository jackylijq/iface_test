# -*- coding:utf-8 -*-
import sys,importlib,pymysql,cx_Oracle
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
sys.path.append("..")
import config,json
from datetime import date, datetime
from pymongo import MongoClient
import time
import logging
import logging.config
# import cx_Oracle
"""
    ljq 2017-04-01
    工具方法
    获取数据库连接方法 get_bizdb_conn get_statdb_conn
    获取查询结果方法 query_for_list query_for_dict
    插入数据库方法 insert_one insert_many
    复制dict方法 copy_dict2dict
    转数据库日期字符串 toDbDateStr
    获取数据库时间 get_db_now
"""
def get_sysConfig_conn():
    conn = ''
    # 获取城管数据库连接
    if config.dbTypeName.lower() == "oracle":
        import cx_Oracle
        user = config.config_conn["user"]
        password = config.config_conn["password"]
        db = config.config_conn["host"] + ":" + str(config.config_conn["port"]) + "/" + config.config_conn["db"]
        conn = cx_Oracle.connect(user, password, db)
    if config.dbTypeName.lower() == "mysql":
        import pymysql
        conn = pymysql.connect(**config.config_conn)
    if config.dbTypeName.lower() == "mongodb":
        conn = MongoClient.connect(**config.config_conn)
    return conn

def get_sysBusiness_conn(db_name):
    # 获取统计数据库连接
    if db_name == "wechat_api":
        conn = pymysql.connect(**config.wechat_api)
        return conn
    if db_name == "washer_service":
        conn = pymysql.connect(**config.washer_service)
        return conn
    if db_name == "cabinet_api":
        conn = pymysql.connect(**config.cabinet_api)
        return conn
    if db_name == "delivery_api":
        conn = pymysql.connect(**config.delivery_api)
        return conn
    if db_name == "blog_test":
        conn = pymysql.connect(**config.blog_test)
        return conn
    if db_name == "zentaoep":
        conn = pymysql.connect(**config.zentaoep)
        return conn
    if db_name in ["etl2300",'yinc2300',"wzc_etl2"]:
        conn = pymysql.connect(**config.etl2300)
        return conn
    if db_name in ["etl2290","yinc2290","wzc_etl3"]:
        conn = pymysql.connect(**config.etl2290)
        return conn
    if db_name == "zentao":
        conn = pymysql.connect(**config.zentao)
        return conn
    if db_name == "MongoDB":
        # conn = MongoClient(config.MongoDB['host'],config.MongoDB['port'])
        connect_config = 'mongodb://%s:%s/' %(config.MongoDB['host'],config.MongoDB['port'])
        if config.MongoDB['user'] != '' and config.MongoDB['password'] != '':
            connect_config = 'mongodb://%s:%s@%s:%s/' %(config.MongoDB['user'],config.MongoDB['password'],config.MongoDB['host'],config.MongoDB['port'])
        conn = MongoClient(connect_config)
        return conn
    # return conn

#重新写获取数据库连接的功能
def get_db_conn(db_name):
    #从config中获取正确的db信息
    for db_id in range(len(config.db_list)):
        config_db_name = config.db_list[db_id]['config_db_name']
        #如果db_name 不在config中，则再次循环获取
        if config.db_list[db_id][config_db_name]['db'] != db_name:
            continue
        if config.db_list[db_id]['db_type'] == 'mysql':
            conn = pymysql.connect(**config.db_list[db_id][config_db_name])
            return conn

#重新写获取数据库连接的功能
def get_conn_accord_config(config_db_name):
    #从config中获取正确的db信息
    for db_id in range(len(config.db_list)):
        # config_db_name = config.db_list[db_id]['config_db_name']
        #如果db_name 不在config中，则再次循环获取
        if config.db_list[db_id]['config_db_name'] != config_db_name:
            continue
        if config.db_list[db_id]['db_type'] == 'mysql':
            conn = pymysql.connect(**config.db_list[db_id][config_db_name])
            return conn
        if config.db_list[db_id]['db_type'] == 'oracle':
            user = config.db_list[db_id][config_db_name]["user"]
            password = config.db_list[db_id][config_db_name]["password"]
            host = config.db_list[db_id][config_db_name]["host"]
            port = config.db_list[db_id][config_db_name]["port"]
            db_name = config.db_list[db_id][config_db_name]["db"]
            db = host + ":" + str(port) + "/" + db_name
            conn = cx_Oracle.connect(user, password, db)
            return conn

def get_yblIns_conn():
    # 获取统计数据库连接
    if config.dbTypeName.lower() == "oracle":
        import cx_Oracle
        user = config.business_conn["user"]
        password = config.business_conn["password"]
        db = config.business_conn["host"] + ":" + str(config.business_conn["port"]) + "/" + config.business_conn["db"]
        conn = cx_Oracle.connect(user, password, db)
    elif config.dbTypeName.lower() == "mysql":
        import pymysql
        conn = pymysql.connect(**config.yblIns_conn)
    else:
        # 默认数据库连接为mysql
        import pymysql
        conn = pymysql.connect(**config.business_conn)
    return conn

def query_for_list(cur, sql, param=None):
    # 返回全部查询结果
    # @return list[dict]格式
    logger = logging.getLogger("main.tools.utils")
    result_list = []
    try:
        if param:
            cur.execute(sql, param)
        else:
            cur.execute(sql)
        # columns = [val[0].lower() for val in cur.description]   #字段名称全部转为小写了，会导致一些问题
        columns = [val[0] for val in cur.description]
        results = cur.fetchall()
        for result in results:
            result_dict = dict(zip(columns, result))
            result_list.append(result_dict)
    except Exception as reason:
        logger.error("select error [%s]:[%s]:[%s]" %(sql, param, str(reason)))
        result_list = None
    return result_list

def query_for_dict(cur, sql, param=None):
    # 返回案件单条查询结果
    # @return dict格式
    logger = logging.getLogger("main.tools.utils")
    result_dict = {}
    try:
        if param:
            cur.execute(sql, param)
        else:
            cur.execute(sql)
        columns = [val[0].lower() for val in cur.description]
        result_dict = dict(zip(columns, cur.fetchone()))
    except Exception as reason:
        logger.error("select error [%s]:[%s]:[%s]" %(sql, param, str(reason)))
        result_dict = None
    return result_dict

def gen_insert_sql_one(table_name, table_dict, field_tuple):
    # 生成插入语句对象
    # {"sql": sql, "param": param}格式
    # [oracle]
    # insert into table_name (field1, field2, field3 ...) values(:1, :2, :3 ...)
    # (value1, value2, value3 ...)
    # [mysql]
    # insert into table_name (field1, field2, field3 ...) values(%s, %s, %s ...)
    # (value1, value2, value3 ...)

    field_str = ""
    value_str = ""
    value_param_list = []
    param_order = 1
    for key, value in table_dict.items():
        if key in field_tuple and (value or value == 0):
            field_str += ", " + key
            if (config.dbTypeName == "oracle"):
                value_str += ", :" + str(param_order)
            else:
                value_str += ", %s"
            value_param_list.append(value)
            param_order += 1
            continue
        else:
            continue
    if len(field_str) > 0:
        sql = "insert into %s (%s) values (%s)" % (table_name, field_str[1:], value_str[1:])
    else:
        return None
    return {"sql": sql, "param": tuple(value_param_list)}

def insert_one(cur, table_name, data_dict, field_tuple):
    # 插入单条数据
    # @param cur 数据库游标
    # @param table_name 表名称
    # @param data_dict 要插入的数据字典
    # @param field_tuple 表的字段元组
    insert_dict = gen_insert_sql_one(table_name, data_dict, field_tuple)
    logger = logging.getLogger("main.tools.utils")
    if insert_dict:
        cur.execute(insert_dict["sql"], insert_dict["param"])

def insert_many(cur, table_name, data_list, field_tuple):
    # 批量插入
    # @param cur 数据库游标
    # @param table_name 表名称
    # @param data_dict 要插入的数据列表
    # @param field_tuple 表的字段元组
    for data_dict in data_list:
        insert_one(cur, table_name, data_dict, field_tuple)

def copy_dict2dict(from_dict, to_dict):
    # 复制字典
    for key, value in from_dict.items():
        to_dict[key] = value

def toDbDateStr(date_str):
    # 将字符串转成对应数据库的日期类型字符串
    # @param date_str yyyy-mm-dd hh24:mi:ss
    # return 字符串
    if config.dbTypeName.lower() == "oracle":
        return "to_date('" + date_str + "', 'yyyy-mm-dd hh24:mi:ss')"
    elif config.dbTypeName.lower() == "mysql":
        return "str_to_date('" + date_str + "', '%Y-%m-%d %H:%i:%s')"
    else:
        return "str_to_date('" + date_str + "', '%Y-%m-%d %H:%i:%s')"

def get_db_now(cur):
    if config.dbTypeName.lower() == "oracle":
        cur.execute("select sysdate from dual")
        return cur.fetchone()[0]
    elif config.dbTypeName.lower() == "mysql":
        cur.execute("select now()")
        return cur.fetchone()[0]
    else:
        return datetime.now()

def data_seach_by_sql(sql):
    config_conn = get_sysConfig_conn()
    business_conn = get_sysBusiness_conn()

    biz_cursor = config_conn.cursor()
    stat_cursor = business_conn.cursor()
    print ('sql = ' + sql)
    biz_cursor.execute(sql)

    result_list = biz_cursor.fetchall()
    result_num = len(result_list)

    biz_cursor.close()
    config_conn.close()
    return result_list

def data_update_by_sql(sql):
    #链接数据库
    config_conn = get_sysConfig_conn()
    business_conn = get_sysBusiness_conn()

    biz_cursor = config_conn.cursor()
    stat_cursor = business_conn.cursor()
    print ('sql = ' + sql)
    #执行更新语句，目前只包含业务库的更新
    biz_cursor.execute(sql)
    #更新提交
    config_conn.commit()

    #关闭链接
    biz_cursor.close()
    config_conn.close()

#接口配置数据库更新方法封装
def sysConfig_db_update(sql):
    print (u'数据库进行数据插入sql: %s' % sql)
    # 新建链接、游标
    config_conn = get_sysConfig_conn()
    config_cursor = config_conn.cursor()
    # 执行sql操作
    config_cursor.execute(sql)
    # 更新提交
    config_conn.commit()
    # 关闭游标、链接
    config_cursor.close()
    config_conn.close()
#业务数据库更新方法封装
def sysBusiness_db_update(sql,db_name):
    print ('sql = ',sql)
    # 新建链接、游标
    business_conn = get_sysBusiness_conn(db_name)
    business_cursor = business_conn.cursor()
    # 执行sql操作
    business_cursor.execute(sql)
    # 更新提交
    business_conn.commit()
    # 关闭游标、链接
    business_cursor.close()
    business_conn.close()

#更新数据库操作
def update_database(sql,config_db_name):
    print('sql = ', sql)
    # 新建链接、游标
    business_conn = get_conn_accord_config(config_db_name)
    business_cursor = business_conn.cursor()
    # 执行sql操作
    business_cursor.execute(sql)
    insert_id = int(business_conn.insert_id())
    # 更新提交
    business_conn.commit()
    # 关闭游标、链接
    business_cursor.close()
    business_conn.close()
    return insert_id

#配置数据库查询
def sysConfig_db_query(sql):
    print ('sql = %s' % sql)
    # 新建链接、游标
    config_conn = get_sysConfig_conn()
    config_cursor = config_conn.cursor()
    # 执行sql操作
    config_cursor.execute(sql)
    result_list = config_cursor.fetchall()
    # 关闭游标、链接
    config_cursor.close()
    config_conn.close()
    #查询数据返回
    return result_list
#业务数据库查询
def sysBusiness_db_query(sql,statis_flag = None):
    # 新建链接、游标
    business_conn = get_sysBusiness_conn()
    business_cursor = business_conn.cursor()
    # 执行sql操作
    business_cursor.execute(sql)
    result_list = business_cursor.fetchall()
    # 关闭游标、链接
    business_cursor.close()
    business_conn.close()
    # 查询数据返回
    return result_list

#配置数据库查询
def sysConfig_db_query_all_dict(sql):
    print ('sql = %s' % sql)
    # 新建链接、游标
    config_conn = get_sysConfig_conn()
    config_cursor = config_conn.cursor()
    # 执行sql操作
    sysConfig_query_all_dict = query_for_list(config_cursor,sql)
    # 关闭游标、链接
    config_cursor.close()
    config_conn.close()
    #查询数据返回
    return sysConfig_query_all_dict

#配置数据库查询
def db_query_all_dict(sql,db_name):
    #使用like % 的时候，会与格式化的 % 冲突，前端使用&&代替，后端进行替换
    sql = str(sql).replace('&&', '%')
    print ('sql = %s' % sql)
    # 新建链接、游标
    # business_conn = get_sysBusiness_conn(db_name)
    business_conn = get_db_conn(db_name)
    business_cursor = business_conn.cursor()
    # 执行sql操作
    query_all_dict = query_for_list(business_cursor,sql)
    # 关闭游标、链接
    business_cursor.close()
    business_conn.close()
    #查询数据返回
    return query_all_dict

#配置数据库查询
def db_query_mysql(sql,config_db_name):
    #使用like % 的时候，会与格式化的 % 冲突，前端使用&&代替，后端进行替换
    sql = str(sql).replace('&&', '%')
    print ('sql = %s' % sql)
    # 新建链接、游标
    # business_conn = get_sysBusiness_conn(db_name)
    # business_conn = get_db_conn(db_name)
    business_conn = get_conn_accord_config(config_db_name)
    business_cursor = business_conn.cursor()
    # 执行sql操作
    query_all_dict = query_for_list(business_cursor,sql)
    # 关闭游标、链接
    business_cursor.close()
    business_conn.close()
    #查询数据返回
    return query_all_dict

#mongodb 数据库查询
def mongodb_db_query(db_name,table_name,query={},projection=[],sort=[],limit=[],pipeline=[]):
    query_condition = {'query':None,'projection':None,'sort':None,'limit':0}
    if query:
        # 使用like % 的时候，会与格式化的 % 冲突，前端使用&&代替，后端进行替换
        sql = json.dumps(query).replace('&&', '%')
        print ('sql = %s' % sql)
        query_condition['query'] = query
    if projection:
        query_condition['projection'] = projection
    if sort:
        query_condition['sort'] = sort
    if limit:
        query_condition['limit'] = limit
    query_result_list = []
    # 新建链接、游标
    business_conn = get_sysBusiness_conn('MongoDB')
    business_db = business_conn[db_name]
    # 设置需要进行操作的表
    collection = business_db[table_name]
    # 进行查询操作
    query_result = collection.find(query_condition['query'], projection=query_condition['projection'],sort=query_condition['sort'], limit=query_condition['limit'])
    try:
        if pipeline:
            query_result = collection.aggregate(pipeline)
        for result in query_result:
            # print result
            query_result_list.append(result)
        #查询数据返回
        return query_result_list
    except Exception as reason:
        print('MongoDB查询失败，原因：'%reason)
        return []

#mongodb 数据库插入操作
def mongodb_db_insert(db_name,table_name,insert_param):
    # 新建链接、游标
    business_conn = get_sysBusiness_conn('MongoDB')
    business_db = business_conn[db_name]
    # 设置需要进行操作的表
    business_collection = business_db[table_name]
    # 进行查询操作
    query_result = business_collection.insert(insert_param)
    business_conn.close()

#报价数据库查询
def yblIns_db_query_all_dict(sql):
    print ('sql = %s' % sql)
    # 新建链接、游标
    yblIns_conn = get_yblIns_conn()
    yblIns_cursor = yblIns_conn.cursor()
    # 执行sql操作
    yblIns_query_all_dict = query_for_list(yblIns_cursor,sql)
    # 关闭游标、链接
    yblIns_cursor.close()
    yblIns_conn.close()
    #查询数据返回
    return yblIns_query_all_dict


if __name__ == '__main__':
    print ("utils test")
    # sql = 'select human_name from tc_human where human_name like ' + "'%测试'"
    # sql5 = "select human_name from tc_human where user_name like 'egova'"
    #
    # sql1 = "select human_name from tc_human where human_name like %(test)s"
    # param = {"test":'测试'}
    #
    # test2 = '%测试123'
    # sql2 = 'select human_name from tc_human where human_name like \"' + test2 +'\"'
    #
    # dlmis = "dlmis" if config.dbTypeName == "oracle" else ""
    #
    # print sql1 % param
    # print sql
    # print sql2
    # print 'dlmis = ' + dlmis
    config_conn = get_sysConfig_conn()
    biz_cursor = config_conn.cursor()
    sql5 = 'select c.* from dlmis.to_rec_act a,dlsys.tc_human_role b,dlsys.tc_human c where a.role_id = b.role_id and b.human_id = c.human_id and a.rec_id = 859'
    test = query_for_list(biz_cursor,sql5)
    # print test[0]['unit_name']
    #
    # print str(test[0]['unit_name']).decode('GBK').encode('UTF-8')
    # print len(test)
