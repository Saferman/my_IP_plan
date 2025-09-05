#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import functools

# 强制 subprocess.Popen 使用 utf-8 编码
subprocess.Popen = functools.partial(subprocess.Popen, encoding="utf-8")
import requests
import json
import execjs
from lxml import etree
from urllib.parse import urljoin



class BaseRequest:
    """基础请求类，包含cookie生成和基础请求功能"""
    
    def __init__(self, uid, token, auto_refresh_cookie=True):
        """
        初始化基础请求类
        :param uid: 用户ID
        :param token: 认证token
        :param auto_refresh_cookie: 是否每次请求都自动刷新cookie，默认True
        """
        self.uid = uid
        self.token = token
        self.session = requests.Session()
        self.auto_refresh_cookie = auto_refresh_cookie
        
        # 设置基础请求头（不包含uid和token，用于生成cookie）
        self.base_headers = {
            "Host": "ticket.sxhm.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254061a) XWEB/16133 Flue",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": "https://ticket.sxhm.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://ticket.sxhm.com/quickticket/index.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Priority": "u=1, i"
        }
        
        # 设置API请求头（包含uid和token）
        self.headers = {
            "Host": "ticket.sxhm.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254061a) XWEB/16133 Flue",
            "uid": self.uid,
            "Content-Type": "application/json",
            "token": self.token,
            "Accept": "*/*",
            "Origin": "https://ticket.sxhm.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://ticket.sxhm.com/quickticket/index.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Priority": "u=1, i"
        }
        
        # 定义基础URL
        self.base_url = "https://ticket.sxhm.com/quickticket/index.html#/pages/sale/index"
        
        # 初始化cookies和JS上下文
        self.cookies = {}
        self.rs_ctx = None

    def get_cookie(self):
        """
        自动生成cookie
        :return: True-成功 False-失败
        """
        print("开始获取cookie...")
        
        try:
            # 清除旧的cookies和会话
            self.cookies.clear()
            self.session.cookies.clear()
            self.rs_ctx = None
            
            # 第一次请求获取初始cookie（使用不带token和uid的请求头）
            response = self.session.get(self.base_url, headers=self.base_headers)
            self.cookies['yrLQQyDMDE1ZO'] = response.cookies.get('yrLQQyDMDE1ZO')
            print(f"获取到yrLQQyDMDE1ZO: {self.cookies['yrLQQyDMDE1ZO']}")

            # 解析HTML获取必要参数
            html = etree.HTML(response.text)
            
            # 获取 content 参数
            content = html.xpath('//meta[@r="m"]/@content')[0]
            print(f"获取到content: {content}")
            
            # 获取自执行方法文件代码（使用不带token和uid的请求头）
            eval_url = urljoin(self.base_url, html.xpath('//script[@charset]/@src')[0])
            eval_code = self.session.get(eval_url, headers=self.base_headers).content.decode('utf-8')
            # 缓存eval代码供错误恢复使用
            self._cached_eval_code = eval_code
            
            # 获取ts代码
            ts_code = html.xpath('//script[not(@charset)]/text()')[0]

            # 读取环境代码
            try:
                with open('rs_env.js', mode='r', encoding='utf-8') as f:
                    env_code = f.read()
            except FileNotFoundError:
                print("错误: rs_env.js文件不存在")
                return False

            # 编译JS代码
            js_code = 'var content="{}";\r\n{};\r\n{};\r\n{}\r\n\nconsole.log(get_cookie())\nconsole.log(get_url("GET","https://ticket.sxhm.com/quickticket/index.html#/pages/sale/index?id=1877339201635090432&name=%E9%99%95%E8%A5%BF%E5%8E%86%E5%8F%B2%E5%8D%9A%E7%89%A9%E9%A6%86%E6%9C%AC%E9%A6%86"))'.format(
                content, env_code, ts_code, eval_code)
            
            self.rs_ctx = execjs.compile(js_code)

            # 保存JS代码到文件（可选）
            with open('execjs.js', mode='w', encoding='utf-8') as f:
                f.write(js_code)

            # 生成第二个cookie参数
            cookie_result = self.rs_ctx.call('get_cookie')
            if cookie_result and '; path=/' in str(cookie_result):
                self.cookies['yrLQQyDMDE1ZP'] = cookie_result.split('; path=/')[0].split('=')[1]
                print(f"获取到yrLQQyDMDE1ZP: {self.cookies['yrLQQyDMDE1ZP']}")
                print(f"完整cookies: {self.cookies}")
                return True
            else:
                print(f"cookie_result格式异常: {cookie_result}")
                return False
            
        except Exception as e:
            print(f"获取cookie失败: {e}")
            return False

    def refresh_cookies(self):
        """
        刷新cookies - 重新生成所有必要的cookies
        :return: True-成功 False-失败
        """
        print("开始刷新cookies...")
        
        # 清除旧的cookies
        self.cookies.clear()
        self.session.cookies.clear()
        
        # 重新获取cookies
        return self.get_cookie()

    def set_auto_refresh_cookie(self, auto_refresh):
        """
        设置是否每次请求都自动刷新cookie
        :param auto_refresh: True-每次请求都刷新 False-仅在必要时刷新
        """
        self.auto_refresh_cookie = auto_refresh
        print(f"Cookie自动刷新策略已设置为: {'开启' if auto_refresh else '关闭'}")

    def regenerate_cookie_from_error_response(self, error_html):
        """
        从412错误响应的HTML中提取代码并重新生成cookie
        :param error_html: 错误响应的HTML内容
        :return: True-成功 False-失败
        """
        try:
            print("正在从错误响应中提取代码...")
            
            # 解析HTML获取新的content参数
            html = etree.HTML(error_html)
            new_content = html.xpath('//meta[@r="m"]/@content')[0]
            print(f"从错误响应中获取到新的content: {new_content[:100]}...")
            
            # 获取新的JS代码
            new_ts_code = html.xpath('//script[not(@charset)]/text()')[0]
            print(f"从错误响应中获取到新的JS代码长度: {len(new_ts_code)}")
            
            # 读取环境代码
            try:
                with open('rs_env.js', mode='r', encoding='utf-8') as f:
                    env_code = f.read()
            except FileNotFoundError:
                print("错误: rs_env.js文件不存在")
                return False

            # 获取自执行方法文件代码（使用缓存的或重新获取）
            if hasattr(self, '_cached_eval_code'):
                eval_code = self._cached_eval_code
            else:
                # 重新获取eval代码（使用不带token和uid的请求头）
                try:
                    response = self.session.get(self.base_url, headers=self.base_headers)
                    page_html = etree.HTML(response.text)
                    eval_url = urljoin(self.base_url, page_html.xpath('//script[@charset]/@src')[0])
                    eval_code = self.session.get(eval_url, headers=self.base_headers).content.decode('utf-8')
                    self._cached_eval_code = eval_code
                except Exception as e:
                    print(f"获取eval代码失败: {e}")
                    return False

            # 编译新的JS代码
            js_code = 'var content="{}";\r\n{};\r\n{};\r\n{}\r\n\nconsole.log(get_cookie())\nconsole.log(get_url("GET","https://ticket.sxhm.com/quickticket/index.html#/pages/sale/index?id=1877339201635090432&name=%E9%99%95%E8%A5%BF%E5%8E%86%E5%8F%B2%E5%8D%9A%E7%89%A9%E9%A6%86%E6%9C%AC%E9%A6%86"))'.format(
                new_content, env_code, new_ts_code, eval_code)
            
            self.rs_ctx = execjs.compile(js_code)

            # 保存新的JS代码到文件
            with open('execjs_error_recovery.js', mode='w', encoding='utf-8') as f:
                f.write(js_code)
            print("已保存错误恢复的JS代码到 execjs_error_recovery.js")

            # 生成新的cookie
            cookie_result = self.rs_ctx.call('get_cookie')
            if cookie_result and '; path=/' in str(cookie_result):
                self.cookies['yrLQQyDMDE1ZP'] = cookie_result.split('; path=/')[0].split('=')[1]
                print(f"从错误响应中重新生成yrLQQyDMDE1ZP: {self.cookies['yrLQQyDMDE1ZP']}")
                return True
            else:
                print(f"从错误响应重新生成cookie失败，cookie_result: {cookie_result}")
                return False
            
        except Exception as e:
            print(f"从错误响应中重新生成cookie失败: {e}")
            return False

    def generate_signed_url(self, method, base_url):
        """
        生成带签名的URL
        :param method: 请求方法 GET/POST
        :param base_url: 基础URL
        :return: 带签名的完整URL
        """
        if not self.rs_ctx:
            print("错误: JS上下文未初始化，请先调用get_cookie()")
            return base_url
        
        try:
            signed_url = self.rs_ctx.call("get_url", method, base_url)
            print(f"生成的签名URL: {signed_url}")
            return signed_url
        except Exception as e:
            print(f"生成签名URL失败: {e}")
            return base_url

    def make_request(self, method, url, data=None, **kwargs):
        """
        发送HTTP请求
        :param method: 请求方法 GET/POST/PUT/DELETE
        :param url: 请求URL
        :param data: 请求数据（字典或JSON字符串）
        :param kwargs: 其他请求参数
        :return: Response对象
        """
        # 根据配置决定是否每次请求前重新生成cookie
        if self.auto_refresh_cookie:
            print(f"正在为 {method.upper()} 请求重新生成cookie...")
            if not self.get_cookie():
                print("重新生成cookie失败，使用现有cookie继续请求")
        elif not self.cookies or not self.rs_ctx:
            print("首次请求或cookie为空，正在生成cookie...")
            if not self.get_cookie():
                print("生成cookie失败，请求可能会失败")
        
        # 生成带签名的URL
        signed_url = self.generate_signed_url(method, url)
        
        # 处理请求数据
        if data and isinstance(data, dict):
            data = json.dumps(data, separators=(',', ':'))
        
        try:
            # 发送请求
            response = self.session.request(
                method=method.upper(),
                url=signed_url,
                headers=self.headers,
                cookies=self.cookies,
                data=data,
                timeout=kwargs.get('timeout', 30),
                **{k: v for k, v in kwargs.items() if k != 'timeout'}
            )
            
            print(f"请求方法: {method.upper()}")
            print(f"请求URL: {response.url}")
            print(f"状态码: {response.status_code}")
            
            # 对412错误进行特殊处理
            if response.status_code == 412:
                print("收到412错误 - 可能是签名验证失败或请求被拒绝")
                print(f"响应头: {dict(response.headers)}")
                if response.text:
                    print("收到错误响应内容可以提取里面的代码生成cookie")
                    # 尝试从错误响应中重新生成cookie
                    if self.regenerate_cookie_from_error_response(response.text):
                        print("从错误响应中重新生成cookie成功，重试请求...")
                        # 重新生成签名URL并重试
                        signed_url = self.generate_signed_url(method, url)
                        response = self.session.request(
                            method=method.upper(),
                            url=signed_url,
                            headers=self.headers,
                            cookies=self.cookies,
                            data=data,
                            timeout=kwargs.get('timeout', 30),
                            **{k: v for k, v in kwargs.items() if k != 'timeout'}
                        )
                        print(f"重试后状态码: {response.status_code}")
            
            return response
            
        except requests.RequestException as e:
            print(f"请求发送失败: {e}")
            return None

    def post(self, url, data=None, **kwargs):
        """POST请求简化方法"""
        return self.make_request('POST', url, data, **kwargs)

    def get(self, url, **kwargs):
        """GET请求简化方法"""
        return self.make_request('GET', url, **kwargs)

    def put(self, url, data=None, **kwargs):
        """PUT请求简化方法"""
        return self.make_request('PUT', url, data, **kwargs)

    def delete(self, url, **kwargs):
        """DELETE请求简化方法"""
        return self.make_request('DELETE', url, **kwargs)

    def init_session(self):
        """初始化会话（获取cookie）"""
        print("初始化会话...")
        return self.get_cookie()

    def print_response(self, response):
        """
        打印响应信息
        :param response: Response对象
        """
        if response:
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            # 尝试解析JSON
            try:
                result = response.json()
                print(f"JSON数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return result
            except json.JSONDecodeError:
                print("响应不是有效的JSON格式")
                return response.text
        else:
            print("响应为空")
            return None

    def is_success(self, response):
        """
        检查响应是否成功
        :param response: Response对象
        :return: True-成功 False-失败
        """
        return response is not None and response.status_code == 200

    def test_cookie_generation(self):
        """
        测试cookie生成功能
        :return: True-成功 False-失败
        """
        print("=" * 50)
        print("测试Cookie生成功能")
        print("=" * 50)
        
        print("生成Cookie使用的请求头（不包含uid和token）:")
        for key, value in self.base_headers.items():
            if key == "User-Agent":
                print(f"  {key}: {value[:50]}...")
            else:
                print(f"  {key}: {value}")
        print()
        
        success = self.get_cookie()
        if success:
            print("✅ Cookie生成测试成功")
            print(f"yrLQQyDMDE1ZO: {self.cookies.get('yrLQQyDMDE1ZO', 'None')}")
            print(f"yrLQQyDMDE1ZP: {self.cookies.get('yrLQQyDMDE1ZP', 'None')}")
        else:
            print("❌ Cookie生成测试失败")
        
        return success

    def show_api_headers(self):
        """
        显示API请求使用的请求头信息
        """
        print("API请求使用的请求头（包含uid和token）:")
        for key, value in self.headers.items():
            if key in ["User-Agent", "token"]:
                print(f"  {key}: {value[:50]}...")
            else:
                print(f"  {key}: {value}")
        print()


# 使用示例
if __name__ == '__main__':
    # 测试基础功能
    uid = "1955128632239742976"
    token = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ3ZWNoYXRfcHVibGljMSIsInVzZXJJZCI6IjE4Nzc1ODcyNjU3MDczMTUyMDAiLCJuYW1lIjoi5b6u5L-h5YWs5LyX5Y-35pWj5a6iIiwib3JnSWQiOiIxODc3MzM4MjQ2MDkyODE2Mzg0IiwiZGV2aWNlQ29kZSI6IiIsInNhbGVTdGF0aW9uSWQiOiIxODc3MzM4MjQ3NzcwNTM3OTg0IiwiY3VzdG9tZXJJZCI6IjE4Nzc1ODcyNjU4NTgzMTAxNDQiLCJzb2NpYWxDdXN0b21lcklkIjoxOTU1MTI4NjMyMjM5NzQyOTc2LCJleHAiOjE3NTUwNjAzNjV9.v3Q-EKCfLvysLHGjed5VLOgXYBk2aq0ritkVf_h7Cy1nHtJranXKcxEoBo-0IC2snyRbDT_I31gSWu-VM-alvm2EPMSlsxynQrI9vVmPcac6yASLIAg466bNGasci4fOVmuIAMNxxPk-ZUeB_ffcdIwP5Ol7zz8j0gcj-8VXa9E"
    
    # 创建基础请求实例
    base_request = BaseRequest(uid, token)
    
    # 初始化会话
    if base_request.init_session():
        print("会话初始化成功")
        
        # 测试GET请求
        # response = base_request.get("https://ticket.sxhm.com/applet/trip/staggered-reservation-daily/list-staggered-reservation-daily-vo")
        # base_request.print_response(response)
        
    else:
        print("会话初始化失败") 