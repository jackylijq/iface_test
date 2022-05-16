#coding=utf-8
import os
import sys,json,random,urllib,time,copy,hashlib,datetime,importlib
from tools import switch
importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
from conf import settings,cabinet_client_constant,constant
from  po import  basic_http_request
from tools import qy_db_manager,usefulTools,switch
from test_case import common_request



#参数实例化
basic_http_request_instances = basic_http_request.basic_http_request()
qy_db_manager_instances = qy_db_manager.database_operate()
usefulTools_instances = usefulTools.userfulToolsFactory()
common_request_instances = common_request.basic_operate()
factory_basic_operate_instances = factory_basic_operate.basic_operate()
iot_basic_operate_instances = iot_basic_operate.basic_operate()
logistics_basic_operate_instances = logistics_basic_operate.basic_operate()
iface_list = cabinet_client_constant.iface_list
iface_param = cabinet_client_constant.iface_param
user_infor = cabinet_client_constant.common_parameter.user_list[settings.cabinet_client_user_id]
web_user_infor = constant.common_parameter.web_user_list[settings.web_user_id]

basic_headers = {'Content-Type':'application/json','Authorization':''}

class basic_operate():
    #获取最基础的header信息,通用获取headers：token、from信息
    def get_headers(self,user_id):
        headers = basic_headers
        # headers['From'] = 'Android'
        # headers['Content-Type'] = 'application/x-www-form-urlencoded'
        if type(user_id) != type(0) and len(user_id) > 10:
            headers['Authorization'] = 'Bearer ' + user_id
            return headers
        if user_id == '':
            return headers
        # headers['From'] = cabinet_client_constant.common_parameter.user_list[int(user_id)]['From']
        headers['Authorization'] = 'Bearer ' + cabinet_client_constant.common_parameter.user_list[int(user_id)]['access_token']
        return headers

    #基础的接口请求服务
    def basic_iface_request(self,user_infor,iface_infor,params,*args):
        if user_infor == '':
            user_infor = settings.cabinet_client_user_id
        if user_infor == 'test_none':
            user_infor = ''
        headers = self.get_headers(user_infor)
        request_param ={}
        Basic_response = ''
        for i in range(len(args)):
            request_param[params[i]] = args[i]
        request_url = settings.cabinet_client_url + iface_infor['url']
        #进行判断是什么类型的请求,进行数据请求：
        time_compare = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
        message =  u'请求时间：',time_compare,u'接口方法类型：',iface_infor['method']
        for method in switch.basic_switch(iface_infor['method']):
            if method('GET'):
                Basic_response = basic_http_request_instances.basic_get_request(request_url, request_param, headers)
            if method('POST'):
                request_param = json.dumps(request_param)
                Basic_response = basic_http_request_instances.basic_post_request(request_url, request_param, headers)
            if method('PUT'):
                Basic_response = basic_http_request_instances.basic_put_request(request_url, request_param, headers)
            if method('DELETE'):
                request_param = json.dumps(request_param)
                Basic_response = basic_http_request_instances.basic_delete_request(request_url, request_param, headers)
        # Basic_response = basic_http_request_instances.basic_get_request(request_url, request_param, headers)
        if Basic_response == 0:
            message =  u'3次接口请求，网络请求异常，返回为0，直接返回为0'
            return 0
        message =  Basic_response.text
        Basic_response_json = json.loads(Basic_response.text)
        return Basic_response_json

    #生成充值记录
    def make_recharge_list(self):
        timestr = time.strftime('%Y%m%d-%H', time.localtime(time.time()))
        #获取可充值金额
        rechargeSchemes = self.basic_iface_request('',iface_list.queryRechargeSchemes,iface_param.queryRechargeSchemes)
        random_int = random.randint(0,len(rechargeSchemes))
        #调用充值接口
        self.basic_iface_request('',iface_list.recharge,iface_param.recharge,rechargeSchemes['data'][random_int]['id'],100)
        # 从数据库获取基础数据
        db_param = [
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
            {'field_name': 'commited', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'created_at', 'filed_concatenation': '=', 'field_value': '\'&&'+timestr+'&&\''},

        ]
        qy_db_manager_instances.update_table_data_sigle('wechat_api', 'recharges', 'commited',1,db_param)

    # 创建优惠券
    def create_exchange_code(self,coupon_type_text,coupon_type):
        #coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
        #coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
        #price：价格，传入的情况下获取 min_price > price 的数据
        timestr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        exchange_code_list = []
        # 先获取可用优惠券列表
        coupon_code_param_list = qy_db_manager_instances.get_coupon_list(coupon_type_text,coupon_type,'')
        # coupon_activity_list = []
        cycle_num = 10 if len(coupon_code_param_list) > 10 else len(coupon_code_param_list)
        for i in range(cycle_num):
            db_param_activity = [
                {'field_name': 'status', 'filed_concatenation': '=', 'field_value': '1'},
                {'field_name': 'end_time', 'filed_concatenation': '>', 'field_value': '\'' + timestr + '\''},
            ]
            #定义查询优惠券的类型：通用/自助洗/干洗
            coupon_condition = {}
            if coupon_code_param_list[i]['common_coupon_id'] != '':
                coupon_condition = {'field_name': 'common_coupon_id', 'filed_concatenation': '=','field_value': coupon_code_param_list[i]['id']}
            if coupon_code_param_list[i]['delivery_coupon_id'] != '':
                coupon_condition = {'field_name': 'delivery_coupon_id', 'filed_concatenation': '=','field_value': coupon_code_param_list[i]['id']}
            if coupon_code_param_list[i]['coupon_id'] != '':
                coupon_condition = {'field_name': 'coupon_id', 'filed_concatenation': '=','field_value': coupon_code_param_list[i]['id']}
            db_param_activity.append(coupon_condition)
            coupon_activity_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'coupon_activity','created_time', db_param_activity)
            # 如果活动没获取到，则自动创建活动
            if len(coupon_activity_list) == 0:
                common_request_instances.add_coupon_activity(web_user_infor['access_token'],coupon_code_param_list[i])
                coupon_activity_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'coupon_activity','created_time',db_param_activity)
            #根据活动查询是否有未兑换的code
            db_param_code = [
                {'field_name': 'user_id', 'filed_concatenation': 'is', 'field_value': 'NULL'},
                {'field_name': 'coupon_activity_id', 'filed_concatenation': '=','field_value': coupon_activity_list[0]['id']},
            ]
            coupon_code_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'coupon_code_list','created_time', db_param_code)
            #如果没有可兑换code，则进行发码操作
            if len(coupon_code_list) == 0:
                # 根据活动进行发码：
                message =  u'根据可用的活动，进行发码'
                code_cycle = 1 if len(coupon_code_param_list) > 2 else 10 / len(coupon_code_param_list) + 1
                common_request_instances.generate_code(web_user_infor['access_token'],code_cycle, coupon_activity_list[0]['id'])
                # 获取最新的兑换码进行兑换
                db_param_code = [
                    {'field_name': 'user_id', 'filed_concatenation': 'is', 'field_value': 'NULL'},
                    {'field_name': 'coupon_activity_id', 'filed_concatenation': '=','field_value': coupon_activity_list[0]['id']},
                ]
                coupon_code_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'coupon_code_list', 'created_time', db_param_code)
            for j in range(len(coupon_code_list)):
                random_int = random.randint(0,len(coupon_code_list)-1)
                coupon_code_list[random_int]['coupon_type_text'] = coupon_code_param_list[i]['coupon_type_text']
                coupon_code_list[random_int]['coupon_id'] = 0
                coupon_code_list[random_int]['delivery_coupon_id'] = 0
                coupon_code_list[random_int]['common_coupon_id'] = 0
                if coupon_code_param_list[i]['coupon_type_text'] == 0:
                    coupon_code_list[random_int]['common_coupon_id'] = coupon_code_param_list[i]['id']
                if coupon_code_param_list[i]['coupon_type_text'] == 1:
                    coupon_code_list[random_int]['delivery_coupon_id'] = coupon_code_param_list[i]['id']
                if coupon_code_param_list[i]['coupon_type_text'] == 2:
                    coupon_code_list[random_int]['coupon_id'] = coupon_code_param_list[i]['id']
                coupon_code_list[random_int]['money'] = coupon_code_param_list[i]['min_money']
                coupon_code_list[random_int]['start_time'] = coupon_code_param_list[i]['start_time']
                coupon_code_list[random_int]['end_time'] = coupon_code_param_list[i]['end_time']
                coupon_code_list[random_int]['activity_out_id'] = coupon_activity_list[0]['out_id']
                coupon_code_bak = copy.deepcopy(coupon_code_list[random_int])
                exchange_code_list.append(coupon_code_bak)
                break
        return exchange_code_list

    #生成需要的优惠券
    def make_coupon_data(self,coupon_type_text,coupon_type):
        # coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
        # coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
        #生成兑换码
        exchange_code_list = self.create_exchange_code(coupon_type_text,coupon_type)
        # 进行验证码领取操作
        message =  u'进行兑换码领取操作。。。。。'
        for i in range(len(exchange_code_list)):
            if exchange_code_list[i]['coupon_type_text'] !=2:
                self.basic_iface_request('',iface_list.exchangeCoupon,iface_param.exchangeCoupon,exchange_code_list[i]['code'])

    #根据需要生成订单
    def make_order_according_need(self,good_type,order_coupon_infor,order_status=None):
        # good_type:单件洗:goods,活动：activity
        # good_status：online、offline、delete
        # coupon_infor = {'use_coupon':'YES','coupon_type_text':'','coupon_type':'','order_infor':'','pay_status':'','payPrice':1}
        # coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
        # coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
        # order_infor:社区洗：订单价格，根据价格进行优惠券获取，自助洗：number、service_id
        # pay_status:优惠券可支付金额 与 订单金额比较，above:订单金额>优惠券金额，below订单金额<=优惠券金额
        # #order_status={'status': 0, 'pay_status': 1,'orders_status_process':'','balance_status':'','risk':''}订单的实际状态
        goods_online = []
        activity_online = []
        order_number = 0
        goods = []
        comment = ''
        timestr = time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time()))
        coupon_infor = {'id': '', 'discount': 0}
        order_price = 0
        #good_type 如果不传，默认给单件洗
        if good_type == '':
            good_type = 'goods'
        for good_type in switch.basic_switch(good_type):
            if good_type('goods'):
                comment = u'自动生成订单，单件洗，时间：' + str(timestr)
                goods_online = qy_db_manager_instances.get_goodInfor_accordingNeed('goods','online','')
                for i in range(3):
                    # random_goods = random.randint(0, len(goods_online) - 1)
                    random_goods = random.randint(0, 20)
                    random_int = random.randint(1, 1)
                    goods_infor = {"goodsId": goods_online[random_goods]['id'], "amount": random_int, "activityId": ''}
                    # 计算总价
                    order_price = order_price + goods_online[random_goods]['price'] * random_int
                    goods_infor_bak = copy.deepcopy(goods_infor)
                    goods.append(goods_infor_bak)
            if good_type('activity'):
                comment = u'自动生成订单，活动，时间：' + str(timestr)
                activity_online = qy_db_manager_instances.get_goodInfor_accordingNeed('activity', 'online', 'old')
                for i in range(100):
                    random_activity = random.randint(0, len(activity_online) - 1)
                    activityId = activity_online[random_activity]['id']
                    # 判断activityId 是否已经达到order_limit 上限
                    order_id_list = '(' + 'SELECT id FROM orders where user_id = ' + user_infor['user_id'] + ' and status!=-1' + ')'
                    db_param = [
                        {'field_name': 'goods_activity_id', 'filed_concatenation': '=', 'field_value': activityId},
                        {'field_name': 'order_id', 'filed_concatenation': 'in', 'field_value': order_id_list},
                    ]
                    order_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'order_detail','created_at', db_param)
                    if activity_online[random_activity]['order_limit'] !=0 and len(order_detail_list) == activity_online[random_activity]['order_limit']:
                        continue
                    activity_infor = {"goodsId": '1', "amount": '1',"activityId": activity_online[random_activity]['id']}
                    # 先把总价赋值给支付金额，如果有优惠券，则重新计算
                    order_price = activity_online[random_activity]['activity_price']
                    activity_infor_bak = copy.deepcopy(activity_infor)
                    goods.append(activity_infor_bak)
                    break
        # 根据需求进行优惠券的获取
        # if order_coupon_infor['use_coupon'] == 'YES' or order_coupon_infor['use_coupon'] >0:
        if order_coupon_infor['coupon_money'] > 0:
            coupon_type_text = order_coupon_infor['coupon_type_text']
            coupon_type = order_coupon_infor['coupon_type']
            order_infor = float(order_price)
            pay_status = order_coupon_infor['pay_status']
            coupon_use_infor = self.get_coupon_accrodingOrder(coupon_type_text, coupon_type,order_infor, pay_status)
            if coupon_use_infor != 0:
                coupon_infor = coupon_use_infor
            else:
                message =  u'未获取到优惠券，按照优惠券为空进行数据提交'
        response_infor_json = self.basic_iface_request('',iface_list.createOrder,iface_param.createOrder,goods, coupon_infor['id'], comment)
        if response_infor_json['status'] == 200:
            order_number = response_infor_json['data']['orderNumber']
        #根据order_number 获取订单详情
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=', 'field_value': order_number},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',db_param)
        if order_status is None:
            return order_number
        if order_status['status'] == -1:
            message =  u'进行订单取消操作'
            self.basic_iface_request('',iface_list.cancelOrder,iface_param.cancelOrder,order_number)
            return order_number
        if order_status['pay_status'] == 1:
            message =  u'进行支付请求,使用余额支付'
            #进行用户余额更新，直接使用order_price进行更新
            qy_db_manager_instances.update_user_infor(user_infor['phone'],order_price,order_price,order_price*2)
            #进行支付请求：
            orderPay = self.basic_iface_request('',iface_list.orderPay,iface_param.orderPay,order_number,'balance','0')
            if orderPay['status'] != 200:
                raise (u'支付失败,调用orderPay接口进行支付，返回400')
        if order_status['status'] == 0:
            return order_number
        message =  u'进行柜子预约操作'
        self.basic_iface_request('',iface_list.assignBox,iface_param.assignBox,order_number,settings.cabinetId)
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'ASSIGNED_BOX':
            return order_number
        message =  u'进行扫码开柜操作'
        # qrcode_base = 'https://cabinet-api.funxi.cn/cabinet?id=027131_'
        # time_str = str(int(time.time()-60))
        # qrcode = qrcode_base + time_str
        # openBoxWithQrcode = self.basic_iface_request('', cabinet_client_constant.iface_list.openBoxWithQrcode,iface_param.openBoxWithQrcode, order_number, qrcode, '', '')
        openBoxWithQrcode = self.openBoxWithQrcode(order_number,settings.cabinetId)
        if openBoxWithQrcode['status'] != 200:
            raise(u'扫码开柜失败,调用扫码开柜接口返回400')
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'DELIVERY_PICKUP':
            return order_number
        #管家取出脏衣...................................................................................
        rfId_list = qy_db_manager_instances.get_sealNumber_rfId()
        #循环调用管家取衣接口，直到取到自己的衣物
        seal_number = ''
        for i in range(20):
            seal_number = iot_basic_operate_instances.manager_out_dirty(settings.cabinetId,rfId_list,1)
            # 根据order_number 获取订单详情
            db_param = [
                {'field_name': 'source_number', 'filed_concatenation': '=', 'field_value': seal_number},
            ]
            order_receipt_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_receipt', 'created_at', db_param)
            if order_receipt_list[0]['order_id'] == order_list[0]['id']:
                break
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'DELIVERY_PICKUPED':
            return order_number
        #到达工厂.......................................................................................
        factory_basic_operate_instances.clothes_arrive_factory(seal_number)
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'ARRIVED_FACTORY':
            return order_number
        #进行分拣操作
        factory_basic_operate_instances.clothes_store_wash(seal_number,order_list[0]['id'],order_status['balance_status'],order_status['risk'])
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'SORTED_AND_WASH':
            return order_number
        #根据封签号进行上挂操作
        receiptId = factory_basic_operate_instances.racking_accord_rfId(seal_number,order_list[0]['id'])
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'UP_HOOKS':
            return order_number
        #根据上挂ID进行打包操作,当前只打包一个包裹，如果多包裹后续在完成订单部分重新调用
        package_num = factory_basic_operate_instances.factory_packing(receiptId)
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'PACKED':
            return order_number
        #进行出厂操作
        logistics_basic_operate_instances.logistics_dealWith_package(receiptId,'OUT_FACTORY')
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'OUT_FACTORY':
            return order_number
        #管家进行净衣入柜
        logistics_basic_operate_instances.logistics_dealWith_package(receiptId, 'WAIT_USER_RECEIVE')
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'WAIT_USER_RECEIVE':
            return order_number
        # #用户扫码取净衣
        # time_str = str(int(time.time()-60))
        # qrcode = qrcode_base + time_str
        # self.basic_iface_request('', cabinet_client_constant.iface_list.openBoxWithQrcode,iface_param.openBoxWithQrcode, order_number, qrcode, '', '')
        # if order_status['status'] == 1 and order_status['orders_status_process'] == 'USER_OUT_ClEAN':
        #     return order_number
        #已部分取衣的情况
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'user_pickup_part':
            self.openBoxWithQrcode(order_number,settings.cabinetId)
            return order_number
        #如果为多包裹同时到达状态，需要重复调用打包、出厂、存衣操作
        if order_status['status'] == 1 and order_status['orders_status_process'] == 'mutil_package_ar':
            self.order_done_operate(receiptId,seal_number,package_num-1,order_list[0]['id'])
            return order_number
        #如果是完成状态，重复调用取衣操作
        if order_status['status'] == 2:
            message =  u'重复进行取衣操作'
            for i in range(package_num):
                self.openBoxWithQrcode(order_number,settings.cabinetId)

    #打包、出厂、存衣、取衣操作
    def order_done_operate(self,receiptId,seal_number,package_num,order_id):
        message =  u'循环进行订单的打包、出厂、存衣操作'
        #循环调用打包、出厂、存衣、取衣操作
        # for i in range(package_num):
        factory_basic_operate_instances.racking_accord_rfId(seal_number,order_id)
        factory_basic_operate_instances.factory_packing(receiptId)
        logistics_basic_operate_instances.logistics_dealWith_package(receiptId,'')

    #进行清柜操作
    def clean_box_accordOrder(self,order_number):
        message =  u'进行柜子的清理操作'
        #先调用iot进行脏衣取出
        seal_number = ''
        order_id = 0
        rfId_list = qy_db_manager_instances.get_sealNumber_rfId()
        for i in range(24):
            seal_number = iot_basic_operate_instances.manager_out_dirty(settings.cabinetId,rfId_list,1)
            if seal_number ==0:
                message =  u'干洗柜无脏衣可取，直接异常处理'
                raise (u'根据order_number未获取到封签ID，柜子不存在该订单的衣物')
            db_param = [
                {'field_name': 'number', 'filed_concatenation': '=', 'field_value': '\''+order_number+'\''},
            ]
            order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
            db_param = [
                {'field_name': 'source_number', 'filed_concatenation': '=', 'field_value': '\''+seal_number+'\''},
            ]
            factory_receipt_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_receipt', 'id', db_param)
            #检查order_id 是否等于封签绑定的ID，等于，则说明已经柜子已经释放
            if order_list[0]['id'] == factory_receipt_list[0]['order_id']:
                order_id = order_list[0]['id']
                break
            else:
                order_id = factory_receipt_list[0]['order_id']
                # 根据 seal_number 进行封签码的释放
                factory_basic_operate_instances.clothes_store_wash(seal_number, order_id, 'above', '1')
                order_id = 0
        if order_id != 0:
            #根据 seal_number 进行封签码的释放
            factory_basic_operate_instances.clothes_store_wash(seal_number,order_id,'above','1')


    #根据下单需求获取优惠券
    def get_coupon_appropriate(self,coupon_type_text,coupon_type,order_infor,pay_status):
        # coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
        # coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
        #order_infor:社区洗：订单价格，根据价格进行优惠券获取，自助洗：number、service_id
        #pay_status:优惠券可支付金额 与 订单金额比较，above:订单金额>优惠券金额，below：订单金额<=优惠券金额
        userCouponList = []
        coupon_type_text_name = ''
        order_price = order_infor
        for coupon_type_text in switch.basic_switch(coupon_type_text):
            if coupon_type_text('self'):
                coupon_type_text_name = u'自助洗'
                order_price = order_infor['price']
                break
            if coupon_type_text('common'):
                coupon_type_text_name = u'通用券'
                break
            if coupon_type_text('delivery'):
                coupon_type_text_name = u'干洗券'
            else:
                coupon_type_text_name = ''
        for coupon_type_text in switch.basic_switch(coupon_type_text):
            if coupon_type_text('self'):
                message =  u'调用自助洗获取优惠券的接口'
            else:
                message =  u'调用社区洗获取可用优惠券接口'
                userCouponList = self.basic_iface_request('',iface_list.userCouponList,iface_param.userCouponList,'',order_infor,'')
        userCouponList = userCouponList['data']['coupons']
        for i in range(len(userCouponList)):
            if userCouponList[i]['canUse'] == 0:
                continue
            if coupon_type_text_name != '' and coupon_type_text_name != userCouponList[i]['couponScene']:
                continue
            if coupon_type != '' and int(coupon_type) != userCouponList[i]['couponType']:
                continue
            if coupon_type != '' and int(coupon_type) == 2 and int(coupon_type) == userCouponList[i]['couponType']:
                return userCouponList[i]
            #进行价格判断
            for pay_status_value in switch.basic_switch(pay_status):
                if pay_status_value('above'):
                    if int(order_price) > userCouponList[i]['money']:
                        return userCouponList[i]
                if pay_status_value('below'):
                    if int(order_price) < userCouponList[i]['money']:
                        return userCouponList[i]
                if pay_status_value(''):
                    return userCouponList[i]
        #如果未找到合适的优惠券则返回0
        return 0

    # 根据下单需求获取优惠券
    def get_coupon_accrodingOrder(self,coupon_type_text,coupon_type,order_infor,pay_status):
        #coupon_infor = {'use_coupon':'YES','coupon_type_text':'','coupon_type':'','order_infor':'','pay_status':''}
        # coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
        # coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
        #order_infor:社区洗：订单价格，根据价格进行优惠券获取，自助洗：number、service_id
        #pay_status:优惠券可支付金额 与 订单金额比较，above:订单金额>优惠券金额，below订单金额<=优惠券金额
        coupon_infor = self.get_coupon_appropriate(coupon_type_text,coupon_type,order_infor,pay_status)
        #如果没有获取到优惠券，重新进行一次发券操作，重新获取
        if coupon_infor == 0:
            #生成并领取优惠券,生成通用、干洗柜 类型的优惠券
            self.make_coupon_data('','')
            #重新进行一次获取操作
            coupon_infor = self.get_coupon_appropriate(coupon_type_text, coupon_type, order_infor, pay_status)
        message =  coupon_infor
        return coupon_infor

    #根据需求取消订单
    def cancelOrder_accroding_request(self,good_type,cancel_order_condition,number):
        #good_type:单件洗：goods，活动：activity
        #order_status：字典表：{'status':0,'pay_status':0,'user_id':0,'goods_activity_id':0,'goods_id':0},订单状态+支付状态
        #根据需求进行订单列表获取
        order_list = qy_db_manager_instances.get_deliveryOrder_accroding_request('',cancel_order_condition)
        cycle = number if len(order_list) > number else len(order_list)
        for i in range(cycle):
            self.basic_iface_request('',iface_list.cancelOrder,iface_param.cancelOrder,order_list[i]['number'])
        message =  'test'

    #根据需求获取订单
    def get_order_accroding_request(self,good_type,order_condition,order_status=None):
        #good_type:单件洗：goods，活动：activity
        #order_condition：字典表：{'status':0,'pay_status':0,'user_id':user_infor['user_id'],'goods_activity_id':'','goods_id':'','payPrice':0},订单状态+支付状态
        #根据需求进行订单列表获取
        order_list = qy_db_manager_instances.get_deliveryOrder_accroding_request(good_type,order_condition)
        for i in range(len(order_list)):
            order_detail = self.basic_iface_request('',iface_list.orderDetail,iface_param.orderDetail,order_list[i]['number'])
            if order_condition['coupon_money'] > 0:
                if order_detail['data']['payInfo']['discount'] == 0:
                    continue
            if order_condition['payPrice'] == 0:
                if order_detail['data']['payInfo']['payPrice'] == 0:
                    return order_list[i]['number']
            if order_condition['payPrice'] != 0:
                if order_detail['data']['payInfo']['payPrice'] != 0:
                    return order_list[i]['number']
        return 0

    #根据需求获取订单
    def get_order_accrod_status(self,good_type,order_condition,order_status):
        #good_type:单件洗：goods，活动：activity
        #order_condition：字典表：{'status':0,'pay_status':0,'user_id':user_infor['user_id'],'goods_activity_id':'','goods_id':'','payPrice':0},订单状态+支付状态
        #order_status={'status': 0, 'pay_status': 1,'orders_status_process':'','balance_status':'','risk':''}订单的实际状态
        #根据需求进行订单列表获取
        order_list = qy_db_manager_instances.get_deliveryOrder_accroding_request(good_type,order_condition)
        for i in range(len(order_list)):
            #获取订单的 orders_status_process
            db_param = [
                {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[i]['id']},
            ]
            orders_status_process = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_status_process', 'id', db_param)
            if order_status['status'] in [0,-1,-2]:
                return order_list[i]['number']
            if order_status['orders_status_process'] == '':
                return order_list[i]['number']
            if orders_status_process[0]['status'] == order_status['orders_status_process']:
                return order_list[i]['number']
        return 0
        #未获取到订单，则进行订单创建

    #进行扫码开柜
    def openBoxWithQrcode(self,orderNumber,cabinet_id):
        if len(str(cabinet_id)) == 2:
            cabinet_id = '0'+str(cabinet_id)
        if len(str(cabinet_id)) == 1:
            cabinet_id = '00'+str(cabinet_id)
        qrcode_base = 'https://cabinet-api.funxi.cn/cabinet?id=027'+str(cabinet_id)+'_'
        time_str = str(int(time.time() - 60))
        qrcode = qrcode_base + time_str
        response_infor_json = self.basic_iface_request('',cabinet_client_constant.iface_list.openBoxWithQrcode,iface_param.openBoxWithQrcode,orderNumber,qrcode)
        return response_infor_json

    #进行订单处理
    def order_status_deal(self,order_number,target_order_status,order_status):
        #target_order_status = {'status':'','pay_status':'','orders_status_process':''} orders_status_process 真实状态
        for i in range(20):
            db_param = [
                {'field_name': 'number', 'filed_concatenation': '=', 'field_value': order_number},
            ]
            order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
            db_param = [
                {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
            ]
            order_status_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_status_process', 'id', db_param)
            #订单未支付，则调用支付操作
            if order_list[0]['pay_status'] == 0:
                # 进行更新用户余额
                qy_db_manager_instances.update_user_balance(user_infor, 'balance',float(order_list[0]['predict_price']))
                # 进行支付
                basic_operate_instances.basic_iface_request('', iface_list.orderPay, iface_param.orderPay, order_number,'balance', 0)
            if target_order_status['status'] == 0 and target_order_status['pay_status'] == 1:
                return order_number

            #检查当前状态是否与目标一致
            if order_status_list[0]['status'] == target_order_status['orders_status_process']:
                break
            #如果未预约存柜，则进行预约存柜
            if order_list[0]['status'] == 0 and order_status_list[0]['status'] == 'ORDERED':
                self.basic_iface_request('',iface_list.assignBox,iface_param.assignBox,order_number,settings.cabinetId)
                continue
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'ASSIGNED_BOX':
                return order_number

            # 进行扫码开柜
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'ASSIGNED_BOX':
                self.openBoxWithQrcode(order_number, settings.cabinetId)
                continue
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'DELIVERY_PICKUP':
                return order_number

            # 管家取出脏衣...................................................................................
            seal_number = ''
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'DELIVERY_PICKUP':
                rfId_list = qy_db_manager_instances.get_sealNumber_rfId()
                # 循环调用管家取衣接口，直到取到自己的衣物
                seal_number = ''
                for i in range(20):
                    seal_number = iot_basic_operate_instances.manager_out_dirty(settings.cabinetId, rfId_list, 1)
                    # 根据order_number 获取订单详情
                    db_param = [
                        {'field_name': 'source_number', 'filed_concatenation': '=', 'field_value': seal_number},
                    ]
                    order_receipt_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_receipt','created_at', db_param)
                    if order_receipt_list[0]['order_id'] == order_list[0]['id']:
                        break
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'DELIVERY_PICKUPED':
                return order_number

            # 获取交接单列表数据
            db_param = [
                {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
            ]
            receipt_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_receipt', 'id', db_param)

            #获取封签码
            seal_number = receipt_list[0]['source_number']

            #到达工厂操作
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'DELIVERY_PICKUPED':
                factory_basic_operate_instances.clothes_arrive_factory(seal_number)
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'ARRIVED_FACTORY':
                return order_number

            # 进行分拣操作，对于非反洗的订单进行创建衣物操作
            receiptId = 0
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'ARRIVED_FACTORY' and order_list[0]['repeat_wash_status'] ==0:
                receiptId = factory_basic_operate_instances.clothes_store_wash(seal_number, order_list[0]['id'],order_status['balance_status'], order_status['risk'])
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'SORTED_AND_WASH':
                return order_number
            #进行 receiptId 获取
            receiptId = receipt_list[0]['id']
            # 进行分拣操作，对于反洗的订单直接确认
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'ARRIVED_FACTORY' and order_list[0]['repeat_wash_status'] ==1:
                factory_basic_operate_instances.clothes_sorting_submit(receiptId)
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'SORTED_AND_WASH':
                return order_number
            # 根据封签号进行上挂操作
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'SORTED_AND_WASH':
                receiptId = factory_basic_operate_instances.racking_accord_rfId(seal_number,order_list[0]['id'])
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'UP_HOOKS':
                return order_number
            # 根据上挂ID进行打包操作,当前只打包一个包裹，如果多包裹后续在完成订单部分重新调用
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'UP_HOOKS':
                package_num = factory_basic_operate_instances.factory_packing(receiptId)
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'PACKED':
                return order_number
            # 进行出厂操作
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'PACKED':
                logistics_basic_operate_instances.logistics_dealWith_package(receiptId, 'OUT_FACTORY')
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'OUT_FACTORY':
                return order_number
            # 进行存衣操作
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'OUT_FACTORY':
                logistics_basic_operate_instances.logistics_dealWith_package(receiptId, 'WAIT_USER_RECEIVE')
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'WAIT_USER_RECEIVE':
                return order_number
            #进行完成操作
            if order_list[0]['status'] == 1 and order_status_list[0]['status'] == 'WAIT_USER_RECEIVE':
                logistics_basic_operate_instances.logistics_dealWith_package(receiptId, '')
                for i in range(5):
                    response_infor_json = self.openBoxWithQrcode(order_number,settings.cabinetId)
                    if response_infor_json['message'] == u'订单与二维码不匹配':
                        db_param = [
                            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
                        ]
                        order_cabinet_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_cabinet', 'id',db_param)
                        self.openBoxWithQrcode(order_number,order_cabinet_list[0]['user_send_cabinet_id'])
                    if response_infor_json['message'] == u'尚无可取衣物，请稍后重试':
                        break
            if target_order_status['status'] == 1 and target_order_status['orders_status_process'] == 'DONE':
                return order_number
            if order_list[0]['status'] == 2 and order_status_list[0]['status'] == 'DONE':
                return order_number

    #清理柜子，根据不同的订单类型
    def clean_cabinet_byOrderType(self,cabinet_id,order_type):
        #柜子中衣物存在的状态：DELIVERY_PICKUP：2，ASSIGNED_BOX：0，WAIT_USER_RECEIVE：1
        if order_type == 'DELIVERY_PICKUP':
            self.clean_box_accordOrder('5239353753970679808')
            return 0
        #先获取到所有的格子的订单number及衣物类型
        code_list = qy_db_manager_instances.get_cabinet_clothes(cabinet_id)
        if order_type == 'all':
            for i in range(len(code_list)):
                if code_list[i]['order_status'] == 'ASSIGNED_BOX':
                    self.basic_iface_request('',iface_list.cancelOrder,iface_param.cancelOrder,code_list[i]['order_number'])
                if code_list[i]['order_status'] == 'WAIT_USER_RECEIVE':
                    self.openBoxWithQrcode(code_list[i]['order_number'],cabinet_id)
            self.clean_box_accordOrder('5239353753970679808')
        for i in range(len(code_list)):
            if code_list[i]['order_status'] == order_type and order_type == 'ASSIGNED_BOX':
                self.basic_iface_request('', iface_list.cancelOrder, iface_param.cancelOrder,code_list[i]['order_number'])
            if code_list[i]['order_status'] == order_type and order_type == 'WAIT_USER_RECEIVE':
                self.openBoxWithQrcode(code_list[i]['order_number'], cabinet_id)
        message =  u'清理完成，清理的衣物类型：',order_type



if __name__ == '__main__':
    basic_operate_instances = basic_operate()
    # timestr = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    millis_7days_ago = int(round((time.time()-60*60*24*7) * 1000))
    millis = int(round(time.time() * 1000))
    message =  time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
    # basic_operate_instances.clean_box_accordOrder('5239353753970679808')
    # basic_operate_instances.clean_cabinet_byOrderType(settings.cabinetId,'all')
    # basic_operate_instances.order_done_operate(543,1)
    # basic_operate_instances.create_exchange_code('delivery','')
    order_coupon_infor = {'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': '', 'coupon_money': 10}
    order_status = {'status': 0, 'pay_status': 1,'balance_status':'above','risk':'1'}
    target_order_status = {'status': '1', 'pay_status': '1', 'orders_status_process': 'UP_HOOKS'}
    # basic_operate_instances.order_status_deal('389182114685292544', target_order_status,order_status)
    # basic_operate_instances.make_order_according_need('activity',order_coupon_infor,order_status)
    # basic_operate_instances.get_coupon_accrodingOrder('common','2','50','above')
    order_condition = {'status':1,'pay_status':1,'user_id':user_infor['user_id'],'goods_activity_id':'','goods_id':'','payPrice':0,'discount':0}
    order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'ARRIVED_FACTORY', 'balance_status': '', 'risk': ''}
    # basic_operate_instances.cancelOrder_accroding_request('',order_condition,100)
    # basic_operate_instances.get_order_accroding_request('',order_condition,0)
    # basic_operate_instances.get_order_accrod_status('',order_condition,order_status)
    qrcode_base = 'https://cabinet-api.funxi.cn/cabinet?id=027131_'
    # time_str = str(time.time()-60)[0:10]
    time_str = str(int(time.time()-60))
    qrcode = qrcode_base + time_str
    # qrcode = 'https://cabinet-api.funxi.cn/cabinet?id=027131_1570508845'
    # basic_operate_instances.basic_iface_request('', iface_list.cancelOrder, iface_param.cancelOrder,'389197120298586112')
    # basic_operate_instances.basic_iface_request('',cabinet_client_constant.iface_list.openBoxWithQrcode,iface_param.openBoxWithQrcode,'386218118344642560',qrcode)
    goods = [{"goodsId":'1',"amount":'1',"activityId":30}]
    #  ,'371427361297551360','balance','0'
    basic_operate_instances.basic_iface_request('',iface_list.sales_task_list,iface_param.sales_task_list,13,1,1,1)

    # basic_operate_instances.basic_iface_request('',iface_list.userCouponList,iface_param.userCouponList,'153','','')
    # basic_operate_instances.basic_iface_request('', iface_list.orderDetail, iface_param.orderDetail,'380049462652858368')
    repeat_clothe = [{"comment": "", "pic": cabinet_client_constant.common_parameter.test_img, "id": 4448}]
    # basic_operate_instances.basic_iface_request('', iface_list.assignBox, iface_param.assignBox,'389197120298586112',273)


