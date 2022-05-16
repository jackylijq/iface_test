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
    #获取用户信息
    userInfo = {'url':'/cabinet_client/wx/user/userInfo','method':'GET','Authorization':'YES','remark':u'用户信息'}
    # 上报微信from_id
    reportFormId = {'url': '/cabinet_client/wx/user/reportFormId', 'method': 'POST','Authorization':'YES','remark': u'上报微信from_id'}
    #附近的干洗柜
    neighbourCabinets = {'url':'/cabinet_client/api/v1/cabinets/neighbourCabinets','method':'GET','Authorization':'YES','remark':u'附近的干洗柜'}
    # 干洗下单
    createOrder = {'url': '/cabinet_client/api/v1/order/createOrder', 'method': 'POST','Authorization':'YES','remark': u'干洗下单'}
    # 订单物流状态
    orderExpress = {'url': '/cabinet_client/api/v1/order/orderExpress', 'method': 'GET','Authorization':'YES','remark': u'订单物流状态'}
    # 取消订单
    cancelOrder = {'url': '/cabinet_client/api/v1/order/cancelOrder', 'method': 'DELETE','Authorization':'YES','remark': u'取消订单'}
    # 充值明细
    queryRechargeDetail = {'url': '/cabinet_client/api/v1/pay/queryRechargeDetail', 'method': 'GET','Authorization':'YES','remark': u'充值明细'}
    # 可提现金额
    refundBalance = {'url': '/cabinet_client/api/v1/pay/refundBalance', 'method': 'GET','Authorization':'YES','remark': u'可提现金额'}
    # 申请提现
    applyRefund = {'url': '/cabinet_client/api/v1/pay/applyRefund', 'method': 'POST','Authorization':'YES','remark': u'申请提现'}
    # 提现原因
    refundReasons = {'url': '/cabinet_client/api/v1/pay/refundReasons', 'method': 'GET','Authorization':'YES','remark': u'提现原因'}
    # 获取用户反馈类型
    queryAdviceType = {'url': '/cabinet_client/api/v1/advice/queryAdviceType', 'method': 'GET','Authorization':'YES','remark': u'获取用户反馈类型'}
    # 提交反馈
    addUserAdvice = {'url': '/cabinet_client/api/v1/advice/addUserAdvice', 'method': 'POST','Authorization':'YES','remark': u'提交反馈'}
    # 可申请返洗的衣物
    repeatWashClothes = {'url': '/cabinet_client/api/v1/order/repeatWashClothes', 'method': 'GET','Authorization':'YES','remark': u'可申请返洗的衣物'}
    # 返洗历史
    repeatWashHistory = {'url': '/cabinet_client/api/v1/order/repeatWashHistory', 'method': 'GET','Authorization':'YES','remark': u'返洗历史'}
    # 提交返洗申请
    applyRepeatWash = {'url': '/cabinet_client/api/v1/order/applyRepeatWash', 'method': 'POST','Authorization':'YES','remark': u'提交返洗申请'}
    # 获取验证码
    getCode = {'url': '/cabinet_client/wx/user/getCode', 'method': 'POST','Authorization':'YES','remark': u'获取验证码'}
    # 活动信息
    queryCouponActivity = {'url': '/cabinet_client/api/v1/activity/queryCouponActivity', 'method': 'GET','Authorization':'YES','remark': u'活动信息'}
    # 订单分享确认
    shareConfirm = {'url': '/cabinet_client/api/v1/activity/shareConfirm', 'method': 'POST','Authorization':'YES','remark': u'订单分享确认'}
    # 订单删除
    deleteOrder = {'url': '/cabinet_client/api/v1/order/deleteOrder', 'method': 'DELETE','Authorization':'YES','remark': u'订单删除'}
    # 领取优惠券
    receiveCoupons = {'url': '/cabinet_client/api/v1/activity/receiveCoupons', 'method': 'POST','Authorization':'YES','remark': u'领取优惠券'}
    # 扫码检测
    scanQrcodeCheck = {'url': '/cabinet_client/api/v1/order/scanQrcodeCheck', 'method': 'POST','Authorization':'YES','remark': u'扫码检测'}
    # 上报是否开柜成功
    openBoxStatusConfirm = {'url': '/cabinet_client/api/v1/cabinets/openBoxStatusConfirm', 'method': 'POST','Authorization':'YES','remark': u'上报是否开柜成功'}
    # 充值
    recharge = {'url': '/cabinet_client/api/v1/pay/recharge', 'method': 'POST','Authorization':'YES','remark': u'充值'}
    # 获取充值选项
    queryRechargeSchemes = {'url': '/cabinet_client/api/v1/pay/queryRechargeSchemes', 'method': 'GET','Authorization':'YES','remark': u'获取充值选项'}
    # 轮训获取是否开柜成功
    openBoxStatus = {'url': '/cabinet_client/api/v1/cabinets/openBoxStatus', 'method': 'GET','Authorization':'YES','remark': u'轮训获取是否开柜成功'}
    # 分配柜子/预约柜子
    assignBox = {'url': '/cabinet_client/api/v1/cabinets/assignBox', 'method': 'POST','Authorization':'YES','remark': u'分配柜子/预约柜子'}
    #扫码开柜接口
    openBoxWithQrcode = {'url': '/cabinet_client/api/v1/cabinets/openBoxWithQrcode', 'method': 'POST','Authorization':'YES','remark': u'扫码开柜接口'}
    # 订单评价
    score = {'url': '/cabinet_client/api/v1/order/score', 'method': 'POST','Authorization':'YES','remark': u'订单评价'}
    # 商品评论列表
    goodsComments = {'url': '/cabinet_client/api/v1/goods/goodsComments', 'method': 'GET','Authorization':'YES','remark': u'商品评论'}
    # 检查是否可以加入购物车
    queryCartInfo = {'url': '/cabinet_client/api/v1/goods/queryCartInfo', 'method': 'GET','Authorization':'YES','remark': u'检查是否可以加入购物车'}
    # 商品购买记录
    goodsPurchasingRecord = {'url': '/cabinet_client/api/v1/goods/goodsPurchasingRecord', 'method': 'GET','Authorization':'YES','remark': u'商品购买记录'}
    # 邀请返利数据统计
    dataStatistics = {'url': '/cabinet_client/api/v1/invitation/dataStatistics', 'method': 'GET','Authorization':'YES','remark': u'邀请返利数据统计'}
    # 返利提现申请
    withdraw = {'url': '/cabinet_client/api/v1/invitation/withdraw', 'method': 'POST','Authorization':'YES','remark': u'返利提现申请'}
    # 登陆成功获取优惠券
    getCoupons = {'url': '/cabinet_client/api/v1/invitation/getCoupons', 'method': 'POST','Authorization':'YES','remark': u'登陆成功获取优惠券'}
    # 邀请人信息
    inviterInfo = {'url': '/cabinet_client/api/v1/invitation/inviterInfo', 'method': 'GET','Authorization':'YES','remark': u'邀请人信息'}
    # 风险确认
    detectionConfirm = {'url': '/cabinet_client/api/v1/order/detectionConfirm', 'method': 'POST','Authorization':'YES','remark': u'风险确认'}
    # 预检报告
    detectionReport = {'url': '/cabinet_client/api/v1/order/detectionReport', 'method': 'GET','Authorization':'YES','remark': u'预检报告'}
    # 订单详情
    orderDetail = {'url': '/cabinet_client/api/v1/order/orderDetail', 'method': 'GET','Authorization':'YES','remark': u'订单详情'}
    # 订单支付
    orderPay = {'url': '/cabinet_client/api/v1/order/pay', 'method': 'POST','Authorization':'YES','remark': u'订单支付'}
    # 订单列表
    orderList = {'url': '/cabinet_client/api/v1/order/orderList', 'method': 'GET','Authorization':'YES','remark': u'订单列表'}
    # 城市列表
    cities = {'url': '/cabinet_client/api/v1/goods/cities', 'method': 'GET','Authorization':'YES','remark': u'城市列表'}
    # 筛选城市对应的柜子
    queryCityCabinets = {'url': '/cabinet_client/api/v1/cabinets/queryCityCabinets', 'method': 'GET','Authorization':'YES','remark': u'筛选城市对应的柜子'}
    # 首页数据获取
    homeIndex = {'url': '/cabinet_client/api/v1/goods/homeIndex', 'method': 'GET','Authorization':'YES','remark': u'首页数据获取'}
    # 优惠券兑换
    exchangeCoupon = {'url': '/cabinet_client/api/v1/activity/exchangeCoupon', 'method': 'POST','Authorization':'YES','remark': u'优惠券兑换'}
    # 获取本人分享链接
    shareLink = {'url': '/cabinet_client/api/v1/activity/shareLink', 'method': 'GET','Authorization':'YES','remark': u'获取本人分享链接'}
    # 大礼包检查
    giftPackageCheck = {'url': '/cabinet_client/api/v1/activity/giftPackageCheck', 'method': 'GET','Authorization':'YES','remark': u'大礼包检查'}
    # 领取大礼包
    receiveGiftPackage = {'url': '/cabinet_client/api/v1/activity/receiveGiftPackage', 'method': 'POST','Authorization':'YES','remark': u'领取大礼包'}
    # 我的优惠券
    myCouponList = {'url': '/cabinet_client/api/v1/activity/myCouponList', 'method': 'GET','Authorization':'YES','remark': u'我的优惠券'}
    # 首页未读优惠券
    unreadCoupons = {'url': '/cabinet_client/api/v1/activity/unreadCoupons', 'method': 'GET','Authorization':'YES','remark': u'首页未读优惠券'}
    # 优惠券列表
    userCouponList = {'url': '/cabinet_client/api/v1/activity/userCouponList', 'method': 'GET','Authorization':'YES','remark': u'优惠券列表'}
    # 用户优惠券
    queryUserCoupons = {'url': '/cabinet_client/api/v1/activity/queryUserCoupons', 'method': 'GET','Authorization':'YES','remark': u'用户优惠券'}
    # 支持的城市列表--团购
    groupOrderCities = {'url': '/cabinet_client/api/v1/groupOrder/cities', 'method': 'GET','Authorization':'YES','remark': u'团购支持的城市'}
    # 团购请求提交--团购
    applyGroupOrder = {'url': '/cabinet_client/api/v1/groupOrder/applyGroupOrder', 'method': 'POST','Authorization':'YES','remark': u'团购请求提交'}
    # 柜子业务信息
    businessInfo = {'url': '/cabinet_client/map/businessInfo', 'method': 'GET', 'Authorization': 'YES','remark': u'柜子业务信息'}
    #新手指南
    guide = {'url': '/cabinet_client/navigation/guide', 'method': 'GET', 'Authorization': 'NO','remark': u'新手指南'}
    #柜子搜索
    cabinet_search = {'url': '/cabinet_client/map/search', 'method': 'GET', 'Authorization': 'NO','remark': u'柜子搜索'}
    # 附加服务列表
    additionalservices ={'url': '/cabinet_client/additionalservices/list', 'method': 'GET', 'Authorization': 'NO','remark': u'附加服务列表'}
    # 附加服务列表
    navigation_home ={'url': '/cabinet_client/navigation/home', 'method': 'GET', 'Authorization': 'NO','remark': u'附加服务列表'}
    # 评论概览
    comment_view = {'url': '/cabinet_client/comment/overview', 'method': 'GET', 'Authorization': 'NO','remark': u'评论概览'}
    #视野内的柜子
    withinview = {'url': '/cabinet_client/map/withinview', 'method': 'GET', 'Authorization': 'NO','remark': u'视野内的柜子'}
    #任务信息
    salesManTasks = {'url': '/cabinet_client/api/v1/salesManTask/salesManTasks', 'method': 'GET', 'Authorization': 'NO','remark': u'任务信息'}
    # 店员邀请老用户
    salesManInvite = {'url': '/cabinet_client//wx/user/salesManInvite', 'method': 'POST', 'Authorization': 'NO','remark': u'店员邀请老用户'}
    #任务详情
    salesManTaskInfo = {'url': '/cabinet_client/api/v1/salesManTask/salesManTaskInfo', 'method': 'GET', 'Authorization': 'NO','remark': u'任务详情'}
    #店员信息
    salesManInfo = {'url': '/cabinet_client/api/v1/salesManTask/salesManInfo', 'method': 'GET', 'Authorization': 'NO','remark': u'店员信息'}
    #领取奖励
    receiveReward = {'url': '/cabinet_client/api/v1/salesManTask/receiveReward', 'method': 'POST', 'Authorization': 'NO','remark': u'领取奖励'}
    #小掌柜提现
    sales_withdraw ={'url': '/cabinet_client/api/v1/salesManTask/withdraw', 'method': 'POST', 'Authorization': 'NO','remark': u'小掌柜提现'}
    #店员邀请记录
    salesManInviteRecord = {'url': '/cabinet_client//api/v1/salesManTask/salesManInviteRecord', 'method': 'GET', 'Authorization': 'NO','remark': u'店员邀请记录'}
    #任务收入明细
    sales_task_list = {'url': '/cabinet_client/api/v1/salesManTask/task/list', 'method': 'GET', 'Authorization': 'NO','remark': u'任务收入明细'}

