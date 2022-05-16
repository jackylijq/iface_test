#coding=utf-8
#主要用来存储所有查询的控件的id/xpath等信息

class common_controls():
    #微信发现按钮
    wechat_find_button = ['wechat_find_button', 'xpath', '//*[@text="发现"]']
    #小程序按钮
    small_routine_button = ['small_routine_button','xpath', '//*[@text="小程序"]']
    # 我的都小程序按钮
    small_routine_me = ['small_routine_button', 'xpath', '//*[@text="我的小程序"]']
    #自助洗小程序
    self_wash_button = ['self_wash_button','xpath', '//*[@text="轻氧洗衣校园版"]']
    #s

class self_wash_controls():
    #订单列表
    self_order_list= ['self_order_list','xpath', '//*[@text="订单"]']
    #我的
    owner_button = ['owner_button','xpath', '//*[@text="我的"]']
    #首页
    main_paige = ['main_paige','xpath', '//*[@text="首页"]']
    #首页-进行中的订单
    main_running_order = ['main_running_order','xpath', '//*[@text="进行中的订单"]']
    # 首页-扫一扫
    main_scan_devices = ['main_scan_devices', 'xpath', '//*[@text="扫一扫"]']
    #首页查看设备
    main_check_devices = ['main_check_devices', 'xpath', '//*[@text="查看设备"]']
    #首页优惠券入口
    main_coupon_list = ['main_check_devices', 'xpath', '//*[@text="优惠券"]']
    #我的页面优惠券入口
    owner_coupon_list = ['main_check_devices', 'xpath', '//*[contains(@text,"优惠券")]']
    #优惠券兑换码输入框
    exchange_code_text = ['exchange_code_text', 'xpath', '//*[@text="请输入您的优惠码"]']
    #兑换码 兑换按钮
    exchange_code_button = ['exchange_code_button', 'xpath', '//*[@text="立即兑换"]']
    #兑换失败提示
    exchange_filed_toast = ['exchange_code_button', 'xpath', '//*[contains(@text,"该兑换码不存在")]']



class cabinet_wash_controls():
    wash_clothes_entry = ['self_wash_button','xpath', '//*[@text="点我洗衣"]']


    #返回上一层按钮
    back_to_up_level = ['back_to_up_level', 'id', 'android:id/action_bar_title']
    #导航 - 工作
    navigation_work = ['navigation_work','name','工作']
    navigation_message = ['navigation_message', 'name', '消息']
    navigation_contacts = ['navigation_contacts', 'name', '联系人']
    navigation_me = ['navigation_me', 'name', '我']
    #插件：
    Plugin_newReport = ['Plugin_newReport', 'name', '问题上报']
    Plugin_TodayTip = ['Plugin_TodayTip', 'name', '今日提示']
    Plugin_Bulletin = ['Plugin_Bulletin', 'name', '公文通告']
    Plugin_VerifyCheck = ['Plugin_VerifyCheck', 'name', '我的任务']
    Plugin_SelfDeal = ['Plugin_SelfDeal', 'name', '自行处置']
    Plugin_Query = ['Plugin_Query', 'name', '通用查询']
    Plugin_Map = ['Plugin_Map', 'name', '地图']
    Plugin_LeaderAssign = ['Plugin_LeaderAssign', 'name', '领导交办']
    Plugin_Statistics = ['Plugin_Statistics', 'name', '综合评价']
    Plugin_Monitor = ['Plugin_Monitor', 'name', '动态监控']
    Plugin_Manager = ['Plugin_Manager', 'name', '案卷督办']
    Plugin_DealHelper = ['Plugin_DealHelper', 'name', '案件处置']

    #下拉列表-第一个选项
    drop_down_list_first = ['drop_down_list_first', 'id', 'android:id/text1']

    #弹窗的确认、关闭等信息提示按钮
    confirm_button = ['confirm_button', 'id', 'cn.com.egova.egovamobile:id/confirm_button']
    #弹窗的文本信息区域
    confirm_text_location = ['confirm_text_location', 'id', 'cn.com.egova.egovamobile:id/content_text']
    #弹窗取消按钮
    cancel_button = ['cancel_button', 'id', 'cn.com.egova.egovamobile:id/cancel_button']
    #确定按钮
    makeSure_button =['makeSure_button', 'name', '确 定']

    #系统拍照功能参数=================================================================================================
    open_camera_button = ['open_camera_button', 'id', 'cn.com.egova.egovamobile:id/media_add_camera']
    #拍照按钮
    camera_take_photo = ['camera_take_photo', 'id', 'cn.com.egova.egovamobile:id/camera_btnTakePhoto']
    #保存按钮
    camera_save_pic_button = ['camera_save_pic_button', 'id', 'cn.com.egova.egovamobile:id/camera_btnSave']
    #继续拍照按钮
    keep_take_photo_button = ['keep_take_photo_button', 'id', 'cn.com.egova.egovamobile:id/camera_btnGoOn']

    #权限控制 -允许 =======================================================================================================
    access_control_enable = ['access_control_enable', 'name', '允许']
    #右上角菜单按钮
    right_cornor_menu = ['right_cornor_menu', 'id', 'cn.com.egova.egovamobile:id/menu_text_item']
    #多媒体栏位置
    media_infor_location = ['media_infor_location', 'id', 'cn.com.egova.egovamobile:id/task_list_item_medianum']
    # 案件号
    task_num_location = ['task_num_location', 'id','cn.com.egova.egovamobile:id/task_list_item_task_num']
    #案件描述
    task_description = ['task_description', 'id','cn.com.egova.egovamobile:id/task_list_item_description']
    # 案件 位置描述
    task_address_desc = ['task_address_desc', 'id', 'cn.com.egova.egovamobile:id/task_list_item_address']
    # 右上角的+按钮
    actionbar_menuview_image = ['actionbar_id', 'id', "cn.com.egova.egovamobile:id/actionbar_menuview_image"]
    #发起讨论，领导交办等选择人员部门 =======================================================================================================
    #部门按钮
    contact_select_unit = ['contact_select_unit', 'xpath',"//android.widget.LinearLayout[@resource-id='cn.com.egova.egovamobile:id/base_tab_tabs_top']/android.widget.TextView[2]"]
    #部门列表，第一个复选框
    first_unit_checkbox = ['first_unit_checkbox', 'id', 'cn.com.egova.egovamobile:id/contact_list_item_select']
    #列表第一个，可以点击打开该部门列表
    unit_list_location = ['unit_list_location', 'id', 'cn.com.egova.egovamobile:id/contact_search_listitem_info']
    #部门选择完成之后的确定按钮
    contact_confirm_id = ['contact_confirm_id', 'id', "cn.com.egova.egovamobile:id/multi_contact_multi_confirm"]
    #联系人发送消息按钮
    contact_send_message = ['contact_send_message', 'id', "cn.com.egova.egovamobile:id/btn_chat"]


