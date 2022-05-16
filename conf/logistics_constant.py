#coding=utf-8

""""
user_list:APP、小程序等访问的用户token信息
web_user_list：后台访问的token信息
其他的一些字典表的定义：主要用于匹配接口返回文本内容，数据库为ID，无法对应的情况
"""

class common_parameter():
    user_list = [
        {'phone': '15107129282', 'password': '123456', 'From': 'Android', 'remak': u'6',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJ0eXBlIjoiand0IiwiYWxnIjoiSFMyNTYiLCJhbGdvcml0aG0iOiJoczI1NiJ9.eyJwYXlsb2FkIjoie1wiYXV0aG9yaXRpZXNcIjpbe1wiYXV0aG9yaXR5XCI6XCJBTExcIn1dLFwiYnV0bGVySWRcIjo1MixcIm5hbWVcIjpcIuW8oOW6hjHlj7fnur9cIn0iLCJleHAiOjE1Nzg3MjY0NTgsImlhdCI6MTU3NjEzNDQ1OH0.3_LYbEfxSP1HfpFOuCezrRMLaNFnZUeG1pjnmi-L1Hs'},
        {'phone': '18207107979', 'user_id': '937553', 'From': 'Android', 'remak': u'6',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJ0eXBlIjoiand0IiwiYWxnIjoiSFMyNTYiLCJhbGdvcml0aG0iOiJoczI1NiJ9.eyJwYXlsb2FkIjoie1wiYXV0aG9yaXRpZXNcIjpbe1wiYXV0aG9yaXR5XCI6XCJBTExcIn1dLFwiYnV0bGVySWRcIjo0NTUsXCJuYW1lXCI6XCLovbvmsKfkvIHkuJrkuJPnur9cIn0iLCJleHAiOjE1Nzg3MzA4NzcsImlhdCI6MTU3NjEzODg3N30.AhWoZQRCbAryOaw31k5LYopm2tLETJnym9NrjLu0aVs'},

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
    #风险类型：
    risk_list = [u'扣/拉链易掉漆',u'填充物易结团',u'面料易掉色',u'图层易脱落',u'皮革易开裂']

class iface_list:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    #工厂签出成衣（包裹）
    factory_out_processed = {'url':'/self_logistics/butler/factory/out/processed','method':'POST','Authorization':'YES','remark':u'工厂签出成衣（包裹）'}
    # 管家端登录
    login = {'url': '/self_logistics/login', 'method': 'POST', 'Authorization': 'YES','remark': u'管家端登录'}
    #入柜成衣
    cabinet_in_processed = {'url':'/self_logistics/butler/cabinet/in/processed','method':'POST','Authorization':'YES','remark':u'入柜成衣'}
    #柜子详情
    cabinet_detail = {'url':'/self_logistics/butler/cabinet/details','method':'GET','Authorization':'YES','remark':u'柜子详情'}
    #存件绑定封签
    outFactory_rfid = {'url':'/self_logistics/api/logistics/outFactory/rfid','method':'GET','Authorization':'YES','remark':u'存件绑定封签'}


class iface_param:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    # 工厂签出成衣（包裹）:outLabel 工厂的封签订单号
    factory_out_processed = ['outLabel']
    # 管家端登录
    login = ['username','password']
    # 入柜成衣
    cabinet_in_processed = ['outLabel']
    # 柜子详情
    cabinet_detail = ['cabinetId']
    # 存件绑定封签
    outFactory_rfid = ['cabinetId','boxNumber','rfid']


iface_list_base = [
    {'url':'/cabinet_client/wx/user/userInfo','method':'GET','Authorization':'YES','remark':u'用户信息'},
    # 上报微信from_id
    {'url': '/cabinet_client/wx/user/reportFormId', 'method': 'POST','Authorization':'YES','remark': u'上报微信from_id'},

]