class iface_param:
    """"
    接口列表，包含接口的地址，请求方式，参数列表
    参数包含路径参数、query、body
    """
    #获取用户信息
    userInfo = []
    # 订单物流状态
    reportFormId = ['formId']
    #附近的干洗柜
    neighbourCabinets = ['latitude','longitude','keywords']
    # 干洗下单
    createOrder = ['goods','couponId','comment']
    # 订单物流状态
    orderExpress = ['orderNumber']
    # 取消订单
    cancelOrder = ['orderNumber']
    # 充值明细
    queryRechargeDetail = ['pageNumber','pageSize']
    # 可提现金额
    refundBalance = []
    # 申请提现
    applyRefund = ['reason']
    # 提现原因
    refundReasons = []
    # 获取用户反馈类型
    queryAdviceType = []
    # 提交反馈
    addUserAdvice = ['adviceTypeId','advice']
    # 可申请返洗的衣物
    repeatWashClothes = ['orderNumber']
    # 返洗历史
    repeatWashHistory = ['orderNumber']
    # 提交返洗申请
    applyRepeatWash = ['clothes','orderNumber']
    # 获取验证码
    getCode = ['phone','voice','rebind']
    # 活动信息
    queryCouponActivity = ['outId']
    # 订单分享确认
    shareConfirm = ['orderNumber','outId']
    # 订单删除
    deleteOrder = ['orderNumber']
    # 领取优惠券
    receiveCoupons = ['orderId','outId']
    # 扫码检测
    scanQrcodeCheck = ['q','scanCodeTime']
    # 上报是否开柜成功
    openBoxStatusConfirm = ['orderNumber','status']
    # 充值
    recharge = ['schemeId','amount','inviter']
    # 获取充值选项
    queryRechargeSchemes = []
    # 轮训获取是否开柜成功
    openBoxStatus = ['orderNumber','messageId']
    # 分配柜子/预约柜子
    assignBox = ['orderNumber','cabinetId']
    #扫码开柜接口
    openBoxWithQrcode = ['orderNumber','qrcode','latitude','longitude']
    # 订单评价
    score = ['orderNumber','price','quality','time','comment','images','isAnonymous']
    # 商品评论
    goodsComments = ['limit','page','goodsId']
    # 检查是否可以加入购物车
    queryCartInfo = ['goodsIds']
    # 商品购买记录
    goodsPurchasingRecord = ['limit','page','goodsId']
    # 邀请返利数据统计
    dataStatistics = []
    # 返利提现申请
    withdraw = []
    # 登陆成功获取优惠券
    getCoupons = ['inviter']
    # 邀请人信息
    inviterInfo = ['inviter']
    # 风险确认
    detectionConfirm = ['orderNumber','clothesId','status']
    # 预检报告
    detectionReport = ['orderNumber']
    # 订单详情
    orderDetail = ['orderNumber']
    # 订单支付
    orderPay = ['orderNumber','payChannel','payType']
    # 订单列表
    orderList = ['type','page','limit']
    # 城市列表
    cities = []
    # 筛选城市对应的柜子
    queryCityCabinets = ['city','keywords','page','limit','longitude','latitude']
    # 首页数据获取
    homeIndex = ['city']
    # 优惠券兑换
    exchangeCoupon = ['code']
    # 获取本人分享链接
    shareLink = []
    # 大礼包检查
    giftPackageCheck = []
    # 领取大礼包
    receiveGiftPackage = []
    # 我的优惠券
    myCouponList = []
    # 首页未读优惠券
    unreadCoupons = []
    # 优惠券列表
    userCouponList = ['cabinet','price','goods_activity_id']
    # 用户优惠券
    queryUserCoupons = ['outId','orderId']
    # 支持的城市列表--团购
    groupOrderCities = []
    # 支持的城市列表--团购
    applyGroupOrder = ['name','phone','province','city','type','company','counts','remarks']
    # 柜子业务信息
    businessInfo = ['cabinetId']
    #新手指南
    guide = []
    # 柜子搜索
    cabinet_search =['latitude','longitude','keywords']
    #附加服务列表
    additionalservices = ['serviceType','serviceClientType','serviceClient']
    # 附加服务列表
    navigation_home = ['city','latitude','longitude','distance']
    # 评论概览
    comment_view = []
    # 视野内的柜子
    withinview = ['centralLatitude','centralLongitude','southwestLatitude','southwestLongitude','northeastLatitude','northeastLongitude']
    #任务信息
    salesManTasks = []
    #店员邀请老用户
    salesManInvite = ['inviter']
    # 任务详情
    salesManTaskInfo = ['taskId']
    # 店员信息
    salesManInfo = []
    #领取奖励
    receiveReward = ['taskId']
    #小掌柜提现
    sales_withdraw = []
    # 店员邀请记录
    salesManInviteRecord = []
    #任务收入明细
    sales_task_list = ['salesManId','type','pageSize','pageNumber']


