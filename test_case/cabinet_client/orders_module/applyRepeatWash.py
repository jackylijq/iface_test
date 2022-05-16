# -*- coding:utf-8 -*-
"""
ljq 2019-10-12
接口名称：提交返洗申请
接口地址：/cabinet_client/api/v1/order/applyRepeatWash
method：POST

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
import unittest,json,random,copy,utils_logging,time,datetime
from test_case.cabinet_client import cabinet_basic_operate
from tools import qy_db_manager,usefulTools,switch
from conf import settings,cabinet_client_constant
from time import sleep

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

class applyRepeatWash_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        self.assertEqual(1,1)

    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.applyRepeatWash,iface_param.applyRepeatWash,*args)
        return response_infor_json

    #提交返洗申请，参数为空的情况
    def test_applyRepeatWash_noPrame(self):
        print u'提交返洗申请，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],400,u'系统响应码为：400')
        self.assertIn(u'订单有误',response_infor_json['message'],  u'系统响message包含:订单有误')

    # 参数为空字符串的情况
    def test_applyRepeatWash_paramNull(self):
        print u'提交返洗申请，参数为空字符串的情况，全部为空'
        response_infor_json = self.basic_data_request('','')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # orderNumber不存在的情况
    def test_applyRepeatWash_numberNotExist(self):
        print u'提交返洗申请，orderNumber不存在的情况'
        repeat_clothe = [{"comment": "", "pic": cabinet_client_constant.common_parameter.test_img, "id": 4448}]
        response_infor_json = self.basic_data_request(repeat_clothe,'123123123')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 已支付的订单：order_status=0,pay_status = 1
    def test_applyRepeatWash_Paid(self):
        print u'提交返洗申请，已支付的订单：order_status=0,pay_status = 1'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        repeat_clothe = [{"comment": "", "pic": cabinet_client_constant.common_parameter.test_img, "id": 4448}]
        response_infor_json = self.basic_data_request(repeat_clothe,order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 套餐已支付的订单：order_status=0,pay_status = 1
    def test_applyRepeatWash_activityPaid(self):
        print u'提交返洗申请，已支付的套餐订单：order_status=0,pay_status = 1，good_type=activity'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('activity', 10, 10, order_status, 'above')
        repeat_clothe = [{"comment": "", "pic": cabinet_client_constant.common_parameter.test_img, "id": 4448}]
        response_infor_json = self.basic_data_request(repeat_clothe, order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    #还差扫码之后的订单状态检查

    # 已分拣 的订单：order_status=1,pay_status = 1
    def test_applyRepeatWash_orderSorted(self):
        print u'提交返洗申请，已分拣 的订单：order_status=1,pay_status = 1,SORTED_AND_WASH'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'SORTED_AND_WASH','balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        repeat_clothe = [{"comment": "", "pic": cabinet_client_constant.common_parameter.test_img, "id": 4448}]
        response_infor_json = self.basic_data_request(repeat_clothe, order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行数据比对
        # self.applyRepeatWash_compare(response_infor_json,order_number)

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_applyRepeat_clothesIdErr(self):
        print u'提交返洗申请，订单与需要反洗的衣物ID不一致'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above', 'risk': ''}
        #获取订单信息
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        repeat_clothe = [{"comment": "", "pic": cabinet_client_constant.common_parameter.test_img, "id": 4448}]
        #进行接口请求
        response_infor_json = self.basic_data_request(repeat_clothe,order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单返洗衣物不存在', response_infor_json['message'], u'系统响message包含:订单返洗衣物不存在')

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_applyRepeat_normal(self):
        print u'提交返洗申请，已完成 的订单：order_status=1,pay_status = 1,DONE，正常进行反洗单提交'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above','risk': ''}
        risk_repeat_status = {'risk_confirm_status': '', 'repeat_status': '0'}
        #获取反洗单信息
        repeat_wash_infor = self.get_riskRepeat_order('', 10, 10, order_status, 'above',risk_repeat_status)
        response_infor_json = self.basic_data_request(repeat_wash_infor['clothes'],repeat_wash_infor['orderNumber'])
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'申请返洗成功', response_infor_json['message'], u'系统响message包含:申请返洗成功')
        # 进行数据比对
        repeat_order_list = self.applyRepeatWash_compare(repeat_wash_infor)
        #进行柜子清理操作,走完整个反洗流程
        target_order_status = {'status': '2', 'pay_status': '1', 'orders_status_process': 'DONE'}
        basic_operate_instances.order_status_deal(repeat_order_list[0]['number'],target_order_status,order_status)

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_applyRepeat_repeat(self):
        print u'提交返洗申请，已提交反洗申请，无法重复提交'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above','risk': ''}
        risk_repeat_status = {'risk_confirm_status': '', 'repeat_status': '1'}
        # 获取反洗单信息
        repeat_wash_infor = self.get_riskRepeat_order('', 10, 10, order_status, 'above', risk_repeat_status)
        response_infor_json = self.basic_data_request(repeat_wash_infor['clothes'],repeat_wash_infor['orderNumber'])
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单返洗衣物不存在', response_infor_json['message'], u'系统响message包含:订单返洗衣物不存在')

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_applyRepeat_repeatDone(self):
        print u'提交返洗申请，反洗单完成之后无法再次提交反洗'
        clothes = []
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above','risk': ''}
        risk_repeat_status = {'risk_confirm_status': '', 'repeat_status': '1'}
        db_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 2},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
            {'field_name': 'repeat_wash_status', 'filed_concatenation': '=', 'field_value': 1},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
        if len(order_list) == 0:
            print u'无已反洗完成的订单，此用例跳过'
            return 0
        #根据订单号获取可反洗的衣物信息
        receipt_id = 'SELECT id FROM factory_receipt t where t.order_id = ' + str(order_list[0]['id'])
        db_param = [
            {'field_name': 'receipt_id', 'filed_concatenation': 'in', 'field_value': '(' + str(receipt_id) + ')'},
        ]
        order_clothes_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_order_clothes', 'id', db_param)
        repeat_clothe_infor = {}
        repeat_clothe_infor['id'] = order_clothes_list[0]['id']
        repeat_clothe_infor['pic'] = cabinet_client_constant.common_parameter.test_img
        repeat_clothe_infor['comment'] = u'进行反洗操作_已反洗完成的'
        clothes.append(repeat_clothe_infor)

        response_infor_json = self.basic_data_request(clothes,order_list[0]['number'])
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'该订单为返洗单，不允许再次申请返洗', response_infor_json['message'], u'系统响message包含:该订单为返洗单，不允许再次申请返洗')

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_aapplyRepeat_7dayAgoOrder(self):
        print u'提交返洗申请，7日前的订单 等待审核'
        clothes = []
        time7dayAgo = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        db_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 2},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
            {'field_name': 'repeat_wash_status', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'updated_at', 'filed_concatenation': '<', 'field_value': '\'' + time7dayAgo + '\''},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
        if len(order_list) == 0:
            print u'未找到7日前的订单，此用例跳过'
            return 0
        # 调用反洗衣物查询，获取可用的反洗衣物信息
        repeatWashClothes = 0
        order_number = ''
        for i in range(len(order_list)):
            repeatWashClothes = basic_operate_instances.basic_iface_request('', iface_list.repeatWashClothes,iface_param.repeatWashClothes,order_list[i]['number'])
            if repeatWashClothes['message'] == 'success' and len(repeatWashClothes['data']) > 0:
                order_number = order_list[i]['number']
                break
        # 根据订单号获取可反洗的衣物信息
        if repeatWashClothes != 0 and len(repeatWashClothes['data']) > 0:
            repeat_clothe_infor = {}
            repeat_clothe_infor['id'] = repeatWashClothes['data'][0]['clothesId']
            repeat_clothe_infor['pic'] = cabinet_client_constant.common_parameter.test_img
            repeat_clothe_infor['comment'] = u'进行反洗操作_已反洗完成的'
            clothes.append(repeat_clothe_infor)
        else:
            print u'未找到7日前的订单，此用例跳过'
            return 0
        response_infor_json = self.basic_data_request(clothes, order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'提交成功，请等待客服审核', response_infor_json['message'], u'系统响message包含:提交成功，请等待客服审核')

    # 检查反洗完成的时候用户不用重新支付
    def test_applyRepeat_result(self):
        print u'提交返洗申请，检查反洗完成的时候用户不用重新支付'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above','risk': ''}
        risk_repeat_status = {'risk_confirm_status': '', 'repeat_status': '0'}
        # 获取反洗单信息
        repeat_wash_infor = self.get_riskRepeat_order('', 10, 10, order_status, 'above', risk_repeat_status)
        response_infor_json = self.basic_data_request(repeat_wash_infor['clothes'],repeat_wash_infor['orderNumber'])
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'申请返洗成功', response_infor_json['message'], u'系统响message包含:申请返洗成功')
        # 进行数据比对
        repeat_order_list = self.applyRepeatWash_compare(repeat_wash_infor)
        # 进行柜子清理操作,走完整个反洗流程
        target_order_status = {'status': '2', 'pay_status': '1', 'orders_status_process': 'DONE'}
        basic_operate_instances.order_status_deal(repeat_order_list[0]['number'], target_order_status,order_status)
        #检查反洗完成之后的状态
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=', 'field_value': repeat_order_list[0]['number']},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        self.assertEqual(order_list[0]['status'],2,u'反洗订单状态')
        self.assertEqual(order_list[0]['paid_price'],0,u'反洗支付的金额')

    # 反洗单取消之后，可以重新提交反洗
    def test_applyRepeat_cancelReSubmit(self):
        print u'提交返洗申请，反洗单取消之后，可以重新提交反洗'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above','risk': ''}
        risk_repeat_status = {'risk_confirm_status': '', 'repeat_status': '0'}
        repeat_wash_infor = self.get_riskRepeat_order('', 10, 10, order_status, 'above', risk_repeat_status)
        response_infor_json = self.basic_data_request(repeat_wash_infor['clothes'],repeat_wash_infor['orderNumber'])
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'申请返洗成功', response_infor_json['message'], u'系统响message包含:申请返洗成功')
        # 进行数据比对
        repeat_order_list = self.applyRepeatWash_compare(repeat_wash_infor)
        # 进行反洗单取消操作
        basic_operate_instances.basic_iface_request('',iface_list.cancelOrder,iface_param.cancelOrder,repeat_order_list[0]['number'])
        #重新提交反洗操作
        response_infor_json = self.basic_data_request(repeat_wash_infor['clothes'], repeat_wash_infor['orderNumber'])
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'申请返洗成功', response_infor_json['message'], u'系统响message包含:申请返洗成功')
        # 进行数据比对
        repeat_order_list = self.applyRepeatWash_compare(repeat_wash_infor)
        #进行取消操作
        basic_operate_instances.basic_iface_request('', iface_list.cancelOrder, iface_param.cancelOrder,repeat_order_list[0]['number'])

    # 根据需要获取可以进行风险确认的订单
    def get_riskRepeat_order(self, good_type, payPrice, coupon_money, order_status, pay_status, risk_repeat_status):
        order_clother_list = []
        order_condition = {'status': 0, 'pay_status': 0, 'user_id': user_infor['user_id'], 'payPrice': 10}
        order_condition['payPrice'] = payPrice
        order_condition['coupon_money'] = coupon_money
        order_condition['status'] = order_status['status']
        order_condition['pay_status'] = order_status['pay_status']
        for i in range(2):
            # 获取可进行风险确认的衣物，订单信息
            order_clother_list = qy_db_manager_instances.get_risk_repeat_order(order_condition, order_status,risk_repeat_status)
            # 定义需要创建的订单类型,真实支付金额>0,优惠券支付金额>0
            order_coupon_infor = {'coupon_type_text': '', 'coupon_type': '', 'order_infor': '', 'pay_status': '','coupon_money': 10}
            order_coupon_infor['pay_status'] = pay_status
            if len(order_clother_list) == 0:
                basic_operate_instances.make_order_according_need(good_type, order_coupon_infor, order_status)
            else:
                break
        repeat_wash_infor = {}
        repeat_clothe = []
        random.shuffle(order_clother_list)
        cloths_num = len(order_clother_list)/2 if len(order_clother_list) > 2 else len(order_clother_list)
        for i in range(cloths_num):
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            repeat_clothe_infor = {}
            repeat_clothe_infor['id'] = order_clother_list[i]['id']
            repeat_clothe_infor['pic'] = cabinet_client_constant.common_parameter.test_img
            repeat_clothe_infor['comment'] = u'进行反洗操作_'+ str(time_str)
            repeat_clothe_infor_bak = copy.deepcopy(repeat_clothe_infor)
            repeat_clothe.append(repeat_clothe_infor_bak)
        repeat_wash_infor['clothes'] = repeat_clothe
        repeat_wash_infor['orderNumber'] = order_clother_list[0]['order_number']
        return repeat_wash_infor

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
    def applyRepeatWash_compare(self,repeat_wash_infor):
        # 根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=', 'field_value': repeat_wash_infor['orderNumber']},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        #查询反洗订单ID,等待5s进行查询
        sleep(5)
        db_param = [
            {'field_name': 'parent_order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        repeat_wash = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'apply_repeat_wash', 'id', db_param)
        # 查询反洗订单ID
        db_param = [
            {'field_name': 'apply_id', 'filed_concatenation': '=', 'field_value': repeat_wash[0]['id']},
        ]
        repeat_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'apply_repeat_wash_detail','id', db_param)
        print repeat_wash[0]
        db_param = [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': repeat_wash[0]['order_id']},
        ]
        repeat_order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
        # 订单柜子相关
        orders_cabinet_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': repeat_order_list[0]['id']},
        ]
        orders_cabinet_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_cabinet', 'id',orders_cabinet_param)
        #获取衣物列表信息
        receipt_id = 'SELECT id FROM factory_receipt where order_id =' + str(repeat_order_list[0]['id'])
        db_param = [
            {'field_name': 'receipt_id', 'filed_concatenation': 'in', 'field_value': '(' + receipt_id + ')'},
        ]
        clothes_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_order_clothes', 'id', db_param)

        #检查数量是否相等
        self.assertEqual(len(repeat_wash_infor['clothes']),len(clothes_list),u'反洗的衣物数量与提交的一致')
        self.assertEqual(len(repeat_detail_list),len(clothes_list),u'反洗的衣物数量与提交的一致')

        #反洗订单检查：
        self.assertEqual(repeat_order_list[0]['user_id'],int(user_infor['user_id']),u'user_id')
        self.assertEqual(repeat_order_list[0]['pay_status'],1,u'pay_status')
        self.assertEqual(repeat_order_list[0]['price'],0,u'price')
        self.assertEqual(repeat_order_list[0]['predict_price'],0,u'predict_price')
        self.assertEqual(repeat_order_list[0]['paid_price'],0,u'paid_price')
        self.assertEqual(repeat_order_list[0]['is_repeat_wash'],1,u'is_repeat_wash')
        self.assertEqual(repeat_order_list[0]['repeat_wash_status'],1,u'repeat_wash_status')
        self.assertEqual(repeat_order_list[0]['parent_id'],order_list[0]['id'],u'parent_id')

        #预约的柜子检查
        if repeat_order_list[0]['status'] == 'ASSIGNED_BOX':
            self.assertEqual(len(orders_cabinet_list),1)
            self.assertEqual(repeat_order_list[0]['status'], 1, u'status')
            self.assertEqual(orders_cabinet_list[0]['status'],'ASSIGNED_BOX',u'status')
            self.assertEqual(orders_cabinet_list[0]['user_send_cabinet_id'],settings.cabinetId,u'cabinetId')
            cabinet_code_param = [
                {'field_name': 'cabinet_id', 'filed_concatenation': '=', 'field_value': settings.cabinetId},
                {'field_name': 'box_number', 'filed_concatenation': '=','field_value': orders_cabinet_list[0]['user_send_box_number']},
            ]
            cabinet_code_list = qy_db_manager_instances.get_table_data_sigle('cabinet_iot', 'cabinet_code', 'id',cabinet_code_param)
            self.assertEqual(len(cabinet_code_list), 1, u'cabinet_code 记录数=1')
            self.assertEqual(cabinet_code_list[0]['type'], 0,u'type 为预约存衣的code')

        #衣物表数据检查
        order_clothe_list = repeat_wash_infor['clothes']
        order_clothe_list.reverse()
        for i in range(len(repeat_detail_list)):
            self.assertEqual(repeat_detail_list[i]['imgs'],order_clothe_list[i]['pic'])
            self.assertEqual(repeat_detail_list[i]['parent_clothes_id'],order_clothe_list[i]['id'])
            self.assertEqual(repeat_detail_list[i]['comment'],order_clothe_list[i]['comment'])
            parent_clothes_param= [
            {'field_name': 'id', 'filed_concatenation': '=', 'field_value': repeat_detail_list[i]['parent_clothes_id']},
            ]
            parent_clothes_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_order_clothes', 'id', parent_clothes_param)
            clothes_param = [
                {'field_name': 'id', 'filed_concatenation': '=','field_value': repeat_detail_list[i]['clothes_id']},
            ]
            clothes_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_order_clothes','id', clothes_param)
            self.assertEqual(parent_clothes_list[0]['service_id'],clothes_list[0]['service_id'],u'service_id')
            self.assertEqual(parent_clothes_list[0]['first'],clothes_list[0]['first'],u'first')
            self.assertEqual(parent_clothes_list[0]['name'],clothes_list[0]['name'],u'name')
            self.assertEqual(0,clothes_list[0]['price'],u'price')
            self.assertEqual(parent_clothes_list[0]['defect_id'],clothes_list[0]['defect_id'],u'defect_id')
            self.assertEqual(parent_clothes_list[0]['defect'],clothes_list[0]['defect'],u'defect')
            self.assertEqual(parent_clothes_list[0]['color_id'],clothes_list[0]['color_id'],u'color_id')
            self.assertEqual(parent_clothes_list[0]['color'],clothes_list[0]['color'],u'color')
            self.assertEqual(parent_clothes_list[0]['id'],clothes_list[0]['parent_clothes_id'],u'parent_clothes_id')
            # self.assertEqual(parent_clothes_list[0]['is_parts'],clothes_list[0]['id'],u'目前都为0')
            self.assertEqual(order_clothe_list[i]['comment'],order_clothe_list[i]['comment'],u'user_back_comment')
            self.assertEqual(parent_clothes_list[0]['applied_repeat_wash'],1,u'applied_repeat_wash')
            self.assertEqual(clothes_list[0]['applied_repeat_wash'],1,u'applied_repeat_wash')
            self.assertEqual(clothes_list[0]['repeat_wash_status'],1,u'applied_repeat_wash')
            self.assertEqual(clothes_list[0]['status'],'CREATED',u'status')
        #返回反洗订单信息，用于后续处理
        return repeat_order_list


