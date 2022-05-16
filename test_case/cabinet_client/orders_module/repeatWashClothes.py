# -*- coding:utf-8 -*-
"""
ljq 2019-10-12
接口名称：可申请返洗的衣物
接口地址：/cabinet_client/api/v1/order/repeatWashClothes
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

class repeatWashClothes_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        self.assertEqual(1,1)

    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.repeatWashClothes,iface_param.repeatWashClothes,*args)
        return response_infor_json

    #可申请返洗的衣物，参数为空的情况
    def test_repeatWashClothes_noPrame(self):
        print u'可申请返洗的衣物，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],500,u'系统响应码为：400，目前为500')
        self.assertIn(u'系统异常',response_infor_json['message'],  u'系统响message包含:系统异常')

    # 参数为空字符串的情况
    def test_repeatWashClothes_paramNull(self):
        print u'可申请返洗的衣物，参数为空字符串的情况，全部为空'
        response_infor_json = self.basic_data_request('')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # orderNumber不存在的情况
    def test_repeatWashClothes_numberNotExist(self):
        print u'可申请返洗的衣物，orderNumber不存在的情况'
        response_infor_json = self.basic_data_request('123123123')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # order_status=delete
    def test_repeatWashClothes_deleteOrder(self):
        print u'可申请返洗的衣物，order_status=delete'
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
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json)

    def atest_repeatWashClothes_notOwner(self):
        print u'可申请返洗的衣物，非本人订单不可获取详情'
        db_param = [
            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': '1'},
            {'field_name': 'user_id', 'filed_concatenation': '!=', 'field_value': user_infor['user_id']},
        ]
        orders_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',db_param)
        if len(orders_list) == 0:
            print u'无删除订单，删除订单查看详情跳过'
        response_infor_json = self.basic_data_request(orders_list[0]['number'])
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json)

    # 已取消的订单：order_status=-1,pay_status = 0
    def test_repeatWashClothes_canceled(self):
        print u'可申请返洗的衣物，已取消的订单：order_status=-1,pay_status = 0'
        order_status = {'status':-1,'pay_status':0}
        order_number = self.get_order_accord_request('',10,10,order_status,'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json,order_number)

    # 未支付的订单：order_status=0,pay_status = 0
    def test_repeatWashClothes_noPay(self):
        print u'可申请返洗的衣物，未支付的订单：order_status=0,pay_status = 0'
        order_status = {'status': 0, 'pay_status': 0}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 已支付的订单：order_status=0,pay_status = 1
    def test_repeatWashClothes_Paid(self):
        print u'可申请返洗的衣物，已支付的订单：order_status=0,pay_status = 1'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 套餐已支付的订单：order_status=0,pay_status = 1
    def test_repeatWashClothes_activityPaid(self):
        print u'可申请返洗的衣物，已支付的套餐订单：order_status=0,pay_status = 1，good_type=activity'
        order_status = {'status': 0, 'pay_status': 1}
        order_number = self.get_order_accord_request('activity', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    #还差扫码之后的订单状态检查
    # 已可申请返洗的衣物的订单：order_status=1,pay_status = 1
    def atest_repeatWashClothes_pickupOrder(self):
        print u'可申请返洗的衣物，已存衣的订单：order_status=1,pay_status = 1,DELIVERY_PICKUP'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUP'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.repeatWashClothes_compare(response_infor_json,order_number)
        # 进行柜子释放
        basic_operate_instances.clean_box_accordOrder(order_number)

    # 管家已取衣 的订单：order_status=1,pay_status = 1
    def atest_repeatWashClothes_orderPICKUPED(self):
        print u'可申请返洗的衣物，管家已取衣 的订单：order_status=1,pay_status = 1,DELIVERY_PICKUPED'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUPED'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json,order_number)

    # 已到工厂 的订单：order_status=1,pay_status = 1
    def test_repeatWashClothes_orderArFactory(self):
        print u'可申请返洗的衣物，已到工厂 的订单：order_status=1,pay_status = 1,ARRIVED_FACTORY'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'ARRIVED_FACTORY'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json,order_number)

    # 已分拣 的订单：order_status=1,pay_status = 1
    def test_repeatWashClothes_orderSorted(self):
        print u'可申请返洗的衣物，已分拣 的订单：order_status=1,pay_status = 1,SORTED_AND_WASH'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'SORTED_AND_WASH','balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json,order_number)

    # 已上挂 的订单：order_status=1,pay_status = 1
    def test_repeatWashClothes_orderUpHooks(self):
        print u'可申请返洗的衣物，已分拣 的订单：order_status=1,pay_status = 1,UP_HOOKS'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'UP_HOOKS', 'balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json,order_number)

    # 已打包 的订单：order_status=1,pay_status = 1
    def test_repeatWashClothes_orderPacked(self):
        print u'可申请返洗的衣物，已打包 的订单：order_status=1,pay_status = 1,PACKED'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'PACKED', 'balance_status': 'above','risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json,order_number)

    # 已出厂，未存衣 的订单：order_status=1,pay_status = 1
    def test_repeatWashClothes_orderOutFactory(self):
        print u'可申请返洗的衣物，已出厂，未存衣 的订单：order_status=1,pay_status = 1,OUT_FACTORY'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'OUT_FACTORY',
                        'balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行数据比对
        # self.repeatWashClothes_compare(response_infor_json,order_number)

    # 管家已存衣 的订单：order_status=1,pay_status = 1
    def atest_repeatWashClothes_orderSaveClean(self):
        print u'可申请返洗的衣物，管家已存衣 的订单：order_status=1,pay_status = 1,WAIT_USER_RECEIVE'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'WAIT_USER_RECEIVE','balance_status': 'above', 'risk': '1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.repeatWashClothes_compare(response_infor_json,order_number)
        # 进行柜子释放
        for i in range(3):
            basic_operate_instances.openBoxWithQrcode(order_number,settings.cabinetId)

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_arepeatWashClothes_orderDone(self):
        print u'可申请返洗的衣物，已完成 的订单：order_status=1,pay_status = 1,DONE'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE', 'balance_status': 'above','risk': ''}
        risk_repeat_status = {'risk_confirm_status': '', 'repeat_status': '0'}
        order_clothe_list = self.get_riskRepeat_order('', 10, 10, order_status, 'above',risk_repeat_status)
        order_random = random.randint(0, len(order_clothe_list) - 1)
        response_infor_json = self.basic_data_request(order_clothe_list[order_random]['order_number'])
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'success', response_infor_json['message'], u'系统响message包含:success')
        # 进行数据比对
        self.repeatWashClothes_compare(response_infor_json,order_clothe_list)

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
                return order_clother_list
        return order_clother_list

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
    def repeatWashClothes_compare(self,if_response,order_clothe_list):
        if_response_data = if_response['data']
        #检查数量是否相等
        self.assertEqual(len(if_response_data),len(order_clothe_list),u'可反洗的衣物数量是否准确')
        order_clothe_list.reverse()
        #检查基础数据
        for i in range(len(if_response_data)):
            self.assertEqual(if_response_data[i]['price'],float(order_clothe_list[i]['price']),u'price 比对')
            self.assertEqual(if_response_data[i]['clothesId'],order_clothe_list[i]['id'],u'clothesId 比对')
            self.assertEqual(if_response_data[i]['name'],order_clothe_list[i]['name'],u'name 比对')
            self.assertEqual(if_response_data[i]['category'],order_clothe_list[i]['first'],u'category 比对')