iface_list_base = [
    {'url':'/cabinet_client/wx/user/userInfo','method':'GET','Authorization':'YES','remark':u'用户信息'},
    # 上报微信from_id
    {'url': '/cabinet_client/wx/user/reportFormId', 'method': 'POST','Authorization':'YES','remark': u'上报微信from_id'},
    #附近的干洗柜
    {'url':'/cabinet_client/api/v1/cabinets/neighbourCabinets','method':'GET','Authorization':'YES','remark':u'附近的干洗柜'},
    # 干洗下单
    {'url': '/cabinet_client/api/v1/order/createOrder', 'method': 'POST','Authorization':'YES','remark': u'干洗下单'},
    # 订单物流状态
    {'url': '/cabinet_client/api/v1/order/orderExpress', 'method': 'GET','Authorization':'YES','remark': u'订单物流状态'},
    # 取消订单
    {'url': '/cabinet_client/api/v1/order/cancelOrder', 'method': 'DELETE','Authorization':'YES','remark': u'取消订单'},
    # 充值明细
    {'url': '/cabinet_client/api/v1/pay/queryRechargeDetail', 'method': 'GET','Authorization':'YES','remark': u'充值明细'},
    # 可提现金额,
    {'url': '/cabinet_client/api/v1/pay/refundBalance', 'method': 'GET','Authorization':'YES','remark': u'可提现金额'},
    # 申请提现
    {'url': '/cabinet_client/api/v1/pay/applyRefund', 'method': 'POST','Authorization':'YES','remark': u'申请提现'},
    # 提现原因
    {'url': '/cabinet_client/api/v1/pay/refundReasons', 'method': 'GET','Authorization':'YES','remark': u'提现原因'},
    # 获取用户反馈类型,
    {'url': '/cabinet_client/api/v1/advice/queryAdviceType', 'method': 'GET','Authorization':'YES','remark': u'获取用户反馈类型'},
    # 提交反馈
    {'url': '/cabinet_client/api/v1/advice/addUserAdvice', 'method': 'POST','Authorization':'YES','remark': u'提交反馈'},
    # 可申请返洗的衣物
    {'url': '/cabinet_client/api/v1/order/repeatWashClothes', 'method': 'GET','Authorization':'YES','remark': u'可申请返洗的衣物'},
    # 返洗历史
    {'url': '/cabinet_client/api/v1/order/repeatWashHistory', 'method': 'GET','Authorization':'YES','remark': u'返洗历史'},
    # 提交返洗申请
    {'url': '/cabinet_client/api/v1/order/applyRepeatWash', 'method': 'POST','Authorization':'YES','remark': u'提交返洗申请'},
    # 获取验证码
    {'url': '/cabinet_client/wx/user/getCode', 'method': 'POST','Authorization':'YES','remark': u'获取验证码'},
    # 活动信息
    {'url': '/cabinet_client/api/v1/activity/queryCouponActivity', 'method': 'GET','Authorization':'YES','remark': u'活动信息'},
    # 订单分享确认
    {'url': '/cabinet_client/api/v1/activity/shareConfirm', 'method': 'POST','Authorization':'YES','remark': u'订单分享确认'},
    # 订单删除
    {'url': '/cabinet_client/api/v1/order/deleteOrder', 'method': 'DELETE','Authorization':'YES','remark': u'订单删除'},
    # 领取优惠券
    {'url': '/cabinet_client/api/v1/activity/receiveCoupons', 'method': 'POST','Authorization':'YES','remark': u'领取优惠券'},
    # 扫码检测
    {'url': '/cabinet_client/api/v1/order/scanQrcodeCheck', 'method': 'POST','Authorization':'YES','remark': u'扫码检测'},
    # 上报是否开柜成功
    {'url': '/cabinet_client/api/v1/cabinets/openBoxStatusConfirm', 'method': 'POST','Authorization':'YES','remark': u'上报是否开柜成功'},
    # 充值
    {'url': '/cabinet_client/api/v1/pay/recharge', 'method': 'POST','Authorization':'YES','remark': u'充值'},
    # 获取充值选项
    {'url': '/cabinet_client/api/v1/pay/queryRechargeSchemes', 'method': 'GET','Authorization':'YES','remark': u'获取充值选项'},
    # 轮训获取是否开柜成功
    {'url': '/cabinet_client/api/v1/cabinets/openBoxStatus', 'method': 'GET','Authorization':'YES','remark': u'轮训获取是否开柜成功'},
    # 分配柜子/预约柜子
    {'url': '/cabinet_client/api/v1/cabinets/assignBox', 'method': 'POST','Authorization':'YES','remark': u'分配柜子/预约柜子'},
    #扫码开柜接口
    {'url': '/cabinet_client/api/v1/cabinets/openBoxWithQrcode', 'method': 'POST','Authorization':'YES','remark': u'扫码开柜接口'},
    # 订单评价
    {'url': '/cabinet_client/api/v1/order/score', 'method': 'POST','Authorization':'YES','remark': u'订单评价'},
    # 商品评论列表
    {'url': '/cabinet_client/api/v1/goods/goodsComments', 'method': 'GET','Authorization':'YES','remark': u'商品评论'},
    # 检查是否可以加入购物车
    {'url': '/cabinet_client/api/v1/goods/queryCartInfo', 'method': 'GET','Authorization':'YES','remark': u'检查是否可以加入购物车'},
    # 商品购买记录
    {'url': '/cabinet_client/api/v1/goods/goodsPurchasingRecord', 'method': 'GET','Authorization':'YES','remark': u'商品购买记录'},
    # 邀请返利数据统计
    {'url': '/cabinet_client/api/v1/invitation/dataStatistics', 'method': 'GET','Authorization':'YES','remark': u'邀请返利数据统计'},
    # 返利提现申请
    {'url': '/cabinet_client/api/v1/invitation/withdraw', 'method': 'POST','Authorization':'YES','remark': u'返利提现申请'},
    # 登陆成功获取优惠券
    {'url': '/cabinet_client/api/v1/invitation/getCoupons', 'method': 'POST','Authorization':'YES','remark': u'登陆成功获取优惠券'},
    # 邀请人信息
    {'url': '/cabinet_client/api/v1/invitation/inviterInfo', 'method': 'GET','Authorization':'YES','remark': u'邀请人信息'},
    # 风险确认
    {'url': '/cabinet_client/api/v1/order/detectionConfirm', 'method': 'POST','Authorization':'YES','remark': u'风险确认'},
    # 预检报告
    {'url': '/cabinet_client/api/v1/order/detectionReport', 'method': 'GET','Authorization':'YES','remark': u'预检报告'},
    # 订单详情,
    {'url': '/cabinet_client/api/v1/order/orderDetail', 'method': 'GET','Authorization':'YES','remark': u'订单详情'},
    # 订单支付
    {'url': '/cabinet_client/api/v1/order/pay', 'method': 'POST','Authorization':'YES','remark': u'订单支付'},
    # 订单列表
    {'url': '/cabinet_client/api/v1/order/orderList', 'method': 'GET','Authorization':'YES','remark': u'订单列表'},
    # 城市列表
    {'url': '/cabinet_client/api/v1/goods/cities', 'method': 'GET','Authorization':'YES','remark': u'城市列表'},
    # 筛选城市对应的柜子
    {'url': '/cabinet_client/api/v1/cabinets/queryCityCabinets', 'method': 'GET','Authorization':'YES','remark': u'筛选城市对应的柜子'},
    # 首页数据获取
    {'url': '/cabinet_client/api/v1/goods/homeIndex', 'method': 'GET','Authorization':'YES','remark': u'首页数据获取'},
    # 优惠券兑换
    {'url': '/cabinet_client/api/v1/activity/exchangeCoupon', 'method': 'POST','Authorization':'YES','remark': u'优惠券兑换'},
    # 获取本人分享链接,
    {'url': '/cabinet_client/api/v1/activity/shareLink', 'method': 'GET','Authorization':'YES','remark': u'获取本人分享链接'},
    # 大礼包检查
    {'url': '/cabinet_client/api/v1/activity/giftPackageCheck', 'method': 'GET','Authorization':'YES','remark': u'大礼包检查'},
    # 领取大礼包,
    {'url': '/cabinet_client/api/v1/activity/receiveGiftPackage', 'method': 'POST','Authorization':'YES','remark': u'领取大礼包'},
    # 我的优惠券
    {'url': '/cabinet_client/api/v1/activity/myCouponList', 'method': 'GET','Authorization':'YES','remark': u'我的优惠券'},
    # 首页未读优惠券
    {'url': '/cabinet_client/api/v1/activity/unreadCoupons', 'method': 'GET','Authorization':'YES','remark': u'首页未读优惠券'},
    # 优惠券列表
    {'url': '/cabinet_client/api/v1/activity/userCouponList', 'method': 'GET','Authorization':'YES','remark': u'优惠券列表'},
    # 用户优惠券
    {'url': '/cabinet_client/api/v1/activity/queryUserCoupons', 'method': 'GET','Authorization':'YES','remark': u'用户优惠券'},
    # 支持的城市列表--团购
    {'url': '/cabinet_client/api/v1/groupOrder/cities', 'method': 'GET','Authorization':'YES','remark': u'团购支持的城市'},
    # 团购请求提交
    {'url': '/cabinet_client/api/v1/groupOrder/applyGroupOrder', 'method': 'POST','Authorization':'YES','remark': u'团购请求提交'},
]