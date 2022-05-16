# -*- coding:utf-8 -*-
"""
ljq 2019-10-11
接口名称：订单物流状态
接口地址：/cabinet_client/api/v1/order/orderExpress
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

#定义接口返回数据集
if_response_list = []
recharge_param = []

class orderExpress_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        self.assertEqual(1,1)

    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.orderExpress,iface_param.orderExpress,*args)
        return response_infor_json

    #订单物流状态，参数为空的情况
    def test_orderExpress_noPrame(self):
        print u'订单物流状态，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],500,u'系统响应码为：400，目前为500')
        self.assertIn(u'系统异常',response_infor_json['message'],  u'系统响message包含:系统异常')

    # 参数为空字符串的情况
    def test_orderExpress_paramNull(self):
        print u'订单物流状态，参数为空字符串的情况，全部为空'
        response_infor_json = self.basic_data_request('')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # orderNumber不存在的情况
    def test_orderExpress_numberNotExist(self):
        print u'订单物流状态，orderNumber不存在的情况'
        response_infor_json = self.basic_data_request('123123123')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # order_status=delete
    def test_orderExpress_deleteOrder(self):
        print u'订单物流状态，order_status=delete'
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
        # self.orderExpress_compare(response_infor_json)

    def atest_orderExpress_notOwner(self):
        print u'订单物流状态，非本人订单不可获取详情'
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
        # self.orderExpress_compare(response_infor_json)

    # 已取消的订单：order_status=-1,pay_status = 0
    def test_orderExpress_canceled(self):
        print u'订单物流状态，已取消的订单：order_status=-1,pay_status = 0'
        order_status = {'status':-1,'pay_status':0}
        order_number = self.get_order_accord_request('',10,10,order_status,'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 未支付的订单：order_status=0,pay_status = 0
    def test_orderExpress_noPay(self):
        print u'订单物流状态，未支付的订单：order_status=0,pay_status = 0'
        order_status = {'status': 0, 'pay_status': 0}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 已支付的订单：order_status=0,pay_status = 1
    def test_orderExpress_Paid(self):
        print u'订单物流状态，已支付的订单：order_status=0,pay_status = 1'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        #进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 套餐已支付的订单：order_status=0,pay_status = 1
    def test_orderExpress_activityPaid(self):
        print u'订单物流状态，已支付的套餐订单：order_status=0,pay_status = 1，good_type=activity'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('activity', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    #还差扫码之后的订单状态检查
    # 已订单物流状态的订单：order_status=1,pay_status = 1
    def test_orderExpress_pickupOrder(self):
        print u'订单物流状态，已存衣的订单：order_status=1,pay_status = 1,DELIVERY_PICKUP'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUP'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)
        # 进行柜子释放
        basic_operate_instances.clean_box_accordOrder(order_number)

    # 管家已取衣 的订单：order_status=1,pay_status = 1
    def test_orderExpress_orderPICKUPED(self):
        print u'订单物流状态，管家已取衣 的订单：order_status=1,pay_status = 1,DELIVERY_PICKUPED'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUPED'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 已到工厂 的订单：order_status=1,pay_status = 1
    def test_orderExpress_orderArFactory(self):
        print u'订单物流状态，已到工厂 的订单：order_status=1,pay_status = 1,ARRIVED_FACTORY'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'ARRIVED_FACTORY'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 已分拣 的订单：order_status=1,pay_status = 1
    def test_orderExpress_orderSorted(self):
        print u'订单物流状态，已分拣 的订单：order_status=1,pay_status = 1,SORTED_AND_WASH'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'SORTED_AND_WASH','balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 已上挂 的订单：order_status=1,pay_status = 1
    def test_orderExpress_orderUpHooks(self):
        print u'订单物流状态，已分拣 的订单：order_status=1,pay_status = 1,UP_HOOKS'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'UP_HOOKS', 'balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 已打包 的订单：order_status=1,pay_status = 1
    def test_orderExpress_orderPacked(self):
        print u'订单物流状态，已打包 的订单：order_status=1,pay_status = 1,PACKED'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'PACKED', 'balance_status': 'above','risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 已出厂，未存衣 的订单：order_status=1,pay_status = 1
    def test_aorderExpress_orderOutFactory(self):
        print u'订单物流状态，已出厂，未存衣 的订单：order_status=1,pay_status = 1,OUT_FACTORY'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'OUT_FACTORY',
                        'balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)

    # 管家已存衣 的订单：order_status=1,pay_status = 1
    def test_orderExpress_orderSaveClean(self):
        print u'订单物流状态，管家已存衣 的订单：order_status=1,pay_status = 1,WAIT_USER_RECEIVE'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'WAIT_USER_RECEIVE','balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)
        # 进行柜子释放
        for i in range(3):
            basic_operate_instances.openBoxWithQrcode(order_number,settings.cabinetId)

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_orderExpress_orderDone(self):
        print u'订单物流状态，已完成 的订单：order_status=1,pay_status = 1,DONE'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above','risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.orderExpress_compare(response_infor_json,order_number)


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
    def orderExpress_compare(self,order_detail,order_number):
        order_detail_data = order_detail['data']
        #根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=','field_value': order_number},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        # 订单进度
        orders_status_process_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        orders_status_process_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_status_process', 'id',orders_status_process_param)
        # 订单衣物表
        receipt_id = 'SELECT id FROM factory_receipt t where t.order_id = ' + str(order_list[0]['id'])
        db_param = [
            {'field_name': 'receipt_id', 'filed_concatenation': 'in', 'field_value': '(' + str(receipt_id) + ')'},
        ]
        packs_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'factory_packs', 'id',db_param)
        #计算接口返回数据的数量
        order_detail_data_num = 1 if len(packs_list) < 2 else len(packs_list)
        #进行数量检查
        self.assertEqual(len(order_detail_data),order_detail_data_num,u'接口返回的data数量')
        #定义基本的物流信息
        order_express = []
        packs_express_list = []
        orders_status_process_list.reverse()
        for i in range(len(orders_status_process_list)):
            if orders_status_process_list[i]['status'] == 'ORDERED':
                order_express.append(cabinet_client_constant.common_parameter.ORDERED)
            if orders_status_process_list[i]['status'] == 'ORDERED' and order_list[0]['pay_status'] ==1:
                order_express.append(cabinet_client_constant.common_parameter.PAID)
            if orders_status_process_list[i]['status'] == 'CANCEL':
                order_express.append(cabinet_client_constant.common_parameter.CANCEL)
            if orders_status_process_list[i]['status'] == 'DELIVERY_PICKUP':
                order_express.append(cabinet_client_constant.common_parameter.DELIVERY_PICKUP)
            if orders_status_process_list[i]['status'] == 'DELIVERY_PICKUPED':
                order_express.append(cabinet_client_constant.common_parameter.DELIVERY_PICKUPED)
            if orders_status_process_list[i]['status'] == 'ARRIVED_FACTORY':
                order_express.append(cabinet_client_constant.common_parameter.ARRIVED_FACTORY)
        #根据包裹状态定义额外的信息
        if len(packs_list) == 0:
            order_express.reverse()
            packs_express_list.append(order_express)
        for j in range(len(packs_list)):
            order_express_package = copy.deepcopy(order_express)
            if packs_list[j]['status'] == 1:
                order_express_package.append(cabinet_client_constant.common_parameter.OUT_FACTORY)
            if packs_list[j]['status'] == 2:
                order_express_package.append(cabinet_client_constant.common_parameter.OUT_FACTORY)
                order_express_package.append(cabinet_client_constant.common_parameter.WAIT_USER_RECEIVE)
            if packs_list[j]['status'] == 3:
                order_express_package.append(cabinet_client_constant.common_parameter.OUT_FACTORY)
                order_express_package.append(cabinet_client_constant.common_parameter.WAIT_USER_RECEIVE)
                order_express_package.append(cabinet_client_constant.common_parameter.DONE_LIST)
            order_express_package.reverse()
            order_express_bak = order_express_package
            packs_express_list.append(order_express_bak)
        #进行packs_list 重新排序
        packs_express_list.reverse()
        #处理接口返回的数据，去掉日期
        for i in range(len(order_detail_data)):
            order_detail_data_express_list = order_detail_data[i]
            for j in range(len(order_detail_data_express_list)):
                order_detail_data_express_list[j].pop('createdAt')
        #比对2个数组是否一致
        for i in range(len(order_detail_data)):
            print str(order_detail_data[i]).decode('unicode_escape')
            print str(packs_express_list[i]).decode('unicode_escape')
            self.assertEqual(order_detail_data[i],packs_express_list[i],u'比对数组')