class Server_Url_Paramter():
    setting_button = ['setting_butoon','id','cn.com.egova.egovamobile:id/login_set_server_url']
    setting_edit = ['setting_edit','id','cn.com.egova.egovamobile:id/setting_edit']
    setting_ok_button = ['setting_ok_button','id','cn.com.egova.egovamobile:id/server_setting_ok']
    setting_check_button = ['setting_check_button', 'id', 'cn.com.egova.egovamobile:id/server_setting_test']

class Login_egova_Paramter():
    login_txtUsername = ['login_txtUsername','id','cn.com.egova.egovamobile:id/login_username']
    login_txtPassword = ['login_txtPassword','id','cn.com.egova.egovamobile:id/login_txtPassword']
    save_pwd = ['save_pwd','id','cn.com.egova.egovamobile:id/save_pwd']
    login_btnSubmit = ['login_btnSubmit','id','cn.com.egova.egovamobile:id/login_submit']
    home_tab_item_icon = ['home_tab_item_icon','id','cn.com.egova.egovamobile:id/home_tab_item_icon']

class Messagebar_Paramter():
    case_assistant_name = ['case_assistant_name','name','案件处置助手']
    exit_id = ['exit_id','id','android:id/up']
    my_task_name =['my_task_name','name','我的任务']
    leader_assign_name = ['leader_assign_name','name','领导交办']

class Today_tips_Paramter():
    tip_name = ['tip_name','name','今日提示']
    exit_id = ['exit_id', 'id', 'android:id/up']
    back_to_up_lever = ['back_to_up_lever', 'id','android:id/action_bar_title']
    today_tips_title = ['today_tips_title','id','cn.com.egova.egovamobile:id/today_tip_title']

class Map_Paramter():
    select_name = ['select_name','name','选定位置']
    confirm_name =['confirm_name','name','确定']
    full_map_button = ['full_map_button','id','cn.com.egova.egovamobile:id/map_imgbtnBigMap']
    zoom_map_button = ['zoom_map_button','id','cn.com.egova.egovamobile:id/map_imgbtnZoomIn']

class General_queryp_Paramter():
    query_StartDate_id =['query_StartDate_id','id','cn.com.egova.query:id/event_query_StartDate']  # 开始日期
    set_up_id =['set_up_id','id','android:id/button1']  # 设定按钮
    query_EndDate_id = ['query_EndDate_id','id','cn.com.egova.query:id/event_query_EndDate'] # 结束日期
    query_TaskNumber_id = ['query_TaskNumber_id','id','cn.com.egova.egovamobile:id/event_query_txtTaskNumber']  # 任务号
    query_EventType_id = ['query_EventType_id','id','cn.com.egova.query:id/event_query_spnEventType'] # 类型
    query_Type_keys = ['query_Type_keys','name','全部']
    query_MainType_id = ['query_MainType_id','id','cn.com.egova.query:id/event_query_spnMainType'] # 大类
    query_SubType_id = ['query_SubType_id','id','cn.com.egova.query:id/event_query_spnSubType']  # 小类
    query_cbunit_id = ['query_cbunit_id','id','cn.com.egova.query:id/event_query_cbunit']  # 本部门
    query_StatusNormal_id = ['query_StatusNormal_id','id','cn.com.egova.query:id/event_query_ckbStatusNormal'] # 处理中
    query_StatusClosed_id = ['query_StatusClosed_id','id','cn.com.egova.query:id/event_query_ckbStatusClosed'] # 结案
    query_StatusUnregistered_id = ['query_StatusUnregistered_id','id','cn.com.egova.query:id/event_query_ckbStatusUnregistered']  # 挂账
    query_StatusInvalid_id = ['query_StatusInvalid_id','id','cn.com.egova.query:id/event_query_ckbStatusInvalid'] # 作废
    query_Map_id = ['query_Map_id','id','cn.com.egova.query:id/event_query_Map']  # 地图定位
    map_bottom_id = ['map_bottom_id','id','cn.com.egova.pluginmap:id/map_bottom_menu']  # 选定位置
    btnQuery_id = ['btnQuery_id','id','cn.com.egova.egovamobile:id/event_query_btnQuery']  # 查询按钮
    btnDescription_id = ['btnDescription_id','id','cn.com.egova.query:id/event_query_btnDescription']  # 描述
    query_txtRange_id = ['query_txtRange_id','id','cn.com.egova.query:id/event_query_txtRange'] # 查询范围
    ReporterSelf_id = ['ReporterSelf_id','id','cn.com.egova.query:id/event_query_ckbReporterSelf'] # 上报人
    exit_id = ['exit_id','id','android:id/up']
    back_to_up = ['back_to_up', 'id', 'android:id/action_bar_title']
    back_to_qure_list = ['back_to_qure_list','name','案件详情']

#公文通告
class Announcement_Paramter():
    file_bar_name = ['file_bar_name','name','文件']
    file_xpath = ['file_xpath','xpth',"//android.widget.ListView[@resource-id='cn.com.egova.bulletin:id/g_base_list']/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]"]
    exit_id = ['exit_id','id','android:id/action_bar_title']
    Exit_id = ['Exit_id','id','android:id/up']
    Bulletin_first_title = ['Bulletin_first_title','id','cn.com.egova.egovamobile:id/bulletin_title']

class My_work_Paramter():
    btn_duty_id = ['btn_duty_id','id','cn.com.egova.work:id/btn_duty']
    confirm_btn_id = ['confirm_btn_id','id','android:id/button1']
    after_work_name =  ['after_work_name','name','下班']
    menu_list_id = ['menu_list_id','id','cn.com.egova.work:id/actionbar_menuview_item']
    track_id = ['track_id','id','cn.com.egova.work:id/actionbar_menu_list_item_title']
    map_track_id = ['map_track_id','id','cn.com.egova.pluginmap:id/map_track_play']
    exit_name = ['exit_name','name','我的工作']

