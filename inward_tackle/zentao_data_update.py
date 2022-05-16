#coding=utf-8
import random,os,string,pymysql,time,datetime,json,requests,copy
from threading import Thread
path = 'f:/test/'
db_config = {
    "host": '10.10.64.20',
    "port": 3308,
    "db": "zentao",
    "user": 'root',
    "password": 'Tong.8199',
    "charset": "utf8"
}
table_name = 'stand_data_01'

#基础数据库操作
class db_handle():
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
        print('sql:%s' %sql)
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
    #根据日期生成问题解决的截止日期
    def afirm_deadline(self,severity,openedDate,activatedDate):
        '''
        根据不同的时间格式 time_format ，生成需要的实际
        :param time_format: 时间格式：YYYY-MM-DDHH、YYYY-MM-DD、YYYYMM、YYYYQn
        :param days:
        :param week:MONDAY、
        :return:
        '''
        #获取当前月份
        mouth_str = (datetime.datetime.now()).strftime('%Y-%m')
        mouth_str_20 = mouth_str + '-20'
        mouth_str_19 = mouth_str + '-19'
        mouth_str_15 = mouth_str + '-15'
        #判断当前时间
        day_str = (datetime.datetime.now()).strftime('%Y-%m-%d')
        deadline = datetime.datetime.now()
        #创建时间转为str
        openedDate_str = openedDate.strftime('%Y-%m-%d')
        activatedDate_str = activatedDate.strftime('%Y-%m-%d') if type(activatedDate) != str else '0000-00-00'
        if openedDate_str < activatedDate_str:
            openedDate_str = activatedDate_str
            openedDate = activatedDate
        #如果创建时间<15号：
        if openedDate_str <= mouth_str_20:
            if severity == 1:
                holiday_status = self.check_holiday(openedDate,1)
                delay_days = 1 if holiday_status == 0 else 1 + holiday_status
                deadline = openedDate + datetime.timedelta(days=delay_days)
            if severity == 2:
                holiday_status = self.check_holiday(openedDate, 2)
                delay_days = 2 if holiday_status == 0 else 2 + holiday_status
                deadline = openedDate + datetime.timedelta(days=delay_days)
            if severity > 2:
                holiday_status = self.check_holiday(openedDate, 5)
                delay_days = 5 if holiday_status == 0 else 5 + holiday_status
                deadline = openedDate + datetime.timedelta(days=delay_days)
        #如果创建时间大于15号
        # if openedDate_str >= mouth_str_15 and openedDate_str <= mouth_str_20:
        #     if severity == 1:
        #         deadline = openedDate + datetime.timedelta(days=1)
        #     if severity == 2:
        #         deadline = openedDate + datetime.timedelta(days=1)
        #     if severity > 2:
        #         deadline = openedDate + datetime.timedelta(days=2)
        #     deadline_str = deadline.strftime('%Y-%m-%d')
        #     if deadline_str >= mouth_str_20:
        #         deadline = mouth_str_20 + ' 23:00:00'
        if openedDate_str >= mouth_str_20:
            holiday_status = self.check_holiday(openedDate, 5)
            delay_days = 5 if holiday_status == 0 else 5 + holiday_status
            deadline = openedDate + datetime.timedelta(days=delay_days)
        #对deadline 进行格式化
        deadline_str = deadline.strftime('%Y-%m-%d %H:%M:%S') if type(deadline) != str else deadline
        return deadline_str

    # 根据日期生成问题解决的截止日期
    def afirm_deadline_new(self, severity, openedDate, activatedDate):
        '''
        根据不同的时间格式 time_format ，生成需要的实际
        :param time_format: 时间格式：YYYY-MM-DDHH、YYYY-MM-DD、YYYYMM、YYYYQn
        :param days:
        :param week:MONDAY、
        :return:
        '''
        # 创建时间转为str
        # 创建时间转为str
        openedDate_str = openedDate.strftime('%Y-%m-%d')
        activatedDate_str = activatedDate.strftime('%Y-%m-%d') if type(activatedDate) != str else '0000-00-00'
        if openedDate_str < activatedDate_str:
            openedDate_str = activatedDate_str
            openedDate = activatedDate

        # 对deadline 进行格式化
        deadline_str = ''
        if openedDate.strftime('%Y-%m-%d %H:%M:%S') > openedDate_str + ' 12:00:00':
            # openedDate = openedDate + datetime.timedelta(days=1)
            openedDate = openedDate + datetime.timedelta(days=30)
            deadline_str = openedDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # deadline_str = openedDate_str + ' 23:59:50'
            openedDate = openedDate + datetime.timedelta(days=30)
            deadline_str = openedDate.strftime('%Y-%m-%d %H:%M:%S')
        return deadline_str

    # 根据解决日期生成问题回归的截止日期
    def regression_deadline(self, resolvedDate):
        '''
        根据不同的时间格式 time_format ，生成需要的实际
        :param time_format: 时间格式：YYYY-MM-DDHH、YYYY-MM-DD、YYYYMM、YYYYQn
        :param days:
        :param week:MONDAY、
        :return:
        '''
        # 获取当前月份
        mouth_str = (datetime.datetime.now()).strftime('%Y-%m')
        mouth_str_20 = mouth_str + '-20'
        mouth_str_19 = mouth_str + '-19'
        mouth_str_15 = mouth_str + '-15'
        mouth_str_25 = mouth_str + '-25'
        mouth_str_5 = mouth_str + '-05'
        # 判断当前时间
        day_str = (datetime.datetime.now()).strftime('%Y-%m-%d')
        deadline = datetime.datetime.now()
        # 创建时间转为str
        openedDate_str = resolvedDate.strftime('%Y-%m-%d')
        # 如果创建时间大于15号
        if mouth_str_5 < openedDate_str < mouth_str_20:
            deadline = resolvedDate + datetime.timedelta(days=5)
        else:
            deadline = resolvedDate + datetime.timedelta(days=20)
        # 对deadline 进行格式化
        deadline_str = deadline.strftime('%Y-%m-%d %H:%M:%S') if type(deadline) != str else deadline
        return deadline_str

    #进行截止时间更新操作
    def update_deadline(self):
        time_now = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        message = u'进行截止时间更新操作，当前操作时间为：%s' %time_now
        print(message)
        # sql = "SELECT * FROM zt_bug t where t.status = 'active' and t.openedBy != 'lixl' and t.id = 10048"
        sql = "SELECT * FROM zt_bug t where t.status = 'active' and t.openedBy != 'lixl' and t.openedDate > '2021-05-30'"
        # sql = "SELECT * FROM zt_bug t where t.openedBy != 'lixl' and t.openedDate > '2021-05-30' and t.id = 11700"
        active_bug_list = db_instances.data_query(sql)
        sql_list = []
        for i in range(len(active_bug_list)):
            deadline_str = self.afirm_deadline_new(active_bug_list[i]['severity'],active_bug_list[i]['openedDate'],active_bug_list[i]['activatedDate'])
            param = {'deadline_str':'\''+deadline_str+'\'','bug_id':active_bug_list[i]['id']}
            update_sql = 'UPDATE zt_bug SET deadline = %(deadline_str)s WHERE id = %(bug_id)s'
            sql_list.append(update_sql %param)
        self.data_insert_update(sql_list)

    #进行截止时间更新操作
    def update_regression_deadline(self):
        sql = "SELECT * FROM zt_bug t where t.status = 'resolved'"
        active_bug_list = db_instances.data_query(sql)
        sql_list = []
        for i in range(len(active_bug_list)):
            deadline_str = self.regression_deadline(active_bug_list[i]['resolvedDate'])
            param = {'deadline_str':'\''+deadline_str+'\'','bug_id':active_bug_list[i]['id']}
            update_sql = 'UPDATE zt_bug SET deadline = %(deadline_str)s WHERE id = %(bug_id)s'
            sql_list.append(update_sql %param)
        self.data_insert_update(sql_list)
        time_now = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        message = u'进行截止时间更新操作，更新完成时间为：%s' % time_now
        print(message)

    #检查当前日期是否包含节假日
    def check_holiday(self,openedDate,dataNum):
        server_url = "http://www.easybots.cn/api/holiday.php?d="
        server_url_2021 = 'http://10.10.64.41:5000/tongtech/holiday/judge?datestr='
        holiday_status = 0
        for i in range(dataNum+1):
            deadline = (openedDate + datetime.timedelta(days=i)).strftime('%Y%m%d')
            server_url = server_url_2021 if deadline >= '20210101' else server_url
            vop_data = {}
            try:
                vop_response = requests.get(server_url+deadline,  verify=True, timeout=10)
                vop_data = json.loads(vop_response.text)
            except Exception as reason:
                print(u'获取接口数据失败')
            if vop_data == {}:
                return holiday_status
            if vop_data[deadline] != '0':
                holiday_status = int(vop_data[deadline])
                return holiday_status
        return holiday_status

    #更新当前
    def catch_bug_status(self):
        '''
        获取当前版本的所有bug的状态，写入到数据库
        :return:
        '''
        #定义一个json串，用来存储所有的状态数据
        bug_status = {'name':'','all_sum':0,'block_sum':0,'serious_sum':0,'hung_up':0,'torequest':0,'normal':0,'active_all':0,'active_block':0,'active_serious':0,'wait_close':0}
        bug_status_list = []
        #定义sql：
        version = '%V21.09%'
        all_sum = "SELECT COUNT(*) as all_sum,p.name,p.id FROM zt_bug b,zt_build p where  b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) GROUP BY b.openedBuild;" %version
        block_sum = "SELECT COUNT(*) as block_sum,p.name FROM zt_bug b,zt_build p where  b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) and b.severity =1 GROUP BY b.openedBuild;" %version
        serious_sum = "SELECT COUNT(*) as serious_sum,p.name FROM zt_bug b,zt_build p where b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) and b.severity =2 GROUP BY b.openedBuild;" %version
        hung_up = "SELECT COUNT(*) as hung_up,p.name FROM zt_bug b,zt_build p where b.`status` = 'resolved' AND b.resolution in ('hangUp') and b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) GROUP BY b.openedBuild;" %version
        torequest = "SELECT COUNT(*) as torequest,p.name FROM zt_bug b,zt_build p where b.`status` = 'resolved' AND b.resolution in ('tostory') and b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) and b.severity =2 GROUP BY b.openedBuild;" %version
        active_all = "SELECT COUNT(*) as active_all,p.name FROM zt_bug b,zt_build p where b.`status` = 'active' and b.deleted = '0' and b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) GROUP BY b.openedBuild;" %version
        active_block = "SELECT COUNT(*) as active_block,p.name FROM zt_bug b,zt_build p where b.`status` = 'active' and b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) and b.severity =1 GROUP BY b.openedBuild;" %version
        active_serious = "SELECT COUNT(*) as active_serious,p.name FROM zt_bug b,zt_build p where b.`status` = 'active' and b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) and b.severity =2 GROUP BY b.openedBuild;" %version
        wait_close = "SELECT COUNT(*) as wait_close,p.name FROM zt_bug b,zt_build p where b.`status` = 'resolved' AND b.resolution not in ('tostory','hangUp') and b.openedBy != 'lixl' and b.openedBuild=p.id and p.id in (SELECT id FROM zt_build t WHERE (t.name like '%s') ) GROUP BY b.openedBuild;" %version
        sql_list = [all_sum,block_sum,serious_sum,hung_up,torequest,active_all,active_block,active_serious,wait_close]
        field_list = ['all_sum','block_sum','serious_sum','hung_up','torequest','active_all','active_block','active_serious','wait_close']
        insert_field_list = ['all_sum','block_sum','serious_sum','hung_up','torequest','normal','active_all','active_block','active_serious','wait_close']

        #获取所有的bug状态写入到json
        for sql_id in range(len(sql_list)):
            print(sql_list[sql_id])
            data_list = self.data_query(sql_list[sql_id])
            if len(data_list) == 0:
                continue
            key_list = list(data_list[0].keys())
            if 'all_sum' in key_list:
                for i in range(len(data_list)):
                    bug_status['name'] = data_list[i]['name']
                    bug_status['all_sum'] = data_list[i]['all_sum']
                    bug_status_bak = copy.deepcopy(bug_status)
                    bug_status_list.append(bug_status_bak)
            else:
                for i in range(len(data_list)):
                    for j in range(len(bug_status_list)):
                        if data_list[i]['name'] == bug_status_list[j]['name']:
                            bug_status_list[j][field_list[sql_id]] = data_list[i][field_list[sql_id]]
                            break
        #进行普通数量的计算获取
        for i in range(len(bug_status_list)):
            bug_status_list[i]['normal'] = bug_status_list[i]['all_sum'] - bug_status_list[i]['block_sum'] - bug_status_list[i]['serious_sum']

        #先进行原始数据清理
        TRUNCATE_SQL = ['TRUNCATE TABLE bug_status']
        # 进行数据库插入更新
        self.data_insert_update(TRUNCATE_SQL)

        #生成sql插入语句
        basic_sql = "INSERT INTO bug_status VALUES ("
        insert_sql_list = []

        for i in range(len(bug_status_list)):
            sql = basic_sql + '\''+bug_status_list[i]['name']+'\''
            for j in range(len(insert_field_list)):
                append_sql = str(bug_status_list[i][insert_field_list[j]]) if type(bug_status_list[i][insert_field_list[j]]) == int else '\''+bug_status_list[i][insert_field_list[j]]+'\''
                sql = sql + ',' + append_sql
            sql = sql + ')'
            insert_sql_list.append(sql)
        #进行数据库插入更新
        self.data_insert_update(insert_sql_list)

if __name__ == '__main__':
    db_instances = db_handle()
    # sql = "SELECT * FROM zt_bug t where t.status = 'active'"
    # db_instances.data_query(sql)
    # time_now = datetime.datetime.now()
    # db_instances.check_holiday(time_now,10)
    # db_instances.update_deadline()
    # db_instances.update_regression_deadline()
    db_instances.catch_bug_status()
