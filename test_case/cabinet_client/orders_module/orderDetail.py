# -*- coding:utf-8 -*-
"""
ljq 2019-09-23
接口名称：订单详情
接口地址：/cabinet_client/api/v1/order/orderDetail
method：GET

接口设计：
1、参数异常的情况：空值、空字符串、格式不对
2、订单错误、不存在的情况，无法支付
3、非本人订单无法查询
4、不同状态的订单进行查询
5、订单信息与数据库进行比对

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

class orderDetail_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        self.assertEqual(1,1)

    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.orderDetail,iface_param.orderDetail,*args)
        return response_infor_json

    #进行订单详情请求，参数为空的情况
    def test_orderDetail_noPrame(self):
        print u'进行订单详情请求，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],500,u'系统响应码为：400，目前为500')
        self.assertIn(u'系统异常',response_infor_json['message'],  u'系统响message包含:系统异常')

    # 参数为空字符串的情况
    def test_orderDetail_paramNull(self):
        print u'进行订单详情请求，参数为空字符串的情况，全部为空'
        response_infor_json = self.basic_data_request('')
        self.assertEqual(response_infor_json['status'], 500, u'系统响应码为：400，目前500')
        # self.assertIn(u'订单不存在', response_infor_json['message'], u'系统响message包含:订单不存在')

    # orderNumber不存在的情况
    def test_orderDetail_numberNotExist(self):
        print u'进行订单详情请求，orderNumber不存在的情况'
        response_infor_json = self.basic_data_request('123123123')
        self.assertEqual(response_infor_json['status'], 500, u'系统响应码为：400,目前为500')
        # self.assertIn(u'订单不存在', response_infor_json['message'], u'系统响message包含:订单不存在')

    # order_status=delete
    def test_orderDetail_deleteOrder(self):
        print u'进行订单详情请求，order_status=delete'
        db_param = [
            {'field_name': 'deleted_at', 'filed_concatenation': 'is not', 'field_value': 'NULL'},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        ]
        orders_delete = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',db_param)
        if len(orders_delete) == 0:
            print u'无删除订单，删除订单查看详情跳过'
        response_infor_json = self.basic_data_request(orders_delete[0]['number'])
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    def test_orderDetail_notOwner(self):
        print u'进行订单详情请求，非本人订单不可获取详情'
        db_param = [
            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': '1'},
            {'field_name': 'user_id', 'filed_concatenation': '!=', 'field_value': user_infor['user_id']},
        ]
        orders_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',db_param)
        if len(orders_list) == 0:
            print u'无删除订单，删除订单查看详情跳过'
        response_infor_json = self.basic_data_request(orders_list[0]['number'])
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：400,目前未校验，为200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        # self.orderDetail_compare(response_infor_json)

    # 已取消的订单：order_status=-1,pay_status = 0
    def test_orderDetail_canceled(self):
        print u'进行订单详情请求，已取消的订单：order_status=-1,pay_status = 0'
        order_status = {'status':-1,'pay_status':1}
        order_number = self.get_order_accord_request('',10,10,order_status,'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 未支付的订单：order_status=0,pay_status = 0
    def test_orderDetail_noPay(self):
        print u'进行订单详情请求，未支付的订单：order_status=0,pay_status = 0'
        order_status = {'status': 0, 'pay_status': 0}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 已支付的订单：order_status=0,pay_status = 1
    def test_orderDetail_Paid(self):
        print u'进行订单详情请求，已支付的订单：order_status=0,pay_status = 1'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('goods', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        #进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 套餐已支付的订单：order_status=0,pay_status = 1
    def test_orderDetail_activityPaid(self):
        print u'进行订单详情请求，已支付的套餐订单：order_status=0,pay_status = 1，good_type=activity'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('activity', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    #还差扫码之后的订单状态检查
    # 已订单详情的订单：order_status=1,pay_status = 1
    def test_orderDetail_assignedBox(self):
        print u'订单详情，已存衣的订单：order_status=1,pay_status = 1,ASSIGNED_BOX'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'ASSIGNED_BOX'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)
        # 进行柜子释放
        # basic_operate_instances.basic_iface_request('',iface_list.cancelOrder,iface_param.cancelOrder,order_number)

    # 已订单详情的订单：order_status=1,pay_status = 1
    def test_orderDetail_pickupOrder(self):
        print u'订单详情，已存衣的订单：order_status=1,pay_status = 1,DELIVERY_PICKUP'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUP'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)
        # 进行柜子释放
        basic_operate_instances.clean_box_accordOrder(order_number)

    # 管家已取衣 的订单：order_status=1,pay_status = 1
    def test_orderDetail_orderPICKUPED(self):
        print u'订单详情，管家已取衣 的订单：order_status=1,pay_status = 1,DELIVERY_PICKUPED'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUPED'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 已到工厂 的订单：order_status=1,pay_status = 1
    def test_orderDetail_orderArFactory(self):
        print u'订单详情，已到工厂 的订单：order_status=1,pay_status = 1,ARRIVED_FACTORY'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'ARRIVED_FACTORY'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 已分拣 的订单：order_status=1,pay_status = 1
    def test_orderDetail_orderSorted(self):
        print u'订单详情，已分拣 的订单：order_status=1,pay_status = 1,SORTED_AND_WASH'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'SORTED_AND_WASH','balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 已上挂 的订单：order_status=1,pay_status = 1
    def test_orderDetail_orderUpHooks(self):
        print u'订单详情，已分拣 的订单：order_status=1,pay_status = 1,UP_HOOKS'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'UP_HOOKS', 'balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 已打包 的订单：order_status=1,pay_status = 1
    def test_orderDetail_orderPacked(self):
        print u'订单详情，已打包 的订单：order_status=1,pay_status = 1,PACKED'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'PACKED', 'balance_status': 'above','risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 已出厂，未存衣 的订单：order_status=1,pay_status = 1
    def test_orderDetail_orderOutFactory(self):
        print u'订单详情，已出厂，未存衣 的订单：order_status=1,pay_status = 1,OUT_FACTORY'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'OUT_FACTORY','balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)

    # 管家已存衣 的订单：order_status=1,pay_status = 1
    def test_orderDetail_orderSaveClean(self):
        print u'订单详情，管家已存衣 的订单：order_status=1,pay_status = 1,WAIT_USER_RECEIVE'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'WAIT_USER_RECEIVE','balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)
        # 进行柜子释放
        for i in range(3):
            basic_operate_instances.openBoxWithQrcode(order_number,settings.cabinetId)

    # 管家已存衣 的订单：需要补费
    def test_orderDetail_supplementFee(self):
        print u'订单详情，管家已存衣,需要补费 的订单,WAIT_USER_RECEIVE'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'WAIT_USER_RECEIVE','balance_status': 'below', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)
        # 进行柜子释放
        for i in range(3):
            basic_operate_instances.openBoxWithQrcode(order_number, settings.cabinetId)

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_orderDetail_orderDone(self):
        print u'订单详情，已完成 的订单：order_status=1,pay_status = 1,DONE'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above','risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderDetail_compare(response_infor_json)


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
    def orderDetail_compare(self,order_detail):
        order_detail_data = order_detail['data']
        #根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=','field_value': order_detail['data']['number']},
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
        refund_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_refund', 'id',refund_param)

        #订单的基础数据比较
        self.assertEqual(order_detail_data['id'], order_list[0]['id'], u'orders:id')
        self.assertEqual(order_detail_data['orderType'], order_list[0]['type'], u'orders:orderType:type')
        self.assertEqual(order_detail_data['predictPrice'], order_list[0]['predict_price'], u'orders:orderType:predict_price')
        self.assertEqual(order_detail_data['couponId'], order_list[0]['coupon_id'], u'orders:orderType:coupon_id')
        self.assertEqual(order_detail_data['number'], order_list[0]['number'], u'orders:number')
        self.assertEqual(order_detail_data['createdAt'], order_list[0]['created_at'].strftime("%Y-%m-%d %H:%M:%S"), u'orders:created_at')
        self.assertEqual(order_detail_data['price'], float(order_list[0]['price']), u'orders:price')
        self.assertEqual(order_detail_data['balanceStatus'], order_list[0]['balance_status'], u'orders:balance_status')
        self.assertEqual(order_detail_data['balancePrice'], float(order_list[0]['balance_price']), u'orders:balance_price')
        self.assertEqual(order_detail_data['activityOutId'], order_list[0]['activity_out_id'], u'orders:activity_out_id')
        self.assertEqual(order_detail_data['isRepeatWash'], order_list[0]['is_repeat_wash'], u'orders:is_repeat_wash')
        self.assertEqual(order_detail_data['comment'], usefulTools_instances.NoneTransitStr(order_list[0]['comment']), u'orders:comment')
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
        self.assertIn(orders_status_process_list[0]['created_at'].strftime("%Y-%m-%d"),order_detail_data_express['created_at'], u'orders_status_process:created_at')
        if orders_status_process_list[0]['status'] in ['DELIVERY_PICKUP','DELIVERY_PICKUPED','WAIT_USER_RECEIVE','DONE','CANCEL','BACK','OUT_FACTORY',]:
            self.assertEqual(order_detail_data_express['type'], orders_status_process_list[0]['status'],u'状态校验')
            self.assertEqual(order_detail_data['ordersCabinetStatus'], orders_status_process_list[0]['status'],u'orders_status_process:status')
        elif orders_status_process_list[0]['status'] == 'ASSIGNED_BOX':
            self.assertEqual(order_detail_data_express['type'], u'ASSIGNED_BOX', u'状态校验')
        elif orders_status_process_list[0]['status'] == 'CANCEL_BOX':
            self.assertEqual(order_detail_data_express['type'], u'PAID', u'状态校验')
        elif orders_status_process_list[0]['status'] == 'ORDERED' and order_list[0]['pay_status'] == 0:
            self.assertEqual(order_detail_data_express['type'],  orders_status_process_list[0]['status'],u'状态校验')
            self.assertEqual(order_detail_data_express['status'],common_parameter.ORDERED['description'], u'显示名称')
            self.assertEqual(order_detail_data['ordersCabinetStatus'], orders_status_process_list[0]['status'], u'ordersCabinetStatus')
        elif orders_status_process_list[0]['status'] == 'ORDERED' and order_list[0]['pay_status'] == 1:
            self.assertEqual(order_detail_data_express['type'],  'PAID',u'状态校验')
            self.assertEqual(order_detail_data_express['status'],common_parameter.PAID['description'], u'显示名称')
            self.assertEqual(order_detail_data['ordersCabinetStatus'], 'PAID', u'orders_status_process:status')
        else:
            self.assertEqual(order_detail_data_express['type'], u'ARRIVED_FACTORY', u'状态校验')
            self.assertEqual(order_detail_data_express['status'], common_parameter.ARRIVED_FACTORY['description'],u'显示名称')
        if orders_status_process_list[0]['status'] == 'CANCEL_BOX':
            # self.assertEqual(order_detail_data_express['status'],common_parameter.CANCEL_BOX['description'], u'显示名称')
            self.assertEqual(order_detail_data_express['status'],common_parameter.PAID['description'], u'显示名称')
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
            #校验补费金额
            self.assertEqual(float('%.2f' % order_detail_data['balancePrice']),float(payments_list[0]['real_amount'] + payments_list[0]['gift_amount']), u'user_coupon:money')
        #details校验
        order_detail_list.reverse()
        order_detail_data_details = order_detail_data['details']
        for i in range(len(order_detail_data_details)):
            self.assertEqual(order_detail_data_details[i]['amount'], order_detail_list[i]['amount'], u'order_detail_list:amount')
            self.assertEqual(order_detail_data_details[i]['goodsActivityId'], order_detail_list[i]['goods_activity_id'], u'order_detail_list:goodsActivityId')
            self.assertEqual(order_detail_data_details[i]['goodsId'], order_detail_list[i]['goods_id'], u'order_detail_list:goods_id')
            self.assertEqual(order_detail_data_details[i]['goodsName'], order_detail_list[i]['goods_name'], u'order_detail_list:goods_name')
            self.assertEqual(order_detail_data_details[i]['goodsPrice'], order_detail_list[i]['goods_price'], u'order_detail_list:goods_price')
            self.assertEqual(order_detail_data_details[i]['goodsThumbnail'], order_detail_list[i]['goods_thumbnail'], u'order_detail_list:goods_thumbnail')
            self.assertEqual(order_detail_data_details[i]['id'], order_detail_list[i]['id'], u'order_detail_list:id')
            self.assertEqual(order_detail_data_details[i]['orderId'], order_detail_list[i]['order_id'], u'order_detail_list:order_id')

        #优惠券校验
        order_detail_data_coupon = order_detail_data['coupon']
        if order_list[0]['coupon_id'] is not None and order_list[0]['coupon_id'] !=0:
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
            self.assertEqual(order_detail_data_coupon['commonCouponId'], user_coupon[0]['common_coupon_id'], u'user_coupon:common_coupon_id')
            self.assertEqual(order_detail_data_coupon['couponId'], user_coupon[0]['coupon_id'], u'user_coupon:coupon_id')
            self.assertEqual(order_detail_data_coupon['couponType'], coupon_list[0]['coupon_type'], u'coupon_list:coupon_type')
            self.assertEqual(order_detail_data_coupon['deliveryCouponId'], user_coupon[0]['delivery_coupon_id'], u'user_coupon:delivery_coupon_id')
            self.assertEqual(order_detail_data_coupon['id'], user_coupon[0]['id'], u'user_coupon:id')
            self.assertEqual(order_detail_data_coupon['isUsed'], user_coupon[0]['is_used'], u'user_coupon:is_used')
            if coupon_list[0]['coupon_type'] ==0 and order_detail_data['price'] < float(coupon_list[0]['max_money']):
                print u'实际分拣价格 < 优惠券使用条件，不进行校验优惠券的使用状态'
            else:
                self.assertEqual(order_detail_data_coupon['isUsed'], 1, u'user_coupon:is_used')
            self.assertEqual(order_detail_data_coupon['maxMoney'], float(coupon_list[0]['max_money']), u'coupon_list:maxMoney')
            self.assertEqual(order_detail_data_coupon['minMoney'], float(coupon_list[0]['min_money']), u'coupon_list:minMoney')
            #计算优惠券的金额
            discount = float(user_coupon[0]['money']) if coupon_list[0]['coupon_type'] != 2 else float(order_detail_data['predictPrice']*(1-float(user_coupon[0]['money'])/10))
            #根据折扣券金额是否大于最大抵扣金额进行修改
            if order_detail_data_coupon['couponType'] == 2:
                discount = float('%.2f' %discount) if float('%.2f' %discount) < float(coupon_list[0]['max_money']) else float(coupon_list[0]['max_money'])
            #根据支付金额是否为0进行修改
            discount = discount if float('%.2f' % order_detail_data['payInfo']['payPrice']) >0 else float(user_coupon[0]['money'])
            self.assertEqual(order_detail_data_coupon['money'], float(user_coupon[0]['money']), u'user_coupon:money')
            self.assertEqual(order_detail_data['payInfo']['discount'], discount, u'user_coupon:money')

            #计算优惠券的金额
            coupon_real_amount = discount if order_detail_data['predictPrice'] > discount else order_detail_data['predictPrice']
            payPrice = float('%.2f' % (order_detail_data['predictPrice'] - coupon_real_amount))
            #检查需要支付的金额是否正确
            self.assertEqual(float('%.2f' % order_detail_data['payInfo']['payPrice']), payPrice, u'user_coupon:money')
            # 检查payments表中的数据
            if len(payments_list) == 1:
                self.assertEqual(payments_list[0]['coupon_id'], order_detail_data_coupon['id'],u'orders_payments:coupon_id')
                self.assertEqual(float(payments_list[0]['coupon_amount']), order_detail_data_coupon['money'],u'orders_payments:money')
                self.assertEqual(float(payments_list[0]['coupon_real_amount']), coupon_real_amount, u'orders_payments:coupon_real_amount')
                self.assertEqual(float('%.2f' % order_detail_data['payInfo']['payPrice']), float('%.2f' % float(payments_list[0]['real_amount']+payments_list[0]['gift_amount'])), u'user_coupon:money')
            if len(payments_list) == 2:
                self.assertEqual(payments_list[1]['coupon_id'], order_detail_data['couponId'],u'orders_payments:coupon_id')
                self.assertEqual(float(payments_list[1]['coupon_real_amount']), coupon_real_amount,u'orders_payments:coupon_real_amount')
        #如果状态=0，则直接返回，不检查柜子相关数据
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
            {'field_name': 'cabinet_id', 'filed_concatenation': '=', 'field_value': settings.cabinetId},
            {'field_name': 'box_number', 'filed_concatenation': '=','field_value': orders_cabinet_list[0]['user_send_box_number']},
        ]
        cabinet_code_list = qy_db_manager_instances.get_table_data_sigle('cabinet_iot', 'cabinet_code', 'id', cabinet_code_param)
        if order_detail_data_express['type'] in ['DELIVERY_PICKUP']:
            # 用户存衣、用户待取的时候生成取衣码
            self.assertEqual(len(cabinet_code_list), 1, u'cabinet_code 记录数=1')
        if order_detail_data_express['type'] == 'WAIT_USER_RECEIVE':
            self.assertTrue(len(cabinet_code_list) > 0, u'cabinet_code 记录数>0')
        if orders_cabinet_list[0]['status'] == 'DELIVERY_PICKUP':
            self.assertEqual(order_detail_data_express['status'], common_parameter.DELIVERY_PICKUP['description'], u'orders_cabinet:status')
            self.assertEqual(cabinet_code_list[0]['type'], 2,u'存衣之后，code_type为管家取衣码')
        if orders_cabinet_list[0]['status'] == 'DELIVERY_PICKUPED':
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
        if orders_status_process_list[0]['status'] == 'DONE':
            self.assertEqual(order_detail_data_express['status'], common_parameter.DONE_LIST['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'BACK':
            self.assertEqual(order_detail_data_express['status'], common_parameter.BACK['description'], u'显示名称')
        if orders_status_process_list[0]['status'] == 'CANCEL':
            self.assertEqual(order_detail_data_express['status'], common_parameter.CANCEL['description'], u'显示名称')

        #进行package检查
        order_detail_data_packs = order_detail_data['packs']
        if orders_cabinet_list[0]['status'] in ['PACKED','OUT_FACTORY','WAIT_USER_RECEIVE']:
            receipt_id = 'SELECT id FROM factory_receipt where order_id ='+ str(order_list[0]['id'])
            db_param = [
                {'field_name': 'receipt_id', 'filed_concatenation': 'in', 'field_value': '('+receipt_id+')'},
            ]
            packs_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_packs', 'id',db_param)
            self.assertEqual(len(order_detail_data_packs),len(packs_list),u'打包的数量是否一致')
            packs_list.reverse()
            for i in range(len(packs_list)):
                # code = u'已取出' if packs_list[i]['status'] == 3 else (u'尚未送回' if packs_list[i]['status'] == 0 else u'物流已存柜')
                cargo_id = 'SELECT id FROM cabinet_iot.cargo WHERE pack_id =' + str(packs_list[i]['id'])
                db_param = [
                    {'field_name': 'pack_id', 'filed_concatenation': 'in', 'field_value': '('+cargo_id+')'},
                ]
                cabinet_code_list = qy_db_manager_instances.get_table_data_sigle('cabinet_iot', 'cabinet_code', 'id',db_param)
                code = u'已取出' if packs_list[i]['status'] == 3 else (u'尚未送回' if packs_list[i]['status'] != 2 else cabinet_code_list[0]['code'])
                if order_list[0]['balance_price'] !=0 and order_list[0]['balance_status'] == 0:
                    code = u'支付后查看'
                self.assertEqual(order_detail_data_packs[i]['packId'],packs_list[i]['id'],u'packId')
                self.assertEqual(order_detail_data_packs[i]['code'],code,u'code')
        #检查退费情况
        if order_list[0]['balance_price'] < 0 and order_list[0]['balance_status'] == 0:
            self.assertEqual(len(refund_list),0,u'退款记录数')
        if order_list[0]['balance_price'] < 0 and order_list[0]['balance_status'] == 1:
            self.assertEqual(len(refund_list),1,u'退款记录数')
            self.assertEqual(abs(order_detail_data['balancePrice']), float(refund_list[0]['fee']), u'校验退款的金额')
        #根据需要进行二次支付
        if order_list[0]['balance_price'] > 0 and order_list[0]['balance_status'] == 0:
            qy_db_manager_instances.update_user_balance(user_infor, 'balance', order_detail_data['balancePrice'])
            basic_operate_instances.basic_iface_request('',iface_list.orderPay,iface_param.orderPay,order_list[0]['number'],'balance',1)




