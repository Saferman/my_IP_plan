import os
import random
import datetime
import math,re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from bs4 import BeautifulSoup
from pathlib import Path

new_html_dir = "newdata" # one-step得到的目录
rss_dir = "rss" # 生成的rss文件目录
posted_rss_dir = "posted_rss" # 已提交的rss文件目录
base_link = "https://cscodetutor.com/" #填入网站首页地址
batch_size = 30 #每多少个html组成一个rss
update_date = "2025-07-19" # 新文章更新日期
add_update = False # 是否进行重复判断，True为进行重复判断，False为不进行（会影响日期生成方式）
os.makedirs(rss_dir, exist_ok=True)

# 加载已提交的HTML文件记录
def load_posted_html_files():
    """
    从posted_rss目录下的所有RSS文件中提取已提交的HTML文件名
    返回一个集合，包含所有已提交的HTML文件名（不含.html后缀）
    """
    posted_files = set()
    
    if not os.path.exists(posted_rss_dir):
        print(f"📁 {posted_rss_dir} 目录不存在，跳过已提交文件检查")
        return posted_files
    
    rss_files = [f for f in os.listdir(posted_rss_dir) if f.endswith('.xml')]
    if not rss_files:
        print(f"📁 {posted_rss_dir} 目录下没有RSS文件")
        return posted_files
    
    print(f"📋 开始加载已提交的RSS文件...")
    
    for rss_file in rss_files:
        rss_path = os.path.join(posted_rss_dir, rss_file)
        try:
            tree = ET.parse(rss_path)
            root = tree.getroot()
            
            # 查找所有item元素
            for item in root.findall('.//item'):
                link_elem = item.find('link')
                if link_elem is not None and link_elem.text:
                    # 从链接中提取HTML文件名
                    link = link_elem.text
                    if link.startswith(base_link):
                        # 提取文件名部分（去掉base_link和.html后缀）
                        filename = link.replace(base_link, '').replace('.html', '')
                        posted_files.add(filename)
                        print(f"  📄 已提交: {filename}")
            
        except Exception as e:
            print(f"❌ 解析RSS文件 {rss_file} 时出错: {e}")
            continue
    
    print(f"✅ 共加载 {len(posted_files)} 个已提交的HTML文件")
    return posted_files

def random_date(year):
    """
    根据年份生成该年的某个随机日期
    """
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    rand_day = start + datetime.timedelta(days=random.randint(0, (end - start).days))
    rand_time = datetime.time(hour=random.randint(0, 23), minute=random.randint(0, 59))
    return datetime.datetime.combine(rand_day, rand_time).strftime("%a, %d %b %Y %H:%M:%S +0000")

def random_date_range(start_date_str, end_date_str):
    """
    根据指定的日期范围生成随机日期
    """
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    rand_day = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    rand_time = datetime.time(hour=random.randint(0, 23), minute=random.randint(0, 59))
    return datetime.datetime.combine(rand_day, rand_time).strftime("%a, %d %b %Y %H:%M:%S +0000")

def extract_between_tags(filepath):
    inside = False
    collected = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if '</header>' in line:
                inside = True
                continue
            if '<footer class="post-footer">' in line:
                break
            if inside:
                collected.append(line.strip())
    raw_html = ''.join(collected).replace('\n', '')
    # 清理非法字符（如控制字符）
    clean_html = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\u4E00-\u9FA5\u3000-\u303F\uFF00-\uFFEF]', '', raw_html)
    return clean_html

def main():
    # 根据add_update参数决定是否加载已提交的HTML文件
    posted_files = set()
    if add_update:
        posted_files = load_posted_html_files()
        print(f"🔍 启用重复判断模式")
    else:
        print(f"🚀 跳过重复判断模式")
    
    # 获取所有HTML文件并根据add_update参数决定是否过滤
    all_files = [f for f in os.listdir(new_html_dir) if f.endswith(".html")]
    available_files = []
    
    if add_update:
        # 过滤掉已提交的文件
        for file in all_files:
            html_name = file.replace('.html', '')
            if html_name not in posted_files:
                available_files.append(file)
            else:
                print(f"⏭️ 跳过已提交的文件: {file}")
    else:
        # 不进行重复判断，使用所有文件
        available_files = all_files
    
    print(f"📄 总文件数: {len(all_files)}, 可用文件数: {len(available_files)}")
    
    if not available_files:
        if add_update:
            print("❌ 没有可用的HTML文件，所有文件都已提交过")
        else:
            print("❌ 没有可用的HTML文件")
        return
    
    # 打乱可用文件顺序
    random.shuffle(available_files)
    total_batches = math.ceil(len(available_files) / batch_size)
    
    # 根据add_update参数决定日期生成策略
    if add_update:
        # 使用update_date到今天随机选择日期
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        print(f"📅 新文章日期范围: {update_date} 到 {today_str}")
    else:
        # 构建年份池,确保每个年份都比较均匀
        years = list(range(2016, 2026))
        year_pool = (years * ((len(available_files) // len(years)) + 1))[:len(available_files)]
        random.shuffle(year_pool)
        print(f"📅 使用历史年份池生成日期")
    
    print(f"🔄 将生成 {total_batches} 个RSS批次")
    
    for batch_idx in range(total_batches):
        batch_files = available_files[batch_idx * batch_size : (batch_idx + 1) * batch_size]
        rss_root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss_root, "channel")

        ET.SubElement(channel, "title").text = f"Batch {batch_idx + 1}"
        ET.SubElement(channel, "link").text = base_link
        ET.SubElement(channel, "description").text = "WordPress RSS Import Batch"

        for file_idx, filename in enumerate(batch_files):
            with open(os.path.join(new_html_dir, filename), "r", encoding="utf-8") as f:
                html = f.read()
            soup = BeautifulSoup(html, "html.parser")

            title_tag = soup.find("h1", class_="post-title")
            title = title_tag.get_text(strip=True) if title_tag else "Untitled"

            # 提取 <header> 到 <footer> 之间 HTML
            description_html = extract_between_tags(os.path.join(new_html_dir, filename))

            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = title
            ET.SubElement(item, "link").text = base_link + filename.replace(".html", "")
            
            # 根据add_update参数选择日期生成方式
            if add_update:
                ET.SubElement(item, "pubDate").text = random_date_range(update_date, today_str)
            else:
                ET.SubElement(item, "pubDate").text = random_date(year_pool.pop())
                
            ET.SubElement(item, "description").text = "<![CDATA[" + description_html + "]]>"

        rss_path = os.path.join(rss_dir, f"rss_{batch_idx + 1}.xml")
        rough_string = ET.tostring(rss_root, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        with open(rss_path, "w", encoding="utf-8") as f:
            f.write(reparsed.toprettyxml(indent="  "))
        
        print(f"✅ 生成RSS批次 {batch_idx + 1}: {len(batch_files)} 个文件")

if __name__ == "__main__":
    main()