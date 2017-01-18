# -*- coding: utf-8 -*-

import json

import requests

from utils import md5_encode, get_sign_data, get_rsa_sign


class Bestsign(object):

    def __init__(self, host, mid, private_key, *args, **kwargs):
        """
        :param mid: 开发者编号
        """

        self.host = host
        self.mid = mid
        self.private_key = private_key

    def _post(self, request_path, data, sign_data):
        """
        发送post请求
        """

        url = self.host.strip('/') + request_path
        sign = get_rsa_sign(sign_data, self.private_key)
        headers = {
            'mid': self.mid,
            'sign': sign,
        }

        return requests.post(url, headers=headers, json=data)

    def reg_user(self, mobile, name, user_type, email=''):
        """
        注册用户
        :param name: 个人姓名或企业名称
        :param mobile: 手机号码
        :param user_type: 1表示个人用户、2表示企业用户
        """

        method = 'regUser.json'
        path = '/open/' + method

        data = {
            'request': {
                'content': {
                    'name': name,
                    'user_type': user_type,
                    'mobile': mobile,
                    'email': email,
                },
            }
        }

        json_data = json.dumps(data)
        sign_data = get_sign_data(method, self.mid, md5_encode(json_data))

        return self._post(path, data, sign_data)
