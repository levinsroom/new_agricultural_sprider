#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

class Chaojiying_Client(object):
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    }
    base_params = {}
    def __init__(self, username, password, soft_id):
        username = username
        password =  password.encode('utf8')
        password = md5(password).hexdigest()
        self.base_params = {
            'user': username,
            'pass2': password,
            'softid': soft_id,
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    # 用户中心>>软件ID 生成一个替换 96001
	chaojiying = Chaojiying_Client('账号', '密码', '912479')
    # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
	im = open('image\\a.jpg', 'rb').read()
    # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    # {'err_no': 0, 'err_str': 'OK', 'pic_id': '1130921095586800001', 'pic_str': '7261',
    # 'md5': '2310d14232c4465ca59e8b47c8636fcd'}
	print(chaojiying.PostPic(im, 1902))

