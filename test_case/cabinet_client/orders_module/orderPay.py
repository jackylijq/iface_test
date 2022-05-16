# -*- coding:utf-8 -*-
"""
ljq 2019-09-20
接口名称：订单支付
接口地址：/cabinet_client/api/v1/order/createOrder
method：POST

接口设计：
1、参数异常的情况：空值、空字符串、格式不对
2、订单错误、不存在的情况，无法支付
3、非本人订单无法支付
4、已取消的订单无法支付
5、订单金额为0的情况下调用微信支付
6、订单金额为0，可以使用余额支付
7、订单与type不匹配的情况，正常订单 type=1，提示异常。补差价订单，type=0 提示异常
8、正常订单使用真实金额支付
9、正常订单，使用赠送金额支付
10、订单金额大于0，使用微信支付
11、比对支付记录是否正确

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

#定义接口返回数据集
if_response_list = []
recharge_param = []

class orderPay_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        #获取单件洗的一些基础数据
        #本人已取消的订单
        orders_cancel_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': -1},
            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        ]
        self.orders_cancel = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', orders_cancel_param)
        #本人未支付的订单
        orders_noPay_param = [
            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'status', 'filed_concatenation': '!=', 'field_value': -1},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        ]
        self.orders_noPay = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',orders_noPay_param)
        #本人已支付的订单
        orders_Paied_param = [
            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': '1'},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        ]
        self.orders_Paied = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',orders_Paied_param)
        #非本人订单-非支付
        orders_notOwner_param = [
            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'user_id', 'filed_concatenation': '!=', 'field_value': user_infor['user_id']},
        ]
        self.orders_notOwner = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',orders_notOwner_param)

    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.orderPay,iface_param.orderPay,*args)
        return response_infor_json

    #进行支付请求，参数为空的情况
    def test_orderPay_noPrame(self):
        print u'进行支付请求，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],400,u'系统响应码为：400')
        self.assertIn(u'参数错误',response_infor_json['message'],  u'系统响message包含:参数错误')

    # 进行支付请求，参数为空的情况
    def test_orderPay_noPrame2(self):
        print u'进行支付请求，参数为空的情况'
        response_infor_json = self.basic_data_request('371427361297551360')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'参数错误', response_infor_json['message'], u'系统响message包含:参数错误')

    # 参数为空字符串的情况
    def test_orderPay_paramNull(self):
        print u'进行支付请求，参数为空字符串的情况，全部为空'
        response_infor_json = self.basic_data_request('','','')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'参数错误', response_infor_json['message'], u'系统响message包含:参数错误')

    # 参数为空字符串的情况
    def test_orderPay_paramNull2(self):
        print u'进行支付请求，参数为空字符串的情况：payChannel、payType为空'
        response_infor_json = self.basic_data_request('371427361297551360', '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'参数错误', response_infor_json['message'], u'系统响message包含:参数错误')

    # orderNumber不存在的情况
    def test_orderPay_numberNotExist(self):
        print u'进行支付请求，orderNumber不存在的情况'
        response_infor_json = self.basic_data_request('123123123', 'balance', '0')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单不存在', response_infor_json['message'], u'系统响message包含:订单不存在')

    # payChannel不存在的情况
    def test_orderPay_payChannelNotExist(self):
        print u'进行支付请求，payChannel不存在的情况,默认调用微信支付'
        response_infor_json = self.basic_data_request(self.orders_noPay[0]['number'], 'test', '0')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'参数错误', response_infor_json['message'], u'系统响message包含:参数错误')

    # payChannel格式异常
    def test_orderPay_payTypeFormatError(self):
        print u'进行支付请求，payChannel格式异常'
        response_infor_json = self.basic_data_request(self.orders_noPay[0]['number'], 'test', 'a')
        self.assertEqual(response_infor_json['status'], 500, u'系统响应码为：400,目前500')
        # self.assertIn(u'订单不存在', response_infor_json['message'], u'系统响message包含:订单不存在')

    # payChannel不存在的情况
    def test_orderPay_payTypeNotExist(self):
        print u'进行支付请求，payChannel不存在的情况,默认调用微信支付'
        response_infor_json = self.basic_data_request(self.orders_noPay[0]['number'], 'test', '2')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'参数错误', response_infor_json['message'], u'系统响message包含:参数错误')

    # 非本人订单无法支付
    def test_orderPay_othersOrder(self):
        print u'进行支付请求，非本人订单无法支付'
        response_infor_json = self.basic_data_request(self.orders_notOwner[0]['number'], 'wechat', '0')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单不存在', response_infor_json['message'], u'系统响message包含:订单不存在')

    # 已取消的订单，无法进行支付
    def test_orderPay_cancelOrder(self):
        print u'进行支付请求，已取消的订单，无法进行支付'
        response_infor_json = self.basic_data_request(self.orders_cancel[0]['number'], 'wechat', '0')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单已取消', response_infor_json['message'], u'系统响message包含:订单已取消')

    # 正常付费订单，调用补差价的状态payType =1
    def test_orderPay_typeNotMath(self):
        print u'进行支付请求，正常付费订单，调用补差价的状态payType =1 '
        response_infor_json = self.basic_data_request(self.orders_noPay[0]['number'], 'wechat', '1')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'当前订单不需要补费', response_infor_json['message'], u'系统响message包含:当前订单不需要补费')

    # 补差价订单，调用正常付费订单的状态payType =0
    def test_orderPay_typeNotMath2(self):
        print u'进行支付请求，正常付费订单，调用补差价的状态payType =1 '
        response_infor_json = self.basic_data_request(self.orders_noPay[0]['number'], 'wechat', '1')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'当前订单不需要补费', response_infor_json['message'], u'系统响message包含:当前订单不需要补费')

    #支付金额为0，调用微信支付失败
    def test_orderPay_payPriceZero_wechat(self):
        print u'进行支付请求，支付金额为0，微信支付自动转换为余额支付'
        order_number = self.get_order_accord_request('goods',0, 10, 'below')
        #进行接口请求
        response_infor_json = self.basic_data_request(order_number, 'wechat', '0')
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'支付成功', response_infor_json['message'], u'系统响message包含:支付成功')

    # 支付金额为0，调用余额支付成功，余额为0的情况
    def test_orderPay_payPriceZero_balance(self):
        print u'进行支付请求，支付金额为0，调用余额支付成功，余额为0的情况 '
        order_pay_param = []
        order_pay_infor = {}
        payChannel = 'balance'
        payType = 0
        order_number = self.get_order_accord_request('goods',0, 10, 'below')
        #根据orderNumber获取order详情
        order_detail = basic_operate_instances.basic_iface_request('',iface_list.orderDetail,iface_param.orderDetail,order_number)
        #更新当前用户余额为0
        qy_db_manager_instances.update_user_infor(user_infor['phone'], 0,0, 0)
        #获取当前的用户信息
        user_infor_payBefore = basic_operate_instances.basic_iface_request('',iface_list.userInfo,iface_param.userInfo)
        # 进行接口请求
        response_infor_json = self.basic_data_request(order_number, payChannel, payType)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'支付成功', response_infor_json['message'], u'系统响message包含:支付成功')
        #参数进行整理
        order_pay_infor['status'] = 0
        if payChannel == 'balance' and response_infor_json['status'] == 200:
            order_pay_infor['status'] = 1
        order_pay_infor['payChannel'] = cabinet_client_constant.common_parameter.cabinet_payChannel[payChannel]
        order_pay_infor['payType'] = payType
        #进行数据校验：
        self.order_payResult_compare(order_detail,order_pay_infor,user_infor_payBefore)

    # 支付金额>0，使用真实金额进行支付，支付完成之后，真实金额>0
    def test_orderPay_realPayAbove(self):
        print u'进行支付请求，支付金额>0，使用真实金额进行支付，支付完成之后，真实金额>0'
        order_pay_param = []
        order_pay_infor = {}
        payChannel = 'balance'
        payType = 0
        #payPrice：是否需要进行余额支付，>0为需要,coupon_money：是否需要使用优惠券，=0为不用；,pay_status：above:订单金额>优惠券金额，below订单金额<=优惠券金额
        #good_type:单件洗：goods ；活动：activity
        order_number = self.get_order_accord_request('goods',10,10,'above')
        # 根据orderNumber获取order详情
        order_detail = basic_operate_instances.basic_iface_request('', iface_list.orderDetail,iface_param.orderDetail, order_number)
        #更新用户的余额信息#pay_type支付类型：real_balance,gift_balance,balance，为空的时候，默认为0
        payPrice = order_detail['data']['payInfo']['payPrice']
        self.update_user_balance('real_balance',payPrice)
        # 获取当前的用户信息
        user_infor_payBefore = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        # 进行接口请求
        response_infor_json = self.basic_data_request(order_number, payChannel, payType)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'支付成功', response_infor_json['message'], u'系统响message包含:支付成功')
        # 参数进行整理
        order_pay_infor['status'] = 0
        if payChannel == 'balance' and response_infor_json['status'] == 200:
            order_pay_infor['status'] = 1
        order_pay_infor['payChannel'] = cabinet_client_constant.common_parameter.cabinet_payChannel[payChannel]
        order_pay_infor['payType'] = payType
        # 进行数据校验：
        self.order_payResult_compare(order_detail, order_pay_infor, user_infor_payBefore)

    # 支付金额>0，使用赠送金额进行支付，支付完成之后赠送金额>0
    def test_orderPay_giftPayAbove(self):
        print u'进行支付请求，支付金额>0，使用赠送金额进行支付，支付完成之后赠送金额>0'
        order_pay_param = []
        order_pay_infor = {}
        payChannel = 'balance'
        payType = 0
        # payPrice：是否需要进行余额支付，>0为需要,coupon_money：是否需要使用优惠券，=0为不用；,pay_status：above:订单金额>优惠券金额，below订单金额<=优惠券金额
        # good_type:单件洗：goods ；活动：activity
        order_number = self.get_order_accord_request('goods', 10, 10, 'above')
        # 根据orderNumber获取order详情
        order_detail = basic_operate_instances.basic_iface_request('', iface_list.orderDetail,iface_param.orderDetail, order_number)
        # 更新用户的余额信息#pay_type支付类型：real_balance,gift_balance,balance，为空的时候，默认为0
        payPrice = order_detail['data']['payInfo']['payPrice']
        self.update_user_balance('gift_balance', payPrice)
        # 获取当前的用户信息
        user_infor_payBefore = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        # 进行接口请求
        response_infor_json = self.basic_data_request(order_number, payChannel, payType)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'支付成功', response_infor_json['message'], u'系统响message包含:支付成功')
        # 参数进行整理
        order_pay_infor['status'] = 0
        if payChannel == 'balance' and response_infor_json['status'] == 200:
            order_pay_infor['status'] = 1
        order_pay_infor['payChannel'] = cabinet_client_constant.common_parameter.cabinet_payChannel[payChannel]
        order_pay_infor['payType'] = payType
        # 进行数据校验：
        self.order_payResult_compare(order_detail, order_pay_infor, user_infor_payBefore)

    # 支付金额>0，使用余额支付，真实金额+赠送金额
    def test_orderPay_balancePay(self):
        print u'进行支付请求，支付金额>0，使用余额支付，真实金额+赠送金额'
        order_pay_param = []
        order_pay_infor = {}
        payChannel = 'balance'
        payType = 0
        # payPrice：是否需要进行余额支付，>0为需要,coupon_money：是否需要使用优惠券，=0为不用；,pay_status：above:订单金额>优惠券金额，below订单金额<=优惠券金额
        # good_type:单件洗：goods ；活动：activity
        order_number = self.get_order_accord_request('goods', 10, 10, 'above')
        # 根据orderNumber获取order详情
        order_detail = basic_operate_instances.basic_iface_request('', iface_list.orderDetail,iface_param.orderDetail, order_number)
        # 更新用户的余额信息#pay_type支付类型：real_balance,gift_balance,balance，为空的时候，默认为0
        payPrice = order_detail['data']['payInfo']['payPrice']
        self.update_user_balance('balance', payPrice)
        # 获取当前的用户信息
        user_infor_payBefore = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        # 进行接口请求
        response_infor_json = self.basic_data_request(order_number, payChannel, payType)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'支付成功', response_infor_json['message'], u'系统响message包含:支付成功')
        # 参数进行整理
        order_pay_infor['status'] = 0
        if payChannel == 'balance' and response_infor_json['status'] == 200:
            order_pay_infor['status'] = 1
        order_pay_infor['payChannel'] = cabinet_client_constant.common_parameter.cabinet_payChannel[payChannel]
        order_pay_infor['payType'] = payType
        # 进行数据校验：
        self.order_payResult_compare(order_detail, order_pay_infor, user_infor_payBefore)

    # 活动支付，使用余额支付，真实金额+赠送金额
    def test_activityOrderPay_balancePay(self):
        print u'进行支付请求，活动支付，使用余额支付，真实金额+赠送金额'
        order_pay_param = []
        order_pay_infor = {}
        payChannel = 'balance'
        payType = 0
        # payPrice：是否需要进行余额支付，>0为需要,coupon_money：是否需要使用优惠券，=0为不用；,pay_status：above:订单金额>优惠券金额，below订单金额<=优惠券金额
        # good_type:单件洗：goods ；活动：activity
        order_number = self.get_order_accord_request('activity', 10, 10, 'above')
        # 根据orderNumber获取order详情
        order_detail = basic_operate_instances.basic_iface_request('', iface_list.orderDetail,iface_param.orderDetail, order_number)
        # 更新用户的余额信息#pay_type支付类型：real_balance,gift_balance,balance，为空的时候，默认为0
        payPrice = order_detail['data']['payInfo']['payPrice']
        self.update_user_balance('balance', payPrice)
        # 获取当前的用户信息
        user_infor_payBefore = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        # 进行接口请求
        response_infor_json = self.basic_data_request(order_number, payChannel, payType)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'支付成功', response_infor_json['message'], u'系统响message包含:支付成功')
        # 参数进行整理
        order_pay_infor['status'] = 0
        if payChannel == 'balance' and response_infor_json['status'] == 200:
            order_pay_infor['status'] = 1
        order_pay_infor['payChannel'] = cabinet_client_constant.common_parameter.cabinet_payChannel[payChannel]
        order_pay_infor['payType'] = payType
        # 进行数据校验：
        self.order_payResult_compare(order_detail, order_pay_infor, user_infor_payBefore)

    # 支付金额>0，使用微信支付
    def test_orderPay_wechatPay(self):
        print u'进行支付请求，支付金额>0，使用余额支付，真实金额+赠送金额'
        order_pay_param = []
        order_pay_infor = {}
        payChannel = 'wechat'
        payType = 0
        # payPrice：是否需要进行余额支付，>0为需要,coupon_money：是否需要使用优惠券，=0为不用；,pay_status：above:订单金额>优惠券金额，below订单金额<=优惠券金额
        # good_type:单件洗：goods ；活动：activity
        order_number = self.get_order_accord_request('goods', 10, 10, 'above')
        # 根据orderNumber获取order详情
        order_detail = basic_operate_instances.basic_iface_request('', iface_list.orderDetail,iface_param.orderDetail, order_number)
        # 更新用户的余额信息#pay_type支付类型：real_balance,gift_balance,balance，为空的时候，默认为0
        payPrice = order_detail['data']['payInfo']['payPrice']
        self.update_user_balance('balance', payPrice)
        # 获取当前的用户信息
        user_infor_payBefore = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        # 进行接口请求
        response_infor_json = self.basic_data_request(order_number, payChannel, payType)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'支付成功', response_infor_json['message'], u'系统响message包含:支付成功')
        # 参数进行整理
        order_pay_infor['status'] = 0
        if payChannel == 'balance' and response_infor_json['status'] == 200:
            order_pay_infor['status'] = 1
        order_pay_infor['payChannel'] = cabinet_client_constant.common_parameter.cabinet_payChannel[payChannel]
        order_pay_infor['payType'] = payType
        # 进行数据校验：
        self.order_payResult_compare(order_detail, order_pay_infor, user_infor_payBefore)

    # 活动支付，使用微信支付
    def test_activityOrderPay_wechatPay(self):
        print u'进行支付请求，支付金额>0，使用余额支付，真实金额+赠送金额'
        order_pay_param = []
        order_pay_infor = {}
        payChannel = 'wechat'
        payType = 0
        # payPrice：是否需要进行余额支付，>0为需要,coupon_money：是否需要使用优惠券，=0为不用；,pay_status：above:订单金额>优惠券金额，below订单金额<=优惠券金额
        # good_type:单件洗：goods ；活动：activity
        order_number = self.get_order_accord_request('goods', 10, 10, 'above')
        # 根据orderNumber获取order详情
        order_detail = basic_operate_instances.basic_iface_request('', iface_list.orderDetail,iface_param.orderDetail, order_number)
        # 更新用户的余额信息#pay_type支付类型：real_balance,gift_balance,balance，为空的时候，默认为0
        payPrice = order_detail['data']['payInfo']['payPrice']
        self.update_user_balance('balance', payPrice)
        # 获取当前的用户信息
        user_infor_payBefore = basic_operate_instances.basic_iface_request('', iface_list.userInfo,iface_param.userInfo)
        # 进行接口请求
        response_infor_json = self.basic_data_request(order_number, payChannel, payType)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'支付成功', response_infor_json['message'], u'系统响message包含:支付成功')
        # 参数进行整理
        order_pay_infor['status'] = 0
        if payChannel == 'balance' and response_infor_json['status'] == 200:
            order_pay_infor['status'] = 1
        order_pay_infor['payChannel'] = cabinet_client_constant.common_parameter.cabinet_payChannel[payChannel]
        order_pay_infor['payType'] = payType
        # 进行数据校验：
        self.order_payResult_compare(order_detail, order_pay_infor, user_infor_payBefore)

    #根据需要进行查询或是生成订单
    def get_order_accord_request(self,good_type,payPrice,coupon_money,pay_status):
        # 定义需要的订单类型：真实支付金额>0,优惠券支付金额>0
        order_condition = {'status': 0, 'pay_status': 0, 'user_id': user_infor['user_id'], 'goods_activity_id': '','goods_id': '', 'payPrice': 10}
        order_condition['payPrice'] = payPrice
        order_condition['coupon_money'] = coupon_money
        # 定义需要创建的订单类型,真实支付金额>0,优惠券支付金额>0
        order_coupon_infor = {'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': '','coupon_money':10}
        order_coupon_infor['pay_status'] = pay_status
        order_number = basic_operate_instances.get_order_accroding_request(good_type, order_condition)
        # 未获取到支付金额为0的订单，则直接创建
        if order_number == 0:
            order_number = basic_operate_instances.make_order_according_need(good_type, order_coupon_infor)
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
    def order_payResult_compare(self,order_detail,order_pay_infor,user_infor_payBefore):
        #根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=','field_value': order_detail['data']['number']},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        #根据order信息，获取支付信息
        payments_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        payments_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_payments', 'id', payments_param)
        # 检查人员表的金额是否正确
        db_param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        ]
        user_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'users', 'created_at', db_param)
        # 参数进行整理
        # order_pay_infor['status'] = 0
        # if payChannel == 'balance' and response_infor_json['status'] == 200:
        #     order_pay_infor['status'] = 1
        order_pay_infor['balance'] = user_infor_payBefore['data']['balance']
        order_pay_infor['real_balance'] = user_infor_payBefore['data']['realBalance']
        order_pay_infor['gift_balance'] = user_infor_payBefore['data']['giftBalance']
        # order_pay_infor['payChannel'] = cabinet_client_constant.common_parameter.cabinet_payChannel['\'' + payChannel + '\'']
        # order_pay_infor['payType'] = payType
        discount = order_detail['data']['payInfo']['discount']
        order_pay_infor['coupon_id'] = discount if discount == 0 else order_detail['data']['coupon']['id']
        order_pay_infor['coupon_amount'] = 0 if discount == 0 else order_detail['data']['coupon']['money']
        order_pay_infor['coupon_real_amount'] = order_detail['data']['price'] - order_detail['data']['payInfo']['payPrice']
        order_pay_infor['paid_price_need'] = order_detail['data']['payInfo']['payPrice']
        if order_pay_infor['status'] == 1:
            order_pay_infor['paid_price'] = order_detail['data']['payInfo']['payPrice']
        else:
            order_pay_infor['paid_price'] = 0
        order_pay_infor['price'] = order_detail['data']['price']
        order_pay_infor['new_balance'] = order_pay_infor['balance'] - order_detail['data']['payInfo']['payPrice']
        # 真实金额支付金额
        real_balance_pay_money = order_pay_infor['real_balance'] - order_detail['data']['payInfo']['payPrice']
        order_pay_infor['real_amount'] = order_detail['data']['payInfo']['payPrice'] if real_balance_pay_money > 0 else order_pay_infor['real_balance']
        order_pay_infor['new_real_balance'] = real_balance_pay_money if real_balance_pay_money > 0 else 0
        # 赠送金额支付金额
        gift_balance_pay_money = abs(real_balance_pay_money) if real_balance_pay_money < 0 else 0
        order_pay_infor['gift_amount'] = gift_balance_pay_money
        order_pay_infor['new_gift_balance'] = order_pay_infor['gift_balance'] - gift_balance_pay_money

        #先进行order表的比对
        self.assertEqual(order_list[0]['pay_status'], order_pay_infor['status'], u'pay_status')
        self.assertEqual(order_list[0]['status'], 0, u'status')
        self.assertEqual(order_list[0]['user_id'], int(user_infor['user_id']), u'user_id')
        self.assertEqual(float(order_list[0]['price']), order_pay_infor['price'], u'price')
        self.assertEqual(float(order_list[0]['paid_price']), order_pay_infor['paid_price'], u'paid_price')
        self.assertEqual(order_list[0]['type'], order_pay_infor['payType'], u'type:payType')
        self.assertEqual(float(order_list[0]['predict_price']), order_pay_infor['price'], u'predict_price')
        if order_pay_infor['payType'] == 0:
            self.assertEqual(float(order_list[0]['balance_price']), 0, u'balance_price')
            self.assertEqual(float(order_list[0]['balance_status']), 0, u'balance_status')
        #进行payments数据比对
        self.assertEqual(payments_list[0]['status'], order_pay_infor['status'], u'orders_payments:status')
        self.assertEqual(payments_list[0]['payment_type'], order_pay_infor['payChannel'], u'orders_payments:payment_type')
        self.assertEqual(payments_list[0]['user_id'], float(user_infor['user_id']), u'orders_payments:user_id')
        self.assertEqual(payments_list[0]['order_id'], order_list[0]['id'], u'orders_payments:order_id')
        # self.assertEqual(float(payments_list[0]['amount']), order_pay_infor['paid_price_need'], u'orders_payments:amount') #字段已废弃
        self.assertEqual(payments_list[0]['coupon_id'], order_pay_infor['coupon_id'], u'orders_payments:coupon_id')
        self.assertEqual(float(payments_list[0]['coupon_amount']), order_pay_infor['coupon_amount'], u'orders_payments:coupon_amount')
        self.assertEqual(float(payments_list[0]['coupon_real_amount']), float('%.2f'% order_pay_infor['coupon_real_amount']), u'orders_payments:coupon_real_amount')
        #余额支付进行金额计算，并进行比对
        if order_pay_infor['payChannel'] == 1:
            self.assertEqual(float(payments_list[0]['gift_amount']), float('%.2f'% order_pay_infor['gift_amount']), u'orders_payments:gift_amount')
            self.assertEqual(float(payments_list[0]['real_amount']), float('%.2f'% order_pay_infor['real_amount']), u'orders_payments:real_amount')
            self.assertEqual(float(payments_list[0]['balance']), order_pay_infor['balance'], u'orders_payments:balance')
            self.assertEqual(float(payments_list[0]['real_balance']), order_pay_infor['real_balance'], u'orders_payments:real_balance')
            self.assertEqual(float(payments_list[0]['gift_balance']), order_pay_infor['gift_balance'], u'orders_payments:gift_balance')
            self.assertEqual(float(payments_list[0]['new_balance']), float('%.2f'% order_pay_infor['new_balance']), u'orders_payments:new_balance')
            self.assertEqual(float(payments_list[0]['new_real_balance']), float('%.2f'% order_pay_infor['new_real_balance']), u'orders_payments:new_real_balance')
            self.assertEqual(float(payments_list[0]['new_gift_balance']), float('%.2f'% order_pay_infor['new_gift_balance']), u'orders_payments:new_gift_balance')
            self.assertEqual(float(user_list[0]['balance']), float('%.2f' % order_pay_infor['new_balance']),u'user_list:balance')
            self.assertEqual(float(user_list[0]['real_balance']), float('%.2f' % order_pay_infor['new_real_balance']),u'user_list:real_balance')
            self.assertEqual(float(user_list[0]['gift_balance']), float('%.2f' % order_pay_infor['new_gift_balance']),u'user_list:gift_balance')
        #微信支付，余额不变
        if order_pay_infor['payChannel'] == 4:
            self.assertEqual(float(payments_list[0]['gift_amount']),0,u'orders_payments:gift_amount=0，微信')
            self.assertEqual(float(payments_list[0]['real_amount']),order_detail['data']['payInfo']['payPrice'],u'orders_payments:gift_amount=0，微信')
            self.assertEqual(float(payments_list[0]['balance']), order_pay_infor['balance'], u'orders_payments:balance')
            self.assertEqual(float(payments_list[0]['real_balance']), order_pay_infor['real_balance'],u'orders_payments:real_balance')
            self.assertEqual(float(payments_list[0]['gift_balance']), order_pay_infor['gift_balance'],u'orders_payments:gift_balance')
            self.assertEqual(float(payments_list[0]['new_balance']), order_pay_infor['balance'], u'orders_payments:new_balance')
            self.assertEqual(float(payments_list[0]['new_real_balance']), order_pay_infor['real_balance'],u'orders_payments:new_real_balance')
            self.assertEqual(float(payments_list[0]['new_gift_balance']), order_pay_infor['gift_balance'], u'orders_payments:new_gift_balance')
            self.assertEqual(float(user_list[0]['balance']), float('%.2f' % order_pay_infor['balance']),u'user_list:balance')
            self.assertEqual(float(user_list[0]['real_balance']), float('%.2f' % order_pay_infor['real_balance']),u'user_list:real_balance')
            self.assertEqual(float(user_list[0]['gift_balance']), float('%.2f' % order_pay_infor['gift_balance']),u'user_list:gift_balance')
        self.assertEqual(payments_list[0]['type'], order_pay_infor['payType'], u'orders_payments:type')