class report_paramter():

    add_button_id =['add_button_id','id','cn.com.egova.pluginreport:id/report_new'] # 新增按钮ID
    eventtype_list_id = ['eventtype_list_id','id','cn.com.egova.egovamobile:id/report_eventtype']  # 问题类型列表控件
    maintype_list_id = ['maintype_list_id','id','cn.com.egova.egovamobile:id/report_maintype'] # 大类列表控件
    subtype_list_id = ['subtype_list_id','id','cn.com.egova.egovamobile:id/report_subtype'] # 小类列表控件
    eventtype_name = ['eventtype_name','name','事件']
    # maintype_name = [' maintype_name','name','公用设施']
    # subtype_name = ['subtype_name','name','上水井盖']
    #大小类列表第一个
    maintype_location = [' maintype_location', 'id', 'android:id/text1']
    subtype_location = ['subtype_location', 'id', 'android:id/text1']
    drop_down_list_select =  ['drop_down_list_select', 'id', 'android:id/text1']
    childtype_list_id = ['childtype_list_id','id','cn.com.egova.egovamobile:id/report_childtype'] # 小类列表控件
    microtype_list_id = ['childtype_list_id', 'id', 'cn.com.egova.egovamobile:id/report_microtype']  # 小类列表控件
    #小类名称位置
    subtype_name_location = ['subtype_name_location','xpath',"//android.widget.Spinner[@resource-id='cn.com.egova.pluginreport:id/report_subtype']/android.widget.TextView"]
    photo_xpath = ['photo_xpath','xpath',"//android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageButton"]
    select_id = ['select_id','id','cn.com.egova.pluginreport:id/id_select']
    btn_report_id = ['btn_report_id','id','cn.com.egova.egovamobile:id/btn_report']
    #确认按钮
    confirm_report_id = ['confirm_report_id', 'id', 'cn.com.egova.egovamobile:id/confirm_button']
    confirm_keys_name = ['confirm_keys_name','name','确定']
    #描述信息
    description_id = ['description_id','id','cn.com.egova.egovamobile:id/report_desc']
    #选择位置
    location_report_id = ['location_report_id','id','cn.com.egova.egovamobile:id/location_desc']
    map_confirm_id = ['map_confirm_id','id','cn.com.egova.egovamobile:id/map_bottom_menu']
    ok_button_id = ['ok_button_id','id','android:id/button1']
    #上传多媒体相关 --相册
    media_add_by_album = ['media_add_by_album','id','cn.com.egova.egovamobile:id/media_add_select_pic']  # 上传多媒体的+ID
    tool_photoadd_id = ['tool_photoadd_id','id','cn.com.egova.egovamobile:id/id_item_select']  # 上传多媒体的---相册 ID
    album_first_photo = ['album_first_photo','id','cn.com.egova.egovamobile:id/id_item_select'] #选择第一张照片
    select_confirm_button = ['select_confirm_button', 'id', 'cn.com.egova.egovamobile:id/id_select'] #确认按钮
    exit_id = ['exit_id','id','android:id/up']
    report_result = ['report_result','xpath',"//android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ScrollView/android.widget.TextView"]

class Verifycheckt_Paramter():
    filter_id = ['filter_id','id','cn.com.egova.egovamobile:id/actionbar_menuview_image']  # 筛选
    verify_name = ['verify_name','name','核实任务']
    check_name = ['check_name','name','核查任务']
    task_xpath = ['task_xpath','xpth',"//android.widget.ListView[@resource-id='cn.com.egova.verifycheck:id/g_base_list']/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]"]
    #任务号
    verifycheck_task_num = ['verifycheckt_task_num','id','cn.com.egova.egovamobile:id/task_list_item_task_num']
    verify_check_button = ['verify_check_button','id','cn.com.egova.egovamobile:id/task_detail_bottom_menu']  # 点击核实或者核查
    verify_function_button = ['verify_function_button','name','核实']
    check_function_button = ['verify_function_button', 'name', '核查']
    media_view_id = ['media_view_id','id','cn.com.egova.verifycheck:id/media_view']  # 添加图片按钮
    tool_photoadd_id = ['tool_photoadd_id','id','cn.com.egova.verifycheck:id/tool_photoadd']  # 选择相册
    photo_xpath = ['photo_xpath','xpath',"//android.widget.GridView[@resource-id='cn.com.egova.verifycheck:id/id_gridView']/android.widget.RelativeLayout[2]/android.widget.ImageButton[1]"]
    # 第一张图片
    verifycheck_first_photo_select_button = ['verifycheck_first_photo_select_button', 'id', 'cn.com.egova.verifycheck:id/id_item_select']
    select_photo_id = ['select_photo_id','id','cn.com.egova.verifycheck:id/id_select']  # 选择按钮
    verified_id = ['verified_id','id','cn.com.egova.egovamobile:id/rb_handled']  # 属实或者已处理
    verify_desc_location = ['verify_desc_location','id','cn.com.egova.egovamobile:id/base_report_desc']
    verify_desc = '自动化进行核实/核查上报操作'
    report_btn_id = [' report_btn_id','id','cn.com.egova.egovamobile:id/base_report_report_btn']  # 上报
    confirm_name = ['confirm_name','name','确定']
    close_name = ['close_name','name','关闭']
    exit_Verify_name = ['exit_Verify_name','name','核实']
    exit_Verification_name = ['exit_Verification_name','name','核查']
    exit_name = "我的任务"

class Selfdeal_Paramter():
    my_case_name = ['my_case_name','name','我的案件']
    add_case_id = ['add_case_id','id','cn.com.egova.pluginselfdeal:id/report_new'] # 添加
    report_eventtype_id = [' report_eventtype_id','id','cn.com.egova.pluginselfdeal:id/report_eventtype']  # 选择类型
    report_eventtype_keys = ['report_eventtype_keys','name','事件']
    report_maintype_id = ['report_maintype_id','id','cn.com.egova.pluginselfdeal:id/report_maintype']  # 大类
    report_maintype_keys = ['report_maintype_keys','name',"市容环境"]
    report_subtype_id = ['report_subtype_id','id',"cn.com.egova.pluginselfdeal:id/report_subtype" ] # 小类
    report_subtype_keys = ['report_subtype_keys','name',"道路破损"]
    #下拉列表第一个选项
    Main_sub_type_list_first = ['Main_sub_type_list_first', 'id', 'android:id/text1']
    location_desc_id = ['location_desc_id','id','cn.com.egova.pluginselfdeal:id/location_desc']  # 选择位置
    map_bottom_id = ['map_bottom_id ','id','cn.com.egova.pluginmap:id/map_bottom_menu']
    report_desc_id = ['report_desc_id','id','cn.com.egova.pluginselfdeal:id/report_desc']  # 描述
    # 处理前照片
    before_deal_xpath = ['before_deal_xpath','xpath',"//android.widget.LinearLayout[@resource-id='cn.com.egova.pluginselfdeal:id/picklayoutbefore']/android.widget.LinearLayout[1]/android.widget.GridView[1]/android.widget.LinearLayout[1]/android.widget.ImageView[1]"]
    # 处理后照片
    after_deal_xpath = ['after_deal_xpath','xpath',"//android.widget.LinearLayout[@resource-id='cn.com.egova.pluginselfdeal:id/picklayoutafter']/android.widget.LinearLayout[1]/android.widget.GridView[1]/android.widget.LinearLayout[1]/android.widget.ImageView[1]"]
    add_photo_id = ['add_photo_id','id','cn.com.egova.pluginselfdeal:id/tool_photoadd']  # 相册按钮
    select_photo_id = ['select_photo_id','id','cn.com.egova.pluginselfdeal:id/id_item_select']  # 选择相片
    comfirm_photo_id = ['comfirm_photo_id','id','cn.com.egova.pluginselfdeal:id/id_select']  # 选择按钮
    tool_camera_id = ['tool_camera_id','id','cn.com.egova.pluginselfdeal:id/tool_camera']
    TakePhoto_id = ['TakePhoto_id','id','cn.com.egova.egovamobile:id/camera_btnTakePhoto']  # 拍照按钮
    btnSave_id = ['btnSave_id','id','cn.com.egova.egovamobile:id/camera_btnSave']
    report_btn_id = ['report_btn_id','id','cn.com.egova.pluginselfdeal:id/btn_report']  # 自处理按钮
    comfirm_id = ['comfirm_id','id','android:id/button1']
    exit_name = ['exit_name','name',"我的案件"]

