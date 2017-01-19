# -*- coding: utf-8 -*-

import json

import requests

from utils import md5_encode, get_sign_data, get_rsa_sign


class BestSign(object):

    def __init__(self, host, mid, private_key, *args, **kwargs):
        """
        :param mid: 开发者编号
        """

        self.host = host
        self.mid = mid
        self.private_key = private_key

    def _post(self, request_path, header_data, post_data):
        """
        发送post请求
        """

        url = self.host.strip('/') + request_path

        try:
            return requests.post(url, headers=header_data, data=post_data).json()
        except:
            return requests.post(url, headers=header_data, data=post_data).content

    def _execute(self, request_path, post_data, sign_data='', header_data=None, method='post'):

        sign = get_rsa_sign(sign_data, self.private_key)
        headers = {
            'mid': self.mid,
            'sign': sign,
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        if isinstance(header_data, dict):
            headers.update(header_data)

        # print('path', request_path)
        # print('header', headers)
        # print('post_data', post_data)

        if method == 'post':
            return self._post(request_path, headers, post_data)

    def reg_user(self, mobile, name, user_type, email):
        """
        注册用户
        :param name: 个人姓名或企业名称
        :param mobile: 手机号码
        :param email: 邮箱
        :param user_type: 1表示个人用户、2表示企业用户
        """

        method = 'regUser.json'
        path = '/open/' + method

        data = {
            'request': {
                'content': {
                    'name': name,
                    'userType': user_type,
                    'mobile': mobile,
                    'email': email,
                },
            }
        }

        post_data = json.dumps(data)
        sign_data = get_sign_data(method, self.mid, md5_encode(post_data))

        return self._execute(path, post_data, sign_data)

    def certificate_apply_person(self, mobile, name, password, identity, province, city, address, email, duration=24, identity_type='0'):
        """
        申请个人CA证书
        :param name: 个人姓名或企业名称
        :param mobile: 手机号码
        :param email: 邮箱
        :param password: 使用证书密码6-18位，可使用随机数
        :param identity: 对应的证件类型的号码
        :param identity_type: (0-   居民身份证 E-  户口簿 F-  临时居民身份证)
        :param province: 省份
        :param city: 城市
        :param address: 个人具体地址
        """

        method = 'certificateApply.json'
        path = '/open/' + method

        data = {
            'request': {
                'content': {
                    'name': name,
                    'userType': 1,
                    'mobile': mobile,
                    'email': email,
                    'password': password,
                    'identityType': identity_type,
                    'identity': identity,
                    'province': province,
                    'city': city,
                    'address': address,
                    'duration': duration,
                },
            }
        }

        post_data = json.dumps(data)
        sign_data = get_sign_data(method, self.mid, md5_encode(post_data))

        return self._execute(path, post_data, sign_data)

    def certificate_apply_company(self, mobile, name, password, linkman, linkidcode, ic_code, org_code, tax_code, province, city, address, email, duration=24):
        """
        申请企业CA证书
        :param name: 个人姓名或企业名称
        :param mobile: 手机号码
        :param email: 邮箱
        :param password: 使用证书密码6-18位，可使用随机数
        :param linkman: 联系人姓名
        :param linkidcode: 身份证号
        :param ic_code: 工商注册号
        :param org_code: 组织机构代码
        :param tax_code: 税务登记证号
        :param province: 省份
        :param city: 城市
        :param address: 个人具体地址
        """

        method = 'certificateApply.json'
        path = '/open/' + method

        data = {
            'request': {
                'content': {
                    'name': name,
                    'userType': 2,
                    'mobile': mobile,
                    'email': email,
                    'password': password,
                    'province': province,
                    'city': city,
                    'address': address,
                    'duration': duration,
                    'linkMan': linkman,
                    'linkIdCode': linkidcode,
                    'icCode': ic_code,
                    'orgCode': org_code,
                    'taxCode': tax_code,
                },
            }
        }

        json_data = json.dumps(data)
        sign_data = get_sign_data(method, self.mid, md5_encode(json_data))

        return self._execute(path, data, sign_data)

    def send_document(self, filename, filestream, send_user, user_list=None):
        """
        合同发送
        :param filename: 文件名字
        :param filestream: 文件二进制流
        :param send_user: 合同发起人,为dict,其中
                :param emailtitle: 邮件消息主题
                :param emailcontent: 邮件消息内容
                :param sxdays: 合同有效天数
                :param selfsign: 是否需要自己签署 0表示不要自己签署，1表示要自己签署
                :param name: 发件人姓名
                :param mobile: 用户账户
                :param usertype: 发件人用户类型 1表示个人用户、2表示企业用户
                :param Signimagetype: 当用户不存在时生成系统自动签名 传1或0均可
                :param UserfileType: 用户使用文件类型 1表示本地文件上传
        :param user_list: 收件人信息列表,为dict列表,其中
                :param name: 个人姓名
                :param mobile: 手机号码
                :param email: 手机号码
                :param usertype: 发件人用户类型 1表示个人用户、2表示企业用户
                :param Signimagetype: 当用户不存在时生成系统自动签名 传1或0均可
                :param isvideo: 是否存在视频
        """
        method = 'sjdsendcontractdocUpload.json'
        path = '/open/' + method

        spo_json = json.dumps(send_user)
        if user_list:
            sig_json = json.dumps(user_list)
        else:
            sig_json = ''

        subdata = get_sign_data(md5_encode(filestream), filename, sig_json, spo_json)

        sign_data = get_sign_data(method, self.mid, subdata)

        header_data = {
            'userlist': sig_json,
            'senduser': spo_json,
            'filename': filename,
        }

        return self._execute(path, filestream, sign_data, header_data)
