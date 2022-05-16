# -*- coding:utf-8 -*-
import sys,importlib
importlib.reload(sys)
sys.path.append("..")
import config,time,copy,json,random
import utils_logging
import utils_database,usefulTools
from tools import switch
from conf import factory_sorting_constant

usefulTools_instances = usefulTools.userfulToolsFactory()

"""
主要用来处理一些db上需要处理的问题
"""

timestr = time.strftime('%Y%m', time.localtime(time.time()))
event_desc = "web auto test rec - " + timestr + "%"

class database_operate():

    # 根据接口ID或是名称获取接口所有的数据信息
    def get_policy_parameters(self,interface_table_name,query_condition=None,query_data=None):
        JobNOId_policy_sql = ''
        if query_condition and query_data:
            #获取需要查询的工卡号ID
            JobNOId_query_sql = 'SELECT JobNOId,PartnerId FROM %(interface_table_name)s WHERE %(query_condition)s %(query_data)s and PartnerId = 10000'
            #获取需要进行单号获取的工卡号ID
            JobNOId_policy_sql = 'SELECT JobNOId,PartnerId FROM %(interface_table_name)s WHERE %(query_condition)s %(query_data)s and PartnerId != 10000'
            JobNOId_param = {'interface_table_name': interface_table_name, 'query_condition': query_condition, 'query_data': query_data}
        else:
            JobNOId_query_sql = 'SELECT * FROM %(interface_table_name)s'
            JobNOId_param = {'interface_table_name': interface_table_name}
        #获取需要进行单号获取的工卡号ID
        JobNOId_policy_list = utils_database.sysBusiness_db_query_all_dict(JobNOId_policy_sql %JobNOId_param)
        JobNOId_policy_id = JobNOId_policy_list[0]['JobNOId']
        # 获取需要查询的工卡号ID
        JobNOId_query_list = utils_database.sysBusiness_db_query_all_dict(JobNOId_query_sql % JobNOId_param)
        JobNOId_query_id = JobNOId_query_list[0]['JobNOId']
        #根据工卡号id 获取单号列表
        InsuranceNo_list_sql = 'SELECT InsuranceNo from insuranceinfo where JobNoId = %(JobNOId_policy_id)s limit 2'
        InsuranceNo_param = {'JobNOId_policy_id': JobNOId_policy_id}
        InsuranceNo_list = utils_database.sysBusiness_db_query_all_dict(InsuranceNo_list_sql %InsuranceNo_param)
        #进行参数处理
        policy_parameters_list = []
        policy_parameters = {}
        for InsuranceNo_item in InsuranceNo_list:
            policy_parameters['no'] = InsuranceNo_item['InsuranceNo']
            policy_parameters['jid'] = JobNOId_query_id
            policy_parameters_data = copy.deepcopy(policy_parameters)
            policy_parameters_list.append(policy_parameters_data)
        message =  policy_parameters_list
        return policy_parameters_list

    # 根据表明和条件获取数据信息
    def sysConfig_get_table_data(self, interface_table_name,query_condition=None,query_data=None):
        limit_num = 1
        if interface_table_name == 'partnerjobno':
            limit_num = 5
        else:
            limit_num = 10
        if query_condition and type(query_condition) == type('str') :
            query_all_sql = 'SELECT * FROM %(interface_table_name)s WHERE %(query_condition)s %(query_data)s ORDER BY UpdateTime DESC LIMIT %(limit_num)s'
            query_all_param = {'interface_table_name': interface_table_name, 'query_condition': query_condition, 'query_data': query_data,'limit_num':limit_num}
            query_all_result = utils_database.sysBusiness_db_query_all_dict(query_all_sql % query_all_param)
            return query_all_result
        if query_condition and query_data:
            query_list = []
            for i in range(len(query_condition)):
                query_list_sql = query_condition[i] + '=' + usefulTools_instances.String_special_handling(query_data[i])
                query_list.append(query_list_sql)
            query_list_str = ' and '.join(query_list)
            query_all_sql = 'SELECT * FROM %(interface_table_name)s WHERE %(query_list_str)s  ORDER BY UpdateTime DESC LIMIT %(limit_num)s'
            query_all_param = {'interface_table_name': interface_table_name,'query_list_str': query_list_str,'limit_num':limit_num}
            query_all_result = utils_database.sysBusiness_db_query_all_dict(query_all_sql % query_all_param)
            return query_all_result
        #不满足上边情况的，直接进行查询
        query_all_sql = 'SELECT * FROM %(interface_table_name)s  ORDER BY UpdateTime DESC LIMIT 5'
        query_all_param = {'interface_table_name': interface_table_name,'limit_num':limit_num}

        query_all_result = utils_database.sysBusiness_db_query_all_dict(query_all_sql % query_all_param)
        return query_all_result

    #获取所有的可用保单信息
    def get_inscommissionpolicy(self,time_dict,PartnerId,JobNoIds):
        #根据日期、PartnerId、JobNoIds 获取可用的 政策信息
        policy_list_ql = 'SELECT * from inscommissionpolicy where StartDate < %(time_infor)s and EndDate > %(time_infor)s and PartnerId = %(PartnerId)s and JobNoIds=%(JobNoIds)s'
        policy_list_CheckDate_param = {'time_infor': usefulTools_instances.String_special_handling(time_dict['CheckDate']),'PartnerId':PartnerId,'JobNoIds':JobNoIds}
        policy_list_PayTime_param = { 'time_infor': usefulTools_instances.String_special_handling(time_dict['PayTime']), 'PartnerId': PartnerId, 'JobNoIds': JobNoIds}
        policy_list_SignDate_param = {'time_infor': usefulTools_instances.String_special_handling(time_dict['SignDate']), 'PartnerId': PartnerId,'JobNoIds': JobNoIds}
        policy_list_CheckDate = utils_database.sysBusiness_db_query_all_dict(policy_list_ql % policy_list_CheckDate_param)
        policy_list_PayTime = utils_database.sysBusiness_db_query_all_dict(policy_list_ql % policy_list_PayTime_param)
        policy_list_SignDate = utils_database.sysBusiness_db_query_all_dict(policy_list_ql % policy_list_SignDate_param)
        policy_number_dict = {'CheckDate':len(policy_list_CheckDate),'PayTime':len(policy_list_PayTime),'SignDate':len(policy_list_SignDate)}
        return policy_number_dict

    #根据保险公司获取所有可用工号
    def get_JobNOId_bySupplierId(self,SupplierId):
        JobNOId_list_sql = 'SELECT JobNOId,LoginName from partnerjobno t where t.SupplierId = %(SupplierId)s  AND t.AreaConfig LIKE "*石家庄*" and t.`Status` = 0 ORDER BY UpdateTime DESC LIMIT 80'
        # JobNOId_list_sql = "SELECT JobNOId from partnerjobno t where t.SupplierId = %(SupplierId)s  AND t.AreaConfig LIKE '%河北%' and t.`Status` = 0 ORDER BY UpdateTime DESC LIMIT 80"
        # JobNOId_list_sql = 'SELECT JobNOId FROM klb_carinfo.inssupplierserviceorg WHERE SupplierId= %(SupplierId)s and IsQuotedPrice =1'
        query_all_param = {'SupplierId':SupplierId}
        JobNOId_list = utils_database.sysBusiness_db_query_all_dict(JobNOId_list_sql %query_all_param)
        message =  JobNOId_list
        return JobNOId_list

    #根据保险公司获取可用的报价工号
    def get_priceJobNOId_bySupplierId(self,SupplierId):
        # JobNOId_list_sql = 'SELECT JobNOId from partnerjobno t where t.SupplierId = %(SupplierId)s LIMIT 80'
        # JobNOId_list_sql = 'SELECT JobNOId FROM klb_carinfo.inssupplierserviceorg WHERE SupplierId= %(SupplierId)s and IsQuotedPrice =1'
        JobNOId_list_sql = 'SELECT a.JobNOId,b.LoginName FROM klb_carinfo.inssupplierserviceorg a,klb_carinfo.partnerjobno b WHERE a.SupplierId= %(SupplierId)s AND b.AreaConfig LIKE "*河北*" and a.IsQuotedPrice =1 AND a.JobNoId = b.JobNOId and b.`Status` = 0;'
        query_all_param = {'SupplierId':SupplierId}
        JobNOId_list = utils_database.sysBusiness_db_query_all_dict(JobNOId_list_sql %query_all_param)
        message =  JobNOId_list
        return JobNOId_list

    #获取登录验证码
    def get_verify_code(self,phone):
        sql = 'SELECT code FROM captchas WHERE phone = %(phone)s ORDER BY id DESC LIMIT 1;'
        param = {'phone': '\'' + phone + '\''}
        result = utils_database.sysBusiness_db_query_all_dict(sql % param,'wechat_api')
        return result

    #获取用户基础信息
    def get_user_infor(self,phone=None):
        if phone:
            sql = 'SELECT * FROM users t WHERE t.phone = %(phone)s'
            param = {'phone': '\'' + phone + '\''}
            result = utils_database.sysBusiness_db_query_all_dict(sql % param,'wechat_api')
        else:
            sql = 'SELECT * FROM users t WHERE t.phone is not NULL ORDER BY t.created_at DESC LIMIT 10'
            result = utils_database.sysBusiness_db_query_all_dict(sql,'wechat_api')
        return result

    #获取充值金额
    def get_recharges_schemes(self,type):
        sql = "SELECT * FROM recharge_schemes t where t.`disable` = 0 and t.type = %(type)s and t.is_show = 1 ORDER BY t.sort"
        param = {'type': type}
        result = utils_database.sysBusiness_db_query_all_dict(sql % param , 'wechat_api')
        return result

    #获取余额明细
    def get_balance_statement(self,user_id,commited):
        sql = "SELECT * FROM recharges t where t.user_id = %(user_id)s and t.commited = %(commited)s ORDER BY t.created_at DESC;"
        param = {'user_id': user_id,'commited':commited}
        result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'wechat_api')
        return result

    # 更新人员表的数据（为提现准备）
    def update_user_infor(self, phone, real_balance,gift_balance,balance):
        sql = "UPDATE users t SET t.real_balance = %(real_balance)s,t.gift_balance =%(gift_balance)s,t.balance = %(balance)s where t.phone = %(phone)s;"
        param = {'phone': '\'' + phone + '\'','real_balance':real_balance,'gift_balance':gift_balance,'balance':balance}
        result = utils_database.sysBusiness_db_update(sql % param, 'wechat_api')
        return result

    #更新提现记录表，删除已有的提现记录
    def delete_balance_to_cash(self,user_id):
        sql = "DELETE FROM balance_to_cash where user_id = %(user_id)s;"
        param = {'user_id': user_id}
        result = utils_database.sysBusiness_db_update(sql % param, 'wechat_api')
        return result

    # 获取提现记录
    def get_balance_to_cash(self, user_id):
        sql = "SELECT * FROM balance_to_cash t where t.user_id = %(user_id)s;"
        param = {'user_id': user_id}
        result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'wechat_api')
        return result

    #获取干洗柜
    def get_neighbourCabinets(self,latitude,longitude,keyword):
        # sql = "select round((3959 * acos(cos(radians(%(latitude)s)) * cos(radians(c.latitude)) * cos(radians(c.longitude)- radians(%(longitude)s)) + sin(radians(%(latitude)s)) * sin(radians(c.latitude))))*1000,0) as distance,c.* from cabinet_iot.cabinet c where c.status = 1 and c.name like '&&%(keyword)s&&' having distance <= 3000 order by distance ASC"
        sql = 'select id,city,name,latitude,longitude,number,address,status,round(((acos(sin( ( %(latitude)s * pi( ) / 180 ) ) * sin( ( `latitude` * pi( ) / 180 ) ) + cos( ( %(latitude)s * pi( ) / 180 ) ) * cos( ( `latitude` * pi( ) / 180 ) ) * cos( ( ( %(longitude)s - `longitude` ) * pi( ) / 180 ) ))) * 180 / pi( )) * 60 * 1.1515 * 1.609344,2) AS distance from cabinet where status = 1 order by distance asc'
        param = {'latitude': latitude,'longitude': longitude,'keyword':keyword}
        result = utils_database.sysBusiness_db_query_all_dict(sql %param, 'cabinet_iot')
        return result

    # 获取附近洗衣点
    def get_nearby_building_list(self, latitude, longitude):
        sql = "select round((3959 * acos(cos(radians(%(latitude)s)) * cos(radians(b.latitude)) * cos(radians(b.longitude)- radians(%(longitude)s)) + sin(radians(%(latitude)s)) * sin(radians(b.latitude))))*1000,0) as distance,b.longitude,b.latitude,b.id as building_id,b.name as building_name,count(w.id) as device_count from `washers` as `w` inner join `buildings` as `b` on `b`.`id` = `w`.`building_id` where (`father_id` = 0 and `is_down` = 0 and `is_online` = 1) and b.name like '&&1&&' group by `building_id` having distance <= 3000 order by distance ASC"
        param = {'latitude': latitude, 'longitude': longitude}
        result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'washer_service')
        return result

    #获取有评论的商品列表
    def get_goodsId_withComments(self,comment_num):
        sql = "SELECT COUNT(goods_id) as comment_num,goods_id FROM order_score t where t.goods_id in(SELECT goods_id FROM goods_activity ) GROUP BY t.goods_id having comment_num>%(comment_num)s;"
        param = {'comment_num': comment_num}
        result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'cabinet_api')
        return result

    # 获取商品购买记录数量
    def get_goodsId_withPurchase(self, count):
        sql = "SELECT COUNT(*) as count,goods_id,t.activity_id FROM purchasing_records t GROUP BY t.goods_id having count > %(count)s;"
        param = {'count': count}
        result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'cabinet_api')
        return result

    # 获取洗衣设备、building相关的数据
    def get_building_list(self):
        sql = "SELECT DISTINCT building_id FROM washers t, buildings b where t.is_down = 0 and t.is_online =1 and t.father_id = 0 and t.building_id = b.id ORDER BY t.created_at DESC LIMIT 100;"
        # param = {'user_id': user_id}
        result = utils_database.sysBusiness_db_query_all_dict(sql, 'washer_service')
        return result

    # 从cabinet_api.orders中获取所有的退款数据
    def get_refund_order_list(self,user_id):
        sql = "SELECT * FROM cabinet_api.orders t where t.user_id =  %(user_id)s and t.pay_status = 1 and (t.status =-1 or t.status =-2 or (t.balance_price <=0 and t.balance_status=1)) ORDER BY t.updated_at DESC;"
        param = {'user_id': user_id}
        result = utils_database.sysBusiness_db_query_all_dict(sql %param, 'washer_service')
        return result

    #从washers表获取需要的数据
    def get_washers_list(self,building_id,is_down,is_online,father_id,floor=None):
        sql_order = "ORDER BY t.created_at DESC"
        org_id_list = 'SELECT id FROM washer_service.organizations t where t.allow_alipay =1 and t.allow_recharge = 1 and t.allow_wechat_pay = 1'
        if floor:
            sql = "SELECT * FROM washer_service.washers t where t.building_id = %(building_id)s and t.is_down = %(is_down)s and t.is_online =%(is_online)s and t.father_id = %(father_id)s AND floor = %(floor)s AND t.status = 0 AND t.org_id in (%(org_id_list)s)"
            sql = sql + ' ' + sql_order
            param = {'building_id': building_id, 'is_down': is_down, 'is_online': is_online, 'father_id': father_id, 'floor': floor,'org_id_list':org_id_list}
            result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'washer_service')
        else:
            sql = "SELECT * FROM washer_service.washers t where t.building_id = %(building_id)s and t.is_down = %(is_down)s and t.is_online =%(is_online)s and t.father_id = %(father_id)s AND t.status = 0 AND t.org_id in (%(org_id_list)s)"
            sql = sql + ' ' + sql_order
            param = {'building_id': building_id,'is_down':is_down,'is_online':is_online,'father_id':father_id,'org_id_list':org_id_list}
            result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'washer_service')
        return result

    # 从washers表获取需要的数据
    def get_washers_list_all(self, building_id, is_down, is_online, father_id, floor=None):
        sql_order = "ORDER BY t.created_at DESC"
        if floor:
            sql = "SELECT * FROM washer_service.washers t where t.building_id = %(building_id)s and t.is_down = %(is_down)s and t.is_online =%(is_online)s and t.father_id = %(father_id)s AND floor = %(floor)s"
            sql = sql + ' ' + sql_order
            param = {'building_id': building_id, 'is_down': is_down, 'is_online': is_online,'father_id': father_id, 'floor': floor}
            result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'washer_service')
        else:
            sql = "SELECT * FROM washer_service.washers t where t.building_id = %(building_id)s and t.is_down = %(is_down)s and t.is_online =%(is_online)s and t.father_id = %(father_id)s"
            sql = sql + ' ' + sql_order
            param = {'building_id': building_id, 'is_down': is_down, 'is_online': is_online,'father_id': father_id}
            result = utils_database.sysBusiness_db_query_all_dict(sql % param, 'washer_service')

        return result

    #从washers表获取数据，根据传入的参数自动匹配组合
    def get_washers_all(self,param_list):
        sql_base = "SELECT * FROM washer_service.washers t where "
        sql_last = "ORDER BY t.created_at DESC LIMIT 100;"

    #从services表获取数据
    def get_servers_list(self,param_list):
        sql_base = "SELECT * FROM washer_service.services t where "
        # sql_last = "ORDER BY t.created_at DESC LIMIT 100;"
        sql_last = "ORDER BY t.sort"
        sql = ''
        for i in range(len(param_list)):
            sql = sql_base + 't.' + param_list[i]['field_name'] + param_list[i]['filed_concatenation'] + '\'' + str(param_list[i]['field_value']) + '\'' + ' '
        sql = sql + sql_last
        result = utils_database.sysBusiness_db_query_all_dict(sql, 'washer_service')
        return result

    #从 orders 表获取数据
    def get_orders_list(self,param_list,limit=None):
        sql = "SELECT * FROM wechat_api.orders t "
        sql_last = "ORDER BY t.created_at DESC "
        sql_limit = 'LIMIT '
        if len(param_list) > 0:
            sql = sql + 'where' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + str(param_list[i]['field_value']) + ' '
            if i < len(param_list) -1:
                sql = sql + 'and' + ' '
        sql = sql + sql_last
        if limit:
            sql = sql + sql_limit + str(limit) + ';'
        result = utils_database.sysBusiness_db_query_all_dict(sql, 'wechat_api')
        return result

    # 从 orders 表获取数据
    def get_payments_list(self, param_list):
        sql = "SELECT * FROM wechat_api.payments t "
        sql_last = "ORDER BY t.created_at DESC LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'where' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + '\''+param_list[i]['field_value']+'\'' + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        # sql = sql + sql_last
        result = utils_database.sysBusiness_db_query_all_dict(sql, 'wechat_api')
        return result

    # 从 delivery_payments 表获取数据
    def get_delivery_payments_list(self, param_list):
        sql = "SELECT * FROM wechat_api.delivery_payments t "
        sql_last = "ORDER BY t.created_at DESC LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'where' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + str(
                param_list[i]['field_value']) + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        # sql = sql + sql_last
        result = utils_database.sysBusiness_db_query_all_dict(sql, 'wechat_api')
        return result

    # 从 refunds 表获取数据
    def get_refunds_list(self, param_list):
        sql = "SELECT * FROM wechat_api.refunds t "
        sql_order = "ORDER BY t.created_at DESC"
        sql_limit = "LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'where' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + str(
                param_list[i]['field_value']) + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        sql = sql + sql_order
        result = utils_database.sysBusiness_db_query_all_dict(sql, 'wechat_api')
        return result

    # 更新数据，单字段的更新
    def update_table_data_sigle(self,db_name,table_name,field_name,field_value,param_list):
        sql = "UPDATE %(db_name)s.%(table_name)s t SET %(field_name)s = %(field_value)s "
        sql_order = "ORDER BY t.created_at DESC"
        sql_limit = "LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'where' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + str(
                param_list[i]['field_value']) + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        param = {'db_name': db_name,'table_name':table_name,'field_name':field_name,'field_value':field_value}
        # sql = sql + sql_order
        result = utils_database.sysBusiness_db_update(sql %param, 'wechat_api')
        return result

    # 单表获取数据，
    def get_table_data_sigle(self,db_name,table_name,sort_type,param_list,limit = None):
        sql = "SELECT * FROM %(db_name)s.%(table_name)s t "
        sql_order = "ORDER BY t.%(sort_type)s DESC,id "
        sql_limit = "LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'WHERE' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + str(param_list[i]['field_value']) + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        param = {'db_name': db_name,'table_name':table_name,'sort_type':sort_type}
        # sql = sql + sql_order + sql_limit
        sql = sql + sql_order
        if limit is not None:
            sql = sql + sql_limit
        # message =  sql
        result = utils_database.sysBusiness_db_query_all_dict(sql %param, db_name)
        return result

    # 单表数量获取，
    def get_table_data_sum(self, db_name, table_name, sort_type, param_list):
        sql = "SELECT COUNT(*) AS tab_sum FROM %(db_name)s.%(table_name)s t "
        sql_order = "ORDER BY t.%(sort_type)s DESC "
        sql_limit = "LIMIT 100;"
        if len(param_list) > 0:
            sql = sql + 'WHERE' + ' '
        # sql_last = "ORDER BY t.sort"
        for i in range(len(param_list)):
            sql = sql + 't.' + param_list[i]['field_name'] + ' ' + param_list[i]['filed_concatenation'] + ' ' + str(
                param_list[i]['field_value']) + ' '
            if i < len(param_list) - 1:
                sql = sql + 'and' + ' '
        param = {'db_name': db_name, 'table_name': table_name, 'sort_type': sort_type}
        sql = sql + sql_order + sql_limit
        # message =  sql
        result = utils_database.sysBusiness_db_query_all_dict(sql % param, db_name)
        return result

    #获取需要的优惠券数据
    def get_coupon_list(self,coupon_type_text,coupon_type,price):
        # 先获取可用的通用优惠券
        timestr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        coupon_list = []
        db_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': '1'},
            {'field_name': 'user_max_number', 'filed_concatenation': '=', 'field_value': '0'},
            {'field_name': 'stock', 'filed_concatenation': '=', 'field_value': '0'},
            {'field_name': 'is_delete=0 and (end_time', 'filed_concatenation': '>', 'field_value': '\'' + timestr + '\' or t.time_type =2)'},
        ]
        table_name = 'delivery_coupon'
        for coupon_used_type_name in switch.basic_switch(coupon_type_text):
            if coupon_used_type_name('self'):
                table_name = 'coupon'
            if coupon_used_type_name('common'):
                condition = {'field_name': 'coupon_type_text', 'filed_concatenation': '=', 'field_value': '0'}
                db_param.append(condition)
            if coupon_used_type_name('delivery'):
                condition = {'field_name': 'coupon_type_text', 'filed_concatenation': '=', 'field_value': '1'}
                db_param.append(condition)
        if coupon_type != '':
            coupon_type_condition = {'field_name': 'coupon_type', 'filed_concatenation': '=', 'field_value': coupon_type}
            db_param.append(coupon_type_condition)
        if price != '':
            price_condition = {'field_name': 'min_money', 'filed_concatenation': '>', 'field_value':price}
            db_param.append(price_condition)
        message =  u'从“delivery_coupon”获取所有的正常优惠券'
        coupon_list = self.get_table_data_sigle('wechat_api', table_name,'created_time', db_param)
        # 从2个列表中进行规整可用的数据
        coupon_code_param_list = []
        coupon_code_param = {}
        for i in range(len(coupon_list)):
            coupon_code_param['coupon_id'] = ''
            coupon_code_param['delivery_coupon_id'] = ''
            coupon_code_param['common_coupon_id'] = ''
            for coupon_type_text in switch.basic_switch(coupon_list[i]['coupon_type_text']):
                if coupon_type_text(0):
                    coupon_code_param['common_coupon_id'] = coupon_list[i]['id']
                if coupon_type_text(1):
                    coupon_code_param['delivery_coupon_id'] = coupon_list[i]['id']
                if coupon_type_text(2):
                    coupon_code_param['coupon_id'] = coupon_list[i]['id']
                coupon_code_param['id'] = coupon_list[i]['id']
                coupon_code_param['min_money'] = str(coupon_list[i]['min_money'])
                coupon_code_param['coupon_type'] = coupon_list[i]['coupon_type']
                coupon_code_param['coupon_type_text'] = coupon_list[i]['coupon_type_text']
                coupon_code_param['start_time'] = coupon_list[i]['start_time'].strftime('%Y-%m-%d')
                coupon_code_param['end_time'] = coupon_list[i]['start_time'].strftime('%Y-%m-%d')
            coupon_code_param['coupon_head'] = coupon_list[i]['coupon_head']
            coupon_code_param_bak = copy.deepcopy(coupon_code_param)
            coupon_code_param_list.append(coupon_code_param_bak)
            message =  json.dumps(coupon_code_param).decode('unicode_escape')
        return coupon_code_param_list

    #根据需要获取干洗商品信息
    def get_goodInfor_accordingNeed(self,good_typ,good_status,user_status):
        #good_type:单件洗:goods,活动：activity
        #good_status：online、offline、delete
        table_name = 'goods'
        order_type = 'price'
        db_param =[]
        good_list = []
        for good_typ in switch.basic_switch(good_typ):
            if good_typ('goods'):
                db_param = [
                    {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
                    {'field_name': 'cate_id', 'filed_concatenation': 'in', 'field_value': '(SELECT id FROM goods_category where type = 0)'},
                ]
            if good_typ('activity'):
                table_name = 'goods_activity'
                db_param = [
                    {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
                    {'field_name': 'order_type', 'filed_concatenation': '=', 'field_value': '0'},
                    {'field_name': 'activity_type', 'filed_concatenation': '=', 'field_value': '2'},
                    {'field_name': 'goods_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods where status=1 and deleted_at is NULL)'},
                ]
                order_type = 'activity_price'
        for good_status in switch.basic_switch(good_status):
            if good_status('online'):
                online_condition = {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 1}
                db_param.append(online_condition)
            if good_status('offline'):
                offline_condition = {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 0}
                db_param.append(offline_condition)
            if good_status('delete'):
                db_param.pop(0)
                delete_condition = {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NOT NULL'}
                db_param.append(delete_condition)
        for user_status in switch.basic_switch(user_status):
            if user_status('new'):
                new_condition = {'field_name': 'activity_type', 'filed_concatenation': '=', 'field_value': 1}
                db_param.append(new_condition)
            if user_status('old'):
                new_condition = {'field_name': 'activity_type', 'filed_concatenation': '=', 'field_value': 2}
                db_param.append(new_condition)
        # order_type = 'price' if good_typ == 'goods' else 'activity_price'
        good_list = self.get_table_data_sigle('cabinet_api', table_name, order_type,db_param)
        good_list.reverse()
        return good_list

    #根据需求获取订单列表
    def get_deliveryOrder_accroding_request(self,good_type,order_infor):
        # good_type:单件洗：goods，活动：activity
        # order_status：字典表：{'status':0,'pay_status':0,'user_id':0,'goods_activity_id':0,'goods_id':0},订单状态+支付状态
        db_param = [
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': order_infor['user_id']},
            {'field_name': 'status', 'filed_concatenation': '=','field_value': order_infor['status']},
            {'field_name': 'pay_status', 'filed_concatenation': '=', 'field_value': order_infor['pay_status']},
        ]
        if order_infor['goods_activity_id'] != '':
            activity_id_detail = '(SELECT order_id FROM order_detail where goods_activity_id = '+ str(order_infor['goods_activity_id']) + ')'
            activity_id_condition = {'field_name': 'id', 'filed_concatenation': 'in', 'field_value': activity_id_detail}
            db_param.append(activity_id_condition)
        if order_infor['goods_id'] != '':
            goods_detail = '(SELECT order_id FROM order_detail where goods_id = '+ str(order_infor['goods_id']) + ')'
            goods_condition = {'field_name': 'id', 'filed_concatenation': 'in', 'field_value': goods_detail}
            db_param.append(goods_condition)
        if good_type == 'activity' and order_infor['goods_activity_id'] == '':
            activity_detail = '(SELECT order_id FROM order_detail where goods_activity_id is not NULL )'
            activity_condition = {'field_name': 'id', 'filed_concatenation': 'in', 'field_value': activity_detail}
            db_param.append(activity_condition)
        if good_type == 'goods' and order_infor['goods_id'] == '':
            goods_detail = '(SELECT order_id FROM order_detail where goods_activity_id is NULL )'
            goods_condition = {'field_name': 'id', 'filed_concatenation': 'in', 'field_value': goods_detail}
            db_param.append(goods_condition)
        order_list = self.get_table_data_sigle('cabinet_api', 'orders', 'created_at', db_param)
        return order_list

    # 根据订单ID获取需要创建的衣服信息
    def get_clothes_accord_order(self,receiptId,orderId,balance_status,risk):
        goods_price_list = []
        shop_service_list = []
        clothes_param_list = []
        #根据orderId 获取到当前order的goods信息
        db_param = [
            {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': orderId},
        ]
        order_detail_list = self.get_table_data_sigle('cabinet_api', 'order_detail', 'created_at', db_param)
        for i in range(len(order_detail_list)):
            goods_price_list.append(float(order_detail_list[i]['goods_price']))
        goods_price_list.sort()
        #根据是否需要补费进行shop_service数据获取
        for balance_status in switch.basic_switch(balance_status):
            if balance_status('above'):
                db_param = [
                    {'field_name': 'price', 'filed_concatenation': '<', 'field_value': goods_price_list[0]},
                    {'field_name': 'price', 'filed_concatenation': '>', 'field_value': 0},
                ]
                # shop_service_list = self.get_table_data_sigle('delivery_api', 'shop_service', 'id', db_param)
            if balance_status('below'):
                db_param = [
                    {'field_name': 'price', 'filed_concatenation': '>', 'field_value': goods_price_list[len(goods_price_list)-1]},
                ]
                # shop_service_list = self.get_table_data_sigle('delivery_api', 'shop_service', 'id', db_param)
            if balance_status(''):
                db_param = [
                    {'field_name': 'price', 'filed_concatenation': '=', 'field_value': goods_price_list[len(goods_price_list)-1]},
                ]
        shop_service_list = self.get_table_data_sigle('cabinet_api', 'shop_service', 'price', db_param)
        #进行color、defect 获取
        color_list = self.get_table_data_sigle('cabinet_api', 'factory_color', 'id', [])
        defect_list = self.get_table_data_sigle('cabinet_api', 'factory_color', 'id', [])
        db_param = [
                    {'field_name': 'price', 'filed_concatenation': '=', 'field_value': 0},
                ]
        clothes_parts_list = self.get_table_data_sigle('cabinet_api', 'shop_service', 'id', db_param)
        #添加需要洗的衣物进去
        for clothe_id in range(len(goods_price_list)):
            #检查shop_service_list是否为空，为空则为不需要进行退补费的情况
            if len(shop_service_list) == 0:
                db_param = [
                    {'field_name': 'price', 'filed_concatenation': '=', 'field_value': goods_price_list[clothe_id]},
                ]
                shop_service_list = self.get_table_data_sigle('cabinet_api', 'shop_service', 'id', db_param)
            clothes_param_infor = {}
            service_random = random.randint(0,len(shop_service_list)-1)
            color_random = random.randint(0,len(color_list)-1)
            defect_random = random.randint(0,len(defect_list)-1)
            clothes_param_infor['factoryPic'] = ''
            clothes_param_infor['shopServiceId'] = shop_service_list[service_random]['id']
            clothes_param_infor['colorId'] = color_list[color_random]['id']
            clothes_param_infor['defectIds'] = defect_list[defect_random]['id']
            clothes_param_infor['needWash'] = 1
            clothes_param_infor['parentClothesId'] = ''
            clothes_param_infor['isParts'] = ''
            clothes_param_infor['washRisk'] = 0
            clothes_param_infor['showRisk'] = ''
            if risk !='':
                clothes_param_infor['washRisk'] = 1
                clothes_param_infor['showRisk'] = factory_sorting_constant.common_parameter.risk_list[random.randint(0,4)]
            clothes_param_infor_bak = copy.deepcopy(clothes_param_infor)
            clothes_param_list.append(clothes_param_infor_bak)
        #添加需要洗的衣物进去
        for clothe_id in range(len(goods_price_list)):
            #检查shop_service_list是否为空，为空则为不需要进行退补费的情况
            clothes_param_infor = {}
            service_random = random.randint(0,len(clothes_parts_list)-1)
            color_random = random.randint(0,len(color_list)-1)
            defect_random = random.randint(0,len(defect_list)-1)
            clothes_param_infor['factoryPic'] = ''
            clothes_param_infor['shopServiceId'] = clothes_parts_list[service_random]['id']
            clothes_param_infor['colorId'] = color_list[color_random]['id']
            clothes_param_infor['defectIds'] = defect_list[defect_random]['id']
            clothes_param_infor['needWash'] = 1
            clothes_param_infor['parentClothesId'] = ''
            clothes_param_infor['isParts'] = 1
            clothes_param_infor['washRisk'] = 0
            clothes_param_infor['showRisk'] = ''
            clothes_param_infor['washRisk'] = ''
            clothes_param_infor['showRisk'] = ''
            clothes_param_infor_bak = copy.deepcopy(clothes_param_infor)
            clothes_param_list.append(clothes_param_infor_bak)
        #返回可进行创建衣服的列表
        return clothes_param_list

    #获取所有的封签码
    def get_sealNumber_rfId(self):
        db_list = self.get_table_data_sigle('backend_api', 'seal_number', 'id', [],100)
        rfId_list = []
        for i in range(len(db_list)):
            db_param = [
                {'field_name': 'source_number', 'filed_concatenation': '=', 'field_value': db_list[i]['number']},
            ]
            factory_receipt_list = self.get_table_data_sigle('cabinet_api', 'factory_receipt', 'id', db_param,100)
            if len(factory_receipt_list)>0 and factory_receipt_list[0]['status'] in ('CREATED','ARRIVED_FACTORY'):
                continue
            rfId_list.append(db_list[i]['number'])
            if len(rfId_list) > 20:
                return rfId_list
        return rfId_list

    #根据需求获取订单
    def get_risk_repeat_order(self,order_condition,order_status,risk_repeat_status):
        #risk_repeat_status={risk_confirm_status:'',repeat_status:''}订单的实际状态
        riskRepeat_order_list = []
        #根据需求进行订单列表获取
        db_param = [
            {'field_name': 'status', 'filed_concatenation': '=', 'field_value': order_status['status']},
            {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': order_condition['user_id']},
            {'field_name': 'repeat_wash_status', 'filed_concatenation': '=', 'field_value': 0},
        ]
        order_list = self.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
        for i in range(len(order_list)):
            #获取订单的 衣物信息
            receipt_id = 'SELECT id FROM factory_receipt t where t.order_id = ' + str(order_list[i]['id'])
            db_param = [
                {'field_name': 'receipt_id', 'filed_concatenation': 'in', 'field_value': '('+str(receipt_id)+')'},
            ]
            if order_status['risk'] != '':
                risk_status = {'field_name': 'wash_risk', 'filed_concatenation': '=', 'field_value': order_status['risk']}
                db_param.append(risk_status)
            if risk_repeat_status['risk_confirm_status'] != '':
                risk_confirm_status = {'field_name': 'wash_risk_confirm_status', 'filed_concatenation': '=', 'field_value': risk_repeat_status['risk_confirm_status']}
                db_param.append(risk_confirm_status)
            if risk_repeat_status['repeat_status'] != '':
                repeat_status = {'field_name': 'applied_repeat_wash', 'filed_concatenation': '=', 'field_value': risk_repeat_status['repeat_status']}
                db_param.append(repeat_status)
            order_clothes_list = self.get_table_data_sigle('cabinet_api', 'factory_order_clothes', 'id', db_param)
            if len(order_clothes_list) == 0:
                continue
            db_param = [
                {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[i]['id']},
            ]
            orders_status_process = self.get_table_data_sigle('cabinet_api', 'orders_status_process','id', db_param)
            for j in range(len(order_clothes_list)):
                order_clothes_list[j]['order_number'] = order_list[i]['number']
                order_clothes_list[j]['order_id'] = order_list[i]['id']
            if order_status['orders_status_process'] == '':
                return order_clothes_list
            if orders_status_process[0]['status'] == order_status['orders_status_process']:
                return order_clothes_list
        return []
        #未获取到订单，则进行订单创建

    # 根据需求获取需要反洗/风险确认的订单数据
    def get_risk_repeat_clothes(self, order_status, risk_repeat_status,order_number):
        # risk_repeat_status={risk_confirm_status:'',repeat_status:''}订单的实际状态
        riskRepeat_order_list = []
        order_clothes_list = []
        # 根据需求进行订单列表获取
        db_param = [
            {'field_name': 'number', 'filed_concatenation': '=', 'field_value': order_number},
            {'field_name': 'repeat_wash_status', 'filed_concatenation': '=', 'field_value': 0},
        ]
        order_list = self.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
        for i in range(len(order_list)):
            # 获取订单的 衣物信息
            receipt_id = 'SELECT id FROM factory_receipt t where t.order_id = ' + str(order_list[i]['id'])
            db_param = [
                {'field_name': 'receipt_id', 'filed_concatenation': 'in',
                 'field_value': '(' + str(receipt_id) + ')'},
            ]
            if order_status['risk'] != '':
                risk_status = {'field_name': 'wash_risk', 'filed_concatenation': '=','field_value': order_status['risk']}
                db_param.append(risk_status)
            if risk_repeat_status['risk_confirm_status'] != '':
                risk_confirm_status = {'field_name': 'wash_risk_confirm_status', 'filed_concatenation': '=', 'field_value': risk_repeat_status['risk_confirm_status']}
                db_param.append(risk_confirm_status)
            if risk_repeat_status['repeat_status'] != '':
                repeat_status = {'field_name': 'applied_repeat_wash', 'filed_concatenation': '=','field_value': risk_repeat_status['repeat_status']}
                db_param.append(repeat_status)
            order_clothes_list = self.get_table_data_sigle('cabinet_api', 'factory_order_clothes', 'id', db_param)
            if len(order_clothes_list) == 0:
                continue
            db_param = [
                {'field_name': 'order_id', 'filed_concatenation': '=', 'field_value': order_list[i]['id']},
            ]
            orders_status_process = self.get_table_data_sigle('cabinet_api', 'orders_status_process', 'id',db_param)
            for j in range(len(order_clothes_list)):
                order_clothes_list[j]['order_number'] = order_list[i]['number']
                order_clothes_list[j]['order_id'] = order_list[i]['id']
        return order_clothes_list


    #根据需求更新用户信息
    def update_user_balance(self,user_infor,pay_type,payPrice):
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
        self.update_user_infor(user_infor['phone'],real_balance,gift_balance,real_balance+gift_balance)

    #计算实际衣物价格
    def count_clother_price(self,receiptId):
        message =  u'计算所有衣物的总价'
        real_price = 0
        db_param = [
            {'field_name': 'receipt_id', 'filed_concatenation': '=', 'field_value': receiptId},
        ]
        clother_list = self.get_table_data_sigle('cabinet_api', 'factory_order_clothes', 'id',db_param)
        for i in range(len(clother_list)):
            real_price = real_price + float(clother_list[i]['price'])
        real_price = float('%.2f' % real_price)
        return real_price

    #计算实际衣物价格，主要用于未上挂的订单校验
    def count_clother_realPrice(self,receiptId):
        message =  u'计算所有衣物的总价'
        real_price = 0
        db_param = [
            {'field_name': 'receipt_id', 'filed_concatenation': '=', 'field_value': receiptId},
            {'field_name': 'wash_risk_confirm_status', 'filed_concatenation': 'in', 'field_value': '(0,1)'},
        ]
        clother_list = self.get_table_data_sigle('cabinet_api', 'factory_order_clothes', 'id',db_param)
        for i in range(len(clother_list)):
            real_price = real_price + float(clother_list[i]['price'])
        real_price = float('%.2f' % real_price)
        return real_price

    #获取格子所有的衣物信息
    def get_cabinet_clothes(self,cabinet_id):
        code_list = []
        db_param = [
            {'field_name': 'cabinet_id', 'filed_concatenation': '=', 'field_value': cabinet_id},
            {'field_name': 'type', 'filed_concatenation': '!=', 'field_value': 2},
        ]
        cabinet_code_list = self.get_table_data_sigle('cabinet_iot', 'cabinet_code', 'id', db_param)
        for i in range(len(cabinet_code_list)):
            order_id = 'SELECT order_id FROM cabinet_iot.cargo where id = '+str(cabinet_code_list[i]['cargo_id'])
            db_param = [
                {'field_name': 'id', 'filed_concatenation': 'in', 'field_value': '('+order_id+')'},
            ]
            order_list = self.get_table_data_sigle('cabinet_api', 'orders', 'id', db_param)
            order_status_list = self.get_table_data_sigle('cabinet_api', 'orders_status_process', 'id', db_param)
            cabinet_code_list[i]['order_number'] = order_list[0]['number']
            cabinet_code_list[i]['order_id'] = order_list[0]['id']
            cabinet_code_list[i]['order_status'] = order_status_list[0]['status']
            code_list.append(cabinet_code_list[i])
        return code_list






if __name__ == '__main__':
    message =  "utils test"
    database_operate_instances = database_operate()
    database_operate_instances.get_sealNumber_rfId()
    # database_operate_instances.update_user_infor('18212341234',111,222,333)
    time_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    test_list = [1,2,3]
    message =  str(test_list)
    number = '5561819889360486400'
    db_param = [
                {'field_name': 'number', 'filed_concatenation': '=', 'field_value': '\'' + number + '\''},
                {'field_name': 'created_at', 'filed_concatenation': 'like', 'field_value':  '\'&&' + time_data + '&&\''},
                {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': '937290'},
                # {'field_name': 'paid_at', 'filed_concatenation': '!=', 'field_value': '\'' + '' + '\''},
                ]
    db_param = [
        {'field_name': 'user_id', 'filed_concatenation': '=', 'field_value': 8},
        {'field_name': 'status', 'filed_concatenation': '=', 'field_value': '-1 or t.balance_price <0'},
    ]
    goods_online_param = [
        {'field_name': 'status', 'filed_concatenation': '=', 'field_value': 1},
        {'field_name': 'cate_id', 'filed_concatenation': 'in','field_value': '(SELECT id FROM goods_category where type = 0)'},
        {'field_name': 'deleted_at', 'filed_concatenation': 'is', 'field_value': 'NULL'},
    ]
    # database_operate_instances.get_servers_list(db_param)
    # test_list = database_operate_instances.update_table_data_sigle('wechat_api','orders','state',3,db_param)
    # test_list = database_operate_instances.get_table_data_sigle('cabinet_api','goods','created_at',goods_online_param)
    # test_list = database_operate_instances.get_building_list()
    # test_list = database_operate_instances.get_goodInfor_accordingNeed('activity','delete','')
    message =  random.randint(0,0)
    test_list = database_operate_instances.get_coupon_list('common','0','100')
    message =  test_list
    # message =  user_list[0]['paid_at']
    # str123 = '3.0.2'
    # message =  str(int(str123[:1])+1)+str123[1:]