class Sepcial_inspect_Paramter():
    inspect_name = ['inspect_name','name',"正在进行"]
    exit_id = ['exit_id','id',"android:id/up"]
    task_xpath = ['task_xpath','xpath',"//android.widget.ListView[@resource-id='cn.com.egova.plugin.specialinspect:id/g_base_list']/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]"]
    census_report_name = ['census_report_name','name',"普查上报"]
    type_id = ['type_id','id',"cn.com.egova.plugin.specialinspect:id/g_field_selectbox"]
    type_keys_name = "			"
    report_location_id = ['report_location_id','id',"cn.com.egova.plugin.specialinspect:id/si_task_report_location"]
    map_bottom_id = ['map_bottom_id','id',"cn.com.egova.pluginmap:id/map_bottom_menu"]
    confirm_name = ['confirm_name','name',"确定"]
    opinin_name = ['opinin_name','name',"请输入意见..."]
    add_photo_id = ['add_photo_id','id',"cn.com.egova.plugin.specialinspect:id/media_view"]
    tool_photoadd_id = ['tool_photoadd_id','id',"cn.com.egova.plugin.specialinspect:id/tool_photoadd"]
    select_photo_xapth = ['select_photo_xapth','xpath',"//android.widget.GridView[@resource-id='cn.com.egova.plugin.specialinspect:id/id_gridView']/android.widget.RelativeLayout[3]/android.widget.ImageButton[1]"]
    confirm_id = ['confirm_id','id',"cn.com.egova.plugin.specialinspect:id/id_select"]
    report_btn_id = ['report_btn_id','id',"cn.com.egova.plugin.specialinspect:id/si_task_report_btn"]
    finish_name = ['finish_name','name',"已经结束"]
    census_history_name = ['census_history_name','name',"普查记录"]

class Coordinatequery_Paramter():
    query_btn_name = ['query_btn_name','name',"查询"]
    query_StartDate_id = ['query_StartDate_id','id',"cn.com.egova.pluginpatrolquery:id/event_query_editStartDate"]# 查询日期
    query_StartTime_id = ['query_StartTime_id','id',"cn.com.egova.pluginpatrolquery:id/patrol_query_editStartTime" ] # 查询开始时间
    query_EndTime_id = ['query_EndTime_id','id',"cn.com.egova.pluginpatrolquery:id/patrol_query_editEndTime"]  # 查询结束时间
    query_btn_id = ['query_btn_id','id',"cn.com.egova.pluginpatrolquery:id/event_query_btnQuery" ] # 查询
    track_playback_name = ['track_playback_name','name',"轨迹回放"]
    exit_id = ['exit_id ','id',"android:id/action_bar_title"]

class Partrolmanagement_Paramter():
    report_new_id = ['report_new_id','id',"cn.com.egova.pluginpointmanage:id/report_new"]
    grade_type_id = ['grade_type_id','id',"cn.com.egova.pluginpointmanage:id/report_gradetype"]
    grade_type_keys = ['grade_type_keys','name',"日常"]
    event_type_id = ['event_type_id','id',"cn.com.egova.pluginpointmanage:id/report_eventtype"]
    main_type_id = ['main_type_id','id',"cn.com.egova.pluginpointmanage:id/report_maintype" ] # 大类
    sub_type_id = ['sub_type_id','id',"cn.com.egova.pluginpointmanage:id/report_subtype"]
    location_desc_id = ['location_desc_id','id',"cn.com.egova.pluginpointmanage:id/location_desc"]  # 位置
    report_desc_id = ['report_desc_id','id',"cn.com.egova.pluginpointmanage:id/report_desc"]  # 描述
    media_view_id = ['media_view_id','id',"cn.com.egova.pluginpointmanage:id/media_view" ] # 图片
    add_photo_id = ['add_photo_id','id',"cn.com.egova.pluginselfdeal:id/tool_photoadd"]  # 相册按钮
    select_photo_id = ['select_photo_id','id',"cn.com.egova.pluginselfdeal:id/id_item_select"  ]# 选择相片
    comfirm_photo_id = ['comfirm_photo_id','id',"cn.com.egova.pluginselfdeal:id/id_select" ] # 选择按钮
    btn_report_id = ['btn_report_id','id',"cn.com.egova.pluginpointmanage:id/btn_report" ] # 提交
    exit_id = ['exit_id','id',"android:id/up"]

class IllegalReportt_Paramter():
    select_id = ['select_id','id',"cn.com.egova.ibreport:id/id_select"]
    photo_xpath = ['photo_xpath','xpath',"//android.widget.GridView[@resource-id='cn.com.egova.ibreport:id/id_gridView']/android.widget.RelativeLayout[2]/android.widget.ImageButton[1]"]
    photoadd_id = ['photoadd_id','id',"cn.com.egova.ibreport:id/tool_photoadd"]
    media_view_id = ['media_view_id','id',"cn.com.egova.ibreport:id/media_view"]
    location_confirm_name = ['location_confirm_name','name',"选定位置"]
    report_desc_id = ['report_desc_id','id',"cn.com.egova.ibreport:id/report_desc"]
    report_new_id = ['report_new_id','id',"cn.com.egova.ibreport:id/report_new"]
    illegal_person_id = ['illegal_person_id','id',"cn.com.egova.ibreport:id/report_illegal_person"]
    illegal_tel_id = ['illegal_tel_id','id',"cn.com.egova.ibreport:id/report_illegal_tel"]
    location_desc_id = ['location_desc_id','id',"cn.com.egova.ibreport:id/location_desc"]
    confirm_btn_name = ['confirm_btn_name','name',"确定"]

