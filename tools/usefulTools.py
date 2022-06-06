#coding=utf-8
import os,datetime,calendar,importlib,json
import sys,string
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
# import pyautogui as pag
import time,copy,smtplib,random,urllib
from email.mime.text import MIMEText
from email.header import Header
# from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart

class userfulToolsFactory():
    def test_check(self,type,str):
        ReportSuccessful = ""
        if ReportSuccessful.decode("utf-8")in str:
            return True
        else:
            return False

    def creat_dir(self,base_dir):
        timestr = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 本地日期时间作为测试报告的名字
        randomStr = str(random.uniform(5,500))
        relative_address = timestr + '-' + randomStr
        os.makedirs(base_dir + relative_address)

        return relative_address

    def update_file_path_deal(self,file_path):
        update_file_path = file_path.replace("/","\\")
        return update_file_path

    def CaseNameOp(self,casetitle):
        startStr = 'u"'
        endStr = ')"'
        CaseName = casetitle[startStr:endStr]
        print (CaseName)

    # 根据传入的数据进行 字符串的处理
    def SubString_handle(self,str_source,startStr,endStr):
        str_source = str(str_source)
        # startNum = str(str_source).find(startStr)
        startNum = str_source.find(startStr)
        # print str_source[startNum:startNum+50]
        if startNum == -1:
            return ''
        #处理空字符串的问题，如果endStr为空，则直接获取起始到最终完结的字符串
        if endStr == '':
            str_result = str(str_source)[startNum + len(startStr):]
            return str_result
        # endNum = str(str_source).find(endStr,startNum+len(startStr))
        endNum = str_source.find(endStr, startNum + len(startStr))
        str_result = str_source[startNum+len(startStr):endNum]
        # print str_result
        return str_result

    #去掉所有的引号、\、u等数据
    def drop_special_character(self,str_source):
        str_target = str(str_source).replace('\\','').replace('u\'','').replace('u"','').replace('\'','').replace('"','').replace(' ','')
        return str_target


    # 对接口响应的字符串进行获取，根据传入的字段名称，返回列表
    def SubString_handle_mutil(self, response_data, start_str,end_str):
        str_source = (response_data)
        # 定义返回值列表
        field_data_list = []
        # 定义起始的endNum值为0
        endNum = 0
        for i in range(str_source.count(start_str)):
            startNum = str_source.find(start_str, endNum)
            endNum = str_source.find(end_str, startNum)
            field_data = str_source[startNum + len(start_str):endNum]
            field_data_list.append(field_data)
        return field_data_list

    #处理从数据库中查询到的数据，去掉(,)字符，并返回
    def db_data_deal(self,db_data):
        startnum = str(db_data).find('(')
        endnum = str(db_data).find(',)')
        format_date = str(db_data)[startnum+1:endnum]
        return format_date

    #根据传入的参数进行比对，检查是否该案件在 某个 授权阶段
    def accredit_status_check(self,item_menu_set,accredit_tpye):
        if accredit_tpye in str(item_menu_set):
            return True
        else:
            return False
    #根据鼠标的位置，获取当前屏蔽的当前位置的坐标，在Linux运行不了，暂时禁用和GUI有关的操作
    # def get_current_position(self):
    #     try:
    #         while True:
    #             print "Press Ctrl-C to end"
    #             x, y = pag.position()
    #             posStr = "Position:" + str(x).rjust(4) + ',' + str(y).rjust(4)
    #             print posStr
    #             time.sleep(0.2)
    #             os.system('cls')
    #             print u'当前坐标为：' + str(x) + ' , ' + str(y)
    #     except  KeyboardInterrupt:
    #         print 'end....'

    #检查url是否可以正常访问
    def url_get_check(self,url):
        # url = 'http://123.57.173.230:8081/MediaRoot/rec/20170927/1057/415da01a-359b-49ec-a13a-f8523ddfead5/1057123.png?1506492179156'
        resp = urllib.urlopen(url)
        code = resp.getcode()
        print('the result is :', code)
        if code == 200:
            return True
        else:
            return False

    #获取并修改接口显示名称
    def get_interface_name(self,interface_path):
        print (u'输入的接口地址为：%s' % interface_path)
        interface_path_str = str(interface_path)
        #接口地址的格式为/***/***,获取到最后一个 '/'，并返回'/'后的内容,使用 rfind功能可以获取到最后一个，使用find功能是获取的第一个
        strStartNum = interface_path_str.rfind('/')
        interface_name = interface_path_str[strStartNum+1:]
        #针对请求地址包含.的接口，把.替换为_显示，否则会建表失败
        interface_name = interface_name.replace('.','_')
        return interface_name

    #对字符串进行特殊处理，两边加上''
    def String_special_handling(self,hand_str):
        special_handling_result = '\'' + str(hand_str) + '\''
        return special_handling_result

    #对接口响应的字符串进行获取，根据传入的字段名称，返回列表
    def response_data_handle(self,interface_response_data,field_name):
        str_source = str(interface_response_data)
        #定义需要获取的字段起始字符以及结束字符，结束字符可能为 , 或是 }，暂时不考虑 dict的格式
        startStr = '\"'+str(field_name) + '\":'
        endStr1 = ','
        endStr2 = '}'
        #定义返回值列表
        field_data_list = []
        #定义起始的endNum值为0
        endNum = 0
        for i in range(str_source.count(startStr)):
            startNum = str_source.find(startStr,endNum)
            if str_source.find(endStr1) != -1:
                endNum = str_source.find(endStr1,startNum)
            else:
                endNum = str_source.find(endStr2,startNum)
            field_data = str_source[startNum+len(startStr):endNum]
            field_data_list.append(field_data)
        return field_data_list

    #从测试结果中获取总的结果
    def get_result_form_file(self,result_file,result_type):
        htmlfile = open(result_file, 'r')
        htmlpage = htmlfile.read()
        soup = BeautifulSoup(htmlpage, "html.parser")
        # number = self.SubString_handle(soup,result_type.encode('utf-8'),' }'.encode('utf-8'))
        str_source = str(soup)
        start_num = str_source.find(result_type)
        end_num = str_source.find(' }',start_num)
        number = str_source[start_num + len(result_type)/2:end_num]
        # print number
        return number

    #发送邮件
    def send_email_via_smtp(self,title,test_result,basic_filename,report_file_name,receiver_list=None):
        timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        timedate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        test_result['timestr'] = timestr
        test_result['timedate'] = timedate
        # 发送人邮件地址
        # sender = u'lijq1229@126.com'
        sender = u'lijunqiang@qingyangkeji.cn'
        # 群发接收人邮件地址 !!!!!
        # receiver = u'lijunqiang@qingyangkeji.cn;463380250@qq.com;2416011337@qq.com,lijq1229@126.com'
        # print receiver_list
        if receiver_list is None or len(receiver_list) == 0:
            # receiver_list = [u'lijunqiang@qingyangkeji.cn',u'463380250@qq.com',u'lijq1229@126.com']
            receiver_list = [u'lijunqiang@qingyangkeji.cn']
        cc_list = [u'lijunqiang@qingyangkeji.cn']
        if len(receiver_list) > 1:
            cc_list = [u'cenyonghong@qingyangkeji.cn',u'zhangqing@qingyangkeji.cn',u'wangjian@qingyangkeji.cn']
            # cc_list = [u'lijunqiang@qingyangkeji.cn',u'zhangqing@qingyangkeji.cn',u'humeng@qingyangkeji.cn']

        # # smtp服务 - 126邮箱
        # smtpserver = u'smtp.126.com'
        # smtp服务 - 阿里云 邮箱
        smtpserver = u'smtp.aliyun-inc.com'
        # 发送人邮件用户名或专用于smtp账户用户名
        # username = u'lijq1229'
        username = u'lijunqiang@qingyangkeji.cn'
        # 发送人邮件密码或专用于smtp账户的密码
        # password = u'wuhan2011'
        password = u'wuhan2011!'
        # 创建message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title.decode('utf-8')
        # 发送内容
        text = u"result"
        html = u"""
                  大家好，%(timedate)s接口测试结果如下：\n <br/>
                  <br/>
                  本次执行的测试用例-总数：%(all_test_number)s； <br/>
                  测试用例执行-通过-的数量：\n %(pass_num)s； <br/>
                  测试用例执行-失败-的数量：\n %(failed_num)s； <br/>
                  测试用例执行-错误-的数量：\n %(error_num)s； <br/>
                  <br/>
                  生成测试报告测试时间：\n %(timestr)s <br/>
                  <br/>
                  具体测试详情结果请查看附件文档，稍后我会进行结果分析，如果有问题会与对应的开发及时沟通\n<br/>
                  <br/>
                  相关的开发人员如果有接口改动也请提前告知\n<br/>
             """
        html_param = {'partner_number':10,'pass':20,'fail':10}
        # 添加MIME类型
        partText = MIMEText(text, u'plain'.decode('utf-8'),_charset = 'utf-8')
        # partHTML = MIMEText(html %test_result, u'html'.decode('utf-8'),_charset = 'utf-8')
        partHTML = MIMEText(html %test_result, _subtype='html',_charset = 'utf-8')
        msg.attach(partText)
        msg.attach(partHTML)
        # 构造附件
        attach = MIMEText(open(report_file_name,'rb').read(), 'base64', 'utf-8')
        attach['Content-Type'] = 'application/octet-stream'
        # attach['Content-Disposition'] = 'attachment;filename= \"'+ basic_filename +'\"'
        attach.add_header('Content-Disposition', 'attachment', filename=basic_filename)
        msg.attach(attach)
        msg['from'] = sender
        # msg['to'] = receiver
        # 发送邮件
        smtp = smtplib.SMTP()
        #添加Linux安全邮件校验方案
        smtp_ssl = smtplib.SMTP_SSL()
        # smtp.connect('smtp.126.com')
        # smtp.connect('smtp.qingyangkeji.cn')
        # smtp.login(username, password)
        smtp_ssl.connect('smtp.qingyangkeji.cn')
        smtp_ssl.login(username, password)
        # smtp.sendmail(sender, receiver, msg.as_string())
        msg['to'] = ','.join(receiver_list)
        msg['cc'] = ','.join(cc_list)
        toaddrs = receiver_list + cc_list
        # smtp_ssl.sendmail(sender, receiver_list, msg.as_string())
        smtp_ssl.sendmail(sender, toaddrs, msg.as_string())
        # for i in range(len(receiver_list)):
        #     msg['to'] = receiver_list[i]
        #     smtp_ssl.sendmail(sender, receiver_list[i], msg.as_string())
        smtp_ssl.quit()

    #修改文章内容
    def replace_file_context(self,replace_file_path, old_str, new_str):
        try:
            f = open(replace_file_path, 'r+')
            all_lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in all_lines:
                line = line.replace(old_str, new_str)
                f.write(line)
            f.close()
            print (u'文件替换成功....旧的内容：%s' %old_str,u'....新的内容：%s' %new_str)
        except Exception as reason:
            print (reason)

    #给文章写入内容
    def add_file_context(self,file_name,position_str,file_context):
        Constant_file = open(file_name,'r')
        Constant_Context = Constant_file.read()
        insert_position = Constant_Context.find(position_str)
        insert_position = insert_position + len(position_str)
        if insert_position == -1:
            print (u'未找到需要插入的文件的位置')
            return 0
        Constant_Context = Constant_Context[:insert_position] + file_context + Constant_Context[insert_position:]
        Constant_file = open(file_name,'w')
        Constant_file.write(Constant_Context)
        Constant_file.close()
        print (u'写入文件完成')

    #Unicode 转换list
    def dic_unicode_list(self,unicode_str):
        unicode_str_original = str(unicode_str)
        #原始数据：[{"impCount":"2916","_id":"sina.com","clkCount":"584","puburl":"sina.com"},{"impCount":"1895","_id":"home.odinlink.com","clkCount":"0","puburl":"home.odinlink.com"},{"impCount":"208","_id":"sohu.com","clkCount":"50","puburl":"sohu.com"}]
        #转换为list的时候，先进行替换}, --> }},
        result_list = unicode_str_original.replace('},','}},').replace('[','').replace(']','').split('},')
        return result_list

    #随机生成手机号码，根据位数生成
    def make_random_str(self,number):
        result = '13'
        for i in range(number - 2):
            result = result + str(random.randint(0,9))
        return result

    #处理None为空
    def NoneTransitStr(self,param):
        param = param if param is not None else ''
        return param
    #处理htmlrunner返回的结果，需要传入case列表、结果

    #时间戳转换为标准时间
    def strftime_standard(self,time_stamp):
        '''
        # 转换成localtime（毫秒级别的时间戳转换需要先 /1000）
        time_local = time.localtime(timestamp/1000)
        # 转换成新的时间格式(精确到秒)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        :param time_stamp:
        :return:
        '''
        # 转换成localtime
        time_local = time.localtime(time_stamp / 1000)
        # 转换成新的时间格式(精确到秒)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

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

    def make_strftime(self,time_format,days,week):
        '''
        根据不同的时间格式 time_format ，生成需要的实际
        :param time_format: 时间格式：YYYY-MM-DDHH、YYYY-MM-DD、YYYYMM、YYYYQn
        :param days:
        :param week:MONDAY、
        :return:
        '''
        week_list = {'MONDAY':0,'TUESDAY':1,'WEDNESDAY':2,'THURSDAY':3,'FRIDAY':4,'SATURDAY':5,'SUNDAY':6}
        time_format_list = {'YYYY-MM-DDHH':'%Y-%m-%d%H','YYYY-MM-DD':'%Y-%m-%d','YYYYMM':'%Y%m','YYYYQn':'%m','YYYY':'%Y'}
        #如果week不为空，循环从当前日期进行减一天的操作进行比对，today.weekday()可以获取当前的日期为周几
        week = week if week in week_list.keys() else ''
        if week != '':
            days = 0
            oneday = datetime.timedelta(days=1)
            today = datetime.date.today()
            for i in range(7):
                if today.weekday() != week_list[week]:
                    today = today - oneday
                    days = days - 1
                    continue
                break
        #获取 time_format_list 列表的key，如果time_format 在列表中，则重新获取
        if time_format == 'YYYYQn':
            time_format = time_format_list[time_format]
            Qn = (int((datetime.datetime.now()).strftime(time_format))-1)/3 + 1
            timestr = (datetime.datetime.now()).strftime('%Y') + str(Qn)
            return timestr
        time_format_list_keys = time_format_list.keys()
        if time_format in time_format_list_keys:
            time_format = time_format_list[time_format]
        timestr = (datetime.datetime.now() + datetime.timedelta(days=int(days))).strftime(time_format)
        print (timestr)
        return timestr

    #从列表中去掉一部分内容
    def drop_list_context(self,source_list,dorp_list):
        for drop_item in dorp_list:
            for i in range(len(source_list)):
                for j in range(len(source_list)):
                    if drop_item in source_list[j]:
                        source_list.pop(j)
                        break
        return source_list

    #随机生成一串字符串，包含特殊字符
    def ranstr(self,num):
        # 猜猜变量名为啥叫 H
        special_character= '$_'
        target_str = ''.join(random.sample(string.ascii_letters + string.digits, num))
        target_str = target_str + random.choice(special_character)
        # print(target_str)
        return target_str

    # 处理字符串，加入'',传入的是一个列表，对列表中所有字符串格式的内容进行加引号处理
    def quoted_string(self, quoted_list):
        '''
        主要是为了处理sql查询的时候需要的一些字符串中的引号问题，可以传入单个字符串，也可以传入列表格式
        :param quoted_list:
        :return:
        '''
        if type(quoted_list) == str and quoted_list == 'NOW()':
            return quoted_list
        try:
            quoted_list = quoted_list.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as reason:
            pass
        if type(quoted_list) == str:
            return '\'' + quoted_list + '\''
        if type(quoted_list) != str and type(quoted_list) != list:
            return quoted_list
        for i in range(len(quoted_list)):
            if type(quoted_list[i]) == dict:
                quoted_list[i] = json.dumps(quoted_list[i],ensure_ascii=False)
            if type(quoted_list[i]) != str:
                continue
            if quoted_list[i] == 'NOW()':
                continue
            quoted_list[i] = '\'' + quoted_list[i] + '\''
        return quoted_list

    #处理列表中的参数，全部转换为str
    def list_transt_str(self,source_list):
        '''
        list中包含各种类型的内容，除了int类型外，全部转换为str
        :param source_list:
        :return:
        '''
        for i in range(len(source_list)):
            if type(source_list[i]) == list:
                source_list[i] = ','.join('%s' % id for id in source_list[i])
                continue
            # if source_list[i] == str:
            #     continue
            if type(source_list[i]) == dict:
                source_list[i] = json.dumps(source_list[i],ensure_ascii=False)
                continue
        return source_list

    #检查必填参数是否存在
    def check_param_exist(self,param_list,param_json):
        '''
        根据传入的list和json来判断，当前的list是否都在json中
        :param param_list:
        :param param_json:
        :return:
        '''
        param_noExist = []
        #进行格式校验：
        if type(param_list) != list:
            return param_noExist
        if type(param_json) != dict:
            return ['参数异常']
        param_json_kyes = list(param_json.keys())
        for i in range(len(param_list)):
            if param_list[i] in param_json_kyes:
                continue
            param_noExist.append(param_list[i])
        return param_noExist

    #根据post请求的参数生成查询条件
    def create_query_condition(self,param_json):
        query_condition = []
        if type(param_json) != dict:
            return query_condition
        param_json_kyes = list(param_json.keys())
        for i in range(len(param_json_kyes)):
            if param_json_kyes[i] in ['curPage','pageSize']:
                continue
            # if 'title' in param_json_kyes[i] or 'desc' in param_json_kyes[i] or 'Tag' in param_json_kyes[i]:
            if param_json_kyes[i] in ['case_title','iface_name','case_desc','iface_desc']:
                condition = '&&' + param_json[param_json_kyes[i]] + '&&'
                query_infor = {'field_name': param_json_kyes[i], 'filed_concatenation': 'LIKE','field_value': condition}
                query_condition.append(copy.deepcopy(query_infor))
                continue
            query_infor = {'field_name': param_json_kyes[i], 'filed_concatenation': '=', 'field_value': param_json[param_json_kyes[i]]}
            query_condition.append(copy.deepcopy(query_infor))
        return query_condition


