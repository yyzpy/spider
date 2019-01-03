from handler.basehandler import BaseHandler
import requests
import base64
import tornado.escape
import json
import re
headers = {'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'}


class QrcodeHanlder(BaseHandler):
    def get(self):
        # 生成二维码图片的地址，以及所需的lgToken
        res = requests.get('https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage='
                           '&adText=&viewFd4PC=''&viewFd4Mobile=&from=tbTop''&appkey=00000000'
                           '&umid_token=C1546069320822671779156681546148479361489&_ksTS=1546331752782_29'
                           '&callback=jsonp30', headers=headers)
        data = res.text
        rule = '{".*"}'
        res = re.findall(rule, data)[0]
        json_res = json.loads(res)
        qrcode_url = 'https:' + json_res['url']
        lgtoken = json_res['lgToken']
        img = requests.get(qrcode_url)
        img_data = img.content
        data = base64.b64encode(img_data)
        # 返回二维码的base64数据以及lgToken
        img_json = tornado.escape.json_encode({'header': 'data:image/jpg;base64', 'body': data.decode('utf8'),
                                               'loToken': lgtoken})
        self.write(img_json)