# class IllegalCheck_Paramter():
#
#     class IllegalVerification_Paramter():

class IllegalPatrol_Paramter():
    case_xpath = ['case_xpath','xpath',"//android.widget.LinearLayout[@resource-id='cn.com.egova.ibinspect:id/task_list_item_root']"]
    report_desc_id = ['report_desc_id','id',"cn.com.egova.ibinspect:id/report_desc"]
    media_view_id = ['media_view_id','id', "cn.com.egova.ibinspect:id/media_view"]
    photoadd_id = ['photoadd_id','id',"cn.com.egova.ibinspect:id/tool_photoadd"]
    photo_xpath = ['photo_xpath','xpath',"//android.widget.GridView[@resource-id='cn.com.egova.ibinspect:id/id_gridView']/android.widget.RelativeLayout[2]/android.widget.ImageButton[1]"]
    select_id = ['select_id','id',"cn.com.egova.ibinspect:id/id_select"]
    report_btn_name = ['report_btn_name','name',"巡检上报"]
    confirm_btn_name = ['confirm_btn_name','name',"确 定"]

class CompEvaluation_Paramter():
    group_name_id = ['group_name_id','id',"cn.com.egova.egovamobile:id/comment_group_name"]
    comment_daytype_xpath = ['comment_daytype_xpath','xpath',"//android.widget.ExpandableListView/android.widget.LinearLayout[2]/android.widget.LinearLayout[2]/android.widget.TextView[1]"]
    comment_weektype_xpath = ['comment_weektype_xpath','xpath',"//android.widget.ExpandableListView/android.widget.LinearLayout[2]/android.widget.LinearLayout[2]/android.widget.TextView[2]"]
    comment_monthtype_xpath = ['comment_monthtype_xpath','xpath', "//android.widget.ExpandableListView/android.widget.LinearLayout[2]/android.widget.LinearLayout[2]/android.widget.TextView[3]"]
    #高发问题分组--问题分类统计（部件）
    comment_day_xpath = ['comment_day_xpath','xpath',"//android.widget.ExpandableListView/android.widget.LinearLayout[4]/android.widget.LinearLayout[2]/android.widget.TextView[1]"]
    comment_week_xpath = ['comment_week_xpath','xpath',"//android.widget.ExpandableListView/android.widget.LinearLayout[4]/android.widget.LinearLayout[2]/android.widget.TextView[2]"]
    comment_month_xpath = ['comment_month_xpath','xpath',"//android.widget.ExpandableListView/android.widget.LinearLayout[4]/android.widget.LinearLayout[2]/android.widget.TextView[3]"]
    # 高发问题分组--问题分类统计（事件）
    third_month = ['third_month','xpath',"//android.widget.ExpandableListView/android.widget.LinearLayout[5]/android.widget.LinearLayout[2]/android.widget.TextView[3]"]
    # 高发问题分组--事件高发TOP5
    fourth_month = ['fourth_month', 'xpath',"//android.widget.ExpandableListView/android.widget.LinearLayout[6]/android.widget.LinearLayout[2]/android.widget.TextView[3]"]
    #高发问题分组--部件高发TOP5
    fifth_month = ['fifth_month', 'xpath',"//android.widget.ExpandableListView/android.widget.LinearLayout[7]/android.widget.LinearLayout[2]/android.widget.TextView[3]"]
    #返回按钮
    exit_id = ['exit_id','xpath',"android:id/up"]
    comment_trend_name = ['comment_trend_name','name',"趋势分析"]
    comment_Type_name = ['comment_Type_name','name',"同比"]
    comment_type_name = ['comment_type_name','name',"环比"]
    exit_name = ['exit_name','name',"综合评价"]
    Statistics_pegging_num2 = ['Statistics_pegging_report_num', 'xpath',"//android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout/android.widget.TextView[3]"]
    Statistics_pegging_num = ['Statistics_pegging_report_num', 'xpath',"//android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout/android.widget.TextView[4]"]
    Statistics_chart_switch_button = ['Statistics_chart_switch_button','id','cn.com.egova.egovamobile:id/action_switch']
    #反查之后的第一条案件
    Statistics_first_Rec_location = ['Statistics_first_Rec_location', 'id', 'cn.com.egova.egovamobile:id/task_list_item_task_num']
    #本月按钮
    comment_month = ['comment_month', 'id', 'cn.com.egova.egovamobile:id/comment_month']


class Persmonitor_Paramter():
    case_monitor_name = ['case_monitor_name','name',"案件"]
    exit_id = ['exit_id','id',"android:id/up"]

