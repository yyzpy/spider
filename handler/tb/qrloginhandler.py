from handler.basehandler import BaseHandler
import requests
import base64
import tornado.escape
import json
import time

headers = {'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'}


class QrloginHandler(BaseHandler):

    def get(self):
        lgtoken = self.get_argument('lgToken')
        while True:
            time.sleep(1)
            url = 'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken=%s' \
                  '&defaulturl=https://www.taobao.com/&_ksTS=1460659151617_231' % lgtoken
            login = requests.get(url, headers=headers)
            qrcode_json = json.loads(login.content)
            login_code = qrcode_json['code']
            print(login_code)
            print(type(login_code))
            if login_code == '10006':
                self.write(tornado.escape.json_encode({'data': qrcode_json}))
                break
            if login_code == '10004':
                self.write(tornado.escape.json_encode({'code': '10004'}))
                break

