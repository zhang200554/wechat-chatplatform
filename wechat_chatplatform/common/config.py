# -*- coding: utf-8 -*-

from enum import Enum


class ErrorCode(Enum):
    success = 0
    not_found = 1
    unauthorized = 2
    bad_request = 3


class ErrorMsg(Enum):
    success = 'success'
    not_found = 'resource not found'
    unauthorized = 'unauthorized access'
    bad_request = 'bad request'


HTTP_X_API_KEY = 'HTTP_X_API_KEY'
API_KEY = '227415ba68c811e9b1a48c8590c7151e'
DOMAIN = 'http://www.suavechat.com/'
LOGIN_REDIRECT = 'admin/login/'
ACCEPT_ORDER = '/api/v1/order/accept/?id={}'
ADMIN_INDEX = 'admin/'

MYSQL_COMMAND = 'sudo docker run --name mysql --restart always  --privileged=true -e MYSQL_USER="lihuan" ' \
                '-e MYSQL_PASSWORD="lihuan" -e MYSQL_ROOT_PASSWORD="lihuan" -v=/mnt/mysql/log/:/var/log/mysql/ ' \
                '-v=/mnt/mysql/data:/var/lib/mysql -p 8088:3306 -d mysql --character-set-server=utf8mb4 ' \
                '--collation-server=utf8mb4_general_ci --default-authentication-plugin=mysql_native_password'
