"""
    主要用来做用例执行的工作，分为2种执行，一种为直接界面测试，不进行结果写入，一种为写入结果
"""
import json,requests
from flask import jsonify
from flask import Blueprint, g
# from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
# from app.models.book import Book
# from app.validators.forms import BookSearchForm, CreateOrUpdateBookForm
from flask import Flask,request

from base_frame import standard_api_request

testcase_api = Blueprint("case", __name__)

#实例化class
standard_api_instances = standard_api_request.standard_api()

# 这与真实的情况是一致的，因为一般的情况下，重要的接口需要被保护，重要的消息才需要推送
@testcase_api.route('/<bid>', methods=['GET'])
@login_required
def get_book(bid):
    book = Book.get_detail(bid)
    return jsonify(book)

@testcase_api.route('/execute/sigle', methods=['GET'])
def execute_sigle():
    # 定义默认结果：
    result = {'code': 402, 'message': '更新数据成', 'data': []}
    # 获取接口传入的内容
    post_data = json.loads(request.data)
    # 定义参数检测
    case_key_list = ['test_plan', 'test_module', 'test_case', 'record_db', 'branch']
    args_key_list = post_data.keys()
    for i in range(len(case_key_list)):
        if case_key_list[i] in args_key_list:
            continue
        result['message'] = u'请求参数中缺少字段：%s' % case_key_list[i]
        return result
    test_plan_list = post_data['test_plan']
    test_module_list = post_data['test_module']
    test_case_list = post_data['test_case']
    if len(test_plan_list) == 0 and len(test_module_list) == 0 and len(test_case_list) == 0:
        result['message'] = u'所有参数都为空，无需要执行的用例'
        return result
    test_result = standard_api_instances.api_request_entry(post_data)
    return test_result



@testcase_api.route('', methods=['GET'])
@login_required
def get_books():
    books = Book.get_all()
    return jsonify(books)


@testcase_api.route('/search', methods=['GET'])
def search():
    form = BookSearchForm().validate_for_api()
    books = Book.search_by_keywords(form.q.data)
    return jsonify(books)


@testcase_api.route('', methods=['POST'])
def create_book():
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.new_book(form)
    return Success(msg='新建图书成功')


@testcase_api.route('/<bid>', methods=['PUT'])
def update_book(bid):
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.edit_book(bid, form)
    return Success(msg='更新图书成功')


@testcase_api.route('/<bid>', methods=['DELETE'])
@route_meta(auth='删除图书', module='图书')
@group_required
def delete_book(bid):
    Book.remove_book(bid)
    return Success(msg='删除图书成功')