class Leaderassign_Paramter():
    newassign_id = ['newassign_id','id',"cn.com.egova.egovamobile:id/action_newassign"]
    member_xpath = ['member_xpath','xpath',"//android.widget.ListView[@resource-id='cn.com.egova.egovamobile:id/common_contact_list']/android.widget.LinearLayout[1]/android.widget.CheckBox[1]"]
    contact_confirm_id = ['contact_confirm_id','id',"cn.com.egova.egovamobile:id/multi_contact_multi_confirm"]
    b_4h_id = ['b_4h_id','id',"cn.com.egova.egovamobile:id/rb_4h"]
    b_12h_id = ['b_12h_id','id',"cn.com.egova.egovamobile:id/rb_12h"]
    b_1d_id = ['b_1d_id','id',"cn.com.egova.egovamobile:id/rb_1d"]
    b_7d_id = ['b_7d_id','id',"cn.com.egova.egovamobile:id/rb_7d"]
    b_else_id = ['b_else_id','id',"cn.com.egova.egovamobile:id/rb_else"]
    btn_send_id = ['btn_send_id','id',"cn.com.egova.egovamobile:id/btn_send"]
    recive_members_id = ['recive_members_id','id',"cn.com.egova.egovamobile:id/add_members"]  # 选择接收人员
    tip_content_id = ['tip_content_id','id',"cn.com.egova.egovamobile:id/tip_content" ] # 交办内容
    exit_id = ['exit_id','id',"android:id/action_bar_title"]
    Exit_id = ['Exit_id','id',"android:id/up"]
    contact_select_name = ['contact_select_name','name',"部门"]
    contact_select_unit = ['contact_select_unit', 'xpath', "//android.widget.LinearLayout[@resource-id='cn.com.egova.egovamobile:id/base_tab_tabs_top']/android.widget.TextView[2]"]
    #选择一个部门
    unit_list_location = ['unit_list_location','id','cn.com.egova.egovamobile:id/contact_search_listitem_info']
    first_unit_checkbox_bak = ['first_unit_checkbox_bak', 'xpath', "//android.widget.ListView[@resource-id='cn.com.egova.egovamobile:id/part_contact_list']/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.CheckBox"]
    first_unit_checkbox = ['first_unit_checkbox','id','cn.com.egova.egovamobile:id/contact_list_item_select']
    #接收人员区域
    Receiver_area_xpath = ['Receiver_area_xpath','xpath',"//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.TextView"]
    Receiver_area = ['Receiver_area','id','cn.com.egova.egovamobile:id/memberlist']
    #选择人员
    choose_xpath = ['choose_xpath','xpath',"//android.widget.ListView[@resource-id='cn.com.egova.egovamobile:id/multi_contact_list']/android.widget.LinearLayout[4]/android.widget.LinearLayout[1]/android.widget.CheckBox[1]"]

    contact_select_xpath = ['contact_select_xpath','xpath',"//android.widget.ListView[@resource-id='cn.com.egova.egovamobile:id/multi_contact_list']/android.widget.LinearLayout[4]/android.widget.LinearLayout[1]/android.widget.CheckBox[1]"]
    # 勾选部门界面确认按钮
    contact_confirm_unit = ['contact_confirm_unit','id',"cn.com.egova.egovamobile:id/choose_part_multi_confirm"]
    # 右上角菜单按钮
    menu_view_image_id = ['menuview_image_id','id',"cn.com.egova.egovamobile:id/actionbar_menuview_image"]
    need_dealt_name = ['need_dealt_name','name',"待办"]
    need_replt_name = ['need_replt_name','name',"结案"]
    need_answer_name = ['need_replt_name', 'name', "待回复"]
    reply_xpath = ['reply_xpath','xpath',"//android.widget.ListView/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.LinearLayout[5]/android.widget.LinearLayout[1]/android.widget.Button[1]"]
    send_xpath = ['send_xpath','xpath',"//android.widget.ListView/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.LinearLayout[5]/android.widget.LinearLayout[1]/android.widget.Button[2]"]
    reply_content_id = ['replycontent_id','id',"cn.com.egova.egovamobile:id/replycontent"]
    #领导交办-转发按钮
    assigner_options_transmit = ['assigner_options_transmit','id',"cn.com.egova.egovamobile:id/assigner_options_transmit"]
    # 领导交办-回复按钮
    assigner_options_reply = ['assigner_options_reply', 'id',"cn.com.egova.egovamobile:id/assigner_options_reply"]
    #惯用语界面确定按钮
    phrase_add_OK_button = ['phrase_add_OK_button','id','android:id/button1']

    btn_reply_id = ['btn_reply_id','id',"cn.com.egova.egovamobile:id/btn_reply"]
    btn_forward_id = ['Btn_send_id','id',"cn.com.egova.egovamobile:id/btn_forward"]
    add_members_id = ['add_members_id','id',"cn.com.egova.egovamobile:id/add_members"]
    all_name = ['all_name','name',"全部"]
    #任务交办界面接收人员信息
    leaderassign_receiver = ['leaderassign_receiver','id','cn.com.egova.egovamobile:id/txt_yq']
    #转发界面--转交人员
    leaderassign_Forwarding_personne = ['leaderassign_Forwarding_personnel','id','cn.com.egova.egovamobile:id/assign_creater']

class Casesupervise_Paramter():
    supervise_name = ['supervise_name','name',"督办"]
    #案件详情--督办按钮
    supervise_btn_id = ['supervise_btn_id','id',"cn.com.egova.egovamobile:id/task_detail_bottom_menu"]
    #答复天数
    replyDays_id = ['replyDays_id','id',"cn.com.egova.egovamobile:id/replyDays_txt"]
    replyDays_keys = ['replyDays_keys','name',"2"]
    # 发送短信
    sendmsg_sbn_id = ['sendmsg_sbn_id','id',"cn.com.egova.egovamobile:id/sendmsg_sbn"]
    #答复意见
    send_opinion_name = ['end_opinion_name','name',"请输入意见..."]
    #录音附件
    add_record_name = ['add_record_name','name',"录音"]
    #开始录音按钮
    opinion_btnRecord_id = ['opinion_btnRecord_id','id',"com.android.soundrecorder:id/btn_record"]
    #完成按钮
    opinion_btnStop_id = ['opinion_btnStop_id','id',"com.android.soundrecorder:id/btn_record_stop"]
    #选择按钮
    opinion_btnfinish_id = ['opinion_btnfinish_id','id',"com.android.soundrecorder:id/btn_finish"]
    #发送按钮
    opinion_btnSend_id = ['opinion_btnSend_id','id',"cn.com.egova.egovamobile:id/send_opinion_btnSend"]

    comfirm_id = ['comfirm_id','id',"android:id/button1"]
    exit_id = ['exit_id','id',"android:id/action_bar_title"]
    #超时件箱子
    overtime_rec_task = ['overtime_rec_task','name','超时件']
    #督办件箱子
    suplist_rec_task = ['suplist_rec_task','name','督办件']
    #获取案件号
    supervise_task_num_location = ['supervise_task_num_location', 'id', 'cn.com.egova.egovamobile:id/task_list_item_task_num']

class Inspectercheck_Paramter():
    base_tab_name = ['base_tab_name','name',"考评历史"]
    exit_id = ['exit_id','id',"android:id/up"]

class Reportevaluationn_Paramter():
    action_add_id = ['action_add_id','id',"cn.com.egova.examine:id/action_add"]
    select_id = ['select_id','id',"cn.com.egova.examine:id/id_select"]
    photo_xpath = ['photo_xpath','xpath',"//android.widget.GridView[@resource-id='cn.com.egova.examine:id/id_gridView']/android.widget.RelativeLayout[3]/android.widget.ImageView[1]"]
    #第一张图片
    first_photo_select_button = ['first_photo_select_button','id','cn.com.egova.examine:id/id_item_select']
    photoadd_id = ['photoadd_id','id',"cn.com.egova.examine:id/tool_photoadd"]
    report_btn_id = ['report_btn_id','id',"cn.com.egova.examine:id/base_report_report_btn"]
    media_view_id = ['media_view_id','id',"cn.com.egova.examine:id/media_view"]
    report_desc_id = ['report_desc_id','id',"cn.com.egova.examine:id/base_report_desc"]
    location_desc_id = ['location_desc_id','id',"cn.com.egova.examine:id/location_desc"]
    location_desc_name = ['location_desc_name','name',"选定位置"]
    confirm_name = ['location_desc_name','name',"确定"]
    sub_type_id = ['sub_type_id','id',"cn.com.egova.examine:id/base_report_subtype_spinner"]
    sub_type_name = ['sub_type_name','name',"停车场"]
    main_type_id = ['main_type_id','id',"cn.com.egova.examine:id/base_report_maintype_spinner"]
    main_type_name = ['main_type_name','name',"道路交通"]
    event_type_id = ['event_type_id','id',"cn.com.egova.examine:id/base_report_eventtype_spinner"]
    event_type_name = ['event_type_name','name',"部件"]
    evaluation_task_name = ['evaluation_task_name','name',"考评任务"]

