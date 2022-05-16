#coding=utf-8

""""
user_list:APP、小程序等访问的用户token信息
web_user_list：后台访问的token信息
其他的一些字典表的定义：主要用于匹配接口返回文本内容，数据库为ID，无法对应的情况
"""

class common_parameter():

    #订单列表状态
    order_list_type = {'0':u'全部订单','1':u'未支付','2':u'需补费','3':u'已完成','4':u'待评价','5':u'反洗单','6':u'待存衣',}


class iface_list:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    #全局流量统计(时间区间)
    totalsec = {'url':'/aaa/user/this/v1/add','method':'POST','Authorization':'YES','remark':u'全局流量统计(时间区间)'}


class iface_param:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    # 订单物流状态
    totalsec = ['starttime','endtime','type','pagetype','sortfield','sorttype']
