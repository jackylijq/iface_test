"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint
from app.api.iftest.testcase import testcase_api
from app.api.iftest.gw_api import gwapi
from app.api.iftest.date_handle import datehandle
from app.api.iftest.interface import interface
from app.api.iftest.dispose import dispose
from app.api.iftest.holiday import holiday

def iface_test():
    iftest = Blueprint('iftest', __name__)
    # testcase.testcase_api.register(iftest)
    # gw_api.gwapi.register(iftest)
    # date_handle.datehandle.register(iftest)
    # interface.interface.register(iftest)
    # dispose.dispose.register(iftest)
    # holiday.holiday.register(iftest)
    #接口注册
    iftest.register_blueprint(testcase_api, url_prefix="/case")
    iftest.register_blueprint(gwapi, url_prefix="/gwapi")
    iftest.register_blueprint(datehandle, url_prefix="/datehandle")
    iftest.register_blueprint(interface, url_prefix="/interface")
    iftest.register_blueprint(dispose, url_prefix="/dispose")
    iftest.register_blueprint(holiday, url_prefix="/holiday")

    return iftest
