#coding=utf-8

""""
user_list:APP、小程序等访问的用户token信息
web_user_list：后台访问的token信息
其他的一些字典表的定义：主要用于匹配接口返回文本内容，数据库为ID，无法对应的情况
"""

class common_parameter():
    user_list = [
        {'username': 'zhangqing@qingyangkeji.cn', 'password': '123456', 'remark': u'测试环境', 'factoryId': u'35',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJ0eXBlIjoiand0IiwiYWxnIjoiSFMyNTYiLCJhbGdvcml0aG0iOiJoczI1NiJ9.eyJwYXlsb2FkIjoie1wiYXV0aG9yaXRpZXNcIjpbe1wiYXV0aG9yaXR5XCI6XCIxXCJ9LHtcImF1dGhvcml0eVwiOlwiMlwifSx7XCJhdXRob3JpdHlcIjpcIjNcIn0se1wiYXV0aG9yaXR5XCI6XCI0XCJ9LHtcImF1dGhvcml0eVwiOlwiNVwifSx7XCJhdXRob3JpdHlcIjpcIjZcIn0se1wiYXV0aG9yaXR5XCI6XCI3XCJ9XSxcImZhY3RvcnlSb2xlXCI6e1wiY3JlYXRlZEF0XCI6MTUzOTkzNzEzNzAwMCxcImlkXCI6MSxcIm5hbWVcIjpcIueuoeeQhuWRmFwiLFwicGVybWlzc2lvbnNJZFwiOlwiMSwyLDMsNCw1LDYsN1wifSxcImZhY3RvcnlVc2VyXCI6e1wiY2FiaW5ldElkc1wiOlwiXCIsXCJjaGFyYWN0ZXJJZFwiOjEsXCJjaXR5XCI6XCLmrabmsYnluIJcIixcImNyZWF0ZWRBdFwiOjE1NjQwMzYxMTIwMDAsXCJkZXBhcnRtZW50XCI6XCJcIixcImVtYWlsXCI6XCJ6aGFuZ3FpbmdAcWluZ3lhbmdrZWppLmNuXCIsXCJmYWN0b3J5SWRcIjpcIjM1XCIsXCJpZFwiOjExNixcIm1lcmNoYW50SWRcIjowLFwibmFtZVwiOlwiemhhbmdxaW5nXCIsXCJwaG9uZVwiOlwiMTUxMDcxMjkyODJcIixcInBvc2l0aW9uXCI6XCJcIixcInJvbGVJZFwiOlwiXCIsXCJzdGF0dXNcIjoxfX0iLCJleHAiOjE1NzQ4NDE5MTUsImlhdCI6MTU3MjI0OTkxNX0.3ZgEnf_7ECssUIxGv9Yys6ZJf7ihw9GUYRAW51q4mUU'},
        {'username': 'humeng@qingyangkeji.cn', 'password': '123456', 'remark': u'线上环境', 'factoryId': u'3',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJ0eXBlIjoiand0IiwiYWxnIjoiSFMyNTYiLCJhbGdvcml0aG0iOiJoczI1NiJ9.eyJwYXlsb2FkIjoie1wiYXV0aG9yaXRpZXNcIjpbe1wiYXV0aG9yaXR5XCI6XCIxXCJ9LHtcImF1dGhvcml0eVwiOlwiMlwifSx7XCJhdXRob3JpdHlcIjpcIjNcIn0se1wiYXV0aG9yaXR5XCI6XCI0XCJ9LHtcImF1dGhvcml0eVwiOlwiNVwifSx7XCJhdXRob3JpdHlcIjpcIjZcIn0se1wiYXV0aG9yaXR5XCI6XCI3XCJ9XSxcImZhY3RvcnlSb2xlXCI6e1wiY3JlYXRlZEF0XCI6MTUzOTkzNzEzNzAwMCxcImlkXCI6MSxcIm5hbWVcIjpcIueuoeeQhuWRmFwiLFwicGVybWlzc2lvbnNJZFwiOlwiMSwyLDMsNCw1LDYsN1wifSxcImZhY3RvcnlVc2VyXCI6e1wiY2FiaW5ldElkc1wiOlwiXCIsXCJjaGFyYWN0ZXJJZFwiOjEsXCJjaXR5XCI6XCLmrabmsYnluIJcIixcImNyZWF0ZWRBdFwiOjE1Njg4NTg0NTEwMDAsXCJkZXBhcnRtZW50XCI6XCJcIixcImVtYWlsXCI6XCJodW1lbmdAcWluZ3lhbmdrZWppLmNuXCIsXCJmYWN0b3J5SWRcIjpcIjNcIixcImlkXCI6MjcsXCJtZXJjaGFudElkXCI6MCxcIm5hbWVcIjpcImh1bWVuZ1wiLFwicGhvbmVcIjpcIjE1MTA3MTI5MjgyXCIsXCJwb3NpdGlvblwiOlwiXCIsXCJyb2xlSWRcIjpcIlwiLFwic3RhdHVzXCI6MX19IiwiZXhwIjoxNTc4NzI5Nzc1LCJpYXQiOjE1NzYxMzc3NzV9.QOQ4lhXEzJ6shCoYsw7noLg9Fpeg5kSsEbSAgjI_6-Y'},
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
    #登录
    login = {'url': '/login', 'method': 'POST', 'Authorization': 'NO','remark': u'登录'}
    # 工厂详情
    factory_detail = {'url': '/factory_hangup/api/v3/factory_detail', 'method': 'GET', 'Authorization': 'YES', 'remark': u'工厂详情'}
    #修改工厂详情
    factory_update = {'url': '/factory_hangup/api/v3/factory_update', 'method': 'POST', 'Authorization': 'YES', 'remark': u'工厂详情'}
    #工厂分拣检查
    sorting_scan = {'url':'/factory_sorting/api/v3/sorting/scan','method':'GET','Authorization':'YES','remark':u'工厂分拣检查'}
    # 获取交割单业务信息
    businessinfo = {'url': '/factory_sorting/api/v3/sorting/receipt/businessinfo', 'method': 'GET', 'Authorization': 'YES','remark': u'获取交割单业务信息'}
    #创建分拣衣物
    clothes_create = {'url':'/factory_sorting/api/v3/sorting/clothes/create','method':'POST','Authorization':'YES','remark':u'创建分拣衣物'}
    # 进行提交分拣
    sorting_submit = {'url': '/factory_sorting/api/v3/sorting/submit', 'method': 'POST', 'Authorization': 'YES','remark': u'进行提交分拣'}
    # 上挂
    racking = {'url': '/factory_hangup/api/v3/racking', 'method': 'POST', 'Authorization': 'YES', 'remark': u'上挂'}
    #检查水洗码上挂状态
    scanWasherNum = {'url': '/factory_hangup/api/v3/scanWasherNum', 'method': 'GET', 'Authorization': 'YES', 'remark': u'检查水洗码上挂状态'}
    # 获取所有可打包的列表
    pack_list = {'url': '/factory_hangup/api/v3/pack_list', 'method': 'GET', 'Authorization': 'YES','remark': u'获取所有可打包的列表'}
    # 进行打包封签
    factory_pack = {'url': '/factory_hangup/api/v3/pack', 'method': 'POST', 'Authorization': 'YES','remark': u'进行打包封签'}

class iface_param:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    # 登录
    login = ['username','password']
    # 工厂详情
    factory_detail = ['factoryId']
    # 修改工厂详情
    factory_update = ['factoryId','name','address','phone','number','perHookVolume','hooks']
    # 工厂分拣检查
    sorting_scan = ['number']
    # 获取交割单业务信息
    businessinfo = ['number']
    # 创建分拣衣物
    clothes_create = ['receiptId','factoryPic','shopServiceId','colorId','defectIds','needWash','parentClothesId','isParts','washRisk','showRisk']
    # 进行提交分拣
    sorting_submit = ['receiptId']
    # 上挂
    racking = ['washerNums']
    # 检查水洗码上挂状态
    scanWasherNum = ['washerNums']
    # 获取所有可打包的列表
    pack_list = []
    # 进行打包封签
    factory_pack = ['receiptId','hookNumber']

iface_list_base = [
    {'url':'/cabinet_client/wx/user/userInfo','method':'GET','Authorization':'YES','remark':u'用户信息'},
    # 上报微信from_id
    {'url': '/cabinet_client/wx/user/reportFormId', 'method': 'POST','Authorization':'YES','remark': u'上报微信from_id'},

]