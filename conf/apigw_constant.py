#coding=utf-8

""""
user_list:APP、小程序等访问的用户token信息
web_user_list：后台访问的token信息
其他的一些字典表的定义：主要用于匹配接口返回文本内容，数据库为ID，无法对应的情况
"""

class common_parameter():
    user_list = [
        {'phone': '18207107979', 'user_id': '937553', 'From': 'Android', 'remak': u'dev',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdCI6MTU2ODE4NzA0OTYyMywib3BlbmlkIjoib3hVV2Y0dXI0QmE4MEtxSWRlUFVZaTMxZkx4VSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJleHAiOjE1NzA3NzkwNDk2MjN9.0Jv6z3cPf7oARyBmnK33pAOmjEXrNrRjkItlY0hdk_Q'},
        {'phone': '18672315356', 'user_id': '1466648', 'From': 'Android', 'remak': u'online',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdCI6MTU3NjEzNDcxMDk1MCwib3BlbmlkIjoib3hVV2Y0cTVCZXRvTlNxWC1qYzFUdGhfaVJJSSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJleHAiOjE1Nzg3MjY3MTA5NTB9.-DQbiIaSJE4vPM6y5k5DxG60ub0zVZGi2HV03UEwOIA'},
    ]

    web_user_list = [
        {'phone': '18212341234', 'user_id': '937290', 'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiJSamNYd3c0eWJZSFMiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJpYXQiOjE1Njc2NjkwNDYsImV4cCI6MTU2ODI3Mzg0NiwianRpIjoiNDBoUDZ5T3hQT25MQ1JrNW9wWnpWMSJ9.Z3dl82wknJu9DoScZVTr_viSUjih28DJCG5F2SAUdaM'},
    ]

    #设备类型
    modles = {'5':u'商用波轮','6':u'商用烘干','7':u'商用滚筒','8':u'商用洗鞋'}
    #设备ICON
    modles_icon = {'5':u'web-static/2018-09-05-bolun.png','6':u'web-static/2018-09-05-honggan.png','7':u'web-static/2018-09-05-guntong.png','8':u'web-static/2018-09-05-xixie.png'}
    #洗衣机状态
    washer_status = {'0':u'free','1':u'used','2':u'used','3':u'used'}
    #支付类型：
    payment_type = {'1':u'余额','2':u'支付宝(app)','3':u'微信支付(app)'}
    #充值支付类型
    pay_type = {u'2': u'系统充值', u'3': u'微信(APP)', u'4': u'支付宝(APP)', u'5': u'微信(小程序)'}
    #提现状态
    cash_status = {'0':u'提现(已申请)','1':u'提现(待审核)','2':u'提现(已审核)','3':u'提现(已打款)'}
    #优惠券类型（通用/干洗）：
    coupon_type = {'0':'common','1':'','2':'self'}
    coupon_type_text = {'0':u'通用', '1': '','2':u'自助洗'}
    #优惠券类型（满减/折扣）
    delivery_coupon_type = {'0':'common','1':'common','2':'discount'}
    #干洗支付类型
    cabinet_payChannel = {'balance':1,'wechat':4}
    #订单物流状态
    ORDERED = {'description': u'订单提交成功，请及时支付', 'status': u'ORDERED'}
    CANCEL_BOX = {'description': u'预约超时，请重新预约', 'status': u'CANCEL_BOX'}
    PAID = {'description': u'支付成功，可随时前往干洗存取柜存衣', 'status': u'PAID'}
    DELIVERY_PICKUP = {'description': u'存衣成功，管家正在取衣途中', 'status': u'DELIVERY_PICKUP'}
    DELIVERY_PICKUPED = {'description': u'管家已取衣，正在送往智能洗护中心', 'status': u'DELIVERY_PICKUPED'}
    ARRIVED_FACTORY = {'description': u'衣物已到达智能洗护中心，正在由洗护专家清洗养护中', 'status': u'ARRIVED_FACTORY'}
    OUT_FACTORY = {'description': u'物流配送中', 'status': u'OUT_FACTORY'}
    WAIT_USER_RECEIVE = {'description': u'管家已存衣，请您前往干洗柜取走衣物', 'status': u'WAIT_USER_RECEIVE'}
    DONE = {'description': u'已取衣，订单完成', 'status': u'DONE'}
    CANCEL = {'description': u'订单已取消', 'status': u'CANCEL'}
    DONE_LIST = {'description': u'取衣成功，感谢使用轻氧洗衣，期待再次为您服务', 'status': u'DONE'}
    BACK = {'description': u'您的衣物不在我们的清洗服务范围之内，订单已取消', 'status': u'BACK'}

    #测试图片
    test_img = 'https://qingyang-wechat-web.oss-cn-hangzhou.aliyuncs.com/wechat/1559274164485.png'

    #订单列表状态
    order_list_type = {'0':u'全部订单','1':u'未支付','2':u'需补费','3':u'已完成','4':u'待评价','5':u'反洗单','6':u'待存衣',}


class iface_list:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    #全局流量统计(时间区间)
    totalsec = {'url':'/aah/apigw/totalsec/v1/list','method':'POST','Authorization':'YES','remark':u'全局流量统计(时间区间)'}


class iface_param:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    # 订单物流状态
    totalsec = ['starttime','endtime','type','pagetype','sortfield','sorttype']
