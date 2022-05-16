# -*- coding:utf-8 -*-
"""
ljq 2019-10-15
接口名称：订单详情
接口地址：/cabinet_client/api/v1/order/orderList
method：GET

接口设计：
1、参数异常的情况：空值、空字符串、格式不对
2、不同type类型的订单：0：全部、1：未支付、2：需补费、3：已完成、4：待评价、5：反洗单
3、不同page的请求、不同limit的请求

order_condition：={'status':0,'pay_status':0,'user_id':user_infor['user_id'],'goods_activity_id':'','goods_id':'','payPrice':0}
status：订单状态；pay_status：订单支付状态；user_id：用户ID，goods_activity_id：活动ID；goods_id：商品ID；
payPrice：实际支付金额；discount：优惠券支付金额

coupon_infor = {'use_coupon':'YES','coupon_type_text':'','coupon_type':'','order_infor':'','pay_status':'','payPrice':1}
# coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
# coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
# order_infor:社区洗：订单价格，根据价格进行优惠券获取，自助洗：number、service_id
# pay_status:优惠券可支付金额 与 订单金额比较，above:订单金额>优惠券金额，below订单金额<=优惠券金额
"""
import unittest,json,random,copy,utils_logging,time
from test_case.cabinet_client import cabinet_basic_operate
from tools import qy_db_manager,usefulTools,switch
from conf import settings,cabinet_client_constant

#实例化调用的class

basic_operate_instances = cabinet_basic_operate.basic_operate()
qy_db_manager_instances = qy_db_manager.database_operate()
usefulTools_instances = usefulTools.userfulToolsFactory()
iface_list = cabinet_client_constant.iface_list
iface_param = cabinet_client_constant.iface_param
user_infor = cabinet_client_constant.common_parameter.user_list[settings.cabinet_client_user_id]
common_parameter = cabinet_client_constant.common_parameter

#定义接口返回数据集
if_response_list = []
recharge_param = []

