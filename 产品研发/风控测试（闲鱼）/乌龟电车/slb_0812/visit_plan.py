#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from base_request import BaseRequest


class VisitPlan(BaseRequest):
    def __init__(self, uid, token):
        """
        初始化类
        :param uid: 用户ID
        :param token: 认证token
        """
        super().__init__(uid, token)

    def save_visit_plan(self, scenic_spots_id="1877339390596874240", 
                       staggered_reservation_daily_id="1953848720004579328",
                       visit_plan_name="陕西历史博物馆秦汉馆",
                       visitor_list=None):
        """
        保存参观计划
        :param scenic_spots_id: 景区ID
        :param staggered_reservation_daily_id: 错峰预约日期ID
        :param visit_plan_name: 参观计划名称
        :param visitor_list: 游客列表
        :return: 响应结果
        """
        # 默认游客信息
        if visitor_list is None:
            visitor_list = [{
                "visitorName": "张伟",
                "visitorCertificateType": "1",
                "visitorCertificateNo": "440101199812204792",
                "isChildren": "F"
            }]
        
        # 请求数据
        data = {
            "scenicSpotsId": scenic_spots_id,
            "staggeredReservationDailyId": staggered_reservation_daily_id,
            "visitPlanName": visit_plan_name,
            "visitorList": visitor_list
        }
        
        # 打印请求数据
        print(f"请求数据: {json.dumps(data, separators=(',', ':'))}")
        
        # 使用基类的POST方法发送请求
        url = "https://ticket.sxhm.com/applet/bms/visitplan/visitPlan/save"
        return self.post(url, data)

    def update_visit_plan(self, visit_plan_id, scenic_spots_id="1877339390596874240",
                         staggered_reservation_daily_id="1953848719870361601",
                         visit_plan_name="陕西历史博物馆秦汉馆",
                         visitor_list=None):
        """
        更新参观计划
        :param visit_plan_id: 参观计划ID
        :param scenic_spots_id: 景区ID
        :param staggered_reservation_daily_id: 错峰预约日期ID
        :param visit_plan_name: 参观计划名称
        :param visitor_list: 游客列表
        :return: 响应结果
        """
        # 默认游客信息
        if visitor_list is None:
            visitor_list = [{
                "visitorName": "张伟",
                "visitorCertificateType": "1",
                "visitorCertificateNo": "440101199812204792",
                "isChildren": "F"
            }]
        
        # 请求数据
        data = {
            "id": visit_plan_id,
            "scenicSpotsId": scenic_spots_id,
            "staggeredReservationDailyId": staggered_reservation_daily_id,
            "visitPlanName": visit_plan_name,
            "visitorList": visitor_list
        }
        
        print(f"更新参观计划请求数据: {json.dumps(data, separators=(',', ':'))}")
        
        # 使用基类的POST方法发送请求
        url = "https://ticket.sxhm.com/applet/bms/visitplan/visitPlan/update"
        return self.post(url, data)

    def query_visit_plans(self):
        """
        查询参观计划列表
        :return: 响应结果
        """
        url = "https://ticket.sxhm.com/applet/bms/visitplan/visitPlan/list"
        return self.post(url, {})

    def get_visit_plan_ids(self):
        """
        获取参观计划ID列表
        :return: 计划ID列表，失败返回空列表
        """
        response = self.query_visit_plans()
        if self.is_success(response):
            try:
                result = response.json()
                if result.get('code') == 0 and result.get('data'):
                    plan_ids = [plan['id'] for plan in result['data']]
                    print(f"获取到参观计划ID列表: {plan_ids}")
                    return plan_ids
                else:
                    print("未获取到参观计划数据")
                    return []
            except Exception as e:
                print(f"解析参观计划列表失败: {e}")
                return []
        else:
            print("查询参观计划列表失败")
            return []

    def delete_visit_plan(self, plan_id):
        """
        删除参观计划
        :param plan_id: 参观计划ID
        :return: 响应结果
        """
        data = {"id": plan_id}
        print(f"删除参观计划ID: {plan_id}")
        
        url = "https://ticket.sxhm.com/applet/bms/visitplan/visitPlan/delete"
        return self.post(url, data)

    def save_visitor(self, name, certificate_no, certificate_type="1", nationality=None):
        """
        保存常用游客信息
        :param name: 游客姓名
        :param certificate_no: 证件号码
        :param certificate_type: 证件类型，默认"1"为身份证
        :param nationality: 国籍
        :return: 响应结果
        """
        data = {
            "name": name,
            "certificateTypeName": None,
            "certificateType": certificate_type,
            "certificateNo": certificate_no,
            "nationality": nationality,
            "nationalityName": None
        }
        
        print(f"保存游客信息: {json.dumps(data, ensure_ascii=False)}")
        
        url = "https://ticket.sxhm.com/applet/bms/contacts/frequentlyUsedContacts/save"
        return self.post(url, data)

    def delete_visitor(self, visitor_id):
        """
        删除常用游客
        :param visitor_id: 游客ID
        :return: 响应结果
        """
        data = {"id": visitor_id}
        print(f"删除游客ID: {visitor_id}")
        
        url = "https://ticket.sxhm.com/applet/bms/contacts/frequentlyUsedContacts/delete"
        return self.post(url, data)

    def get_visitor_list(self, limit=500, page=1, visitor_type="tourist"):
        """
        获取常用游客列表
        :param limit: 每页数量
        :param page: 页码
        :param visitor_type: 游客类型
        :return: 响应结果
        """
        data = {
            "limit": limit,
            "page": page,
            "type": visitor_type
        }
        
        url = "https://ticket.sxhm.com/applet/bms/contacts/frequentlyUsedContacts/page"
        return self.post(url, data)

    def get_visitor_ids(self):
        """
        获取常用游客ID列表
        :return: 游客ID列表，失败返回空列表
        """
        response = self.get_visitor_list()
        if self.is_success(response):
            try:
                result = response.json()
                if result.get('code') == 0 and result.get('data', {}).get('list'):
                    visitor_ids = [visitor['id'] for visitor in result['data']['list']]
                    print(f"获取到{len(visitor_ids)}个游客ID: {visitor_ids}")
                    return visitor_ids
                else:
                    print("未获取到游客数据")
                    return []
            except Exception as e:
                print(f"解析游客列表失败: {e}")
                return []
        else:
            print("查询游客列表失败")
            return []

    def get_visitor_id_by_certificate(self, certificate_no):
        """
        根据证件号获取游客ID
        :param certificate_no: 证件号码
        :return: 游客ID，未找到返回None
        """
        response = self.get_visitor_list()
        if self.is_success(response):
            try:
                result = response.json()
                if result.get('code') == 0 and result.get('data', {}).get('list'):
                    for visitor in result['data']['list']:
                        if visitor.get('certificateNo') == certificate_no:
                            print(f"找到证件号{certificate_no}对应的游客ID: {visitor['id']}")
                            return visitor['id']
                    print(f"未找到证件号为{certificate_no}的游客")
                    return None
                else:
                    print("未获取到游客数据")
                    return None
            except Exception as e:
                print(f"查找游客ID失败: {e}")
                return None
        else:
            print("查询游客列表失败")
            return None

    def main(self):
        """主方法"""
        # 首先初始化会话
        if not self.init_session():
            print("会话初始化失败，无法继续")
            return
        
        print("开始发送保存参观计划请求...")
        response = self.save_visit_plan()
        
        # 使用基类方法打印响应
        self.print_response(response)

    def add_visitor(self, name, cert_type="1", cert_no="", is_children="F"):
        """
        添加游客信息
        :param name: 游客姓名
        :param cert_type: 证件类型 1-身份证 2-护照等
        :param cert_no: 证件号码
        :param is_children: 是否儿童 F-否 T-是
        :return: 游客信息字典
        """
        return {
            "visitorName": name,
            "visitorCertificateType": cert_type,
            "visitorCertificateNo": cert_no,
            "isChildren": is_children
        }

    def save_custom_visit_plan(self, scenic_spots_id, staggered_reservation_daily_id, 
                             visit_plan_name, visitors):
        """
        保存自定义参观计划
        :param scenic_spots_id: 景区ID
        :param staggered_reservation_daily_id: 错峰预约日期ID
        :param visit_plan_name: 参观计划名称
        :param visitors: 游客列表（字典列表）
        """
        # 首先初始化会话
        if not self.init_session():
            print("会话初始化失败，无法继续")
            return
        
        print(f"开始保存参观计划: {visit_plan_name}")
        print(f"游客数量: {len(visitors)}")
        
        response = self.save_visit_plan(
            scenic_spots_id=scenic_spots_id,
            staggered_reservation_daily_id=staggered_reservation_daily_id,
            visit_plan_name=visit_plan_name,
            visitor_list=visitors
        )
        
        if self.is_success(response):
            print("参观计划保存成功！")
            return self.print_response(response)
        else:
            print("参观计划保存失败")
            self.print_response(response)
            return None

    def batch_delete_visit_plans(self):
        """
        批量删除所有参观计划
        :return: 删除结果列表
        """
        # 首先初始化会话
        if not self.init_session():
            print("会话初始化失败，无法继续")
            return []
        
        # 获取所有计划ID
        plan_ids = self.get_visit_plan_ids()
        if not plan_ids:
            print("没有找到需要删除的参观计划")
            return []
        
        results = []
        for plan_id in plan_ids:
            try:
                response = self.delete_visit_plan(plan_id)
                if self.is_success(response):
                    result = response.json()
                    if result.get('code') == 0:
                        print(f"成功删除参观计划ID: {plan_id}")
                        results.append({"id": plan_id, "status": "success"})
                    else:
                        print(f"删除参观计划ID {plan_id} 失败: {result.get('error', '未知错误')}")
                        results.append({"id": plan_id, "status": "failed", "error": result.get('error')})
                else:
                    print(f"删除参观计划ID {plan_id} 请求失败")
                    results.append({"id": plan_id, "status": "failed", "error": "请求失败"})
            except Exception as e:
                print(f"删除参观计划ID {plan_id} 出现异常: {e}")
                results.append({"id": plan_id, "status": "failed", "error": str(e)})
        
        return results

    def batch_delete_visitors(self):
        """
        批量删除所有常用游客
        :return: 删除结果列表
        """
        # 首先初始化会话
        if not self.init_session():
            print("会话初始化失败，无法继续")
            return []
        
        # 获取所有游客ID
        visitor_ids = self.get_visitor_ids()
        if not visitor_ids:
            print("没有找到需要删除的游客")
            return []
        
        results = []
        for visitor_id in visitor_ids:
            try:
                response = self.delete_visitor(visitor_id)
                if self.is_success(response):
                    result = response.json()
                    if result.get('code') == 0:
                        print(f"成功删除游客ID: {visitor_id}")
                        results.append({"id": visitor_id, "status": "success"})
                    else:
                        print(f"删除游客ID {visitor_id} 失败: {result.get('error', '未知错误')}")
                        results.append({"id": visitor_id, "status": "failed", "error": result.get('error')})
                else:
                    print(f"删除游客ID {visitor_id} 请求失败")
                    results.append({"id": visitor_id, "status": "failed", "error": "请求失败"})
            except Exception as e:
                print(f"删除游客ID {visitor_id} 出现异常: {e}")
                results.append({"id": visitor_id, "status": "failed", "error": str(e)})
        
        return results

    def generate_virtual_person(self):
        """
        生成一个虚拟人物信息（包含合格的身份证号）
        :return: 包含姓名和身份证号的字典
        """
        import random
        from datetime import datetime, timedelta
        
        # 常见姓氏
        surnames = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴", 
                   "徐", "孙", "马", "朱", "胡", "林", "郭", "何", "高", "罗"]
        
        # 常见名字
        names = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军",
                "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞"]
        
        # 生成姓名
        surname = random.choice(surnames)
        name = random.choice(names)
        if random.random() > 0.7:  # 30%概率生成双字名
            name += random.choice(names)
        full_name = surname + name
        
        # 生成身份证号
        # 地区代码（使用常见的几个城市）
        area_codes = ["110101", "310101", "440101", "500101", "320101", "330101"]
        area_code = random.choice(area_codes)
        
        # 生成出生日期（1970-2000年之间）
        start_date = datetime(1970, 1, 1)
        end_date = datetime(2000, 12, 31)
        birth_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        birth_str = birth_date.strftime("%Y%m%d")
        
        # 生成顺序码（前两位随机，第三位表示性别）
        sequence = f"{random.randint(10, 99)}{random.choice([1, 3, 5, 7, 9])}"  # 奇数表示男性
        
        # 计算校验码
        id_17 = area_code + birth_str + sequence
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        
        sum_val = sum(int(id_17[i]) * weights[i] for i in range(17))
        check_code = check_codes[sum_val % 11]
        
        id_number = id_17 + check_code
        
        return {
            "name": full_name,
            "id_number": id_number,
            "birth_date": birth_date.strftime("%Y-%m-%d"),
            "gender": "男"
        }

    def show_current_status(self):
        """
        显示当前常用游客和观影计划的状态
        """
        print("=" * 60)
        print("📊 当前状态查询")
        print("=" * 60)
        
        # 初始化会话
        if not self.init_session():
            print("❌ 会话初始化失败")
            return False
        
        # 查询常用游客
        print("\n🧑‍🤝‍🧑 常用游客列表:")
        try:
            visitor_response = self.get_visitor_list()
            if self.is_success(visitor_response):
                result = visitor_response.json()
                if result.get('code') == 0 and result.get('data', {}).get('list'):
                    visitors = result['data']['list']
                    print(f"   共有 {len(visitors)} 个常用游客:")
                    for i, visitor in enumerate(visitors, 1):
                        name = visitor.get('name', 'N/A')
                        cert_no = visitor.get('certificateNo', 'N/A')
                        visitor_id = visitor.get('id', 'N/A')
                        print(f"   {i:2d}. {name} - {cert_no} (ID: {visitor_id})")
                else:
                    print("   ✅ 暂无常用游客")
            else:
                print("   ❌ 查询失败")
        except Exception as e:
            print(f"   ❌ 查询异常: {e}")
        
        # 查询观影计划
        print("\n🎬 观影计划列表:")
        try:
            plan_response = self.query_visit_plans()
            if self.is_success(plan_response):
                result = plan_response.json()
                if result.get('code') == 0 and result.get('data'):
                    plans = result['data']
                    print(f"   共有 {len(plans)} 个观影计划:")
                    for i, plan in enumerate(plans, 1):
                        plan_name = plan.get('visitPlanName', 'N/A')
                        plan_id = plan.get('id', 'N/A')
                        visitor_list = plan.get('visitorList', [])
                        visitor_names = [v.get('visitorName', 'N/A') for v in visitor_list]
                        print(f"   {i:2d}. {plan_name} (ID: {plan_id})")
                        print(f"       游客: {', '.join(visitor_names) if visitor_names else '无'}")
                else:
                    print("   ✅ 暂无观影计划")
            else:
                print("   ❌ 查询失败")
        except Exception as e:
            print(f"   ❌ 查询异常: {e}")
        
        print("=" * 60)
        return True

    def complete_visit_plan_flow(self, scenic_spots_id="1877339390596874240", 
                                staggered_reservation_daily_id="1953848719870361601",
                                visit_plan_name="陕西历史博物馆秦汉馆"):
        """
        完整的参观计划流程
        :param scenic_spots_id: 景区ID
        :param staggered_reservation_daily_id: 错峰预约日期ID
        :param visit_plan_name: 参观计划名称
        :return: 流程执行结果
        """
        print("=" * 60)
        print("开始执行完整的参观计划流程")
        print("=" * 60)
        
        # 步骤1: 初始化会话
        print("\n步骤1: 初始化会话...")
        if not self.init_session():
            print("❌ 会话初始化失败，无法继续")
            return False
        print("✅ 会话初始化成功")
        
        # 步骤2: 生成虚拟人物
        print("\n步骤2: 生成虚拟人物信息...")
        person = self.generate_virtual_person()
        print(f"✅ 生成虚拟人物: {person['name']}")
        print(f"   身份证号: {person['id_number']}")
        print(f"   出生日期: {person['birth_date']}")
        print(f"   性别: {person['gender']}")
        
        # 步骤3: 查询现有常用游客列表
        print("\n步骤3: 查询现有常用游客列表...")
        try:
            existing_visitors = self.get_visitor_list()
            if self.is_success(existing_visitors):
                result = existing_visitors.json()
                if result.get('code') == 0 and result.get('data', {}).get('list'):
                    visitor_list = result['data']['list']
                    print(f"✅ 查询到 {len(visitor_list)} 个现有常用游客:")
                    for i, visitor in enumerate(visitor_list[:5], 1):  # 只显示前5个
                        print(f"   {i}. {visitor.get('name', 'N/A')} - {visitor.get('certificateNo', 'N/A')}")
                    if len(visitor_list) > 5:
                        print(f"   ... 还有 {len(visitor_list) - 5} 个游客")
                else:
                    print("✅ 当前没有常用游客")
            else:
                print("⚠️ 查询常用游客列表失败，继续执行")
        except Exception as e:
            print(f"⚠️ 查询常用游客列表时出现异常: {e}，继续执行")

        # 步骤4: 保存新的常用游客信息
        print("\n步骤4: 保存新的常用游客信息...")
        try:
            # 先检查是否已存在相同身份证的游客
            existing_visitor_id = self.get_visitor_id_by_certificate(person['id_number'])
            if existing_visitor_id:
                print(f"✅ 发现已存在相同身份证的游客，游客ID: {existing_visitor_id}")
                visitor_id = existing_visitor_id
            else:
                # 保存新游客
                response = self.save_visitor(person['name'], person['id_number'])
                if self.is_success(response):
                    result = response.json()
                    if result.get('code') == 0:
                        visitor_id = result.get('data', {}).get('id')
                        print(f"✅ 新游客信息保存成功，游客ID: {visitor_id}")
                    else:
                        print(f"❌ 游客信息保存失败: {result.get('error', '未知错误')}")
                        return False
                else:
                    print("❌ 游客信息保存请求失败")
                    return False
        except Exception as e:
            print(f"❌ 保存游客信息时出现异常: {e}")
            return False
        
        # 步骤5: 查询现有观影计划列表
        print("\n步骤5: 查询现有观影计划列表...")
        try:
            existing_plans = self.query_visit_plans()
            if self.is_success(existing_plans):
                result = existing_plans.json()
                if result.get('code') == 0 and result.get('data'):
                    plan_list = result['data']
                    print(f"✅ 查询到 {len(plan_list)} 个现有观影计划:")
                    for i, plan in enumerate(plan_list[:3], 1):  # 只显示前3个
                        plan_name = plan.get('visitPlanName', 'N/A')
                        plan_id = plan.get('id', 'N/A')
                        visitor_count = len(plan.get('visitorList', []))
                        print(f"   {i}. {plan_name} (ID: {plan_id}, 游客数: {visitor_count})")
                    if len(plan_list) > 3:
                        print(f"   ... 还有 {len(plan_list) - 3} 个计划")
                else:
                    print("✅ 当前没有观影计划")
            else:
                print("⚠️ 查询观影计划列表失败，继续执行")
        except Exception as e:
            print(f"⚠️ 查询观影计划列表时出现异常: {e}，继续执行")

        # 步骤6: 创建游客列表
        print("\n步骤6: 创建游客列表...")
        visitors = [self.add_visitor(person['name'], "1", person['id_number'], "F")]
        print(f"✅ 游客列表创建完成: {visitors}")

        time.sleep(6)

        
        # 步骤7: 保存参观计划
        print("\n步骤7: 保存参观计划...")
        try:
            response = self.save_visit_plan(
                scenic_spots_id=scenic_spots_id,
                staggered_reservation_daily_id=staggered_reservation_daily_id,
                visit_plan_name=visit_plan_name,
                visitor_list=visitors
            )

            if self.is_success(response):
                print(response.text)
                result = response.json()
                if result.get('code') == 0:
                    plan_id = result.get('data', {}).get('id')
                    print(f"✅ 参观计划保存成功！")
                    print(f"   计划ID: {plan_id}")
                    print(f"   计划名称: {visit_plan_name}")
                    print(f"   游客姓名: {person['name']}")
                    print(f"   身份证号: {person['id_number']}")
                else:
                    print(f"❌ 参观计划保存失败: {result.get('error', '未知错误')}")
                    return False
            else:
                print("❌ 参观计划保存请求失败")
                return False
        except Exception as e:
            print(f"❌ 保存参观计划时出现异常: {e}")
            return False
        #
        # # 步骤7: 验证参观计划
        # print("\n步骤7: 验证参观计划...")
        # try:
        #     plan_ids = self.get_visit_plan_ids()
        #     if plan_id in plan_ids:
        #         print(f"✅ 参观计划验证成功，计划ID {plan_id} 存在于计划列表中")
        #     else:
        #         print(f"⚠️  警告: 计划ID {plan_id} 未在计划列表中找到")
        # except Exception as e:
        #     print(f"⚠️  验证参观计划时出现异常: {e}")
        #
        # print("\n" + "=" * 60)
        # print("🎉 完整流程执行成功！")
        # print("=" * 60)
        # print(f"📋 流程总结:")
        # print(f"   • 虚拟游客: {person['name']} ({person['id_number']})")
        # print(f"   • 游客ID: {visitor_id}")
        # print(f"   • 参观计划ID: {plan_id}")
        # print(f"   • 计划名称: {visit_plan_name}")
        # print("=" * 60)
        #
        # return {
        #     "success": True,
        #     "person": person,
        #     "visitor_id": visitor_id,
        #     "plan_id": plan_id,
        #     "plan_name": visit_plan_name
        # }


