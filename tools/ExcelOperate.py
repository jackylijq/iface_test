#coding=utf-8
import unittest
import os
import sys
import time
import  random
from xlwt import *
import xlrd
from xlutils.copy import copy
import xlwt
# from Tools import resultOprate
import settings

class format_setting():
    borders = Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    font_green = xlwt.Font()
    font_green.name = 'Times New Roman'
    font_green.colour_index = 3
    font_green.bold = True

    style_green = xlwt.XFStyle()
    style_green.font = font_green
    style_green.borders = borders

    font_red = xlwt.Font()
    font_red.name = 'Times New Roman'
    font_red.colour_index = 2
    font_red.bold = True

    style_red = xlwt.XFStyle()
    style_red.font = font_red
    style_red.borders = borders

    style_frame = xlwt.XFStyle()
    style_frame.borders = borders

class excel_Operate():
    def create_excel(self):
        excel_path = 'd://'
        excel_name_base = 'test-'
        timestr = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 本地日期时间作为测试报告的名字
        randomStr = str(random.uniform(5, 500))
        excel_name = excel_path + excel_name_base + timestr + randomStr + '.csv'
        message =  'excel_name is '+ str(excel_name)
        excel_file = Workbook(encoding='utf-8')
        ws = excel_file.add_sheet("result")

        excel_file.save(excel_name)
        return  excel_name

    def excel_context_op(self,file_name,rowIndex,newValue):

        date_src = xlrd.open_workbook(file_name)
        date_location = copy(date_src)

        newValueLen = len(newValue)
        message = 'newValueLen='+str(newValueLen)
        for colIndex in range (0,newValueLen,1):
            # print 'cloinex = '+str(cloinex)
            # print newValue[cloinex]
            date_location.get_sheet(0).write(rowIndex, colIndex, newValue[colIndex])
        date_location.save(file_name)

        return  0

    def CaseDataOpreate(self,file_name):
        #打开excel表格，读取内容
        date_src = xlrd.open_workbook(file_name)
        #获取一个sheet的内容
        case_table = date_src.sheet_by_index(0)
        #获取excel表的行数和列数
        case_table_nrows = case_table.nrows
        case_table_nclos = case_table.ncols
        #定义一个变量，用来接收需要执行的case数据
        case_list = []
        #循环从用来的excel取数据，并进行判断是否可以执行，可执行，则放入list中
        for caseId in range(case_table_nrows):
            table_vale_row = case_table.row_values(caseId)
            case_exe_flag = table_vale_row[4]
            case_value = [table_vale_row[2],table_vale_row[3]]
            if 'YES' == case_exe_flag:
                case_list.append(case_value)
        # print case_list
        # print case_list[1]
        return case_list

    def update_case_result(self, resultlist, file_name, result_file):
        # 打开excel表格，读取内容
        date_src = xlrd.open_workbook(file_name)
        # 获取一个sheet的内容
        case_table = date_src.sheet_by_index(0)
        # 设置可写的excel变量
        date_location = copy(date_src)
        # 获取excel表的行数和列数
        case_table_nrows = case_table.nrows
        case_table_nclos = case_table.ncols

        for caseid in range(len(resultlist)):
            result = resultlist[caseid]
            for rowid in range(case_table_nrows):
                # 根据rowid 获取excel一行的内容
                table_vale_row = case_table.row_values(rowid)
                # print table_vale_row[3]
                if table_vale_row[3] == result[0]:
                    date_location.get_sheet(0).write(rowid, 5, result[1], format_setting.style_red)
        date_location.save(result_file)

    def set_excel_format(self, result_file):
        # 打开excel表格，读取内容
        date_src = xlrd.open_workbook(result_file)
        # 获取一个sheet的内容
        case_table = date_src.sheet_by_index(0)
        # 设置可写的excel变量
        date_location = copy(date_src)
        # 获取excel表的行数和列数
        case_table_nrows = case_table.nrows
        case_table_nclos = case_table.ncols

        # 设置Excel的列宽
        data_xlwt_src = xlrd.open_workbook(result_file)
        data_xlwt = copy(data_xlwt_src)
        sheet_xlwt = data_xlwt.get_sheet(0)
        for col_id in range(case_table_nclos - 3):
            col_width = sheet_xlwt.col(col_id)
            col_width.width = 256 * 30

        tall_style = xlwt.easyxf('font:height 540;')  # 36pt,类型小初的字号
        for row_id in range(case_table_nrows):
            rol_hight = sheet_xlwt.row(row_id)
            rol_hight.set_style(tall_style)

        for col_id in range(case_table_nclos):
            for row_id in range(case_table_nrows):
                # print case_table.cell(row_id,col_id).value
                if case_table.cell(row_id, col_id).value == 'pass':
                    sheet_xlwt.write(row_id, col_id, case_table.cell(row_id, col_id).value, format_setting.style_green)
                elif case_table.cell(row_id, col_id).value == 'pass':
                    sheet_xlwt.write(row_id, col_id, case_table.cell(row_id, col_id).value, format_setting.style_red)
                elif case_table.cell(row_id, col_id).value == 'error':
                    sheet_xlwt.write(row_id, col_id, case_table.cell(row_id, col_id).value, format_setting.style_red)
                else:
                    sheet_xlwt.write(row_id, col_id, case_table.cell(row_id, col_id).value, format_setting.style_frame)
        data_xlwt.save(result_file)

        return 0

    def get_userInfo_by_class(self, class_name):
        file_name = settings.test_case_file
        # 打开excel表格，读取内容
        date_src = xlrd.open_workbook(file_name)
        # 获取一个sheet的内容
        case_table = date_src.sheet_by_index(0)
        # 获取excel表的行数和列数
        case_table_nrows = case_table.nrows
        case_table_nclos = case_table.ncols
        # 定义一个变量，用来接收需要执行的case数据
        case_list = []
        # 循环从用来的excel取数据，并进行判断是否可以执行，可执行，则放入list中
        for caseId in range(case_table_nrows):
            table_vale_row = case_table.row_values(caseId)
            class_name_excel = table_vale_row[2]

            if class_name == class_name_excel:
                userinfor = [table_vale_row[6], table_vale_row[7]]
                break
        return userinfor

    def get_userInfo_by_function(self, function_name):
        file_name = settings.test_case_file
        # 打开excel表格，读取内容
        date_src = xlrd.open_workbook(file_name)
        # 获取一个sheet的内容
        case_table = date_src.sheet_by_index(0)
        # 获取excel表的行数和列数
        case_table_nrows = case_table.nrows
        case_table_nclos = case_table.ncols
        # 定义一个变量，用来接收需要执行的case数据
        case_list = []
        # 循环从用来的excel取数据，并进行判断是否可以执行，可执行，则放入list中
        for caseId in range(case_table_nrows):
            table_vale_row = case_table.row_values(caseId)
            class_name_excel = table_vale_row[3]

            if function_name == class_name_excel:
                userinfor = [table_vale_row[6], table_vale_row[7]]
                break
        return userinfor

    def test(self):
        return 0

if __name__ == '__main__':
    test = excel_Operate()
    # test.create_excel()
    # testValue = [10,11,12,13]
    # test.excel_context_op('d://test-2017-04-17276.532827812.csv',0,testValue)
    # test.CaseDataOpreate('D:\Cruise\pythonSrc\egova\Data\TestCaesData.xlsx')
    resultOp = excel_Operate.result_Operate()
    file = 'D:/Cruise/pythonSrc/reprot/egova-test-2016-10-26-39.1815900622.html'
    caselist = ['set_server_url', 'scan_tips']
    resultlist = resultOp.get_result(caselist,file)
    file_name = 'D:\SVN\V15\zx2016\Client\Python\eGovaMobile\Data\TestCaesData1.xls'
    result_name = 'D:\SVN\V15\zx2016\Client\Python\eGovaMobile\Data\TestCaesData1.xls'
    # test.CaseDataOpreate('D:\Cruise\pythonSrc\egova\Data\TestCaesData.xlsx')
    # test.update_case_result(resultlist, file_name)
    test.update_case_result_file(resultlist,file_name,result_name)
    unittest.main()
