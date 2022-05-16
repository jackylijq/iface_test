# -*- coding:utf-8 -*-
"""
ljq 2019-09-17
接口名称：社区洗下单
接口地址：/cabinet_client/api/v1/order/createOrder
method：POST

接口设计：
1、参数异常的情况：空值、空字符串、goods格式不对
2、goods_id存在、不存在，amount 非数字、为0的情况
3、单件洗、活动，amount >0 的情况
4、coupon_id存在、不存在、不可用的情况
5、多个单件洗一起下订单
6、单件洗+套餐下单（失败）
7、多个活动套餐一起下单
8、购买超过活动的限制：order_limit、goods_limit
9、已下线、已删除的单件洗、活动不能下单
"""
import unittest,json,random,copy,utils_logging,time
from test_case.cabinet_client import cabinet_basic_operate
from tools import qy_db_manager,usefulTools
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
#定义优惠券的基础信息
# coupon_infor = {'use_coupon':'YES','coupon_type_text':'','coupon_type':'','order_infor':'','pay_status':''}
# coupon_type_text：优惠券类型：通用：common、自助洗：self、干洗：delivery，不传默认：通用+干洗
# coupon_type：优惠券金额类型：0：固定金额、1：随机金额、2：折扣券，不传默认所有
#order_infor:社区洗：订单价格，根据价格进行优惠券获取，自助洗：number、service_id
#pay_status:优惠券可支付金额 与 订单金额比较，above:订单金额>优惠券金额，below订单金额<=优惠券金额

