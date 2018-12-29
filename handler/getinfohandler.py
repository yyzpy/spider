# encoding:utf8
from handler.basehandler import BaseHandler
from handler.getinfo import getinfo


class GetInfoHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        data = getinfo(self.request.body)
        self.write(data)
