

from lxml import etree
from urllib.parse import urljoin
import subprocess
import functools
# 强制 subprocess.Popen 使用 utf-8 编码
subprocess.Popen = functools.partial(subprocess.Popen, encoding="utf-8")
# --- End of fix ---
import json
import execjs
import requests
session = requests.Session()

with open('rs_env.js', mode='r', encoding='utf-8') as f:
    env_code = f.read()


class RSTemplates:
    def __init__(self):
        # 定义请求头
        self.headers = {
            "Host": "ticket.sxhm.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254061a) XWEB/16133 Flue",
            "uid": "1954819555511242752",
            "Content-Type": "application/json",
            "token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ3ZWNoYXRfcHVibGljMSIsInVzZXJJZCI6IjE4Nzc1ODcyNjU3MDczMTUyMDAiLCJuYW1lIjoi5b6u5L-h5YWs5LyX5Y-35pWj5a6iIiwib3JnSWQiOiIxODc3MzM4MjQ2MDkyODE2Mzg0IiwiZGV2aWNlQ29kZSI6IiIsInNhbGVTdGF0aW9uSWQiOiIxODc3MzM4MjQ3NzcwNTM3OTg0IiwiY3VzdG9tZXJJZCI6IjE4Nzc1ODcyNjU4NTgzMTAxNDQiLCJzb2NpYWxDdXN0b21lcklkIjoxOTU0ODE5NTU1NTExMjQyNzUyLCJleHAiOjE3NTQ5ODY2NzV9.QQbOD1ab4emhCh57VveZpQ8RonFSB1N0u80ZI1d0KmpTBLLLgdhDdsBXHktc1Z9jcXsyzdetRnFvqwKsqJ6H9GunsPzKHxW9zt-UvxObqH1bvC0tWiaLZifdGFTZkKEEGGOEjElHNZul4bz4kecS-sbhDGugGJaw3rwQZogstlo",
            "Accept": "*/*",
            "Origin": "https://ticket.sxhm.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://ticket.sxhm.com/quickticket/index.html",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Priority": "u=1, i"
        }
        # 定义请求地址
        self.url = "https://ticket.sxhm.com/quickticket/index.html#/pages/sale/index"
        self.cookies = dict()
        self.rs_ctx = None

    def get_cookie(self):
        # 第一次请求
        response = session.get(self.url, headers=self.headers)
        self.cookies['yrLQQyDMDE1ZO'] = response.cookies.get('yrLQQyDMDE1ZO')

        html = etree.HTML(response.text)
        # 获取 content 参数
        content = html.xpath('//meta[@r="m"]/@content')[0]
        print(content)
        # 获取 自执行方法 文件代码
        eval_url = urljoin(self.url, html.xpath('//script[@charset]/@src')[0])
        eval_code = session.get(eval_url, headers=self.headers).content.decode('utf-8')
        # 获取ts代码
        ts_code = html.xpath('//script[not(@charset)]/text()')[0]

        # 编译JS代码
        js_code = 'var content="{}";\r\n{};\r\n{};\r\n{}\r\n\nconsole.log(get_cookie())\nconsole.log(get_url("GET","https://ticket.sxhm.com/quickticket/index.html#/pages/sale/index?id=1877339201635090432&name=%E9%99%95%E8%A5%BF%E5%8E%86%E5%8F%B2%E5%8D%9A%E7%89%A9%E9%A6%86%E6%9C%AC%E9%A6%86"))'.format(
            content, env_code, ts_code, eval_code)
        self.rs_ctx = execjs.compile(js_code)

        with open('execjs.js', mode='w', encoding='utf-8') as f:
            f.write(js_code)

        # 生成cookie参数
        self.cookies['yrLQQyDMDE1ZP'] = self.rs_ctx.call('get_cookie').split('; path=/')[0].split('=')[1]
        print(self.cookies)

    def get_data(self):
        # 第二次请求
        response = session.get(self.url, headers=self.headers, cookies=self.cookies)
        print(response.content.decode('utf-8'))
        print(response)

        # 获取接口数据
        url = self.rs_ctx.call("get_url", "POST","https://ticket.sxhm.com/applet/bms/sale_order/orderReservation")
        data = {
            "orderType": "OFFLINE_FAST",
            "orderDetailList": [
                {
                    "ticketId": "1878344095197057024",
                    "quantity": 1,
                    "currentSalePrice": 0,
                    "visitorCertificateNo": "EE1971877",
                    "visitorCertificateType": "2",
                    "visitorName": "",
                    "useStartDate": "2025-08-08 00:00:00",
                    "staggeredReservationDailyId": "1951312004886777856",
                    "visitPlanId": "1951950148970438656",
                    "isChildren": "F"
                }
            ],
            "remark": "小程序下单",
            "isCreateVisitPlan": "T",
            "tokenId": "95fa793d79ef4850bf6a23eaab5348aa",
            "locationX": 318,
            "locationY": 170
        }
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=self.headers, cookies=self.cookies, data=data)

        url = self.rs_ctx.call("get_url", "GET",
                               "https://ticket.sxhm.com/applet/bms/contacts/frequentlyUsedContacts/page")
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        print(response.url)
        print(response.content.decode('utf-8'))
        print(response)

        payload = json.dumps({
            "limit": 500,
            "page": 1,
            "type": "tourist"
        })
        response = requests.post(url, headers=self.headers, cookies=self.cookies, data=payload)

        print(response.text)

    def main(self):
        self.get_cookie()
        self.get_data()


if __name__ == '__main__':
    spider = RSTemplates()
    spider.main()
