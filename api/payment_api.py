#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import time
import urllib.parse
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from import_utils import log
from api.http_utils import HttpUtils
from config.config import load_config


class PaymentApi:
    """
    E pay 统一支付接口 (支持 V1-MD5 和 V2-RSA)
    """

    def __init__(self):
        config_load = load_config()
        self.payment_config = config_load.get("payment", {})
        self.version = self.payment_config.get("version", "v2")
        self.mode = self.payment_config.get("mode", "post")

        # 根据版本加载对应配置
        if self.version == 'v1':
            self.config = self.payment_config.get("v1", {})
            self.sign_type = 'MD5'
        else:
            self.config = self.payment_config.get("v2", {})
            self.sign_type = 'RSA'

        self.api_url = self.config.get('apiurl')
        self.pid = self.config.get('pid')
        self.key = self.config.get('key')  # V1 MD5 Key
        self.platform_public_key = self.config.get('platform_public_key')  # V2 RSA Public Key
        self.merchant_private_key = self.config.get('merchant_private_key')  # V2 RSA Private Key
        self.notify_url = self.config.get('notify_url')
        self.return_url = self.config.get('return_url')

        self.http = HttpUtils(base_url=self.api_url)

    # ========================== V1 (MD5) Methods ==========================

    def _get_sign_v1(self, params):
        """V1 MD5 签名：md5(key1=value1&key2=value2...&key)"""
        keys = sorted(params.keys())
        sign_str = ""
        for k in keys:
            v = params[k]
            if k in ['sign', 'sign_type'] or v is None or str(v).strip() == '':
                continue
            sign_str += f"{k}={v}&"

        sign_str = sign_str[:-1] + self.key
        log.info(f"V1 签名内容：{sign_str}")
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    def _build_params_v1(self, params):
        """V1 参数构建"""
        params['pid'] = self.pid
        params['sign_type'] = self.sign_type
        params['timestamp'] = str(int(time.time()))
        params['sign'] = self._get_sign_v1(params)
        return params

    def _get_pay_link_v1(self, param_tmp):
        """V1 获取支付链接"""
        req_url = self.api_url.rstrip('/') + '/submit.php'
        params = self._build_params_v1(param_tmp)
        return f"{req_url}?{urllib.parse.urlencode(params)}"

    # ========================== V2 (RSA) Methods ==========================
    @staticmethod
    def _get_sign_content_v2(params):
        """
        V2 获取待签名字符串
        """
        keys = sorted(params.keys())
        sign_str = ""
        for k in keys:
            v = params[k]
            if k in ['sign', 'sign_type'] or v is None or str(v).strip() == '':
                continue
            sign_str += f"&{k}={v}"
        return sign_str[1:] if sign_str else ""

    def _rsa_private_sign_v2(self, data):
        """V2 RSA 私钥签名"""
        try:
            key_pem = self._format_private_key_v2(self.merchant_private_key)
            rsakey = RSA.import_key(key_pem)
            signer = pkcs1_15.new(rsakey)
            digest = SHA256.new(data.encode('utf-8'))
            sign = signer.sign(digest)
            return base64.b64encode(sign).decode('utf-8')
        except Exception as e:
            log.error(f"V2 签名错误: {e}")
            raise Exception("签名失败，商户私钥错误")

    def _format_private_key_v2(self, key_content):
        if "-----" in key_content:
            return key_content
        return f"-----BEGIN PRIVATE KEY-----\n{self._chunk_split(key_content)}\n-----END PRIVATE KEY-----"

    def _rsa_public_verify_v2(self, data, sign):
        """V2 RSA 公钥验签"""
        try:
            if "-----" in self.platform_public_key:
                pem_key = self.platform_public_key
            else:
                pem_key = f"-----BEGIN PUBLIC KEY-----\n{self._chunk_split(self.platform_public_key)}\n-----END PUBLIC KEY-----"

            key = RSA.import_key(pem_key)
            h = SHA256.new(data.encode('utf-8'))
            pkcs1_15.new(key).verify(h, base64.b64decode(sign))
            return True
        except Exception as e:
            log.error(f"V2 验签异常: {e}")
            return False

    def _verify_v2(self, data):
        """V2 响应数据验签"""
        if not data or 'sign' not in data:
            return False

        timestamp = int(data.get('timestamp', 0))
        if abs(time.time() - timestamp) > 300:
            log.warning("V2 验签失败: 时间戳过期")
            return False

        sign = data['sign']
        sign_content = self._get_sign_content_v2(data)
        return self._rsa_public_verify_v2(sign_content, sign)

    def _build_params_v2(self, params):
        """V2 参数构建 (Post模式)"""
        params['pid'] = self.pid
        params['timestamp'] = str(int(time.time()))
        params['sign_type'] = self.sign_type

        # 对原始参数签名
        sign_content = self._get_sign_content_v2(params)
        log.info(f"V2 签名内容：{sign_content}")
        params['sign'] = self._rsa_private_sign_v2(sign_content)
        return params

    def _get_pay_link_v2(self, param_tmp):
        """V2 获取支付链接 (根据 mode 选择策略)"""
        req_url = self.api_url.rstrip('/') + '/api/pay/submit'

        # 拼接模式: 先编码后签名 (特殊处理)
        if self.mode == 'url':
            # 1. 准备基础参数
            params = param_tmp.copy()
            params['pid'] = self.pid
            params['timestamp'] = str(int(time.time()))
            params['sign_type'] = self.sign_type

            # 2. 对每个参数值进行 URL 编码
            encoded_params = {}
            for k, v in params.items():
                if v is None or str(v).strip() == '':
                    continue
                encoded_params[k] = urllib.parse.quote_plus(str(v))

            # 3. 对已编码的参数进行签名
            sign_content = self._get_sign_content_v2(encoded_params)
            log.info(f"V2 (拼接模式) 签名内容(已编码): {sign_content}")
            sign = self._rsa_private_sign_v2(sign_content)

            # 4. 将签名也进行 URL 编码
            encoded_params['sign'] = urllib.parse.quote_plus(sign)

            # 5. 手动拼接 Query String
            qs_items = []
            for k, v in encoded_params.items():
                qs_items.append(f"{k}={v}")
            return f"{req_url}?{'&'.join(qs_items)}"

        # 默认模式/Post模式所需的链接 (如果有需要调用 submit): 标准逻辑
        else:
            params = self._build_params_v2(param_tmp)
            return f"{req_url}?{urllib.parse.urlencode(params)}"

    @staticmethod
    def _chunk_split(body, chunk_len=64, end='\n'):
        return end.join(body[i:i + chunk_len] for i in range(0, len(body), chunk_len))

    # ========================== Public Interface ==========================

    def create_order(self, name, money, pay_type, out_trade_no):
        """
        构造订单参数并获取支付链接
        :param name: 商品名称
        :param money: 金额
        :param pay_type: 支付方式 (alipay/wxpay)
        :param out_trade_no: 商户订单号
        :return: 支付跳转链接
        """
        params = {
            "money": money,
            "name": name,
            "notify_url": self.notify_url,
            "return_url": self.return_url,
            "out_trade_no": out_trade_no,
            "type": pay_type
        }

        if self.version == 'v1':
            return self._get_pay_link_v1(params)
        else:
            return self._get_pay_link_v2(params)

    async def api_pay(self, name, money, pay_type, out_trade_no):
        """
        API 发起支付
        V1: mapi.php
        V2: api/pay/create
        """
        params = {
            "money": money,
            "name": name,
            "notify_url": self.notify_url,
            "return_url": self.return_url,
            "out_trade_no": out_trade_no,
            "type": pay_type,
            "clientip": "127.0.0.1"
        }

        if self.version == 'v1':
            return await self._execute('mapi.php', params)
        else:
            return await self._execute('api/pay/create', params)

    async def query_order(self, trade_no=None, out_trade_no=None):
        """
        查询订单
        V1: api.php
        V2: api/pay/query
        """
        params = {}
        if trade_no:
            params['trade_no'] = trade_no
        if out_trade_no:
            params['out_trade_no'] = out_trade_no

        if self.version == 'v1':
            # V1 Query Logic
            params['act'] = 'order'
            params['pid'] = self.pid
            params['key'] = self.key
            req_url = self.api_url.rstrip('/') + '/api.php'
            try:
                # V1 GET Request
                return await self.http.get(req_url, params=params)
            except Exception as e:
                log.error(f"V1 查询错误: {e}")
                raise Exception("查询失败")
        else:
            # V2 验签逻辑
            response = await self._execute('api/pay/query', params)
            if self.version != 'v1':
                verify_result = self._verify_v2(response)
                log.info(f"V2 响应验签结果: {verify_result}")
                if not verify_result:
                    raise Exception("返回数据验签失败")
            return response

    async def _execute(self, path, params):
        """通用的 API 请求与验签逻辑"""
        path = path.lstrip('/')
        req_url = self.api_url.rstrip('/') + '/' + path

        # 根据版本构建参数
        if self.version == 'v1':
            request_params = self._build_params_v1(params)
        else:
            request_params = self._build_params_v2(params)

        try:
            response = await self.http.post(req_url, data=request_params)
            return response
        except Exception as e:
            log.error(f"API 请求错误: {e}")
            raise Exception(f"请求失败: {e}")