class orderList_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        self.db_param = [
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
        ]
        self.assertEqual(1,1)

    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.orderList,iface_param.orderList,*args)
        return response_infor_json

    #订单列表，参数为空的情况
    def test_orderList_noPrame(self):
        print u'订单列表，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],500,u'系统响应码为：400，目前为500')
        self.assertIn(u'系统异常',response_infor_json['message'],  u'系统响message包含:系统异常')

    # 参数为空字符串的情况
    def test_orderList_paramNull(self):
        print u'订单列表，参数为空字符串的情况，全部为空,按照0,1,10进行请求'
        response_infor_json = self.basic_data_request('','','')
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        #进行数据比对

    # 参数格式错误：type
    def test_orderList_formatErr1(self):
        print u'订单列表，参数格式错误：type'
        response_infor_json = self.basic_data_request('a','','')
        self.assertEqual(response_infor_json['status'], 500, u'系统响应码为：400,目前为500')
        self.assertIn(u'系统异常', response_infor_json['message'], u'系统响message包含:系统异常')

    # 参数格式错误：page
    def test_orderList_formatErr2(self):
        print u'订单列表，参数格式错误：page'
        response_infor_json = self.basic_data_request('', 'a', '')
        self.assertEqual(response_infor_json['status'], 500, u'系统响应码为：400,目前为500')
        self.assertIn(u'系统异常', response_infor_json['message'], u'系统响message包含:系统异常')

    # 参数格式错误：limit
    def test_orderList_formatErr3(self):
        print u'订单列表，参数格式错误：limit'
        response_infor_json = self.basic_data_request('', '', 'a')
        self.assertEqual(response_infor_json['status'], 500, u'系统响应码为：400,目前为500')
        self.assertIn(u'系统异常', response_infor_json['message'], u'系统响message包含:系统异常')

    # 参数格式错误：type
    def test_orderList_typeOutRange(self):
        print u'订单列表，type 非1-5的数字，按照0处理'
        response_infor_json = self.basic_data_request('10', '', '')
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对

    # 正常请求：type=0
    def test_orderList_allOrder(self):
        print u'订单列表，type=0,全部订单'
        order_list_type = 0
        order_sum = qy_db_manager_instances.get_table_data_sum('cabinet_api', 'orders', 'created_at', self.db_param)
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', self.db_param)
        response_infor_json = self.basic_data_request('0', 1, 100)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数量比较
        self.assertEqual(response_infor_json['data']['total'], order_sum[0]['tab_sum'])
        response_infor_json_orders = response_infor_json['data']['orders']
        for i in range(len(response_infor_json_orders)):
            self.assertEqual(response_infor_json_orders[i]['id'], order_list[i]['id'])
            self.orderList_compare(response_infor_json_orders[i],order_list_type)

    # 正常请求：type=0，page=2
    def test_orderList_pageCheck(self):
        order_list_type = 0
        print u'订单列表，type=0,全部订单'
        order_sum = qy_db_manager_instances.get_table_data_sum('cabinet_api', 'orders', 'created_at', self.db_param)
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',self.db_param)
        limit = 10 if order_sum[0]['tab_sum'] >10 else [0]['tab_sum'] /2
        response_infor_json = self.basic_data_request('0', 2, limit)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数量比较
        self.assertEqual(response_infor_json['data']['total'], order_sum[0]['tab_sum'])
        response_infor_json_orders = response_infor_json['data']['orders']
        for i in range(limit):
            order_list.pop(0)
        for i in range(len(response_infor_json_orders)):
            self.assertEqual(response_infor_json_orders[i]['id'], order_list[i]['id'])
            self.orderList_compare(response_infor_json_orders[i],order_list_type)

    # 正常请求：type=1
    def test_orderList_unPaid(self):
        order_list_type = 1
        print u'订单列表，type=1,未支付的订单'
        response_infor_json = self.basic_data_request('1', 1, 10)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        pay_status_condition = {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': 0}
        status_condition = {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 0}
        self.db_param.append(pay_status_condition)
        self.db_param.append(status_condition)
        order_sum = qy_db_manager_instances.get_table_data_sum('cabinet_api', 'orders', 'created_at', self.db_param)
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', self.db_param)
        #进行数量比较
        self.assertEqual(response_infor_json['data']['total'],order_sum[0]['tab_sum'])
        response_infor_json_orders = response_infor_json['data']['orders']
        for i in range(len(response_infor_json_orders)):
            self.assertEqual(response_infor_json_orders[i]['id'],order_list[i]['id'])
            self.orderList_compare(response_infor_json_orders[i],order_list_type)

    # 正常请求：type=2
    def test_orderList_type2(self):
        print u'订单列表，type=2,需补费的订单'
        order_list_type =2
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'OUT_FACTORY', 'balance_status': 'below', 'risk': '1'}
        balance = {'balance_price':'patch','balance_status':0}
        order_list = self.get_balance_order('',order_status, 'above',balance)
        #进行接口请求
        response_infor_json = self.basic_data_request(2, 1, 10)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数量比较
        self.assertEqual(response_infor_json['data']['total'], order_list[0]['tab_sum'])
        response_infor_json_orders = response_infor_json['data']['orders']
        for i in range(len(response_infor_json_orders)):
            self.assertEqual(response_infor_json_orders[i]['id'], order_list[i]['id'])
            self.orderList_compare(response_infor_json_orders[i],order_list_type)
        #进行柜子释放
        # for i in range(len(response_infor_json_orders)):
        #     qy_db_manager_instances.update_user_balance(user_infor,'real_balance',float(order_list[i]['balance_price']))
        #     basic_operate_instances.basic_iface_request('',iface_list.orderPay,iface_param.orderPay,order_list[i]['number'],'balance',1)
        #     basic_operate_instances.openBoxWithQrcode(order_list[i]['number'])

    # 正常请求：type=3
    def test_orderList_doneOrder(self):
        print u'订单列表，type=3,已完成 的订单'
        order_list_type = 3
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE','balance_status': 'below', 'risk': '1'}
        pay_status_condition = {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': 1}
        status_condition = {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 2}
        self.db_param.append(pay_status_condition)
        self.db_param.append(status_condition)
        order_sum = qy_db_manager_instances.get_table_data_sum('cabinet_api', 'orders', 'created_at', self.db_param)
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', self.db_param)
        #进行接口请求
        response_infor_json = self.basic_data_request('3', 1, 10)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.assertEqual(response_infor_json['data']['total'], order_sum[0]['tab_sum'])
        response_infor_json_orders = response_infor_json['data']['orders']
        for i in range(len(response_infor_json_orders)):
            self.assertEqual(response_infor_json_orders[i]['id'], order_list[i]['id'])
            self.orderList_compare(response_infor_json_orders[i],order_list_type)

    # 正常请求：type=4
    def test_orderList_waitSource(self):
        print u'订单列表，type=4,待评价 的订单'
        order_list_type =4
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'below','risk': '1'}
        pay_status_condition = {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': 1}
        status_condition = {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 2}
        source_condition = {'field_name': 'judged_at', 'filed_concatenation': 'is', 'field_value': 'NULL'}
        self.db_param.append(pay_status_condition)
        self.db_param.append(status_condition)
        self.db_param.append(source_condition)
        order_sum = qy_db_manager_instances.get_table_data_sum('cabinet_api', 'orders', 'created_at', self.db_param)
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',self.db_param)
        # 进行接口请求
        response_infor_json = self.basic_data_request('4', 1, 10)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.assertEqual(response_infor_json['data']['total'], order_sum[0]['tab_sum'])
        response_infor_json_orders = response_infor_json['data']['orders']
        for i in range(len(response_infor_json_orders)):
            self.assertEqual(response_infor_json_orders[i]['id'], order_list[i]['id'])
            self.orderList_compare(response_infor_json_orders[i],order_list_type)

    # 正常请求：type=5
    def test_orderList_repeatOrder(self):
        print u'订单列表，type=5,待评价 的订单'
        order_list_type = 5
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'below','risk': '1'}
        pay_status_condition = {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': 1}
        status_condition = {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 2}
        repeat_condition = {'field_name': 'repeat_wash_status', 'filed_concatenation': '=', 'field_value': 1}
        # self.db_param.append(pay_status_condition)
        # self.db_param.append(status_condition)
        self.db_param.append(repeat_condition)
        order_sum = qy_db_manager_instances.get_table_data_sum('cabinet_api', 'orders', 'created_at', self.db_param)
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',self.db_param)
        # 进行接口请求
        response_infor_json = self.basic_data_request('5', 1, 10)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.assertEqual(response_infor_json['data']['total'], order_sum[0]['tab_sum'])
        response_infor_json_orders = response_infor_json['data']['orders']
        for i in range(len(response_infor_json_orders)):
            self.assertEqual(response_infor_json_orders[i]['id'], order_list[i]['id'])
            self.orderList_compare(response_infor_json_orders[i],order_list_type)

    # 正常请求：type=6
    def test_orderList_waitClothes(self):
        print u'订单列表，type=6,待存衣 的订单'
        order_list_type = 6
        addition_condition = [{'field_name': 'status', 'filed_concatenation': '=', 'field_value': 0},
                            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': 1},]
        # self.db_param.append(repeat_condition)
        self.db_param = self.db_param + addition_condition
        order_sum = qy_db_manager_instances.get_table_data_sum('cabinet_api', 'orders', 'created_at', self.db_param)
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',self.db_param)
        # 进行接口请求
        response_infor_json = self.basic_data_request('6', 1, 10)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.assertEqual(response_infor_json['data']['total'], order_sum[0]['tab_sum'])
        response_infor_json_orders = response_infor_json['data']['orders']
        for i in range(len(response_infor_json_orders)):
            self.assertEqual(response_infor_json_orders[i]['id'], order_list[i]['id'])
            self.orderList_compare(response_infor_json_orders[i],order_list_type)

    #根据需要进行查询或是生成订单
    def get_balance_order(self,good_type,order_status,pay_status,balance):
        if balance['balance_price'] == 'patch':
            balance_price_condition = {'field_name': 'balance_price', 'filed_concatenation': '>', 'field_value': 0}
        else:
            balance_price_condition = {'field_name': 'balance_price', 'filed_concatenation': '<', 'field_value': 0}
        db_param = [
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': order_status['status']},
            {'field_name': 'balance_status', 'filed_concatenation': '=', 'field_value': balance['balance_status']},
        ]
        db_param.append(balance_price_condition)
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)

        # 定义需要创建的订单类型,真实支付金额>0,优惠券支付金额>0
        order_coupon_infor = {'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': '','coupon_money':10}
        order_coupon_infor['pay_status'] = pay_status

        # 未获取到相应的订单，则直接创建
        if len(order_list) == 0:
            basic_operate_instances.make_order_according_need(good_type, order_coupon_infor,order_status)
            order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',db_param)
        order_sum = qy_db_manager_instances.get_table_data_sum('cabinet_api', 'orders', 'created_at', db_param)
        for i in range(len(order_list)):
            order_list[i]['tab_sum'] = order_sum[0]['tab_sum']
        return order_list

    #根据需求更新用户信息
    def update_user_balance(self,pay_type,payPrice):
        #pay_type支付类型：real_balance,gift_balance,balance
        #payPrice:需要支付的金额
        random_int = random.randint(1, 99)
        real_balance = 0
        gift_balance = 0
        for pay_type in switch.basic_switch(pay_type):
            if pay_type('real_balance'):
                real_balance = payPrice + random_int
                gift_balance = random_int
            if pay_type('gift_balance'):
                gift_balance = payPrice + random_int
            if pay_type('balance'):
                real_balance = payPrice / 2
                gift_balance = payPrice
        qy_db_manager_instances.update_user_infor(user_infor['phone'],real_balance,gift_balance,real_balance+gift_balance)

    #基础的数据比对方法
    def orderList_compare(self,order_detail_data,order_list_type):
        time_compare = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
        print u'进行数据校验................,当前时间：',time_compare
        #根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=','field_value': order_detail_data['number']},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        #根据order信息，获取支付信息
        payments_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_detail_data['id']},
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 1},
        ]
        payments_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_payments', 'id', payments_param)
        #订单柜子相关
        orders_cabinet_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_detail_data['id']},
        ]
        orders_cabinet_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_cabinet', 'id',orders_cabinet_param)
        # 订单进度
        orders_status_process_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_detail_data['id']},
        ]
        orders_status_process_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_status_process', 'id',orders_status_process_param)
        # 订单详情
        order_detail_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_detail_data['id']},
        ]
        order_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'order_detail', 'id',order_detail_param)
        # 订单退费记录
        refund_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_detail_data['id']},
        ]
        refund_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_refund', 'id', refund_param)
        #订单的基础数据比较
        self.assertEqual(order_detail_data['id'], order_list[0]['id'], u'orders:id')
        self.assertEqual(order_detail_data['orderType'], order_list[0]['type'], u'orders:orderType:type')
        self.assertEqual(order_detail_data['predictPrice'], order_list[0]['predict_price'], u'orders:orderType:predict_price')
        if order_list[0]['coupon_id'] is not None and order_list[0]['coupon_id'] != 0:
            self.assertEqual(order_detail_data['couponId'], order_list[0]['coupon_id'], u'orders:orderType:coupon_id')
        self.assertEqual(order_detail_data['number'], order_list[0]['number'], u'orders:number')
        self.assertEqual(order_detail_data['createdAt'], order_list[0]['created_at'].strftime("%Y-%m-%d %H:%M:%S"), u'orders:created_at')
        self.assertEqual(order_detail_data['price'], float(order_list[0]['price']), u'orders:price')
        self.assertEqual(order_detail_data['balanceStatus'], order_list[0]['balance_status'], u'orders:balance_status')
        self.assertEqual(order_detail_data['balancePrice'], float(order_list[0]['balance_price']), u'orders:balance_price')
        self.assertEqual(order_detail_data['isRepeatWash'], order_list[0]['is_repeat_wash'], u'orders:is_repeat_wash')
        if order_list[0]['repeat_wash_status'] == 0:
            self.assertEqual(order_detail_data['comment'], order_list[0]['comment'], u'orders:comment')
        self.assertEqual(order_detail_data['payStatus'], order_list[0]['pay_status'], u'orders:pay_status')
        if order_detail_data['payStatus'] == 1:
            self.assertEqual(float('%.2f' % order_detail_data['payInfo']['payPrice']), float(order_list[0]['paid_price']), u'orders:paid_price')
        if order_detail_data['payStatus'] == 0:
            self.assertEqual(float(order_list[0]['paid_price']),0,u'orders:paid_price')
        if order_list[0]['coupon_id'] is None and order_list[0]['pay_status'] == 0:
            self.assertEqual(float('%.2f' % order_detail_data['payInfo']['payPrice']), float(order_list[0]['predict_price']), u'orders:paid_price')
        self.assertEqual(order_detail_data['status'], order_list[0]['status'], u'orders:status')

        #express校验：
        order_detail_data_express = order_detail_data['express']
        if orders_status_process_list[0]['status'] in ['DELIVERY_PICKUP','DELIVERY_PICKUPED','OUT_FACTORY','WAIT_USER_RECEIVE','DONE','CANCEL','BACK','CANCEL_BOX']:
            self.assertEqual(order_detail_data_express['type'], orders_status_process_list[0]['status'],u'状态校验')
            self.assertEqual(order_detail_data['ordersCabinetStatus'], orders_status_process_list[0]['status'],u'orders_status_process:status')
        elif orders_status_process_list[0]['status'] == 'ASSIGNED_BOX':
            self.assertEqual(order_detail_data_express['type'], u'ORDERED', u'状态校验')
        elif orders_status_process_list[0]['status'] == 'ORDERED' and order_list[0]['pay_status'] == 0:
            self.assertEqual(order_detail_data_express['type'],  orders_status_process_list[0]['status'],u'状态校验')
        elif orders_status_process_list[0]['status'] == 'ORDERED' and order_list[0]['pay_status'] == 1:
            self.assertEqual(order_detail_data_express['type'],  'PAID',u'状态校验')
            self.assertEqual(order_detail_data['ordersCabinetStatus'], 'PAID', u'orders_status_process:status')
        else:
            self.assertEqual(order_detail_data_express['type'], u'ARRIVED_FACTORY', u'状态校验')
            self.assertEqual(order_detail_data['ordersCabinetStatus'], 'ARRIVED_FACTORY', u'orders_status_process:status')
            self.assertEqual(order_detail_data_express['status'], common_parameter.ARRIVED_FACTORY['description'],u'显示名称')
        if orders_status_process_list[0]['status'] == 'ORDERED' and order_list[0]['pay_status'] ==1:
            self.assertEqual(order_detail_data_express['status'],common_parameter.PAID['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'ORDERED' and order_list[0]['pay_status'] ==0:
            self.assertEqual(order_detail_data_express['status'],common_parameter.ORDERED['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'CANCEL_BOX':
            self.assertEqual(order_detail_data_express['status'],common_parameter.CANCEL_BOX['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'DELIVERY_PICKUP':
            self.assertEqual(order_detail_data_express['status'],common_parameter.DELIVERY_PICKUP['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'DELIVERY_PICKUPED':
            self.assertEqual(order_detail_data_express['status'],common_parameter.DELIVERY_PICKUPED['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'ARRIVED_FACTORY':
            self.assertEqual(order_detail_data_express['status'],common_parameter.ARRIVED_FACTORY['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'OUT_FACTORY':
            self.assertEqual(order_detail_data_express['status'],common_parameter.OUT_FACTORY['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'DONE':
            self.assertEqual(order_detail_data_express['status'],common_parameter.DONE_LIST['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'BACK':
            self.assertEqual(order_detail_data_express['status'],common_parameter.BACK['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'CANCEL':
            self.assertEqual(order_detail_data_express['status'],common_parameter.CANCEL['description'], u'显示名称')
        if len(payments_list) ==1:
            self.assertEqual(float('%.2f' % order_detail_data['payInfo']['payPrice']),float(payments_list[0]['real_amount'] + payments_list[0]['gift_amount']), u'user_coupon:money')
        if len(payments_list) > 1:
            self.assertEqual(float('%.2f' % order_detail_data['payInfo']['payPrice']),float(payments_list[1]['real_amount'] + payments_list[1]['gift_amount']), u'user_coupon:money')
            # 校验补费金额
            self.assertEqual(float('%.2f' % order_detail_data['balancePrice']),float(payments_list[0]['real_amount'] + payments_list[0]['gift_amount']),u'user_coupon:money')
        # details校验
        #优惠券校验
        if order_list[0]['coupon_id'] is not None and order_list[0]['coupon_id'] != 0:
            self.assertEqual(order_detail_data['couponId'], order_list[0]['coupon_id'], u'orders:orderType:coupon_id')
            # user_coupon
            user_coupon_param = [
                {'field_name': 'id', 'filed_concatenation': '=', 'field_value': order_list[0]['coupon_id']},
            ]
            user_coupon = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'user_coupon', 'id',user_coupon_param)
            # delivery_coupon
            coupon_id = user_coupon[0]['common_coupon_id'] if user_coupon[0]['common_coupon_id'] !=0 else user_coupon[0]['delivery_coupon_id']
            coupon_param = [
                {'field_name': 'id', 'filed_concatenation': '=', 'field_value': coupon_id},
            ]
            coupon_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'delivery_coupon', 'id',coupon_param)
            # if order_list[0]['number'] != '376104652634316800':
            #     return 0
            #计算优惠券的金额
            discount = float(user_coupon[0]['money']) if coupon_list[0]['coupon_type'] != 2 else float(order_detail_data['predictPrice']*(1-float(user_coupon[0]['money'])/10))
            #根据折扣券金额是否大于最大抵扣金额进行修改
            if coupon_list[0]['coupon_type'] == 2:
                discount = float('%.2f' %discount) if float('%.2f' %discount) < float(coupon_list[0]['max_money']) else float(coupon_list[0]['max_money'])
            #根据支付金额是否为0进行修改
            discount = discount if float('%.2f' % order_detail_data['payInfo']['payPrice']) >0 else float(user_coupon[0]['money'])
            self.assertEqual(order_detail_data['payInfo']['discount'], discount, u'user_coupon:money')
            # 计算优惠券的金额
            coupon_real_amount = discount if order_detail_data['predictPrice'] > discount else order_detail_data['predictPrice']
            payPrice = float('%.2f' % (order_detail_data['predictPrice'] - coupon_real_amount))
            # 检查需要支付的金额是否正确
            self.assertEqual(float('%.2f' % order_detail_data['payInfo']['payPrice']), payPrice, u'user_coupon:money')
            # 检查payments表中的数据
            if len(payments_list) == 1:
                self.assertEqual(payments_list[0]['coupon_id'], order_detail_data['couponId'],u'orders_payments:coupon_id')
                self.assertEqual(float(payments_list[0]['coupon_real_amount']), coupon_real_amount,u'orders_payments:coupon_real_amount')
                self.assertEqual(float('%.2f' % order_detail_data['payInfo']['payPrice']), float( '%.2f' % float(payments_list[0]['real_amount'] + payments_list[0]['gift_amount'])),u'user_coupon:money')
            if len(payments_list) == 2:
                self.assertEqual(payments_list[1]['coupon_id'], order_detail_data['couponId'],u'orders_payments:coupon_id')
                self.assertEqual(float(payments_list[1]['coupon_real_amount']), coupon_real_amount,u'orders_payments:coupon_real_amount')

        # 根据不同的类型进行订单个性化校验
        if order_list_type in [2]:
            print u'当前的订单列表为：%s，进行订单状态、支付状态检查' %common_parameter.order_list_type[str(order_list_type)]
            self.assertEqual(order_detail_data['status'], 1, u'订单当前状态为1')
            self.assertEqual(order_list[0]['status'], 1, u'订单当前状态为1')
            self.assertEqual(order_detail_data['payStatus'], 1, u'订单当前状态为1')
            self.assertEqual(order_list[0]['pay_status'], 1, u'订单当前状态为1')
        if order_list_type == 1:
            print u'当前的订单列表为：待支付，进行订单状态、支付状态检查'
            self.assertEqual(order_detail_data['status'], 0, u'订单当前状态为1')
            self.assertEqual(order_list[0]['status'], 0, u'订单当前状态为1')
            self.assertEqual(order_detail_data['payStatus'], 0, u'订单当前状态为1')
            self.assertEqual(order_list[0]['pay_status'], 0, u'订单当前状态为1')
        if order_list_type in[3,4] :
            print u'当前的订单列表为：待支付，进行订单状态、支付状态检查'
            self.assertEqual(order_detail_data['status'], 2, u'订单当前状态为2')
            self.assertEqual(order_list[0]['status'], 2, u'订单当前状态为2')
            self.assertEqual(order_detail_data['payStatus'], 1, u'订单当前支付状态为1')
            self.assertEqual(order_list[0]['pay_status'], 1, u'订单当前支付状态为1')
        if order_list_type == 2:
            print u'当前的订单列表为：%s，进行补费特殊信息检查' %common_parameter.order_list_type[str(order_list_type)]
            self.assertTrue(order_detail_data['balancePrice']>0, u'退补费金额大于0')
            self.assertEqual(order_detail_data['balanceStatus'], 0, u'退补费状态为0')
        if order_list_type == 5:
            print u'当前的订单列表为：%s，进行反洗单检查' %common_parameter.order_list_type[str(order_list_type)]
            self.assertEqual(order_detail_data['isRepeatWash'], 1, u'反洗状态为1')
        if order_list_type == 6:
            print u'当前的订单列表为：%s，进行待存衣信息检查' %common_parameter.order_list_type[str(order_list_type)]
            self.assertEqual(order_list[0]['pay_status'], 1, u'订单当前状态为1')

        # 如果状态=0，则直接返回，不检查柜子相关数据
        if order_list[0]['status'] in [0,-1]:
            return 0
        #柜子检查
        if order_detail_data['status'] == 1:
            # 根据order_id查询 orders_cabinet 信息
            db_param = [
                {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
            ]
            orders_cabinet_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_cabinet', 'id', db_param)
            #检查数量为1
            self.assertEqual(len(orders_cabinet_list),1,u'开柜记录数=1')

        cabinet_code_param = [
            {'field_name': 'cabinet_id', 'filed_concatenation': '=', 'field_value': orders_cabinet_list[0]['user_send_cabinet_id']},
            {'field_name': 'box_number', 'filed_concatenation': '=','field_value': orders_cabinet_list[0]['user_send_box_number']},
        ]
        cabinet_code_list = qy_db_manager_instances.get_table_data_sigle('cabinet_iot', 'cabinet_code', 'id', cabinet_code_param)
        if order_detail_data_express['type'] in ['DELIVERY_PICKUP']:
            # 用户存衣、用户待取的时候生成取衣码
            self.assertEqual(len(cabinet_code_list), 1, u'cabinet_code 记录数=1')
        if order_detail_data_express['type'] == 'WAIT_USER_RECEIVE':
            self.assertTrue(len(cabinet_code_list) > 0, u'cabinet_code 记录数>0')
        if order_detail_data_express['type'] == 'DELIVERY_PICKUP':
            self.assertEqual(order_detail_data_express['status'], common_parameter.DELIVERY_PICKUP['description'], u'orders_cabinet:status')
            self.assertEqual(cabinet_code_list[0]['type'], 2,u'存衣之后，code_type为管家取衣码')
            self.assertEqual(len(cabinet_code_list), 1, u'cabinet_code 记录数=1')
        if order_detail_data_express['type'] == 'DELIVERY_PICKUPED':
            self.assertEqual(order_detail_data_express['status'], common_parameter.DELIVERY_PICKUPED['description'], u'orders_cabinet:status')
        if orders_cabinet_list[0]['status'] in ['ARRIVED_FACTORY','SORTED_AND_WASH','UP_HOOKS','HOOKED_WAIT_PACK','PACKED']:
            self.assertEqual(order_detail_data_express['type'], 'ARRIVED_FACTORY',u'到达工厂之后都显示为：ARRIVED_FACTORY')
            self.assertEqual(order_detail_data_express['status'], common_parameter.ARRIVED_FACTORY['description'], u'orders_cabinet:status')
        else:
            # 检查状态
            self.assertEqual(order_detail_data_express['type'], orders_cabinet_list[0]['status'], u'orders_cabinet:status')
        if orders_cabinet_list[0]['status'] == 'OUT_FACTORY':
            self.assertEqual(order_detail_data_express['status'],common_parameter.OUT_FACTORY['description'], u'orders_cabinet:status')
        if orders_cabinet_list[0]['status'] == 'WAIT_USER_RECEIVE':
            self.assertEqual(order_detail_data_express['status'], common_parameter.WAIT_USER_RECEIVE['description'], u'orders_cabinet:status')

        # 检查退费情况
        if order_list[0]['balance_price'] < 0 and order_list[0]['balance_status'] == 0:
            self.assertEqual(len(refund_list), 0, u'退款记录数')
        if order_list[0]['balance_price'] < 0 and order_list[0]['balance_status'] == 1:
            self.assertEqual(len(refund_list), 1, u'退款记录数')
            self.assertEqual(abs(order_detail_data['balancePrice']), float(refund_list[0]['fee']), u'校验退款的金额')
        #details校验,如果是反洗单，则不进行detail校验
        order_detail_list.reverse()
        order_detail_data_details = order_detail_data['details']

        if order_list[0]['is_repeat_wash'] == '1':
            self.assertEqual(len(order_detail_data_details),0,u'反洗单的订单详情为空')
            return 0
        for i in range(len(order_detail_data_details)):
            self.assertEqual(order_detail_data_details[i]['amount'], order_detail_list[i]['amount'], u'order_detail_list:amount')
            self.assertEqual(order_detail_data_details[i]['goodsActivityId'], order_detail_list[i]['goods_activity_id'], u'order_detail_list:goodsActivityId')
            self.assertEqual(order_detail_data_details[i]['goodsId'], order_detail_list[i]['goods_id'], u'order_detail_list:goods_id')
            self.assertEqual(order_detail_data_details[i]['goodsName'], order_detail_list[i]['goods_name'], u'order_detail_list:goods_name')
            self.assertEqual(order_detail_data_details[i]['goodsPrice'], order_detail_list[i]['goods_price'], u'order_detail_list:goods_price')
            self.assertEqual(order_detail_data_details[i]['goodsThumbnail'], order_detail_list[i]['goods_thumbnail'], u'order_detail_list:goods_thumbnail')
            self.assertEqual(order_detail_data_details[i]['id'], order_detail_list[i]['id'], u'order_detail_list:id')
            self.assertEqual(order_detail_data_details[i]['orderId'], order_detail_list[i]['order_id'], u'order_detail_list:order_id')