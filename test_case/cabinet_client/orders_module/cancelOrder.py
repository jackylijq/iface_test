# -*- coding:utf-8 -*-
"""
ljq 2019-09-23
接口名称：取消订单
接口地址：/cabinet_client/api/v1/order/cancelOrder
method：DELETE

接口设计：
1、参数异常的情况：空值、空字符串
2、订单不存在的情况
3、已取消的订单无法再次取消
4、未支付、已支付未存衣、已预约未存衣、已扫码存衣的订单可以取消
5、扫码存衣下一个状态之后的订单不可以取消


order_condition：={'status':0,'pay_status':0,'user_id':user_infor['user_id'],'goods_activity_id':'','goods_id':'','payPrice':0}
status：订单状态；pay_status：订单支付状态；user_id：用户ID，goods_activity_id：活动ID；goods_id：商品ID；
payPrice：实际支付金额；discount：优惠券支付金额

coupon_infor = {'use_coupon':'YES','coupon_type_text':'','coupon_type':'','order_infor':'','pay_status':'','payPrice':1}
# coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
# coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
# order_infor:社区洗：订单价格，根据价格进行优惠券获取，自助洗：number、service_id
# pay_status:优惠券可支付金额 与 订单金额比较，above:订单金额>优惠券金额，below订单金额<=优惠券金额

order_status = {'status': 0, 'pay_status': 1}
status:订单状态；pay_status：支付状态
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

#定义接口返回数据集
if_response_list = []
recharge_param = []

class cancelOrder_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        self.assertEqual(1,1)

    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.cancelOrder,iface_param.cancelOrder,*args)
        return response_infor_json

    #进行订单取消请求，参数为空的情况
    def test_cancelOrder_noPrame(self):
        print u'进行订单取消请求，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],400,u'系统响应码为：400')
        self.assertIn(u'订单有误',response_infor_json['message'],  u'系统响message包含:订单有误')

    # 参数为空字符串的情况
    def test_cancelOrder_paramNull(self):
        print u'进行订单取消请求，参数为空字符串的情况，全部为空'
        response_infor_json = self.basic_data_request('')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # orderNumber不存在的情况
    def test_cancelOrder_numberNotExist(self):
        print u'进行订单取消请求，orderNumber不存在的情况'
        response_infor_json = self.basic_data_request('123123123')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # order_status=delete
    def test_cancelOrder_deleteOrder(self):
        print u'进行订单取消请求，已删除的订单：order_status=delete'
        db_param = [
            {'field_name': 'deleted_at', 'filed_concatenation': 'is not', 'field_value': 'NULL'},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        ]
        orders_delete = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',db_param)
        if len(orders_delete) == 0:
            print u'无删除订单，删除订单查看详情跳过'
        response_infor_json = self.basic_data_request(orders_delete[0]['number'])
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    def atest_cancelOrder_notOwner(self):
        print u'进行订单取消请求，非本人订单'
        db_param = [
            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': '1'},
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': '0'},
            {'field_name': 'user_id', 'filed_concatenation': '!=', 'field_value': user_infor['user_id']},
        ]
        orders_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',db_param)
        if len(orders_list) == 0:
            print u'无删除订单，删除订单查看详情跳过'
        response_infor_json = self.basic_data_request(orders_list[0]['number'])
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400,目前未校验，400')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        # self.orderDetail_compare(response_infor_json)

    # 已取消的订单：order_status=-1,pay_status = 0
    def test_cancelOrder_canceled(self):
        print u'进行订单取消请求，已取消的订单：order_status=-1,pay_status = 0'
        order_status = {'status':-1,'pay_status':0}
        order_number = self.get_order_accord_request('',10,10,order_status,'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')


    # 未支付的订单：order_status=0,pay_status = 0
    def test_cancelOrder_noPay(self):
        print u'进行订单取消请求，未支付的订单：order_status=0,pay_status = 0'
        order_status = {'status': 0, 'pay_status': 0}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        # 进行人员信息获取，用于验证退款金额是否正确
        user_infor_beforeCancel = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'订单已取消', response_infor_json['message'], u'系统响message包含:订单已取消')
        # 进行数据比对
        self.cancelOrder_compare(order_number,user_infor_beforeCancel)

    # 已支付的订单：order_status=0,pay_status = 1
    def test_cancelOrder_Paid(self):
        print u'进行订单取消请求，已支付的订单：order_status=0,pay_status = 1'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        # 进行人员信息获取，用于验证退款金额是否正确
        user_infor_beforeCancel = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'订单已取消', response_infor_json['message'], u'系统响message包含:订单已取消')
        #进行数据比对
        self.cancelOrder_compare(order_number,user_infor_beforeCancel)

    # 套餐已支付的订单：order_status=0,pay_status = 1
    def test_cancelOrder_activityPaid(self):
        print u'进行订单取消请求，已支付的套餐订单：order_status=0,pay_status = 1，good_type=activity'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('activity', 10, 10, order_status, 'above')
        #进行人员信息获取，用于验证退款金额是否正确
        user_infor_beforeCancel = basic_operate_instances.basic_iface_request('',iface_list.userInfo,iface_param.userInfo)
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'订单已取消', response_infor_json['message'], u'系统响message包含:订单已取消')
        # 进行数据比对
        self.cancelOrder_compare(order_number,user_infor_beforeCancel)

    #还差扫码之后的订单状态检查-------------------------------------------------------------------------------------
    # 已扫码开柜的订单：order_status=1,pay_status = 1
    def test_cancelOrder_pickupOrder(self):
        print u'扫码开柜，已存衣的订单：order_status=1,pay_status = 1,DELIVERY_PICKUP'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUP'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        # 进行人员信息获取，用于验证退款金额是否正确
        user_infor_beforeCancel = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'订单已取消', response_infor_json['message'], u'系统响message包含:订单已取消')
        # 进行数据比对
        self.cancelOrder_compare(order_number, user_infor_beforeCancel)
        # 进行柜子释放
        basic_operate_instances.openBoxWithQrcode(order_number, settings.cabinetId)
        # 进行数据比对
        self.cancelOrder_compare(order_number, user_infor_beforeCancel)

    # 已预约柜子的订单：order_status=1,pay_status = 1
    def test_cancelOrder_assignOrder(self):
        print u'已预约柜子的订单：order_status=1,pay_status = 1,ASSIGNED_BOX'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'ASSIGNED_BOX'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        # 进行人员信息获取，用于验证退款金额是否正确
        user_infor_beforeCancel = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'订单已取消', response_infor_json['message'], u'系统响message包含:订单已取消')
        # 进行数据比对
        self.cancelOrder_compare(order_number, user_infor_beforeCancel)
        # 进行柜子释放
        basic_operate_instances.openBoxWithQrcode(order_number, settings.cabinetId)
        # 进行数据比对
        self.cancelOrder_compare(order_number, user_infor_beforeCancel)

    # 管家已取衣 的订单：order_status=1,pay_status = 1
    def atest_cancelOrder_orderPICKUPED(self):
        print u'扫码开柜，管家已取衣 的订单：order_status=1,pay_status = 1,DELIVERY_PICKUPED'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUPED'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        # 进行人员信息获取，用于验证退款金额是否正确
        user_infor_beforeCancel = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'订单已取消', response_infor_json['message'], u'系统响message包含:订单已取消')


    #根据需要进行查询或是生成订单
    def get_order_accord_request(self,good_type,payPrice,coupon_money,order_status,pay_status):
        order_number = 0
        # 定义需要的订单类型：真实支付金额>0,优惠券支付金额>0
        order_condition = {'status': 0, 'pay_status': 0, 'user_id': user_infor['user_id'], 'goods_activity_id': '','goods_id': '', 'payPrice': 10}
        order_condition['payPrice'] = payPrice
        order_condition['coupon_money'] = coupon_money
        order_condition['status'] = order_status['status']
        order_condition['pay_status'] = order_status['pay_status']
        #进行数据库数据请求
        order_number = basic_operate_instances.get_order_accrod_status(good_type, order_condition,order_status)

        # 定义需要创建的订单类型,真实支付金额>0,优惠券支付金额>0
        order_coupon_infor = {'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': '','coupon_money':10}
        order_coupon_infor['pay_status'] = pay_status

        # 未获取到相应的订单，则直接创建
        if order_number == 0:
            order_number = basic_operate_instances.make_order_according_need(good_type, order_coupon_infor,order_status)
        return order_number

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
    def cancelOrder_compare(self,order_number,user_infor_beforeCancel):
        #根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=', 'field_value': order_number},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        #根据用户ID获取当前用户数据
        user_param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        ]
        user_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'users', 'created_at', user_param)
        #根据订单信息，获取退款数据
        refund_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        refund_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_refund', 'created_at', refund_param)
        # 根据订单信息，获取支付数据
        payments_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        payments_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_payments', 'created_at',payments_param)
        # 订单进度
        orders_status_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        orders_status_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api','orders_status_process', 'id',orders_status_param)
        # 根据order信息，获取 orders_cabinet 开柜信息
        cabinet_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        orders_cabinet_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_cabinet', 'id',cabinet_param)
        #根据用户信息获取优惠券列表
        user_infor_beforeCancel = user_infor_beforeCancel['data']

        #先进行基础信息判断：
        if len(orders_cabinet_list) == 0:
            self.assertEqual(order_list[0]['status'],-1, u'orders:status')
            self.assertEqual(orders_status_list[0]['status'],'CANCEL', u'orders_status_process:status')
        if len(orders_cabinet_list) == 1:
            cabinet_code_param = [
                {'field_name': 'cabinet_id', 'filed_concatenation': '=', 'field_value': settings.cabinetId},
                {'field_name': 'box_number', 'filed_concatenation': 'in', 'field_value': '(' + orders_cabinet_list[0]['user_send_box_number'] + ')'},
            ]
            cabinet_code_list = qy_db_manager_instances.get_table_data_sigle('cabinet_iot', 'cabinet_code', 'id',cabinet_code_param)
            if order_list[0]['status'] == 1:
                self.assertEqual(orders_status_list[0]['status'], 'WAIT_USER_RECEIVE', u'orders_status_process:status')
                # 检查是否存在取衣码
                self.assertEqual(len(cabinet_code_list), 1, u'检查是否有取衣码')
                self.assertEqual(cabinet_code_list[0]['type'], 1, u'取衣码的类型为1')
            if order_list[0]['status'] == -2:
                self.assertEqual(orders_status_list[0]['status'], 'BACK', u'orders_status_process:status')
                # 检查是否存在取衣码
                self.assertEqual(len(cabinet_code_list), 0, u'检查是否有取衣码')
            if order_list[0]['status'] == -1:
                self.assertEqual(orders_status_list[0]['status'], 'CANCEL', u'orders_status_process:status')
                # 检查是否存在取衣码
                self.assertEqual(len(cabinet_code_list), 0, u'检查是否有取衣码')
        #进行支付退款校验,如果未支付，直接返回
        if order_list[0]['pay_status'] == 0:
            self.assertEqual(float(user_list[0]['balance']),user_infor_beforeCancel['balance'], u'orders_status_process:status')
            self.assertEqual(float(user_list[0]['real_balance']),user_infor_beforeCancel['realBalance'], u'orders_status_process:status')
            self.assertEqual(float(user_list[0]['gift_balance']),user_infor_beforeCancel['giftBalance'], u'orders_status_process:status')
            return 0
        #orders_refund数据比对
        self.assertEqual(len(refund_list), 1, u'orders_refund:数据为1')
        self.assertEqual(float(refund_list[0]['fee']), float(payments_list[0]['real_amount']+payments_list[0]['gift_amount']), u'orders_refund:fee')
        self.assertEqual(float(refund_list[0]['real_fee']), float(payments_list[0]['real_amount']), u'orders_refund:real_fee')
        self.assertEqual(float(refund_list[0]['gift_fee']), float(payments_list[0]['gift_amount']), u'orders_refund:gift_fee')
        self.assertEqual(float(refund_list[0]['type']), 1, u'orders_refund:type')
        #对比前后的退款金额数据
        balance_afterCancel = float('%.2f' %(user_infor_beforeCancel['balance'] + float(refund_list[0]['fee'])))
        real_balance_afterCancel = float('%.2f' %(user_infor_beforeCancel['realBalance'] + float(payments_list[0]['real_amount'])))
        gift_balance_afterCancel = float('%.2f' %(user_infor_beforeCancel['giftBalance'] + float(payments_list[0]['gift_amount'])))
        self.assertEqual(float(user_list[0]['balance']), balance_afterCancel,u'user_list:balance')
        self.assertEqual(float(user_list[0]['real_balance']), real_balance_afterCancel,u'user_list:real_balance')
        self.assertEqual(float(user_list[0]['gift_balance']), gift_balance_afterCancel,u'user_list:gift_balance')
        #进行优惠券检查
        if order_list[0]['coupon_id'] is not None:
            user_coupon_param = [
                {'field_name': 'id', 'filed_concatenation': '=', 'field_value': order_list[0]['coupon_id']},
            ]
            user_coupon = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'user_coupon', 'id',user_coupon_param)
            self.assertEqual(user_coupon[0]['is_used'], 0, u'user_coupon:is_used')



