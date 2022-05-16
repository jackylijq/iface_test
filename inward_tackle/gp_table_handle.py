#coding=utf-8
import random,os,string,pymysql,time,psycopg2,copy
import psycopg2.extras
from threading import Thread
import datetime
path = 'f:/test/'
db_config = {
    "host": '10.10.64.46',
    "port": 3306,
    "db": "lijq",
    "user": 'root',
    "password": '123456',
    "charset": "utf8"
}
table_name = 'stand_data_01'

gp_db_config = {
    "host": '10.10.65.44',
    "port": "5432",
    "dbname": "field100Tbale10w",
    "user": 'gpadmin',
    "password": 'gpadmin'
}

sql_modle = 'CREATE TABLE "public"."%s" (%s);'

#基础数据库操作
class db_handle():
    #生成时间戳
    def get_time_stamp13(self,days=None):
        # 生成13时间戳   eg:1540281250399895
        datetime_now = datetime.datetime.now()
        if days is not None:
            datetime_now = datetime_now - datetime.timedelta(days=days)
        # 10位，时间点相当于从UNIX TIME的纪元时间开始的当年时间编号
        date_stamp = str(int(time.mktime(datetime_now.timetuple())))
        # 3位，微秒
        data_microsecond = str("%06d" % datetime_now.microsecond)[0:3]
        date_stamp = date_stamp + data_microsecond
        print (int(date_stamp))
        return int(date_stamp)
    #获取数据连接
    def get_conn(self):
        conn = psycopg2.connect(**gp_db_config)
        # conn = pymysql.connect(**db_config)

        return conn
    def query_for_list(self,cur, sql, param=None):
        # 返回全部查询结果
        result_list = []
        try:
            if param:
                cur.execute(sql, param)
            else:
                cur.execute(sql)
            columns = [val[0] for val in cur.description]
            results = cur.fetchall()
            result_list = results
            # for result in results:
            #     result_dict = dict(zip(columns, result))
            #     result_list.append(result_dict)
        except Exception as e:
            result_list = []
        return result_list
    #数据查询方法
    def data_query(self,sql):
        sql = 'SELECT * from test_01'
        # sql = 'SELECT * from stand_data_01'

        # 新建链接、游标
        config_conn = self.get_conn()
        config_cursor = config_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # config_cursor = config_conn.cursor()
        config_conn.commit()
        # 执行sql操作
        # config_cursor.execute(sql)
        result_list = self.query_for_list(config_cursor,sql)
        # 关闭游标、链接
        config_cursor.close()
        config_conn.close()
        # 查询数据返回
        return result_list

    # 数据插入、更新的基础方法
    def data_insert_update(self, sql):
        # sql = []
        # sql.append(sql_modle)
        # 新建链接、游标
        config_conn = self.get_conn()
        config_cursor = config_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # config_cursor = config_conn.cursor()
        # 执行sql操作
        for sqlitem in sql:
            # print(sqlitem)
            config_cursor.execute(sqlitem)
        # 更新提交
        config_conn.commit()
        # 关闭游标、链接
        config_cursor.close()
        config_conn.close()

    #数据库插入数据
    def insert_data_db(self,table_name,args):
        # basic_sql = 'INSERT INTO %(table_name)s VALUES (0,'
        basic_sql = 'INSERT INTO "public"."%(table_name)s" VALUES (0,'
        basic_param = {'table_name':table_name}
        for i in range(len(args)):
            sql_last = ',' if i < len(args)-1 else ''
            if type(args[i]) == int or args[i] == 'NOW()':
                basic_sql = basic_sql + str(args[i]) + sql_last
            else:
                basic_sql = basic_sql + '\''+ str(args[i]) + '\'' + sql_last
        basic_sql = basic_sql + ')'
        # print (basic_sql %basic_param)
        return basic_sql %basic_param
        #进行数据库操作
        # self.data_insert_update(basic_sql %basic_param)

    # 随机生成一串字符串，包含特殊字符
    def ranstr(self, num):
        # 猜猜变量名为啥叫 H
        special_character = '$_'
        target_str = ''.join(random.sample(string.ascii_letters + string.digits, num))
        target_str = target_str + random.choice(special_character)
        # print(target_str)
        return target_str

    #根据需要生成随机数据
    def make_data(self,int_num,str_num):
        data_list = []
        for i in range(int_num-1):
            data_list.append(random.randint(999,99999))
        for i in range(str_num):
            data_list.append(self.ranstr(24))
        # for i in range(8):
        #     data_list.append(self.ranstr(24)+self.ranstr(24))
        data_list.append('NOW()')
        return data_list
    #生成库表结构
    def generate_table_structure(self,int_num,str_num):
        field_one_int = '"%s" int4'
        field_one_varchar = '"%s" varchar(255)'
        field_one_time = '"%s" date'
        table_field_list = []
        #增加int类型数据
        for i in range(int_num):
            table_field_list.append(field_one_int %(self.ranstr(24)+str(i)))
        #增加字符串类型：
        for i in range(str_num):
            table_field_list.append(field_one_varchar %(self.ranstr(24)+str(i)))
        #增加时间类型
        table_field_list.append(field_one_time %(self.ranstr(24)))
        # print(table_field_list)
        table_field_infor = ','.join(table_field_list)
        # print(table_field_infor)
        return table_field_infor


    #往数据库进行数据插入
    def insert_date_batch(self,int_num,str_num,cycle_num):
        for i in range(cycle_num):
            #进行数据库插入操作
            sql_list = []
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(u'当前批次：%s，每轮数量：200，总的批次数量：%s,开始时间：%s' %(i,cycle_num,timestr))

            # 生成表名数据
            table_name_list = []
            table_name = self.ranstr(5) + str(self.get_time_stamp13()) + str(i)
            table_field_infor = self.generate_table_structure(int_num,str_num)
            generate_table_sql = sql_modle % (table_name, table_field_infor)
            table_name_list.append(generate_table_sql)
            self.data_insert_update(table_name_list)
            #插入数据
            for j in range(5):
                # 先生成基础数据
                data_list = self.make_data(int_num,str_num)
                sql_list.append(self.insert_data_db(table_name,data_list))
            self.data_insert_update(sql_list)
            if i % 1000 == 0:
                print(u'当前已添加的数量为：%s' %str(i))

    #多线程并发
    def thread_batch(self,table_num,field_num,supervene_num=200):
        int_num = int(field_num / 5)
        str_num  = field_num - int_num
        cycle_num = int(table_num / supervene_num)
        l_thread = (Thread(target=self.insert_date_batch,args=(int_num,str_num,cycle_num)) for i in range(supervene_num))
        for t in l_thread:
            t.start()  # 启动线程开始执行

if __name__ == '__main__':
    create_file_instances = db_handle()
    #文件存储的绝对路径：路径需要手动创建
    path = '/home/test/test1234/'
    #第一个参数为需要生成的文件格式，第二个参数为当前文件的大小，单位M
    # create_file_instances.insert_date_batch()
    # create_file_instances.data_insert_update('-')
    create_file_instances.thread_batch(100000,100)