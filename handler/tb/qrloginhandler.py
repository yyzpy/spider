from handler.basehandler import BaseHandler
import requests
import tornado.escape
import json
import time
import urllib.parse

headers = {'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'}


class QrloginHandler(BaseHandler):
    def get(self):
        lgtoken = self.get_argument('lgToken')
        # 轮询获取登录状态 成功就退出并返回所需的json数据带入下一个请求
        while True:
            time.sleep(1)
            url = 'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken=%s' \
                  '&defaulturl=https://www.taobao.com/&_ksTS=1460659151617_231' % lgtoken
            login = requests.get(url, headers=headers)
            qrcode_json = json.loads(login.content)
            login_code = qrcode_json['code']
            print(login_code)
            if login_code == '10006':
                self.write(tornado.escape.json_encode({'data': qrcode_json}))
                break
            if login_code == '10004':
                self.write(tornado.escape.json_encode({'code': '10004'}))
                break

    def post(self):
        data = self.request.body
        token = data['token']
        login_time = data['time']
        webpas = data['webpas']
        # 将登录时获取的参数带入请求中获取请求订单接口所需的cookies
        res_cookies = requests.get(
            'https://login.taobao.com/member/loginByIm.do?uid=cntaobaoez%E9%9C%B8%E9%9C%B8'
            '&token={0}&time={1}&asker=qrcodelogin&ask_version=1.0.0&defaulturl=http%3A%2F%2Fwww.taobao.com%2F'
            '&webpas={2}&umid_token=C1546069320822671779156681546148479361489'.format(token, login_time, webpas),
            headers=headers, allow_redirects=False)
        cookie_dict = res_cookies.cookies
        cookies = {
            '_cc_': cookie_dict['_cc_'],
            '_l_g_': cookie_dict['_l_g'],
            '_m_h5_tk': '81393c8c5fd9c9a6c9745dd6ccea23e2_1546365896330',
            '_m_h5_tk_enc': '39f4cc363eae55a1d62fb021beb073c3',
            '_nk_': cookie_dict['_nk_'],
            '_tb_token_': cookie_dict['_tb_token'],
            'cna	': 's/ixFCQDxmACAXWXDkMYtddD',
            'cookie1': cookie_dict['1'],
            'cookie17': cookie_dict['17'],
            'cookie2':cookie_dict['2'],
            'csg': cookie_dict['csg'],
            'dnk': cookie_dict['dnk'],
            'existShop': cookie_dict['existShop'],
            'lgc': cookie_dict['lgc'],
            'miid': '1118874391958152902',
            'mt': cookie_dict['mt'],
            'sg': cookie_dict['sg'],
            'skt': cookie_dict['skt'],
            't': cookie_dict['t'],
            'tg': cookie_dict['tg'],
            'thw': 'cn',
            'tracknick': cookie_dict['tracknick'],
            'uc1': cookie_dict['uc1'],
            'uc3': cookie_dict['uc3'],
            'ucn': 'unsz',
            'unb': cookie_dict['unb'],
            'v': '0',
            }
        headers1 = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://buyertrade.taobao.com',
            'referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?'
                       'spm=a21bo.2017.1997525045.2.5af911d9hFzdjk'}

        url = 'https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction' \
              '&event_submit_do_query=1&_input_charset=utf8'
        # pageSize定义返回的订单数量
        form = {'pageNum': '1',
                'pageSize': '50',
                'prePageNo': '1'}
        # 请求返回一个json数据，订单信息全在里面，根据需求再进行解析
        data = requests.post(url, headers=headers1, cookies=cookies, data=urllib.parse.urlencode(form))
        with open('order_list', 'w') as f:
            f.write(data.content)