class contactor_Paramter():
    #右上角的+按钮
    actionbar_menuview_image = ['actionbar_menuview_image','id',"cn.com.egova.egovamobile:id/actionbar_menuview_image"]
    start_talk_name = ['start_talk_name','name',"发起聊天"]
    select_contacts_name = ['select_contacts_name','name',"选择联系人"]
    #聊天窗口
    im_chat_steplistview = ['im_chat_steplistview','id',"cn.com.egova.egovamobile:id/im_chat_steplistview"]
    #聊天窗口 - 已读按钮
    msg_unload_right =  ['msg_unload_right','id',"cn.com.egova.egovamobile:id/msg_unload_right"]
    choose_a_part_id = ['choose_a_part_id','id',"cn.com.egova.egovamobile:id/choose_a_part"]
    selet_a_xpath = ['selet_a_xpath','xpath',"//android.widget.ListView[@resource-id='cn.com.egova.egovamobile:id/part_contact_list']/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.CheckBox[1]"]  # 勾选
    selet_b_xpath = ['selet_b_xpath','xpath',"//android.widget.ListView[@resource-id='cn.com.egova.egovamobile:id/part_contact_list']/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/android.widget.CheckBox[1]"]
    contact_confirm_id = ['contact_confirm_id','id',"cn.com.egova.egovamobile:id/choose_part_multi_confirm"]  # 建群确定
    selectemotion_id = ['selectemotion_id','id',"cn.com.egova.egovamobile:id/iv_selectemotion"]  # 表情栏
    emotion_keys_xpath = ['emotion_keys_xpath','xpath',"//android.widget.GridView[@resource-id='cn.com.egova.egovamobile:id/im_emotion_gridview']/android.widget.LinearLayout[4]"]
    btn_send_id = ['btn_send_id','id',"cn.com.egova.egovamobile:id/btn_send"]
    sendmessage_id = ['sendmessage_id','id',"cn.com.egova.egovamobile:id/et_sendmessage"]

    btn_add_id = ['btn_add_id','id',"cn.com.egova.egovamobile:id/btn_add"]
    #拍照按钮
    im_camera_button = ['photo_add_name', 'name', "拍照"]
    #拍照之后的确定按钮
    gallery_sel_confirm = ['gallery_sel_confirm','id',"cn.com.egova.egovamobile:id/gallery_sel_confirm"]
    #聊天--照片发送按钮
    im_photo_button = ['photo_add_name','name',"图片"]
    im_album_button = ['photo_add_name', 'name', "相册"]
    photo_micro_thumb = ['photo_micro_thumb', 'id', "com.miui.gallery:id/micro_thumb"]
    #聊天-联系人
    im_contact_button = ['photo_add_name', 'name', "联系人"]
    #聊天-录音
    btn_voice_id = ['btn_voice_id', 'id', "cn.com.egova.egovamobile:id/btn_voice"]
    im_voicebtn =  ['im_voicebtn', 'id', "cn.com.egova.egovamobile:id/im_voicebtn"]

    chat_add_xpath = ['chat_add_xpath','xpath',"//android.widget.GridView[@resource-id='cn.com.egova.egovamobile:id/id_gridView']/android.widget.RelativeLayout[2]/android.widget.ImageButton[1]"]
    # 第一张图片
    first_photo_select_button = ['first_photo_select_button', 'id', 'cn.com.egova.egovamobile:id/id_item_select']
    select_id = ['select_id','id',"cn.com.egova.egovamobile:id/id_select"]
    confirm_id = ['confirm_id','id',"android:id/button1"]
    exit_id = ['exit_id','id',"android:id/action_bar_title"]
    contact_phone_id = ['contact_phone_id','id',"cn.com.egova.egovamobile:id/contact_phone_view"]  # 点击手机号
    contact_message_id = ['contact_message_id','id',"cn.com.egova.egovamobile:id/contact_message" ] # 点击短信图标

