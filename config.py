#encoding:utf-8
import os,configparser
from conf import settings
basedir = os.path.abspath(os.path.dirname(__file__))
#阿里内部环境
# host_dev = 'rm-wz9ra72814q3t1yev.mysql.rds.aliyuncs.com'
# host_online = 'rm-wz9pqm56i293ure29.mysql.rds.aliyuncs.com'
#外部环境
host_dev = '127.0.0.1'
host_online = 'rm-wz9pqm56i293ure29o.mysql.rds.aliyuncs.com'
user_dev = 'root'
password_dev = 'tongtech123456'
user_online = 'readonly'
password_online = 'tTkkJjHCiJbKW918'

#定义测试环境为线上、或是本地（online、local）
environment = 'online'
# test_case_db = 'zentao' if environment == 'online' else 'zentaoep'
test_case_db = 'interface_test' if environment == 'online' else 'zentaoep'

branch = 'test'

#从配置文件中读取数据
cfgpath = os.path.join("conf//config.ini")
#调用读取配置模块中的类
conf = configparser.ConfigParser()
conf.read(cfgpath)

# 数据库配置
#=================================Oracle14======================================================
dbTypeName = "mysql"
config_conn = {
    "host": "127.0.0.1",
    "port": 3306,
    "db": "automatic_test",
    "user": "root",
    "password": "admin",
    "charset": "utf8"
}
config_db_name = "automatic_test"
business_conn = {
    "host": host_dev if settings.module == 'dev' else host_online,
    "port": 3306,
    "db": "wechat_api",
    "user": user_dev if settings.module == 'dev' else user_online,
    "password": password_dev if settings.module == 'dev' else password_online,
    "charset": "utf8"
}

wechat_api = {
    "host": host_dev if settings.module == 'dev' else host_online,
    "port": 3306,
    "db": "wechat_api",
    "user": user_dev if settings.module == 'dev' else user_online,
    "password": password_dev if settings.module == 'dev' else password_online,
    "charset": "utf8"
}
zentaoep = {
    "host": host_dev if settings.module == 'dev' else host_online,
    "port": 3308,
    "db": "zentaoep",
    "user": user_dev if settings.module == 'dev' else user_online,
    "password": password_dev if settings.module == 'dev' else password_online,
    "charset": "utf8"
}

zentao = {
    "host": '168.1.9.7',
    "port": 3307,
    "db": "zentao",
    "user": 'zentao',
    "password": '123456',
    "charset": "utf8"
}

blog_test = {
    "host": host_dev if settings.module == 'dev' else host_online,
    "port": 3306,
    "db": "blog_test",
    "user": user_dev if settings.module == 'dev' else user_online,
    "password": 'admin',
    "charset": "utf8"
}

MongoDB = {
    "host": '10.10.64.46',
    "port": 27017,
    "db": "oam",
    "user": 'admin',
    "password": 'tongtech',
    "charset": "utf8"
}

etl2300 = {
    "host": '10.10.64.46',
    "port": 3306,
    "db": "lijq-etl",
    "user": 'root',
    "password": '123456',
    "charset": "utf8"
}

etl2290 = {
    "host": '10.10.64.46',
    "port": 3306,
    "db": "lijq-etl-cs",
    "user": 'root',
    "password": '123456',
    "charset": "utf8"
}

mysql8 = {
    "host": '127.0.0.1',
    "port": 3306,
    "db": "etl2290",
    "user": 'root',
    "password": '123456',
    "charset": "utf8"
}

oracle_tong = {
    "host": '10.10.64.36',
    "port": 1521,
    "db": "ORCL",
    "user": 'usr_datai',
    "password": 'Tong1818',
    "charset": "utf8"
}

lin_cms = {
    "host": '127.0.0.1',
    "port": 3306,
    "db": "lin_cms",
    "user": 'root',
    "password": 'admin',
    "charset": "utf8"
}
case_db = {
    "host": '10.10.64.46',
    "port": 3306,
    "db": "interface_test",
    "user": 'root',
    "password": '123456',
    "charset": "utf8"
}
check_db = {
    "host": '10.10.64.46',
    "port": 3306,
    "db": "interface_test",
    "user": 'root',
    "password": '123456',
    "charset": "utf8"
}
interface_test = {
    "host": '10.10.64.46',
    "port": 3306,
    "db": "interface_test",
    "user": 'root',
    "password": '123456',
    "charset": "utf8"
}

db_list_infor = {'etl2300':etl2300,'etl2290':etl2290}
db_list = [
    {'etl2300':etl2300,'db_type':'mysql','config_db_name':'etl2300'},
    {'etl2290':etl2290,'db_type':'mysql','config_db_name':'etl2290'},
    {'zentao':zentao,'db_type':'mysql','config_db_name':'zentao'},
    {'mysql8':mysql8,'db_type':'mysql','config_db_name':'mysql8'},
    {'oracle_tong':oracle_tong,'db_type':'oracle','config_db_name':'oracle_tong'},
    {'lin_cms':lin_cms,'db_type':'mysql','config_db_name':'lin_cms'},
    {'case_db':case_db,'db_type':'mysql','config_db_name':'case_db'},
    {'check_db':check_db,'db_type':'mysql','config_db_name':'check_db'},
    {'interface_test':interface_test,'db_type':'mysql','config_db_name':'interface_test'},
]