if __name__ == '__main__':
    test = userfulToolsFactory()
    # test.make_strftime('YYYYQn','','MONDAY')
    # test.ranstr(5)
    # userfulToolsFactory.creat_dir(test,'D://Cruise//pythonSrc//reprot//')
    # case = 'u"StartTest(/''login_egova/'')"'
    # test.CaseNameOp(case)
    # test.update_file_path_deal('D:/SVN/V15/zx2016/Client/Python/eUrbanMIS/updatefile/9.jpg')
    # test.Oracel_data_deal('(1234,)')
    # test.get_current_position()
    # str_source = '案件登记 （任务号：201709120001）'
    # start = '：'
    # end = '）'
    # interface_path = '/home/mis/eventtype/gettypebyrectypeid'
    # test.SubString_handle(str_source,start,end)
    # unittest.main()\
    # test.get_interface_name(interface_path)
    # email_title_Insurance = '保单查询测试结果' + '2018-03-06'
    # test_result = {'all_partner_number': 10, 'all_number': 20, 'pass_num': 15,'failed_num': 5}
    # basic_file = 'test_0306_result'
    # test.send_email_via_smtp(email_title_Insurance,test_result,basic_file)
    # test.get_result_form_file('D:\\git-source\\autoFrameIntegration\\Result\\2018-03-05 19-32-35report.html','所有{ ')
    # context = "\n{'phone': '15543406645', 'password': 'd52f01bc80e5115cb9edb46353857effd2adebc7b3b87fade5ee3b50e8c4c864','userName': u'15543406645'},"
    # position_str = 'submit_login_update = ['
    # test.add_file_context('D:\SVN\\test.txt',position_str,context)
    # filename = 'D:\\git-source\\qingyangIF\\Result\\20190828_194720_report.html'
    # test.get_result_form_file(filename,u'所有{ ')
    # receiver = u'lijunqiang@qingyangkeji.cn,463380250@qq.com,2416011337@qq.com,lijq1229@126.com'
    # receiver_list = receiver.split(',')
    # print (receiver_list)
    test_json = {'test':1,"test2":2,'test3':'test11111'}
    # test.check_param_exist([],test_json)
    test.create_query_condition(test_json)



