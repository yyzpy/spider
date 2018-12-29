from handler.basehandler import BaseHandler
import requests
import base64
import tornado.escape
import json

headers = {'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'}


class QrcodeHanlder(BaseHandler):
    def get(self):
        res = requests.get('https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do', headers=headers)
        json_res = json.loads(res.content)
        qrcode_url = 'https:' + json_res['url']
        lgtoken = json_res['lgToken']
        img = requests.get(qrcode_url)
        img_data = img.content
        data = base64.b64encode(img_data)
        img_json = tornado.escape.json_encode({'header': 'data:image/jpg;base64', 'body': data.decode('utf8')})
        self.write(img_json)
        print(lgtoken)

