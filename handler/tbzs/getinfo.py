# encoding:utf8
import json
import urllib.parse
import requests
import re
import time

headers_safe = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                              '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
                'referer': 'https://ic.qq.com/mobile_login.jsp',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://ic.qq.com',
                'x-requested-with': 'XMLHttpRequest'}

headers_contact = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'zh-CN,zh;q=0.9',
                   'referer': 'https://ic.qq.com/mobile_login.jsp',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                                 '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
                   'upgrade-insecure-requests': '1',
                   'cache-control': 'max-age=0'}

header_search = {'referer': 'https://ic.qq.com/pim/contact.jsp',
                 'origin': 'https://ic.qq.com',
                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
                 'x-requested-with': 'XMLHttpRequest',
                 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                 'accept': 'application/json, text/javascript, */*; q=0.01',
                 'accept-encoding': 'gzip, deflate, br',
                 'accept-language': 'zh-CN,zh;q=0.9',
                 'content-length': '150'}


def getinfo(data):
    data = data
    cookies = {'SESSION_JSESSIONID': str(data['SESSION_JSESSIONID']),
               't_user_agent': str(data['t_user_agent'])}
    csrf = data['csrf']
    verify = data['verify']
    verifycode = {'method': 'verify',
                  'verifyCode': str(verify),
                  'csrfToken': str(csrf)}
    user_id = data['user_id']
    # 发送短信验证码
    time.sleep(2)
    res = requests.post('https://ic.qq.com/pim/safeMobileVerify.jsp?', headers=headers_safe,
                        cookies=cookies, data=urllib.parse.urlencode(verifycode))
    code = res.text.replace('\n', '')

    if code == '0':
        # 网页中抓取通讯录总人数
        cookies['pim_mobile'] = '+86' + data['mobile']
        contact = requests.get('https://ic.qq.com/pim/contact.jsp', headers=headers_contact, cookies=cookies,
                               allow_redirects=False)
        size_rule = '"dataListSize":\d+'
        size_number = re.findall(size_rule, contact.text)
        size = size_number[0].replace('"dataListSize":', '')    # 通讯录总人数
        rule = "csrfToken:(.*)"
        csrftoken = re.findall(rule, contact.text)[0].replace(' ', '').replace(',', '').replace("'", '')
        form_data = {'myuinmd5': 'cfcd208495d565ef66e7dff9f98764da',
                     'X_Content_Type': 'json',
                     'csrfToken': csrftoken,
                     'groupId': '-1',
                     'pageNo': '1',
                     'pageSize': size,
                     'order': 'ASC',
                     'sortBy': 'name',
                     'key': ''}

        # 从接口获取通讯录数据
        response = requests.post('https://ic.qq.com/pim/contact/card/search_by_key_json.jsp', headers=header_search,
                                 cookies=cookies, data=urllib.parse.urlencode(form_data))
        try:
            data = json.loads(response.text)
            data = data['info']['vacrds']
        except:
            csrf_text = requests.get('https://ic.qq.com/pim/contact.jsp', headers=headers_contact, cookies=cookies,
                                     allow_redirects=False)
            rule = "csrfToken:(.*)"
            csrftoken = re.findall(rule, csrf_text.text)[0].replace(' ', '').replace(',', '').replace("'", '')
            form_data['csrfToken'] = csrftoken
            again_res = requests.post('https://ic.qq.com/pim/contact/card/search_by_key_json.jsp',
                                      headers=header_search, cookies=cookies, data=form_data, allow_redirects=False)
            data = json.loads(again_res.text)
            data = data['info']['vacrds']

        li_phone = []
        for i in data:
            try:
                all_number = i['vcard']['TEL']
                name = i['vcard']['N'][0]['VALUE'].replace(';', '').replace('+86', '').replace('-', '')
                size = len(i['vcard']['TEL'])
                for j in range(size):
                    data_dict = {}
                    number = all_number[j]['VALUE'].replace('+86', '').replace('-', '')
                    data_dict['name'] = name
                    data_dict['mobile_phone'] = number
                    li_phone.append(data_dict)
            except:
                pass
        headers_safe['Content-Type'] = 'application/json'
        requests.post('https://rcs.jiqiyun.cn/api/phoneBooks', data=json.dumps({'user_id': user_id, 'phone': li_phone}),
                      headers=headers_safe)

        return {'code': 0}
    else:
        return {'code': 1, 'message': '短信验证码错误'}


def get_again(data):
    data = data
    cookies = {'SESSION_JSESSIONID': str(data['SESSION_JSESSIONID']),
               't_user_agent': str(data['t_user_agent'])}
    user_id = data['user_id']
    # 网页中抓取通讯录总人数

    cookies['pim_mobile'] = '+86' + data['mobile']
    contact = requests.get('https://ic.qq.com/pim/contact.jsp', headers=headers_contact, cookies=cookies,
                           allow_redirects=False)
    size_rule = '"dataListSize":\d+'
    size_number = re.findall(size_rule, contact.text)
    size = size_number[0].replace('"dataListSize":', '')    # 通讯录总人数
    rule = "csrfToken:(.*)"
    csrftoken = re.findall(rule, contact.text)[0].replace(' ', '').replace(',', '').replace("'", '')
    form_data = {'myuinmd5': 'cfcd208495d565ef66e7dff9f98764da',
                 'X_Content_Type': 'json',
                 'csrfToken': csrftoken,
                 'groupId': '-1',
                 'pageNo': '1',
                 'pageSize': size,
                 'order': 'ASC',
                 'sortBy': 'name',
                 'key': ''}

    # 从接口获取通讯录数据
    response = requests.post('https://ic.qq.com/pim/contact/card/search_by_key_json.jsp', headers=header_search,
                             cookies=cookies, data=urllib.parse.urlencode(form_data))
    try:
        data = json.loads(response.text)
        data = data['info']['vacrds']
    except:
        csrf_text = requests.get('https://ic.qq.com/pim/contact.jsp', headers=headers_contact, cookies=cookies,
                                 allow_redirects=False)
        rule = "csrfToken:(.*)"
        csrftoken = re.findall(rule, csrf_text.text)[0].replace(' ', '').replace(',', '').replace("'", '')
        form_data['csrfToken'] = csrftoken
        again_res = requests.post('https://ic.qq.com/pim/contact/card/search_by_key_json.jsp',
                                  headers=header_search, cookies=cookies, data=form_data, allow_redirects=False)
        data = json.loads(again_res.text)
        data = data['info']['vacrds']

    li_phone = []
    for i in data:
        try:
            all_number = i['vcard']['TEL']
            name = i['vcard']['N'][0]['VALUE'].replace(';', '').replace('+86', '').replace('-', '')
            size = len(i['vcard']['TEL'])
            for j in range(size):
                data_dict = {}
                number = all_number[j]['VALUE'].replace('+86', '').replace('-', '')
                data_dict['name'] = name
                data_dict['mobile_phone'] = number
                li_phone.append(data_dict)
        except:
            pass
    headers_safe['Content-Type'] = 'application/json'
    requests.post('https://rcs.jiqiyun.cn/api/phoneBooks', data=json.dumps({'user_id': user_id, 'phone': li_phone}),
                  headers=headers_safe)

    return {'code': 0}
