#coding=utf-8

""""
user_list:APP、小程序等访问的用户token信息
web_user_list：后台访问的token信息
其他的一些字典表的定义：主要用于匹配接口返回文本内容，数据库为ID，无法对应的情况
"""

class common_parameter():
    user_list = [
        {'phone': '18212341234', 'user_id': '937290','From':'Android','remak':u'0',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcGVuaWQiOiI3Yjk2OGRmZWFkNTkxMTI4MDU5MWJiZjVjYTZkMTNlYyIsInBob25lIjoiMTgyMTIzNDEyMzQiLCJ1aWQiOiJyOUlQaUNqQUxIRVIiLCJ1c2VyX2lkIjo5MzcyOTAsIndlY2hhdHNfaWQiOjU4MTg4MiwidHlwIjoiYWNjZXNzX3Rva2VuIiwiaWF0IjoxNTc1Njg1MTUzLCJleHAiOjE1NzgyNzcxNTMsImp0aSI6IjFaYlYyU0NpWldUM1BzaHZNMFVzU1EifQ.aTTB6_HquIb69CSuwC4OsnlZ81GjAnI_05YIb-JhNsw'},
        {'phone': '18616138462', 'user_id': '937553','From':'wechat_micro','remak':u'测试微信小程序的token--1',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcGVuaWQiOiJvbFV6NzBOZXV5S2lHWExtZTlaR3g1Zl9kNFhFIiwicGhvbmUiOiIxODYxNjEzODQ2MiIsInVpZCI6ImFYbHlVenR1STF0UiIsInVzZXJfaWQiOjkzNzU1Mywid2VjaGF0c19pZCI6MTIzNDg1NywidHlwIjoiYWNjZXNzX3Rva2VuIiwiaWF0IjoxNTc1OTY3NDE5LCJleHAiOjE1Nzg1NTk0MTksImp0aSI6IjNEcm03NEU3Nzk1YkZvZmZLQmZsV2oifQ.f0mCwW4cCg5XsEXWJTG4jG8jWnKmBv1W4uLECz7SPbQ'},
        {'phone': '18222342234', 'user_id': '986427', 'From': 'Android','remak':u'测试新用户--2',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcGVuaWQiOiJjNmFjMDY2NmVlNDgxYTY0NmFmNDlkYjM0MWUzZDBiNyIsInBob25lIjoiMTgyMjIzNDIyMzQiLCJ1aWQiOiIxRDNjRjhuMEdTWDBzIiwidXNlcl9pZCI6OTg2NDI3LCJ3ZWNoYXRzX2lkIjoxMjM0ODI1LCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJpYXQiOjE1NzU2ODUyMTksImV4cCI6MTU3ODI3NzIxOSwianRpIjoiNnNPUjJHZE92SFhqOWozb0FZa2cxUSJ9.VJ8f8LcAfaL5De6nLTOiHeHwWEa3OJjFNMQgRnKaMhE'},
        {'phone': '......', 'user_id': '986429', 'From': 'Android','remak':u'用来进行换绑的数据--3',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcGVuaWQiOiJhMWRmZDE4MWEwYTRhNmNkYzRjOGZhNjVlZDIxZGE0ZCIsInBob25lIjoiMTM2Mzc4ODU1ODkiLCJ1aWQiOiJFZ3RrVk1JVGgxRmsiLCJ1c2VyX2lkIjo5ODY0MjksIndlY2hhdHNfaWQiOjEyMzQ4MjcsInR5cCI6ImFjY2Vzc190b2tlbiIsImlhdCI6MTU3NTY4NTI1OSwiZXhwIjoxNTc4Mjc3MjU5LCJqdGkiOiI3VTRQUHRITE00OFpSN3ZQOHVHdG40In0.t1y6weMPAVd4qyJHIL59orOcMrgaxtzHOpJVFywyQX0'},
        {'phone': '.....', 'user_id': '986436', 'From': 'Android', 'remak': u'用来进行换绑的数据--4',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcGVuaWQiOiIzZWYzN2Y0ZjE0YzNjMTM0OWRjNzYyZGE5OTc0ZTQ4ZSIsInBob25lIjoiMTM1MjM0NTIzNDUiLCJ1aWQiOiIxMU03ekk1WEg5Y1BNIiwidXNlcl9pZCI6OTg2NDM2LCJ3ZWNoYXRzX2lkIjoxMjM0ODMxLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJpYXQiOjE1NzU2ODUzMDMsImV4cCI6MTU3ODI3NzMwMywianRpIjoiNHVEWUlxSlVaT1Rsc3VGS1Z2aFF4ZSJ9.Att-DrRdd1y89kMi_HqLX_oAkqBubkXjIDqtIWNA9WQ'},
        {'phone': '13811681063', 'user_id': '9', 'From': 'Android', 'remak': u'用来测试老用户--5',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcGVuaWQiOiIxZWYxNDIyZDQzZWZlZWRkMjdiYmE5ZGFkNjczYjZmZiIsInBob25lIjoiMTM4MTE2ODEwNjMiLCJ1aWQiOiJ5bTZZZjgwQXdkdWgiLCJ1c2VyX2lkIjo5LCJ3ZWNoYXRzX2lkIjoxMjM0ODkyLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJpYXQiOjE1NzU2ODUzNDAsImV4cCI6MTU3ODI3NzM0MCwianRpIjoiNTBXVjFUcklFanNvaDBPTW43MXRicSJ9.xSxcGoJJGzKX7MlHIaJpJNy9H4eFTkY8VtPGk9HCdAg'},
        {'phone': '18616138462', 'user_id': '937553', 'From': 'Android', 'remak': u'6',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcGVuaWQiOiI2M2Q4YTA2MjcyZDJhZDZkYmQyMjliYzA3MDQyMzZiNCIsInBob25lIjoiMTg2MTYxMzg0NjIiLCJ1aWQiOiJhWGx5VXp0dUkxdFIiLCJ1c2VyX2lkIjo5Mzc1NTMsIndlY2hhdHNfaWQiOjU4MTk2OCwidHlwIjoiYWNjZXNzX3Rva2VuIiwiaWF0IjoxNTc1Njg1Mzc5LCJleHAiOjE1NzgyNzczNzksImp0aSI6IjJITzBsMkNzb2ZrSjJqeTBIbmZnWHIifQ.l2bh2sNRTJ9-W0KIY-xnTAxLmzncUrdNc4TDBABWPRE'},

    ]

    web_user_list = [
        {'phone': '18212341234', 'user_id': '937290', 'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiJSamNYd3c0eWJZSFMiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJpYXQiOjE1NzIzNTAyNzIsImV4cCI6MTU3Mjk1NTA3MiwianRpIjoiNFYzWU9UNmtQOVdXcVRCSWlCRWNINCJ9.YmSHzCQyjIiFdQy36WcFJtDnh-dnD7Kaiqg2J-Tgnmk'},
        {'phone': 'humeng@', 'user_id': '937290',
         'access_token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiJxcXFxIiwic3lzdGVtSWQiOjAsImlzUmVmcmVzaCI6ZmFsc2UsImxldmVsIjotMSwiaWQiOjE2LCJleHBpcmVBdCI6MTU3OTk0Njk2MCwiY3JlYXRlQXQiOjE1NzQ3NjI5NjB9.w9vR_NpokYz1u9HfjM1Dmc_8GzEEJQDcyLxFVsXKBLk'},
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
    pay_type = {u'2': u'系统充值', u'3': u'微信(APP)充值', u'4': u'支付宝(APP)充值', u'5': u'充值赠送'}
    #提现状态
    cash_status = {'0':u'提现(已申请)','1':u'提现(待审核)','2':u'提现(已审核)','3':u'提现(已打款)'}
    #优惠券类型（通用/干洗）：
    coupon_type = {'0':'common','1':'','2':'self'}
    coupon_type_text = {'0':u'通用', '1': '','2':u'自助洗'}
    #优惠券类型（满减/折扣）
    delivery_coupon_type = {'0':'common','1':'common','2':'discount'}

class iface_list:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    #获取用户信息
    users_me = {'url':'/users/me','method':'POST','path_param':[],'query_param':[],'body_param':[]}
    #订单详情
    order_detail = {'url':'/orders/order_detail/self/{order_number}','method':'GET','path_param':['order_number'],'query_param':[],'body_param':[]}


