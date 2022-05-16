# -*- coding:utf-8 -*-
"""
ljq 2019-09-23
接口名称：分配柜子/预约柜子接口
接口地址：/cabinet_client/api/v1/cabinets/assignBox
method：GET

接口设计：
1、参数异常的情况：空值、空字符串、格式不对
2、订单错误、不存在的情况
3、非本人订单无法开柜
4、未支付的订单无法开柜
5、已取消的订单无法开柜
6、已分拣的订单无法开柜
7、已打包未存衣的订单无法开柜
8、已完成订单无法开柜
9、已支付未存衣的订单可以正常开柜
10、洗衣完成，管家已存衣的订单可以正常开柜
11、已存衣未入场分拣的订单无法正常开柜
12、订单信息与数据库进行比对

order_condition：={'status':0,'pay_status':0,'user_id':user_infor['user_id'],'goods_activity_id':'','goods_id':'','payPrice':0}
status：订单状态；pay_status：订单支付状态；user_id：用户ID，goods_activity_id：活动ID；goods_id：商品ID；
payPrice：实际支付金额；discount：优惠券支付金额

coupon_infor = {'use_coupon':'YES','coupon_type_text':'','coupon_type':'','order_infor':'','pay_status':'','payPrice':1}
# coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
# coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
# order_infor:社区洗：订单价格，根据价格进行优惠券获取，自助洗：number、service_id
# pay_status:优惠券可支付金额 与 订单金额比较，above:订单金额>优惠券金额，below订单金额<=优惠券金额

#order_status={'status': 0, 'pay_status': 1,'orders_status_process':'','balance_status':'','risk':''}订单的实际状态
"""
import unittest,json,random,copy,utils_logging,time
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

