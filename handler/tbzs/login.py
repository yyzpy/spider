import json
import hashlib
import urllib.parse
import requests
import re

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
           'origin': 'https://ic.qq.com',
           'referer': 'https://ic.qq.com/pim/login.jsp',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'cache-control': 'max-age=0',
           'content-length': '83',
           'Content-Type': 'application/x-www-form-urlencoded',
           'upgrade-insecure-requests': '1'}


def address(data):
    cookie = {}
    data = json.loads(data.decode('utf8'))
    cookie['SESSION_JSESSIONID'] = data['SESSION_JSESSIONID']
    mobile = data['mobile']
    password = data['password']
    verify = data['verify']
    status_code = str(data['status'])

    md5 = hashlib.md5()
    md5.update(password.encode('utf8'))
    password = md5.hexdigest()
    form = {
        'area': '+86',
        'mobile': mobile,
        'password': password,
        'verify': verify}

    if status_code == 'true':
        # 请求登录 获取csrfToken
        csrftoken = requests.post('https://ic.qq.com/mobile_login.jsp', headers=headers, cookies=cookie,
                                  data=urllib.parse.urlencode(form), allow_redirects=False)
        flag_rule = 'flag=(.*)&'

        if csrftoken.status_code == 200:
            rule = '<input type="hidden" name="csrfToken" id="csrfToken" value=(".*")/>'
            csrf = re.findall(rule, csrftoken.text)[0].replace('"', '')
            csrf_form = {'method': 'getSmsVerifyCode',
                         'csrfToken': csrf,
                         'scenario': '2'}

            # 请求短信验证码
            cookie['t_user_agent'] = data['t_user_agent']
            requests.post('https://ic.qq.com/pim/safeMobileVerify.jsp', headers=headers, cookies=cookie,
                          data=urllib.parse.urlencode(csrf_form), allow_redirects=False)
            return json.dumps({'t_user_agent': data['t_user_agent'], 'SESSION_JSESSIONID': data['SESSION_JSESSIONID'],
                               'csrfToken': csrf})

        else:
            flag = re.findall(flag_rule, csrftoken.text)[0]
            if flag == '-1':
                return {'code': -1}
            if flag == '18':
                return {'code': 18}
            if flag == '203':
                return {'code': 203}

    else:
        return {'code': -2}
