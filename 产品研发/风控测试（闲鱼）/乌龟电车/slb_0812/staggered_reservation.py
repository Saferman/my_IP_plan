#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import threading
from datetime import datetime
from base_request import BaseRequest


class StaggeredReservation(BaseRequest):
    def __init__(self, uid, token):
        """
        初始化类
        :param uid: 用户ID
        :param token: 认证token
        """
        super().__init__(uid, token)
    

    
    def get_staggered_reservation_list(self, scenic_spots_id="1877339390596874240", reservation_date="2025-08-15"):
        """
        获取错峰预约日期列表
        :param scenic_spots_id: 景区ID
        :param reservation_date: 预约日期
        :return: 响应结果
        """
        # 请求数据
        data = {
            "isUseCurrentLoginCustomer": "T",
            "scenicSpotsId": scenic_spots_id,
            "reservationDate": reservation_date
        }
        
        # 使用基类的POST方法发送请求
        url = "https://ticket.sxhm.com/applet/trip/staggered-reservation-daily/list-staggered-reservation-daily-vo"
        return self.post(url, data)
    
    def main(self):
        """主方法"""
        print("开始错峰预约监控...")
        request_count = 0
        
        while True:
            request_count += 1
            print(f"\n--- 第{request_count}次请求 ---")
            
            # 每次请求前都重新初始化会话（重新生成cookie）
            print("重新生成cookie...")
            if not self.init_session():
                print("cookie生成失败，等待5秒后重试...")
                time.sleep(5)
                continue
            
            # 发送请求
            response = self.get_staggered_reservation_list()
            
            if response and response.status_code == 200:
                # 使用基类方法打印响应
                result = self.print_response(response)
                print(f"第{request_count}次请求成功")
                
                # 分析返回数据
                if result and isinstance(result, dict) and 'data' in result:
                    data = result['data']
                    print(f"获取到{len(data)}个时间段的预约信息:")
                    for item in data:
                        print(f"  时间段: {item.get('reservationBeginTime')}-{item.get('reservationEndTime')}, "
                              f"剩余票数: {item.get('surplusStockNum')}, "
                              f"已预约人数: {item.get('visitPlanPersonQuantity')}")
                
                print("等待10秒后继续请求...")
                time.sleep(10)
                
            else:
                print(f"第{request_count}次请求失败，状态码: {response.status_code if response else 'None'}")
                print("等待5秒后重试...")
                time.sleep(5)

        



if __name__ == '__main__':
    # 使用示例 - 请替换为实际的参数值
    uid = "1955128632239742976"
    token = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ3ZWNoYXRfcHVibGljMSIsInVzZXJJZCI6IjE4Nzc1ODcyNjU3MDczMTUyMDAiLCJuYW1lIjoi5b6u5L-h5YWs5LyX5Y-35pWj5a6iIiwib3JnSWQiOiIxODc3MzM4MjQ2MDkyODE2Mzg0IiwiZGV2aWNlQ29kZSI6IiIsInNhbGVTdGF0aW9uSWQiOiIxODc3MzM4MjQ3NzcwNTM3OTg0IiwiY3VzdG9tZXJJZCI6IjE4Nzc1ODcyNjU4NTgzMTAxNDQiLCJzb2NpYWxDdXN0b21lcklkIjoxOTU1MTI4NjMyMjM5NzQyOTc2LCJleHAiOjE3NTUwNjAzNjV9.v3Q-EKCfLvysLHGjed5VLOgXYBk2aq0ritkVf_h7Cy1nHtJranXKcxEoBo-0IC2snyRbDT_I31gSWu-VM-alvm2EPMSlsxynQrI9vVmPcac6yASLIAg466bNGasci4fOVmuIAMNxxPk-ZUeB_ffcdIwP5Ol7zz8j0gcj-8VXa9E"
    
    # 创建实例并执行
    reservation = StaggeredReservation(uid, token)
    reservation.main() 