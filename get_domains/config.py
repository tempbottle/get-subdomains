# -*- coding:utf8 -*-
from tornado.options import define, options

#服务器配置项
define("port", default=9999, help="run on the given port", type=int)

# mongodb
define("server", default='127.0.0.1')
define('username', default='netxfly')
define('password', default='mypassw0rd')