class Owner_Paramter():
    user_name_id = ['user_name_id','id',"cn.com.egova.egovamobile:id/config_item_user_rlt"]  # 用户名
    speed_dial_id = ['speed_dial_id','id',"cn.com.egova.egovamobile:id/config_item_dial_rlt" ] # 单键拨号
    dial_number_id = ['dial_number_id','id',"cn.com.egova.egovamobile:id/txt_dial_number" ] # 单键拨号内的号码设置
    function_manage_id = ['function_manage_id','id',"cn.com.egova.egovamobile:id/config_item_plugin_rlt" ] # 功能管理
    dial_number_exit_name = ['dial_number_exit_name','name',"功能管理"]
    plugin_extend_name = ['plugin_extend_name','name',"安装全部"]
    function_setting_id = ['function_setting_id','id',"cn.com.egova.egovamobile:id/config_item_phrase_rlt"]  # 功能设置
    config_time_id = ['config_time_id','id',"cn.com.egova.egovamobile:id/new_task_config_time" ] # 提醒时间设置
    config_time_keys = ['config_time_keys','name',"5"]  # 提醒时间
    congif_way_id = ['congif_way_id','id',"android:id/text1" ] # 提醒方式
    congif_way_keys = ['congif_way_keys','name',"响铃"]  # 选择提醒方式为响铃
    case_reminder_setting_id = ['case_reminder_setting_id','id',"cn.com.egova.egovamobile:id/config_item_new_task_rlt"]  # 案件提醒设置
    case_reminder_setting = ['case_reminder_setting','name','案件提醒设置']
    phrase_setting_name = ['phrase_setting_name','name',"惯用语设置" ] # 惯用语设置
    add_phrase_id = ['add_phrase_id','id',"cn.com.egova.egovamobile:id/et_phrase"]  # 惯用语输入框
    add_phrase_bt_id = ['add_phrase_bt_id','id',"cn.com.egova.egovamobile:id/bt_phrase_add"]  # 惯用语设置确定按钮
    up_name = ['up_name','name',"功能设置" ] # 退出
    system_support_id = ['system_support_id','id',"cn.com.egova.egovamobile:id/help_item_homepage_rlt" ] # 系统帮助
    traffic_statistics_id = ['traffic_statistics_id','id',"cn.com.egova.egovamobile:id/config_item_traffic_stats_rlt"]  # 流量统计
    clear_cache_id = ['clear_cache_id','id',"cn.com.egova.egovamobile:id/config_item_clearcache_rlt"]  # 清理缓存
    clear_item_name = ['clear_item_name','name',"搜索历史"]
    drop_out_id = ['drop_out_id','id',"cn.com.egova.egovamobile:id/config_item_exit_rlt"]  # 退出
    user_picture_id = ['user_picture_id','id',"cn.com.egova.egovamobile:id/userinfo_icon_row" ] # 头像
    user_tel_id = ['user_tel_id','id',"cn.com.egova.egovamobile:id/userinfo_tel_row"]  # 电话
    user_email_id = ['user_email_id','id',"cn.com.egova.egovamobile:id/userinfo_email_row" ] # 邮箱
    user_gender_id = ['user_gender_id','id',"cn.com.egova.egovamobile:id/userinfo_gender_row" ] # 性别
    user_collect_id = ['user_collect_id','id',"cn.com.egova.egovamobile:id/userinfo_collection_row"]  # 收藏
    user_collect_exit_name = ['user_collect_exit_name','name',"我的收藏"]  # 退出我的收藏
    user_password_id = ['user_password_id','id',"cn.com.egova.egovamobile:id/userinfo_psw_row"]  # 修改密码
    new_tel_id = ['new_tel_id','id',"cn.com.egova.egovamobile:id/userinfo_update_content"]  # 输入新号码
    cance_id = ['cance_id','id',"android:id/button2" ] # 取消
    ok_id = ['ok_id','id', "android:id/button1"]  # 确定
    new_email_id = ['new_email_id','id',"cn.com.egova.egovamobile:id/userinfo_update_content"]  # 输入新邮箱
    new_gender_keys = ['new_gender_keys','name',"女" ] # 性别设置
    psw_old_id = ['psw_old_id','id',"cn.com.egova.egovamobile:id/psw_old" ] # 输入旧密码
    psw_new_id = ['psw_new_id','id',"cn.com.egova.egovamobile:id/psw_new"]  # 新密码
    psw_new_confirm_id = ['psw_new_confirm_id','id',"cn.com.egova.egovamobile:id/psw_new_confirm"]  # 确认新密码
    exit_personal_information = ['exit_personal_information','name',"个人信息"]
    exit_name = ['exit_name','name',"智信"]
    up_id = ['up_id','id',"android:id/up"]
    Exit_name = ['Exit_name','name',"流量统计"]
    report_history_id = ['report_history_id','id',"cn.com.egova.egovamobile:id/config_item_reporthistory_rlt"]
    history_num_id = ['history_num_id','id',"cn.com.egova.egovamobile:id/report_history_num"]
    confirm_name = ['confirm_name','name',"确 定"]

class DisposeCase:
    #案件过滤按钮
    dealhelper_filter_button = ['dealhelper_filter_button','id','cn.com.egova.egovamobile:id/action_filter']
    filter_by_taskNum = ['filter_taskNum','id','cn.com.egova.egovamobile:id/value_et']
    dealhelper_filter_OK_button = ['dealhelper_filter_OK_button', 'id', 'cn.com.egova.egovamobile:id/btn_filter']
    dealhelper_filter_name = ['dealhelper_filter_name', 'name', '过滤']
    #第一条案件
    dealhelper_first_rec1 = ['dealhelper_first_rec','xpath',"//android.widget.ListView[@resource-id='cn.com.egova.dealhelper:id/g_base_list']/android.widget.LinearLayout[1]"]
    dealhelper_first_rec = ['task_num_location','id','cn.com.egova.egovamobile:id/task_list_item_task_num']
    #案件编号区域
    task_num_location = ['task_num_location','id','cn.com.egova.egovamobile:id/task_list_item_task_num']
    dealhelper_back_button = ['dealhelper_back_button','id','android:id/action_bar_title']
    #详情页面--最下方的按钮
    dealhelper_detail_menu = ['dealhelper_detail_menu','id','cn.com.egova.egovamobile:id/task_detail_bottom_menu']
    dealhelper_more_menu = ['dealhelper_more_menu','id','cn.com.egova.egovamobile:id/task_detail_bottom_more_menu']
    #批转按钮 --名称
    transit_action_button = ['transit_action_button', 'name', "批转"]
    #案件操作 描述信息
    rec_operate_desc = ['transit_action_button', 'name', "请输入意见..."]
    #操作页面-提交按钮
    rec_operate_submit = ['rec_operate_submit','id','cn.com.egova.egovamobile:id/title_right']
    #流向第一个 --单选框
    first_transit_button = ['first_transit_button','id','cn.com.egova.egovamobile:id/tree_select_rdb']
    # 流向第一个 -- 复选框
    transit_select_checkbox = ['transit_box_button', 'id', 'cn.com.egova.egovamobile:id/tree_select_checkbox']
    #案件处置 图片-第一张
    dealhelper_first_photo = ['dealhelper_first_photo','id','cn.com.egova.egovamobile:id/id_item_select']
    #案件处置 图片-确认
    dealhelper_add_photo_OK = ['dealhelper_add_photo_OK', 'id', 'cn.com.egova.egovamobile:id/id_select']
    #急要件
    urgency_action = ['urgency_action','name',"设置为急要件"]
    #急要件原因输入框
    urgency_desc = ['urgency_desc','name',"请输入设置急要件的原因"]
    #作废箱子
    invalid_task_list = ['invalid_task_list','name',"作废案件"]
    #发起讨论
    start_discuss_name = ['start_discuss_name','name',"发起讨论"]
    #查看意见
    scan_suggestion_name = ['scan_suggestion_name','name',"查看意见"]
    #作废案件--恢复按钮
    rec_restore_button = ['rec_restore_button', 'name', "恢复"]
    #案件--回退按钮
    rec_rollback_button = ['rec_rollback_button', 'name', "回退"]
    # 案件--回退按钮
    rec_applycancel_button = ['rec_applycancel_button', 'name', "申请作废"]
    #案件--回退--回退意见
    rec_rollback_desc = ['rec_rollback_desc', 'name', "进行回退操作--自动化脚本"]
    #操作的时候是否有添加附件的按钮
    add_attachment_button = "cn.com.egova.dealhelper:id/media_view"
    #案件详情页面-地图按钮
    rec_detail_map_button = ['rec_detail_map_button','id','cn.com.egova.egovamobile:id/task_detail_map_row']
    # 案件详情页面--查看办理进度
    rec_detail_process_button = ['rec_detail_process_button','id','cn.com.egova.egovamobile:id/task_detail_process_row']
    #立案箱子
    newinst_task_list = ['newinst_task_list', 'name', "立案栏"]