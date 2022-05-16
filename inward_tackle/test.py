# -*- coding: UTF-8 -*-
import requests,sys
import json

def mail_send():

    parameter = sys.argv[1]
    # parameter = json.dumps(parameter).encode(encoding='utf-8')
    # parameter = parse.urlencode(parameter).encode(encoding='utf-8')
    # print('input：' + str(parameter))
    parameter = parameter.replace('\'','"')
    # parameter = json.loads(parameter.encode(encoding='utf-8'))
    # parameter = json.dumps(parameter).encode(encoding='utf-8')
    header_info = {"Content-Type": "application/json"}
    url = "http://10.10.64.20:8011/mail/send"
    res = requests.post(url=url, data=parameter, headers=header_info)

    print(res.text)

if __name__ == '__main__':
    parameter = {'tplcode': '1000','APP_NAME':'TongCSDK'}
    mail_send()
