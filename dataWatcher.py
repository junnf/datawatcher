#!/usr/bin/env python
#encoding=utf-8
#
import time
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

#from sendcloud import sendemail
#from sendcloud import sendmessage 

import torndb as mysqldb

db = mysqldb.Connection('192.168.100.10','jianxunv2','devonlyread', 'onlyread-jianxun5x@JIANXUN.IO')

define("port",default = 9999, help = "nothing",type = int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/api/post",  )
            ]
      

if __name__ == '__main__':

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


