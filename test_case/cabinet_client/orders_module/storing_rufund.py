# -*- coding:utf-8 -*-
"""
ljq 2019-10-10
接口名称：分拣-退款测试
接口地址：
method：POST

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
from test_case.factory_sorting import factory_basic_operate
from test_case.cabinet_iot import iot_basic_operate
from test_case.cabinet_logistics import logistics_basic_operate

#实例化调用的class

basic_operate_instances = cabinet_basic_operate.basic_operate()
qy_db_manager_instances = qy_db_manager.database_operate()
usefulTools_instances = usefulTools.userfulToolsFactory()
factory_basic_operate_instances = factory_basic_operate.basic_operate()
iot_basic_operate_instances = iot_basic_operate.basic_operate()
logistics_basic_operate_instances = logistics_basic_operate.basic_operate()

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
    def create_order_by_request(self,good_type,order_status,order_coupon_addition):
        print u'进行订单取消请求，参数为空的情况'
        # 定义需要创建的订单类型,真实支付金额>0,优惠券支付金额>0
        order_coupon_infor = {'coupon_type_text': '', 'coupon_type': '1', 'order_infor': '', 'pay_status': 'above','coupon_money': 10}
        order_coupon_infor['coupon_type'] = order_coupon_addition['coupon_type']
        order_coupon_infor['pay_status'] = order_coupon_addition['pay_status']
        order_number = basic_operate_instances.make_order_according_need(good_type, order_coupon_infor, order_status)
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=', 'field_value': order_number},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
        #进行更新用户余额
        qy_db_manager_instances.update_user_balance(user_infor,order_status['pay_type'],float(order_list[0]['predict_price']))
        #获取当前账户余额并进行记录
        user_list = qy_db_manager_instances.get_user_infor(user_infor['phone'])
        #进行支付
        basic_operate_instances.basic_iface_request('',iface_list.orderPay,iface_param.orderPay,order_number,'balance',0)
        #进行扫码开柜
        basic_operate_instances.openBoxWithQrcode(order_number,settings.cabinetId)
        # 管家取出脏衣...................................................................................
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
        # 进行分拣操作
        receiptId = factory_basic_operate_instances.clothes_store_wash(seal_number, order_list[0]['id'],order_status['balance_status'], order_status['risk'])
        # 计算所有衣物的总价
        real_price = qy_db_manager_instances.count_clother_price(receiptId)
        #进行风险确认不洗操作
        db_param = [
            {'field_name': 'receipt_id', 'filed_concatenation': '=', 'field_value': receiptId},
            {'field_name': 'wash_risk', 'filed_concatenation': '=', 'field_value': 1},
            {'field_name': 'wash_risk_confirm_status', 'filed_concatenation': '=', 'field_value': 0},
        ]
        clother_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_order_clothes','id', db_param)
        clother_random = random.randint(0,len(clother_list)-1)
        basic_operate_instances.basic_iface_request('',iface_list.detectionConfirm,iface_param.detectionConfirm,order_number,clother_list[clother_random]['id'],-1)
        #重新计算价格
        real_price = float('%.2f' % (real_price-float(clother_list[clother_random]['price'])))
        # 根据封签号进行上挂操作
        receiptId = factory_basic_operate_instances.racking_accord_rfId(seal_number,order_list[0]['id'])
        # 根据上挂ID进行打包操作,当前只打包一个包裹，如果多包裹后续在完成订单部分重新调用
        package_num = factory_basic_operate_instances.factory_packing(receiptId)
        # 进行出厂、存衣操作
        logistics_basic_operate_instances.logistics_dealWith_package(receiptId, 'OUT_FACTORY')
        order_list[0]['real_price'] = real_price
        order_list[0]['real_balance_before'] = user_list[0]['real_balance']
        order_list[0]['gift_balance_before'] = user_list[0]['gift_balance']
        order_list[0]['balance_before'] = user_list[0]['balance']
        order_list[0]['pay_type'] = order_status['pay_type']
        order_list[0]['good_type'] = good_type
        return order_list[0]


    # 使用真实金额支付，分拣之后检查退款情况
    def atest_balanceRufund_realBalance(self):
        print u'进行订单取消请求，参数为空字符串的情况，全部为空'
        order_status = {'status': 0, 'pay_status': 0,'balance_status': 'above', 'risk': '1','pay_type':'real_balance'}
        order_coupon_addition = {'coupon_type':1,'pay_status':'above'}
        order_infor = self.create_order_by_request('goods',order_status,order_coupon_addition)
        #进行数据校验
        self.balanceRufund_data_compare(order_infor)

    # 使用赠送金额支付，分拣之后检查退款情况
    def atest_balanceRufund_giftBalance(self):
        print u'进行订单取消请求，参数为空字符串的情况，全部为空'
        order_status = {'status': 0, 'pay_status': 0, 'balance_status': 'above', 'risk': '1','pay_type': 'gift_balance'}
        order_coupon_addition = {'coupon_type': 1, 'pay_status': 'above'}
        order_infor = self.create_order_by_request('goods', order_status, order_coupon_addition)
        # 进行数据校验
        self.balanceRufund_data_compare(order_infor)

    # 使用赠送金额支付，分拣之后检查退款情况
    def atest_balanceRufund_activity(self):
        print u'进行订单取消请求，参数为空字符串的情况，全部为空'
        order_status = {'status': 0, 'pay_status': 0, 'balance_status': 'above', 'risk': '1','pay_type': 'gift_balance'}
        order_coupon_addition = {'coupon_type': 1, 'pay_status': 'above'}
        order_infor = self.create_order_by_request('activity', order_status, order_coupon_addition)
        # 进行数据校验
        self.balanceRufund_data_compare(order_infor)

    # 使用固定券支付，分拣之后检查退款情况
    def atest_abalanceRufund_fixedCoupon(self):
        print u'进行订单取消请求，参数为空字符串的情况，全部为空'
        order_status = {'status': 0, 'pay_status': 0, 'balance_status': 'above', 'risk': '1', 'pay_type': 'real_balance'}
        order_coupon_addition = {'coupon_type': 0, 'pay_status': 'above'}
        order_infor = self.create_order_by_request('goods', order_status, order_coupon_addition)
        # 进行数据校验
        self.balanceRufund_data_compare(order_infor)

    #基础的数据比对方法
    def balanceRufund_data_compare(self,order_infor):
        #根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=', 'field_value': order_infor['number']},
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
        # 交接单信息
        receipt_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        receipt_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api','factory_receipt', 'id',receipt_param)

        #根据商品类型区分：活动，则不退款
        if order_infor['good_type'] == 'activity':
            self.assertEqual(order_list[0]['balance_status'], 0, u'活动不进行差价处理：0')
            self.assertEqual(order_list[0]['balance_price'], 0, u'活动不进行差价处理：0')
            self.assertEqual(len(refund_list), 0, u'退款记录数：0')
            return 0
        user_coupon_id = order_list[0]['coupon_id'] if order_list[0]['coupon_id'] is not None else 0
        user_coupon_param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': user_coupon_id},
        ]
        user_coupon = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'user_coupon', 'id', user_coupon_param)
        coupon_id = 0
        if len(user_coupon) ==1:
            coupon_id = user_coupon[0]['common_coupon_id'] if user_coupon[0]['common_coupon_id'] !=0 else user_coupon[0]['delivery_coupon_id']
        coupon_list = []
        if coupon_id != 0:
            coupon_param = [
                {'field_name': 'id', 'filed_concatenation': '=', 'field_value': coupon_id},
            ]
            coupon_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'delivery_coupon', 'id',coupon_param)
        #计算当前需要补差价的金额
        balance_price = order_infor['real_price'] - float(order_list[0]['predict_price'])
        balance_price_below = float('%.2f' % balance_price) if abs(float('%.2f' % balance_price)) < float(order_list[0]['paid_price']) else 0 - float(order_list[0]['paid_price'])
        balance_price = balance_price if balance_price > 0 else balance_price_below

        #计算实际需要真实支付的金额
        real_pay_price = float(order_infor['real_price']) - float(payments_list[0]['coupon_real_amount'])
        real_pay_price = float('%.2f' % real_pay_price) if real_pay_price > 0 else 0

        #实际金额 < 固定券起始金额的情况下，优惠券退回，补差价根据实际金额 与支付金额进行比较
        if len(coupon_list) == 1 and coupon_list[0]['coupon_type'] == 0 and order_infor['real_price'] < float(coupon_list[0]['max_money']):
            #实际金额  - 实际支付金额 = 补差价的金额
            balance_price = float('%.2f' % (order_infor['real_price'] - float(order_list[0]['paid_price'])))
            #检查优惠券是否退回
            self.assertEqual(user_coupon[0]['is_used'], 0, u'user_coupon:is_used,优惠券已退回')
            #计算优惠券返回的时候，需要支付的真实金额
            real_pay_price = order_infor['real_price'] if balance_price < 0 else float(order_list[0]['paid_price'])

        #非活动商品则需要进行退补价处理：
        #先进行基础信息判断：
        self.assertEqual(receipt_list[0]['price'],order_infor['real_price'],u'交接单中的金额是否与计算金额相等')
        self.assertEqual(receipt_list[0]['price'],order_list[0]['price'],u'交接单中的金额是否与订单中实际价格相等')
        self.assertEqual(order_list[0]['balance_status'],1,u'是否有差价为是：1')

        #检查需要进行退补费的价格是否正确：退费为 负数，补费为正数
        self.assertEqual(float(order_list[0]['balance_price']),balance_price,u'计算需要补费的金额是否正确')
        #如果退补价为正数，则需要补费，直接返回，不做退款表的校验
        if balance_price > 0:
            return 0
        #检查退款表，orders_refund数据比对
        self.assertEqual(float(refund_list[0]['fee']), abs(balance_price), u'orders_refund:fee')
        self.assertEqual(float(refund_list[0]['fee']), abs(order_list[0]['balance_status']), u'orders_refund:fee')
        self.assertEqual(float(refund_list[0]['type']), 0, u'orders_refund:type')
        #计算余额 并比对
        balance = float('%.2f' % (order_infor['balance_before'] - real_pay_price))
        self.assertEqual(user_list[0]['balance'], balance, u'user:real_balance')
        if order_infor['pay_type'] == 'real_balance':
            self.assertEqual(float(refund_list[0]['real_fee']),abs(balance_price),u'orders_refund:real_fee')
            #计算剩余金额
            real_balance = float('%.2f' %(order_infor['real_balance_before'] - real_pay_price))
            self.assertEqual(user_list[0]['real_balance'],real_balance,u'user:real_balance')
        if order_infor['pay_type'] == 'gift_balance':
            self.assertEqual(float(refund_list[0]['gift_fee']),abs(balance_price),u'orders_refund:real_fee')
            gift_balance = float('%.2f' % (order_infor['gift_balance_before'] - real_pay_price))
            self.assertEqual(user_list[0]['gift_balance'],gift_balance,u'user:real_balance')

        #进行优惠券检查
        self.assertEqual(user_coupon[0]['is_used'], 1, u'user_coupon:is_used')