class assignBox_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        qrcode_base = 'https://cabinet-api.funxi.cn/cabinet?id=027131_'
        time_str = str(int(time.time()-60))
        self.qrcode = qrcode_base + time_str
        self.assertEqual(1,1)

    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.assignBox,iface_param.assignBox,*args)
        return response_infor_json

    #扫码开柜，参数为空的情况
    def test_assignBox_noPrame(self):
        print u'扫码开柜，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],400,u'系统响应码为：400,目前500')
        self.assertIn(u'订单有误',response_infor_json['message'],  u'系统响message包含:订单有误')

    # 参数为空字符串的情况
    def test_assignBox_paramNull(self):
        print u'扫码开柜，参数为空字符串的情况，全部为空'
        response_infor_json = self.basic_data_request('','')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # orderNumber不存在的情况
    def test_assignBox_numberNotExist(self):
        print u'扫码开柜，orderNumber不存在的情况'
        response_infor_json = self.basic_data_request('123123123',settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单不存在')

    # cabinetId  不存在
    def test_assignBox_qrcodeExpire(self):
        print u'扫码开柜，cabinetId  不存在'
        order_status = {'status': 0, 'pay_status': 1, 'orders_status_process': ''}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number, 123321123)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'柜子不存在，请检查参数', response_infor_json['message'], u'系统响message包含:柜子不存在，请检查参数')

    # order_status=delete
    def test_assignBox_deleteOrder(self):
        print u'扫码开柜，order_status=delete'
        db_param = [
            {'field_name': 'deleted_at', 'filed_concatenation': 'is not', 'field_value': 'NULL'},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        ]
        orders_delete = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at',db_param)
        if len(orders_delete) == 0:
            print u'无删除订单，删除订单查看详情跳过'
        response_infor_json = self.basic_data_request(orders_delete[0]['number'],settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    def atest_assignBox_notOwner(self):
        print u'扫码开柜，非本人订单不可获取详情'
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
    def test_assignBox_canceled(self):
        print u'扫码开柜，已取消的订单：order_status=-1,pay_status = 0'
        order_status = {'status':-1,'pay_status':0,'orders_status_process':''}
        order_number = self.get_order_accord_request('',10,10,order_status,'above')
        response_infor_json = self.basic_data_request(order_number,settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 已支付，再取消的订单：order_status=-1,pay_status = 0
    def test_a_assignBox_paidCanceled(self):
        print u'扫码开柜，已支付再取消的订单：order_status=-1,pay_status = 0'
        order_status = {'status': -1, 'pay_status': 1, 'orders_status_process': ''}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number, settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 未支付的订单：order_status=0,pay_status = 0
    def test_assignBox_noPay(self):
        print u'扫码开柜，未支付的订单：order_status=0,pay_status = 0'
        order_status = {'status': 0, 'pay_status': 0,'orders_status_process':''}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number,settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 已删除/已下线的柜子
    def test_assignBox_exceptCabinet(self):
        print u'扫码开柜，已删除/已下线的柜子'
        order_status = {'status': 0, 'pay_status': 1, 'orders_status_process': ''}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        db_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 0},
        ]
        cabinet_list = qy_db_manager_instances.get_table_data_sigle('cabinet_iot', 'cabinet', 'id', db_param)
        response_infor_json = self.basic_data_request(order_number, cabinet_list[0]['id'])
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'暂停服务，请稍后重试', response_infor_json['message'], u'系统响message包含:暂停服务，请稍后重试')

    # 已支付的订单：order_status=0,pay_status = 1
    def test_assignBox_Paid(self):
        print u'扫码开柜，已支付的订单：order_status=0,pay_status = 1'
        order_status = {'status': 0, 'pay_status': 1,'orders_status_process':''}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number,settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'预约成功', response_infor_json['message'], u'系统响message包含:开柜中')
        #进行数据比对
        self.assignBox_data_compare(order_number)
        #进行柜子释放
        basic_operate_instances.basic_iface_request('',iface_list.cancelOrder,iface_param.cancelOrder,order_number)

    # 套餐已支付的订单：order_status=0,pay_status = 1
    def test_assignBox_activityPaid(self):
        print u'扫码开柜，已支付的套餐订单：order_status=0,pay_status = 1，good_type=activity'
        order_status = {'status': 0, 'pay_status': 1,'orders_status_process':''}
        order_number = self.get_order_accord_request('activity', 10, 10, order_status, 'below')
        response_infor_json = self.basic_data_request(order_number,settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'预约成功', response_infor_json['message'], u'系统响message包含:开柜中')
        # 进行数据比对
        self.assignBox_data_compare(order_number)
        # 进行柜子释放
        basic_operate_instances.basic_iface_request('', iface_list.cancelOrder, iface_param.cancelOrder, order_number)

    # 已预约柜子的订单：order_status=1,pay_status = 1
    def test_assignBox_assignOrder(self):
        print u'已预约柜子的订单：order_status=1,pay_status = 1,ASSIGNED_BOX'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'ASSIGNED_BOX'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number, settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行柜子释放
        basic_operate_instances.basic_iface_request('', iface_list.cancelOrder, iface_param.cancelOrder, order_number)

    # 已扫码开柜的订单：order_status=1,pay_status = 1
    def test_assignBox_pickupOrder(self):
        print u'扫码开柜，已存衣的订单：order_status=1,pay_status = 1,DELIVERY_PICKUP'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'DELIVERY_PICKUP'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number, settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')
        # 进行柜子释放
        basic_operate_instances.clean_box_accordOrder(order_number)

    # 已到工厂 的订单：order_status=1,pay_status = 1
    def test_assignBox_orderArFactory(self):
        print u'扫码开柜，已到工厂 的订单：order_status=1,pay_status = 1,ARRIVED_FACTORY'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'ARRIVED_FACTORY'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number, settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 已分拣 的订单：order_status=1,pay_status = 1
    def test_aassignBox_orderSorted(self):
        print u'扫码开柜，已分拣 的订单：order_status=1,pay_status = 1,SORTED_AND_WASH'
        order_status = {'status': 1, 'pay_status': 1, 'orders_status_process': 'SORTED_AND_WASH','balance_status':'above','risk':'1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number, settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

    # 已完成 的订单：order_status=1,pay_status = 1
    def test_assignBox_orderDone(self):
        print u'扫码开柜，已完成 的订单：order_status=1,pay_status = 1,DONE'
        order_status = {'status': 2, 'pay_status': 1, 'orders_status_process': 'DONE','balance_status':'above','risk':'1'}
        order_number = self.get_order_accord_request('', 10, 10, order_status, 'above')
        response_infor_json = self.basic_data_request(order_number, settings.cabinetId)
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'订单有误', response_infor_json['message'], u'系统响message包含:订单有误')

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
    def assignBox_data_compare(self,order_number):
        #根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=','field_value': order_number},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        # 根据order信息，获取 orders_cabinet 开柜信息
        orders_status_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        orders_status_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_status_process', 'id',orders_status_param)
        #根据order信息，获取 orders_cabinet 开柜信息
        cabinet_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        orders_cabinet_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders_cabinet', 'id', cabinet_param)
        #根据order信息，获取 orders_cabinet 开柜信息
        cargo_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[0]['id']},
        ]
        cargo_list = qy_db_manager_instances.get_table_data_sigle('cabinet_iot', 'cargo', 'id',cargo_param)
        # 根据order信息，获取 orders_cabinet 开柜信息
        cabinet_code_param = [
            {'field_name': 'cabinet_id', 'filed_concatenation': '=', 'field_value': settings.cabinetId},
            {'field_name': 'box_number', 'filed_concatenation': '=', 'field_value': orders_cabinet_list[0]['user_send_box_number']},
        ]
        cabinet_code_list = qy_db_manager_instances.get_table_data_sigle('cabinet_iot', 'cabinet_code', 'id', cabinet_code_param)

        #进行数量检查
        self.assertEqual(len(orders_cabinet_list),1,u'开柜记录数=1')
        self.assertNotEqual(len(cargo_list),0,u'货物记录数=1')
        self.assertEqual(orders_status_list[0]['status'], 'ASSIGNED_BOX', 'orders_cabinet:status')
        self.assertEqual(cabinet_code_list[0]['type'], 0, 'cabinet_code:type')

