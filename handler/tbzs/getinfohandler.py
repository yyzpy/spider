# encoding:utf8
from handler.basehandler import BaseHandler
from handler.tbzs.getinfo import getinfo
from handler.tbzs.getinfo import get_again
import json
import requests
import urllib.parse


class GetInfoHandler(BaseHandler):
    def get(self):
        headers_safe = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                                      '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
                        'referer': 'https://ic.qq.com/mobile_login.jsp',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'origin': 'https://ic.qq.com',
                        'x-requested-with': 'XMLHttpRequest'}

        verify = self.get_argument('verify')
        csrf = self.get_argument('csrf')
        session_id = self.get_argument('SESSION_JSESSIONID')
        t_user_agent = self.get_argument('t_user_agent')
        verifycode = {'method': 'verify',
                      'verifyCode': str(verify),
                      'csrfToken': str(csrf)}
        cookies = {'SESSION_JSESSIONID': str(session_id),
                   't_user_agent': str(t_user_agent)}
        res = requests.post('https://ic.qq.com/pim/safeMobileVerify.jsp?', headers=headers_safe,
                            cookies=cookies, data=urllib.parse.urlencode(verifycode))
        code = res.text.replace('\n', '')
        if code == '0':
            self.write(json.dumps({'code': '0'}))
        else:
            self.write(json.dumps({'code': str(code)}))

    def post(self):
        data = self.request.body
        data = json.loads(data.decode('utf8'))
        status_code = data['code']
        if status_code == 0:
            res = getinfo(data)
            self.write(res)

        if status_code == 1:
            res = get_again(data)
            self.write(res)
