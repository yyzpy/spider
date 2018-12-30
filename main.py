import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
from handler.tbzs.getinfohandler import GetInfoHandler
from handler.tbzs.loginhandler import LoginHandler
from handler.tb.qrcodehandler import QrcodeHanlder
from handler.tb.qrloginhandler import QrloginHandler
import tornado.log
import logging.handlers
from tornado.log import LogFormatter


url = [(r'/login', LoginHandler),
       (r'/getinfo', GetInfoHandler),
       (r'/qrcode', QrcodeHanlder),
       (r'/qrlogin', QrloginHandler)]

access_log = logging.getLogger('tornado.access')
access_log.setLevel(logging.INFO)
hanlder = logging.handlers.TimedRotatingFileHandler(filename='log/access.log', when='D')
datefmt = '%Y-%m-%d %H:%M:%S'
fmt = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
formatter = LogFormatter(color=True, datefmt=datefmt, fmt=fmt)
hanlder.setFormatter(formatter)
access_log.addHandler(hanlder)

app_log = logging.getLogger('tornado.application')
app_log.setLevel(logging.WARNING)
hanlder = logging.handlers.TimedRotatingFileHandler(filename='log/application.log', when='D')
fmt = '%(color)s[%(levelname)1.1s %(asctime)s %(funcName)s:%(lineno)d]%(end_color)s %(message)s'
formatter = LogFormatter(color=True, datefmt=datefmt, fmt=fmt)
hanlder.setFormatter(formatter)
app_log.addHandler(hanlder)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(url)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()