if __name__ == '__main__':
    # 使用示例 - 请替换为实际的参数值
    uid = "1955164012735762432"
    token = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ3ZWNoYXRfcHVibGljMSIsInVzZXJJZCI6IjE4Nzc1ODcyNjU3MDczMTUyMDAiLCJuYW1lIjoi5b6u5L-h5YWs5LyX5Y-35pWj5a6iIiwib3JnSWQiOiIxODc3MzM4MjQ2MDkyODE2Mzg0IiwiZGV2aWNlQ29kZSI6IiIsInNhbGVTdGF0aW9uSWQiOiIxODc3MzM4MjQ3NzcwNTM3OTg0IiwiY3VzdG9tZXJJZCI6IjE4Nzc1ODcyNjU4NTgzMTAxNDQiLCJzb2NpYWxDdXN0b21lcklkIjoxOTU1MTY0MDEyNzM1NzYyNDMyLCJleHAiOjE3NTUwNjg4MDB9.H5_3XiQqXCAZSao6b1i7kvRUlJQyhkkexB9cwI0LZQ3j6oHqwDIex76RvyaKgkQ83sqLO6gBEMYTsPADK6gF2yFP7_16d62SP9LdzV56fdYqMW09wNiq9-VGap7rUBFg8mWFyIhINSBJO3l_dVuNtqTkY3mCH7Mo9dNxiA4JW1s"
    
    # 创建实例
    visit_plan = VisitPlan(uid, token)
    
    # 📊 首先显示当前状态
    print("📊 查询当前状态...")
    visit_plan.show_current_status()
    
    print("\n" + "="*60 + "\n")
    
    # 🚀 执行完整流程：生成虚拟人物 -> 保存游客 -> 创建参观计划
    result = visit_plan.complete_visit_plan_flow(
        scenic_spots_id="1877339390596874240",
        staggered_reservation_daily_id="1953848719870361601",
        visit_plan_name="陕西历史博物馆秦汉馆"
    )
    
    if result and result.get('success'):
        print(f"\n🎯 可以使用以下信息进行后续操作:")
        print(f"   游客姓名: {result['person']['name']}")
        print(f"   身份证号: {result['person']['id_number']}")
        print(f"   游客ID: {result['visitor_id']}")
        print(f"   参观计划ID: {result['plan_id']}")
    
    # 📊 最后再次显示状态
    print("\n" + "="*60)
    print("📊 执行完成后的状态:")
    visit_plan.show_current_status()
    
    # ========== 其他示例代码（已注释） ==========
    
    # 示例1: 使用默认参数保存参观计划
    # visit_plan.main()
    
    # 示例2: 自定义游客信息保存参观计划
    # visitors = [
    #     visit_plan.add_visitor("张三", "1", "440101199901010001", "F"),
    #     visit_plan.add_visitor("李四", "1", "440101199902020002", "F")
    # ]
    # visit_plan.save_custom_visit_plan(
    #     scenic_spots_id="1877339390596874240",
    #     staggered_reservation_daily_id="1953848720004579328", 
    #     visit_plan_name="陕西历史博物馆参观",
    #     visitors=visitors
    # )
    
    # 示例3: 查询参观计划列表
    # visit_plan.init_session()
    # response = visit_plan.query_visit_plans()
    # visit_plan.print_response(response)
    
    # 示例4: 获取参观计划ID列表
    # visit_plan.init_session()
    # plan_ids = visit_plan.get_visit_plan_ids()
    
    # 示例5: 删除指定参观计划
    # visit_plan.init_session()
    # response = visit_plan.delete_visit_plan("计划ID")
    # visit_plan.print_response(response)
    
    # 示例6: 批量删除所有参观计划
    # results = visit_plan.batch_delete_visit_plans()
    # print(f"删除结果: {results}")
    
    # 示例7: 保存常用游客
    # visit_plan.init_session()
    # response = visit_plan.save_visitor("张延华", "372431197106191647")
    # visit_plan.print_response(response)
    
    # 示例8: 获取游客ID列表
    # visit_plan.init_session()
    # visitor_ids = visit_plan.get_visitor_ids()
    
    # 示例9: 根据证件号查找游客ID
    # visit_plan.init_session()
    # visitor_id = visit_plan.get_visitor_id_by_certificate("372431197106191647")
    # print(f"游客ID: {visitor_id}")
    
    # 示例10: 批量删除所有游客
    # results = visit_plan.batch_delete_visitors()
    # print(f"删除结果: {results}")
    
    # 示例11: 更新参观计划
    # visit_plan.init_session()
    # visitors = [visit_plan.add_visitor("更新后的姓名", "1", "新的证件号", "F")]
    # response = visit_plan.update_visit_plan(
    #     visit_plan_id="参观计划ID",
    #     visit_plan_name="更新后的计划名称",
    #     visitor_list=visitors
    # )
    # visit_plan.print_response(response)
    
    # 示例12: 生成单个虚拟人物
    # person = visit_plan.generate_virtual_person()
    # print(f"虚拟人物: {person}") 