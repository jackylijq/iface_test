#coding=utf-8
import random,os,string,pymysql,time,json
from threading import Thread
from kafka import KafkaProducer,KafkaConsumer
from kafka.errors import KafkaError




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

#创建kafka连接
producer = KafkaProducer(bootstrap_servers=["10.10.64.21:9092"])

#基础数据库操作
class kafka_db_handle():
    #获取数据连接
    def get_conn(self):
        conn = pymysql.connect(**db_config)
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
            for result in results:
                result_dict = dict(zip(columns, result))
                result_list.append(result_dict)
        except Exception as e:
            result_list = []
        return result_list
    #数据查询方法
    def data_query(self,sql):
        # 新建链接、游标
        config_conn = self.get_conn()
        config_cursor = config_conn.cursor()
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
        # 新建链接、游标
        config_conn = self.get_conn()
        config_cursor = config_conn.cursor()
        # 执行sql操作
        for sqlitem in sql:
            config_cursor.execute(sqlitem)
        # 更新提交
        config_conn.commit()
        # 关闭游标、链接
        config_cursor.close()
        config_conn.close()

    #数据库插入数据
    def insert_data_db(self,table_name,args):
        basic_sql = 'INSERT INTO %(table_name)s VALUES (0,'
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
    def make_data(self):
        data_list = []
        for i in range(8):
            data_list.append(random.randint(999,99999))
        for i in range(16):
            data_list.append(self.ranstr(24))
        for i in range(8):
            data_list.append(self.ranstr(24)+self.ranstr(24))
        data_list.append('NOW()')
        return data_list

    #kafka数据读取
    def catch_kafka_data(self):
        '''
        从kafka中进行数据读取
        :return:
        '''
        consumer = KafkaConsumer('lijq', bootstrap_servers=['10.10.64.21:9092'], auto_offset_reset='earliest')
        for message in consumer:
            print("topic：%s， partition:%d， offset:%d，  key=%s， value=%s" % (message.topic, message.partition,message.offset, message.key,message.value.decode(encoding="unicode_escape")))
            # print(message)

    #kafka数据写入
    def producer_kafka_data(self,message):
        '''
        针对kafka进行消息写入
        :return:
        '''
        # message = {'name':'test1234','age':'12','school':'武汉大学'}
        # message = 'test'
        # message = 'test#1234213'
        test = '#123123'
        future = producer.send('lijq',value=json.dumps(message).encode(encoding="utf-8"),partition=0)
        # future = producer.send('lijq',value=message.encode(encoding="GBK"),partition=0)
        try:
            record = future.get(timeout=10)
            print(record)
        except KafkaError as e:
            print(e)

    #批量写入kafka的数据
    def producer_kafka_data_batch(self):
        message = {'name': 'test1234', 'age': '12', 'school': '武汉大学','id':0}
        # message = '武汉大学'
        # message
        for i in range(100):
            message['id'] = i + 1
            self.producer_kafka_data(message)

    #往数据库进行数据插入
    def insert_date_batch(self):
        for i in range(10):
            #进行数据库插入操作
            sql_list = []
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(u'当前批次：%s，每轮数量：20000，开始时间：%s' %(i,timestr))
            for i in range(20000):
                # 先生成基础数据
                data_list = self.make_data()
                sql_list.append(self.insert_data_db(table_name,data_list))
            self.data_insert_update(sql_list)
            if i % 1000 == 0:
                print(u'当前已添加的数量为：%s' %str(i))

    #多线程并发
    def thread_batch(self,number=200):
        l_thread = (Thread(target=self.insert_date_batch) for i in range(number))
        for t in l_thread:
            t.start()  # 启动线程开始执行

if __name__ == '__main__':
    kafka_data_handel_instances = kafka_db_handle()
    #文件存储的绝对路径：路径需要手动创建
    # path = '/home/test/test1234/'
    #第一个参数为需要生成的文件格式，第二个参数为当前文件的大小，单位M
    # kafka_data_handel_instances.producer_kafka_data_batch()
    kafka_data_handel_instances.catch_kafka_data()