class createOrder_module(unittest.TestCase):
    #初始化准备
    def setUp(self):
        #获取单件洗的一些基础数据
        goods_online_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 1},
            {'field_name': 'cate_id', 'filed_concatenation': 'in', 'field_value': '(SELECT id FROM goods_category where type = 0)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
        ]
        self.goods_online = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods', 'created_at', goods_online_param)
        goods_offline_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'cate_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods_category where type = 0)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
        ]
        self.goods_offline = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods', 'created_at',goods_offline_param)
        goods_delete_param = [
            {'field_name': 'cate_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods_category where type = 0)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NOT NULL'},
        ]
        self.goods_delete = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods', 'created_at',goods_delete_param)
        #获取活动的数据
        goods_activity_online_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 1},
            {'field_name': 'cate_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods_category where type = 1)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
        ]
        self.goods_activity_online = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods', 'created_at',goods_activity_online_param)
        goods_activity_offline_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'cate_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods_category where type = 1)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
        ]
        self.goods_activity_offline = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods', 'created_at',goods_activity_offline_param)
        goods_activity_delete_param = [
            {'field_name': 'cate_id', 'filed_concatenation': 'in', 'field_value': '(SELECT id FROM goods_category where type = 0)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NOT NULL'},
        ]
        self.goods_activity_delete = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods', 'created_at',goods_activity_delete_param)

        #获取活动限制信息- 正常上线
        activity_online_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 1},
            {'field_name': 'activity_type', 'filed_concatenation': '=', 'field_value': 2},
            {'field_name': 'order_type', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'goods_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods where status=1 and deleted_at is NULL)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
        ]
        self.activity_online = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods_activity', 'created_at',activity_online_param)
        # 获取活动限制信息- 新用户活动
        activity_onlineNew_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 1},
            {'field_name': 'activity_type', 'filed_concatenation': '=', 'field_value': 1},
            {'field_name': 'goods_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods where status=1 and deleted_at is NULL)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
        ]
        self.activity_online_new = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods_activity','created_at', activity_onlineNew_param)
        # 获取活动限制信息- 已下线，未删除
        activity_offline_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 0},
            {'field_name': 'goods_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods where status=1 and deleted_at is NULL)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
        ]
        self.activity_offline = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods_activity','created_at', activity_offline_param)
        # 获取活动限制信息- 已删除的活动
        activity_delete_param = [
            {'field_name': 'goods_id', 'filed_concatenation': 'in', 'field_value': '(SELECT id FROM goods where status=1 and deleted_at is NULL)'},
            {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NOT NULL'},
        ]
        self.activity_delete = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods_activity','created_at', activity_delete_param)
        #调用取消接口，取消已下的订单
        # order_list_param =[
        #     {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
        #     {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 0},
        # ]
        # self.order_list_delete = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders','created_at', order_list_param)
        # for i in range(len(self.order_list_delete)):
        #     basic_operate_instances.basic_iface_request('',iface_list.cancelOrder,iface_param.cancelOrder,self.order_list_delete[i]['number'])


    #定义基础的数据请求格式
    def basic_data_request(self,*args):
        #把传入的参数全部传入接口中去
        response_infor_json = basic_operate_instances.basic_iface_request('',iface_list.createOrder,iface_param.createOrder,*args)
        return response_infor_json

    #进行下单请求，参数为空的情况
    def test_createOrder_noPrame(self):
        print u'进行下单请求，参数为空的情况'
        response_infor_json = self.basic_data_request()
        self.assertEqual(response_infor_json['status'],400,u'系统响应码为：400')
        self.assertIn(u'参数错误',response_infor_json['message'],  u'系统响message包含:参数错误')

    # 参数为空字符串的情况
    def test_createOrder_paramNull(self):
        print u'进行下单请求，参数为空字符串的情况'
        response_infor_json = self.basic_data_request('','','')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'参数错误', response_infor_json['message'], u'系统响message包含:参数错误')

    # goodsId不存在的情况
    def test_createOrder_goodsIdNotExist(self):
        print u'进行下单请求，goodsId不存在的情况'
        goods = [{"goodsId": 123123123, "amount": 1, "activityId": ""}]
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'商品不存在或者已下架', response_infor_json['message'], u'系统响message包含:商品不存在或者已下架')

    # amount格式错误
    def test_createOrder_amountFormatError(self):
        print u'进行下单请求，amount格式错误'
        random_int = random.randint(0,len(self.goods_online)-1)
        goods = [{"goodsId": self.goods_online[random_int]['id'], "amount": 'a', "activityId": ""}]
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 500, u'系统响应码为：400,目前为500')
        # self.assertIn(u'商品不存在或者已下架', response_infor_json['message'], u'系统响message包含:商品不存在或者已下架')

    # amount为0的时候，应该下单失败
    def test_createOrder_amountZero(self):
        print u'进行下单请求，amount为0的时候，应该下单失败'
        random_int = random.randint(0, len(self.goods_online)-1)
        goods = [{"goodsId": self.goods_online[random_int]['id'], "amount": '0', "activityId": ""}]
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        # self.assertIn(u'商品不存在或者已下架', response_infor_json['message'], u'系统响message包含:商品不存在或者已下架')

    # coupon_id格式错误
    def test_createOrder_couponIdFormatError(self):
        print u'进行下单请求，coupon_id格式错误情况'
        random_int = random.randint(0, len(self.goods_online)-1)
        goods = [{"goodsId": self.goods_online[random_int]['id'], "amount": '1', "activityId": ""}]
        response_infor_json = self.basic_data_request(goods, 'a', '')
        self.assertEqual(response_infor_json['status'], 500, u'系统响应码为：400,目前500')
        # self.assertIn('success', response_infor_json['message'], u'系统响message包含:success')

    # coupon_id不存在的情况
    def test_createOrder_couponIdNotExist(self):
        print u'进行下单请求，coupon_id不存在的情况'
        random_int = random.randint(0, len(self.goods_online)-1)
        goods = [{"goodsId": self.goods_online[random_int]['id'], "amount": '1', "activityId": ""}]
        response_infor_json = self.basic_data_request(goods, '1', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'活动已失效,优惠券不存在', response_infor_json['message'], u'系统响message包含:活动已失效,优惠券不存在')

    # -----------------和单件洗、活动有关的 异常数据校验-------------------------------------------------------------

    # coupon存在，但是不可用，自助洗的优惠券
    def test_createOrder_couponCanNotUse(self):
        print u'进行下单请求，coupon存在，但是不可用，自助洗的优惠券'
        #获取可用的自助洗的优惠券
        timestr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        db_param = [
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': user_infor['user_id']},
            {'field_name': 'coupon_id', 'filed_concatenation': '!=','field_value': '0'},
            {'field_name': 'end_time', 'filed_concatenation': '>', 'field_value': '\'' + timestr + '\''},
            {'field_name': 'is_used', 'filed_concatenation': '=', 'field_value': '0'},
        ]
        coupon_list = qy_db_manager_instances.get_table_data_sigle('wechat_api', 'user_coupon', 'created_time', db_param)
        random_int = random.randint(0, len(self.goods_online) - 1)
        goods = [{"goodsId": self.goods_online[random_int]['id'], "amount": '1', "activityId": ""}]
        response_infor_json = self.basic_data_request(goods, coupon_list[0]['id'], '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'活动已失效,优惠券不存在', response_infor_json['message'], u'系统响message包含:活动已失效,优惠券不存在')

    # 单件洗-已下线的情况
    def atest_acreateOrder_goodsOffline(self):
        print u'进行下单请求，单件洗-已下线的情况'
        if len(self.goods_offline) == 0:
            print u'已下线的商品为0，用例跳过'
            return 0
        random_int = random.randint(0, len(self.goods_offline))
        goods = [{"goodsId": self.goods_offline[random_int]['id'], "amount": '1', "activityId": ""}]
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'商品不存在或者已下架', response_infor_json['message'], u'系统响message包含:商品不存在或者已下架')

    # 单件洗-已删除的情况
    def atest_createOrder_goodsDelete(self):
        print u'进行下单请求，单件洗-已删除的情况'
        if len(self.goods_delete) == 0:
            print u'已下线的商品为0，用例跳过'
            return 0
        random_int = random.randint(0, len(self.goods_delete)-1)
        goods = [{"goodsId": self.goods_delete[random_int]['id'], "amount": '1', "activityId": ""}]
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'商品不存在或者已下架', response_infor_json['message'], u'系统响message包含:商品不存在或者已下架')

    # 活动-已下线的情况
    def test_createOrder_activityOffline(self):
        print u'进行下单请求，活动-已下线的情况'
        if len(self.activity_offline) == 0:
            print u'已下线的商品为0，用例跳过'
            return 0
        random_int = random.randint(0, len(self.activity_offline)-1)
        goods = [{"goodsId": '1', "amount": '1', "activityId": self.activity_delete[random_int]['id']}]
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'活动不存在', response_infor_json['message'], u'系统响message包含:活动不存在')

    # 活动-已删除的情况
    def test_createOrder_activityDelete(self):
        print u'进行下单请求，活动-已删除的情况'
        if len(self.activity_delete) == 0:
            print u'已下线的商品为0，用例跳过'
            return 0
        random_int = random.randint(0, len(self.activity_delete)-1)
        goods = [{"goodsId": '1', "amount": '1', "activityId": self.activity_delete[random_int]['id']}]
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        self.assertIn(u'活动不存在', response_infor_json['message'], u'系统响message包含:活动不存在')

    #活动、单件洗不能一起下单
    def atest_createOrder_goodsActivityAll(self):
        print u'活动、单件洗不能一起下单'
        goods = []
        random_goods = random.randint(0, len(self.goods_online)-1)
        random_activity = random.randint(0, len(self.activity_online)-1)
        goods_infor = {"goodsId": self.goods_online[random_goods]['id'], "amount": '1', "activityId": ''}
        activity_infor = {"goodsId": '1', "amount": '1', "activityId":self.activity_online[random_activity]['id']}
        goods.append(goods_infor)
        goods.append(activity_infor)
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        # self.assertIn(u'活动不存在', response_infor_json['message'], u'系统响message包含:活动不存在')

    # 多个活动不能一起下单
    def atest_createOrder_mutilActivity(self):
        print u'多个活动不能一起下单'
        goods = []
        for i in range(len(self.activity_online)):
            random_activity = random.randint(0, len(self.activity_online)-1)
            if self.activity_online[random_activity]['goods_limit'] !=0:
                continue
            activity_infor = {"goodsId": '1', "amount": '1', "activityId": self.activity_online[random_activity]['id']}
            activity_infor_bak = copy.deepcopy(activity_infor)
            goods.append(activity_infor_bak)
        response_infor_json = self.basic_data_request(goods, '', '')
        self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
        # self.assertIn(u'活动不存在', response_infor_json['message'], u'系统响message包含:活动不存在')

    # -----------------和单件洗、活动有关的 正常数据校验-------------------------------------------------------------

    #多个单件洗的商品一起下单
    def atest_createOrder_mutilGoods(self):
        print u'多个单件洗的商品一起下单，不使用优惠券'
        goods = []
        order_param = []
        order_price = 0
        timestr = time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time()))
        comment = u'进行下单测试，单件洗，时间：' + str(timestr)
        for i in range(10):
            order_param_infor = {}
            random_goods = random.randint(0, len(self.goods_online)-1)
            random_int  = random.randint(1,10)
            goods_infor = {"goodsId": self.goods_online[random_goods]['id'], "amount": random_int, "activityId":''}
            goods_infor_bak = copy.deepcopy(goods_infor)
            goods.append(goods_infor_bak)
            #下单请求的参数放入字典表
            order_param_infor['goods_id'] = self.goods_online[random_goods]['id']
            order_param_infor['amount'] = random_int
            order_param_infor['price'] = self.goods_online[random_goods]['price']
            order_param_infor['thumbnail'] = self.goods_online[random_goods]['thumbnail']
            order_param_infor['goods_name'] = self.goods_online[random_goods]['name']
            order_param_infor['goods_activity_id'] = ''
            #计算总价
            # order_price = order_price + self.goods_online[random_goods]['price'] * random_int
            order_param_infor_bak = copy.deepcopy(order_param_infor)
            order_param.append(order_param_infor_bak)
        response_infor_json = self.basic_data_request(goods, '', comment)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'下单成功', response_infor_json['message'], u'系统响message包含:下单成功')
        self.assertNotEqual(0,response_infor_json['data']['orderNumber'],u'返回的orderNumber不为0')
        #进行插入的数据比对
        self.order_goods_compare(response_infor_json,order_param,'','')

    # 多个单件洗的商品一起下单，根据传入的优惠券的信息进行判断是否需要优惠券
    def createOrder_mutilGoods(self,order_coupon_infor):
        # print u'多个单件洗的商品一起下单，不使用优惠券'
        # coupon_infor = {'use_coupon':'YES','coupon_type_text':'','coupon_type':'','order_infor':'','pay_status':''}
        goods = []
        order_param = []
        coupon_infor = {'id':'','discount':0}
        order_price = 0
        pay_money = 0
        timestr = time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time()))
        comment = u'进行下单测试，单件洗，时间：' + str(timestr)
        for i in range(5):
            order_param_infor = {}
            random_goods = random.randint(0, len(self.goods_online) - 1)
            random_int = random.randint(1, 2)
            goods_infor = {"goodsId": self.goods_online[random_goods]['id'], "amount": random_int, "activityId": ''}
            goods_infor_bak = copy.deepcopy(goods_infor)
            goods.append(goods_infor_bak)
            # 下单请求的参数放入字典表
            order_param_infor['goods_id'] = self.goods_online[random_goods]['id']
            order_param_infor['amount'] = random_int
            order_param_infor['price'] = self.goods_online[random_goods]['price']
            order_param_infor['thumbnail'] = self.goods_online[random_goods]['thumbnail']
            order_param_infor['goods_name'] = self.goods_online[random_goods]['name']
            order_param_infor['goods_activity_id'] = ''
            # 计算总价
            order_price = order_price + self.goods_online[random_goods]['price'] * random_int
            order_param_infor_bak = copy.deepcopy(order_param_infor)
            order_param.append(order_param_infor_bak)
        #先把总价赋值给支付金额，如果有优惠券，则重新计算
        pay_money = order_price
        #根据需求进行优惠券的获取
        if order_coupon_infor['use_coupon'] == 'YES':
            coupon_type_text = order_coupon_infor['coupon_type_text']
            coupon_type = order_coupon_infor['coupon_type']
            order_infor = order_price
            pay_status = order_coupon_infor['pay_status']
            coupon_use_infor = basic_operate_instances.get_coupon_accrodingOrder(coupon_type_text,coupon_type,order_infor,pay_status)
            if coupon_use_infor != 0:
                coupon_infor = coupon_use_infor
                # 计算实现需要支付的金额,根据是否为折扣券进行区分
                if coupon_infor['couponType'] == 2:
                    discountMoney = float('%.2f' % (float(order_price) * (float(10-coupon_infor['money'])/10)))
                    if discountMoney > float(coupon_infor['useCondition']):
                        coupon_infor['discount'] = float(coupon_infor['useCondition'])
                        real_money = float(order_price) - float(coupon_infor['useCondition'])
                    else:
                        coupon_infor['discount'] = discountMoney
                        real_money = float(order_price) - discountMoney
                else:
                    real_money = float(order_price) - coupon_infor['money']
                    coupon_infor['discount'] = coupon_infor['money']
                pay_money = '%.2f' % real_money if real_money > 0 else 0.0
                # pay_money = '%.2f' % pay_money
            else:
                print u'未获取到优惠券，按照优惠券为空进行数据提交'
        response_infor_json = self.basic_data_request(goods, coupon_infor['id'], comment)
        self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
        self.assertIn(u'下单成功', response_infor_json['message'], u'系统响message包含:下单成功')
        self.assertNotEqual(0, response_infor_json['data']['orderNumber'], u'返回的orderNumber不为0')
        # 进行插入的数据比对
        self.order_goods_compare(response_infor_json, order_param, coupon_infor, '',pay_money)

    # 多个单件洗的商品一起下单，不使用优惠券
    def test_createOrder_mutilGoods_noCoupon(self):
        print u'多个单件洗的商品一起下单，不使用优惠券'
        order_coupon_infor ={'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '', 'pay_status': ''}
        order_coupon_infor['use_coupon'] = 'NO'
        self.createOrder_mutilGoods(order_coupon_infor)

    # 多个单件洗的商品一起下单，不使用优惠券
    def test_createOrder_mutilGoods_deliveryCoupon(self):
        print u'多个单件洗的商品一起下单，使用优惠券：干洗券-固定金额'
        order_coupon_infor = {'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '', 'pay_status': ''}
        order_coupon_infor['coupon_type_text'] = 'delivery'
        order_coupon_infor['coupon_type'] = '0'
        order_coupon_infor['pay_status'] = 'above'
        self.createOrder_mutilGoods(order_coupon_infor)

    # 多个单件洗的商品一起下单，不使用优惠券
    def test_createOrder_mutilGoods_commonCoupon(self):
        print u'多个单件洗的商品一起下单，使用优惠券：通用券-随机金额'
        order_coupon_infor = {'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': ''}
        order_coupon_infor['coupon_type_text'] = 'common'
        order_coupon_infor['coupon_type'] = '1'
        order_coupon_infor['pay_status'] = 'above'
        self.createOrder_mutilGoods(order_coupon_infor)

    # 多个单件洗的商品一起下单，不使用优惠券
    def test_createOrder_mutilGoods_discountCoupon(self):
        print u'多个单件洗的商品一起下单，使用优惠券：干洗券-折扣券'
        order_coupon_infor = {'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': ''}
        order_coupon_infor['coupon_type_text'] = 'delivery'
        order_coupon_infor['coupon_type'] = '2'
        self.createOrder_mutilGoods(order_coupon_infor)

    # 单个活动的商品进行下单
    def atest_createOrder_activity(self):
        print u'单个活动的商品进行下单，不使用优惠券'
        goods = []
        order_param = []
        coupon_infor = {'id': ''}
        timestr = time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time()))
        comment = u'进行下单测试，活动下单，时间：' + str(timestr)
        for i in range(100):
            order_param_infor = {}
            random_int = random.randint(1, 10)
            random_activity = random.randint(0, len(self.activity_online)-1)
            activityId = self.activity_online[random_activity]['id']
            # 判断activityId 是否已经达到order_limit 上限
            order_id_list = '(' + 'SELECT id FROM orders where user_id = ' + user_infor[ 'user_id'] + ' and status!=-1' + ')'
            db_param = [
                {'field_name': 'goods_activity_id', 'filed_concatenation': '=', 'field_value': activityId},
                {'field_name': 'order_id', 'filed_concatenation': 'in', 'field_value': order_id_list},
            ]
            order_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'order_detail', 'created_at',db_param)
            if len(order_detail_list) == self.activity_online[random_activity]['order_limit']:
                continue
            activity_infor = {"goodsId": '1', "amount": '1', "activityId": self.activity_online[random_activity]['id']}
            activity_infor_bak = copy.deepcopy(activity_infor)
            goods.append(activity_infor_bak)
            #根据goods_id 获取活动商品的详情信息
            db_param = [
                {'field_name': 'id', 'filed_concatenation': '=','field_value': self.activity_online[random_activity]['goods_id']},
            ]
            order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods', 'created_at', db_param)
            # 下单请求的参数放入字典表
            order_param_infor['goods_id'] = order_list[0]['id']
            order_param_infor['amount'] = 1
            # order_param_infor['price'] = order_list[0]['price']
            order_param_infor['price'] = self.activity_online[random_activity]['activity_price']
            order_param_infor['activity_price'] = self.activity_online[random_activity]['activity_price']
            order_param_infor['thumbnail'] = order_list[0]['thumbnail']
            order_param_infor['goods_name'] = order_list[0]['name']
            order_param_infor['goods_activity_id'] = self.activity_online[random_activity]['id']
            order_param_infor_bak = copy.deepcopy(order_param_infor)
            order_param.append(order_param_infor_bak)
            response_infor_json = self.basic_data_request(goods, '', comment)
            self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
            self.assertIn(u'下单成功', response_infor_json['message'], u'系统响message包含:下单成功')
            self.assertNotEqual(0, response_infor_json['data']['orderNumber'], u'返回的orderNumber不为0')
            # 进行插入的数据比对
            self.order_goods_compare(response_infor_json, order_param, '', order_param[0]['goods_activity_id'])
            break

    # 单个活动的商品进行下单
    def createOrder_activity(self,order_coupon_infor):
        print u'单个活动的商品进行下单，不使用优惠券'
        goods = []
        order_param = []
        coupon_infor = {'id': '','discount':0}
        timestr = time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time()))
        comment = u'进行下单测试，活动下单，时间：' + str(timestr)
        for i in range(100):
            order_param_infor = {}
            random_int = random.randint(1, 10)
            random_activity = random.randint(0, len(self.activity_online) - 1)
            activityId = self.activity_online[random_activity]['id']
            # 判断activityId 是否已经达到order_limit 上限
            order_id_list = '(' + 'SELECT id FROM orders where user_id = ' + user_infor['user_id'] + ' and status!=-1' + ')'
            db_param = [
                {'field_name': 'goods_activity_id', 'filed_concatenation': '=', 'field_value': activityId},
                {'field_name': 'order_id', 'filed_concatenation': 'in', 'field_value': order_id_list},
            ]
            order_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'order_detail','created_at', db_param)
            if len(order_detail_list) == self.activity_online[random_activity]['order_limit']:
                continue
            activity_infor = {"goodsId": '1', "amount": '1',"activityId": self.activity_online[random_activity]['id']}
            activity_infor_bak = copy.deepcopy(activity_infor)
            goods.append(activity_infor_bak)
            # 根据goods_id 获取活动商品的详情信息
            db_param = [
                {'field_name': 'id', 'filed_concatenation': '=','field_value': self.activity_online[random_activity]['goods_id']},
            ]
            order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'goods', 'created_at',db_param)
            # 下单请求的参数放入字典表
            order_param_infor['goods_id'] = order_list[0]['id']
            order_param_infor['amount'] = 1
            # order_param_infor['price'] = order_list[0]['price']
            order_param_infor['price'] = self.activity_online[random_activity]['activity_price']
            order_param_infor['activity_price'] = self.activity_online[random_activity]['activity_price']
            order_param_infor['thumbnail'] = order_list[0]['thumbnail']
            order_param_infor['goods_name'] = order_list[0]['name']
            order_param_infor['goods_activity_id'] = self.activity_online[random_activity]['id']
            order_param_infor_bak = copy.deepcopy(order_param_infor)
            order_param.append(order_param_infor_bak)
            # 先把总价赋值给支付金额，如果有优惠券，则重新计算
            pay_money = self.activity_online[random_activity]['activity_price']
            # 根据需求进行优惠券的获取
            if order_coupon_infor['use_coupon'] == 'YES':
                coupon_type_text = order_coupon_infor['coupon_type_text']
                coupon_type = order_coupon_infor['coupon_type']
                order_infor = self.activity_online[random_activity]['activity_price']
                pay_status = order_coupon_infor['pay_status']
                coupon_use_infor = basic_operate_instances.get_coupon_accrodingOrder(coupon_type_text, coupon_type,order_infor, pay_status)
                if coupon_use_infor != 0:
                    coupon_infor = coupon_use_infor
                    # #计算实现需要支付的金额：
                    # real_money = float(self.activity_online[random_activity]['activity_price']) - coupon_infor['money']
                    # 计算实现需要支付的金额,根据是否为折扣券进行区分
                    if coupon_infor['couponType'] == 2:
                        discountMoney = float('%.2f' % (float(self.activity_online[random_activity]['activity_price']) * (float(10-coupon_infor['money'])/10)))
                        if discountMoney > float(coupon_infor['useCondition']):
                            coupon_infor['discount'] = float(coupon_infor['useCondition'])
                            real_money = float(self.activity_online[random_activity]['activity_price']) - float(coupon_infor['useCondition'])
                        else:
                            coupon_infor['discount'] = discountMoney
                            real_money = float(self.activity_online[random_activity]['activity_price']) - discountMoney
                    else:
                        real_money = float(self.activity_online[random_activity]['activity_price']) - coupon_infor['money']
                        coupon_infor['discount'] = coupon_infor['money']
                    pay_money = '%.2f' % real_money if real_money > 0 else 0.0
                    # pay_money = '%.2f' % pay_money
                else:
                    print u'未获取到优惠券，按照优惠券为空进行数据提交'
            #进行接口请求
            response_infor_json = self.basic_data_request(goods, coupon_infor['id'], comment)
            self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
            self.assertIn(u'下单成功', response_infor_json['message'], u'系统响message包含:下单成功')
            self.assertNotEqual(0, response_infor_json['data']['orderNumber'], u'返回的orderNumber不为0')
            # 进行插入的数据比对
            self.order_goods_compare(response_infor_json, order_param, coupon_infor, order_param[0]['goods_activity_id'],pay_money)
            break

    # 活动下单，不使用优惠券
    def test_createOrder_activity_noCoupon(self):
        print u'活动下单，不使用优惠券'
        order_coupon_infor = {'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': ''}
        order_coupon_infor['use_coupon'] = 'NO'
        self.createOrder_activity(order_coupon_infor)

    # 活动下单，通用券-固定金额
    def test_createOrder_activityDeliveryCoupon(self):
        print u'活动下单，使用优惠券：通用券-固定金额'
        order_coupon_infor = {'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': ''}
        order_coupon_infor['coupon_type_text'] = 'common'
        order_coupon_infor['coupon_type'] = '0'
        order_coupon_infor['order_infor'] = 'above'
        self.createOrder_activity(order_coupon_infor)

    # 活动下单，，使用优惠券：干洗券-随机金额
    def test_createOrder_activityCommonCoupon(self):
        print u'活动下单，使用优惠券：干洗券-随机金额'
        order_coupon_infor = {'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': ''}
        order_coupon_infor['coupon_type_text'] = 'delivery'
        order_coupon_infor['coupon_type'] = '1'
        order_coupon_infor['order_infor'] = 'above'
        self.createOrder_activity(order_coupon_infor)

    # 活动下单，不使用优惠券
    def test_createOrder_activityDiscountCoupon(self):
        print u'活动下单，使用优惠券：通用-折扣券'
        order_coupon_infor = {'use_coupon': 'YES', 'coupon_type_text': '', 'coupon_type': '', 'order_infor': '','pay_status': ''}
        order_coupon_infor['coupon_type_text'] = 'common'
        order_coupon_infor['coupon_type'] = '2'
        self.createOrder_activity(order_coupon_infor)

    # goods_limit限制，等于的时候可以下单成功
    def test_createOrder_goodsLimit(self):
        print u'活动下单，goods_limit限制，等于的时候可以下单成功'
        goods = []
        for i in range(100):
            random_activity = random.randint(0, len(self.activity_online)-1)
            #先判断是否为不限活动
            if self.activity_online[random_activity]['goods_limit'] == 0:
                continue
            activityId = self.activity_online[random_activity]['id']
            #判断activityId 是否已经达到order_limit 上限
            order_id_list = '('+'SELECT id FROM orders where user_id = '+user_infor['user_id']+' and status!=-1'+')'
            db_param = [
                {'field_name': 'goods_activity_id', 'filed_concatenation': '=', 'field_value': activityId},
                {'field_name': 'order_id', 'filed_concatenation': 'in', 'field_value': order_id_list},
            ]
            order_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'order_detail', 'created_at',db_param)
            if len(order_detail_list) == self.activity_online[random_activity]['order_limit']:
                continue
            activity_infor = {"goodsId": '1', "amount": self.activity_online[random_activity]['goods_limit'], "activityId": self.activity_online[random_activity]['id']}
            goods.append(activity_infor)
            response_infor_json = self.basic_data_request(goods, '', '')
            self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
            self.assertIn(u'下单成功', response_infor_json['message'], u'系统响message包含:下单成功')
            break

    # goods_limit限制，大于的时候下单失败
    def test_createOrder_goodsLimitAbove(self):
        print u'活动下单，goods_limit限制，大于的时候下单失败'
        goods = []
        for i in range(100):
            random_activity = random.randint(0, len(self.activity_online)-1)
            # 先判断是否为不限活动
            if self.activity_online[random_activity]['goods_limit'] == 0:
                continue
            activityId = self.activity_online[random_activity]['id']
            # 判断activityId 是否已经达到order_limit 上线
            order_id_list = '(' + 'SELECT id FROM orders where user_id = ' + user_infor['user_id'] + ' and status!=-1' + ')'
            db_param = [
                {'field_name': 'goods_activity_id', 'filed_concatenation': '=', 'field_value': activityId},
                {'field_name': 'order_id', 'filed_concatenation': 'in', 'field_value': order_id_list},
            ]
            order_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'order_detail', 'created_at', db_param)
            if len(order_detail_list) == self.activity_online[random_activity]['order_limit']:
                continue
            activity_infor = {"goodsId": '1', "amount": self.activity_online[random_activity]['goods_limit']+1,"activityId": self.activity_online[random_activity]['id']}
            goods.append(activity_infor)
            response_infor_json = self.basic_data_request(goods, '', '')
            self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
            self.assertIn(u'每单最多可下', response_infor_json['message'], u'系统响message包含:每单最多可下')
            break

    # order_limit限制，大于的时候下单失败
    def test_createOrder_orderLimit(self):
        print u'活动下单，order_limit限制，小于等于的时候可以下单成功，大于的时候下单失败'
        goods = []
        for i in range(100):
            random_activity = random.randint(0, len(self.activity_online)-1)
            # 先判断是否为不限活动
            if self.activity_online[random_activity]['goods_limit'] == 0:
                continue
            activityId = self.activity_online[random_activity]['id']
            # 判断activityId 是否已经达到order_limit 上线
            order_id_list = '(' + 'SELECT id FROM orders where user_id = ' + user_infor['user_id'] + ' and status!=-1' + ')'
            db_param = [
                {'field_name': 'goods_activity_id', 'filed_concatenation': '=', 'field_value': activityId},
                {'field_name': 'order_id', 'filed_concatenation': 'in', 'field_value': order_id_list},
            ]
            order_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'order_detail', 'created_at',db_param)
            if len(order_detail_list) == self.activity_online[random_activity]['order_limit']:
                continue
            activity_infor = {"goodsId": '1', "amount": self.activity_online[random_activity]['goods_limit'], "activityId": self.activity_online[random_activity]['id']}
            goods.append(activity_infor)
            for i in range(self.activity_online[random_activity]['order_limit']+ 1):
                response_infor_json = self.basic_data_request(goods, '', '')
                if i < self.activity_online[random_activity]['order_limit'] - len(order_detail_list):
                    self.assertEqual(response_infor_json['status'], 200, u'系统响应码为：200')
                    self.assertIn(u'下单成功', response_infor_json['message'], u'系统响message包含:下单成功')
                else:
                    self.assertEqual(response_infor_json['status'], 400, u'系统响应码为：400')
                    self.assertIn(u'每位用户最多可下', response_infor_json['message'], u'系统响message包含:每位用户最多可下')
            break


    #基础的数据比对方法
    def order_goods_compare(self,response_infor_json,order_param,coupon_infor,activity_id,pay_money):
        #根据orderNumber查询order信息
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=','field_value': response_infor_json['data']['orderNumber']},
        ]
        order_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        self.assertEqual(order_list[0]['user_id'],int(user_infor['user_id']),u'user_id')
        self.assertEqual(order_list[0]['phone'],user_infor['phone'],u'phone')
        self.assertEqual(order_list[0]['status'], 0, u'status')
        self.assertEqual(order_list[0]['pay_status'], 0, u'pay_status')
        self.assertEqual(order_list[0]['price'], response_infor_json['data']['predictPrice'], u'payPrice')
        self.assertEqual(order_list[0]['predict_price'], response_infor_json['data']['predictPrice'], u'predictPrice')
        self.assertEqual(order_list[0]['paid_price'], 0, u'paid_price')
        self.assertEqual(order_list[0]['balance_price'], 0, u'balance_price')
        self.assertEqual(order_list[0]['balance_status'], 0, u'balance_status')
        self.assertEqual(float(pay_money), float(response_infor_json['data']['payInfo']['payPrice']), u'payPrice')
        self.assertEqual(coupon_infor['discount'], response_infor_json['data']['payInfo']['discount'], u'discount')
        if coupon_infor['id'] == '':
            self.assertIsNone(order_list[0]['coupon_id'])
        else:
            self.assertEqual(order_list[0]['coupon_id'],int(coupon_infor['id']),u'coupon_id')
        #根据order_id 获取详情
        db_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=','field_value': order_list[0]['id']},
        ]
        order_detail_list = qy_db_manager_instances.get_table_data_sigle('cabinet_api', 'order_detail', 'id', db_param)
        order_detail_list.reverse()
        for i in range(len(order_param)):
            self.assertEqual(order_param[i]['goods_id'],order_detail_list[i]['goods_id'],'goods_id')
            self.assertEqual(order_param[i]['goods_name'],order_detail_list[i]['goods_name'],'goods_name')
            #活动价格和商品价格不一致会报错，屏蔽掉活动校验
            if order_param[i]['goods_activity_id'] == '':
                self.assertEqual(order_param[i]['price'],order_detail_list[i]['goods_price'],'goods_price')
            self.assertEqual(order_param[i]['amount'],order_detail_list[i]['amount'],'amount')
            self.assertEqual(order_param[i]['thumbnail'],order_detail_list[i]['goods_thumbnail'],'goods_thumbnail')
            if activity_id == '':
                self.assertIsNone(order_detail_list[i]['goods_activity_id'])
            else:
                self.assertEqual(order_detail_list[i]['goods_activity_id'], int(activity_id), u'goods_activity_id')
                self.assertEqual(order_list[i]['price'], order_param[i]['activity_price'], u'activity_price')