# encoding:utf8
import tornado.web
from tornado.options import define, options
import tornado.httpserver
import tornado.ioloop
import tornado.escape
import base64
import requests
from handler.basehandler import BaseHandler
from handler.tbzs.login import address


define('port', default=8000, help='run on the given port', type=int)


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
           'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
           'referer': 'https://ic.qq.com/pim/login.jsp',
           }

cookie = {}


class LoginHandler(BaseHandler):
    def get(self):
        res = requests.get('https://ic.qq.com/pim/captcha.jsp', headers=headers)
        img_data = res.content
        data = base64.b64encode(img_data)
        cookie['user_agent'] = res.cookies['t_user_agent']
        cookie['session_id'] = res.cookies['SESSION_JSESSIONID']
        res = data.decode('utf8')
        img_json = tornado.escape.json_encode({'header': 'data:image/jpg;base64', 'body': res,
                                               't_user_agent': cookie['user_agent'],
                                               'SESSION_JSESSIONID': cookie['session_id']})
        self.write(img_json)

    def post(self):
        flag = address(self.request.body)
        try:
            self.write(flag)
        except TypeError:
            self.write(tornado.escape.json_encode({'code': flag}))


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/', LoginHandler)])
    htp_server = tornado.httpserver.HTTPServer(app)
    htp_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
