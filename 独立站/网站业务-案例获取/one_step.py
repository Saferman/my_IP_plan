import os
import re
import shutil
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from pathlib import Path
from tqdm import tqdm

# CSV记录文件路径
IMAGE_RECORD_FILE = "image_download_records.csv"

# 新建目录
os.makedirs("newdata/img", exist_ok=True)

# 加载已下载的图片记录
def load_image_records() -> set:
    records = set()
    if Path(IMAGE_RECORD_FILE).exists():
        with open(IMAGE_RECORD_FILE, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['status'] == '1':  # 只检查成功下载的
                    img_path = row['image_path']
                    html_file = row['html_file']
                    # 检查图片文件是否仍然存在
                    if os.path.exists(img_path):
                        records.add((img_path, html_file))
    return records

# 记录图片下载状态
def record_image_download(image_path: str, html_file: str, status: int, error_msg: str = ""):
    file_exists = Path(IMAGE_RECORD_FILE).exists()
    with open(IMAGE_RECORD_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['image_path', 'html_file', 'status', 'error_message'])
        writer.writerow([image_path, html_file, status, error_msg])

# 第一阶段：预处理 HTML
html_dir = "data"
new_html_dir = "newdata"
new_img_dir = "newdata/img"

# 加载已下载的图片记录
image_records = load_image_records()
print(f"📋 已加载 {len(image_records)} 条图片下载记录")

def download_image(url, dest_dir, html_file, pbar=None):
    # 创建以HTML文件名命名的子目录
    html_name = os.path.splitext(html_file)[0]  # 去掉.html后缀
    html_img_dir = os.path.join(dest_dir, html_name)
    os.makedirs(html_img_dir, exist_ok=True)
    
    filename = os.path.basename(urlsplit(url).path)
    target = os.path.join(html_img_dir, filename)
    
    # 检查是否已经下载过
    relative_path = os.path.relpath(target, os.getcwd())
    if (relative_path, html_file) in image_records:
        if pbar:
            pbar.set_description(f"⏭️ 跳过: {filename}")
        return os.path.basename(target)
    
    try:
        if pbar:
            pbar.set_description(f"📥 下载: {filename}")
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            with open(target, "wb") as f:
                f.write(resp.content)
            if pbar:
                pbar.set_description(f"✅ 成功: {filename}")
            # 记录成功下载
            record_image_download(relative_path, html_file, 1)
            return os.path.basename(target)
        else:
            if pbar:
                pbar.set_description(f"❌ 失败: {filename}")
            record_image_download(relative_path, html_file, 0, f"HTTP {resp.status_code}")
    except Exception as e:
        if pbar:
            pbar.set_description(f"❌ 异常: {filename}")
        record_image_download(relative_path, html_file, 0, str(e))
    return None

# 获取需要处理的HTML文件列表
html_files = [f for f in os.listdir(html_dir) if f.endswith(".html")]
print(f"📄 找到 {len(html_files)} 个HTML文件需要处理")

# 主处理循环
for file in tqdm(html_files, desc="处理HTML文件", unit="file"):
    path = os.path.join(html_dir, file)
    
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    # 找到所有需要下载的图片
    images_to_download = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("http"):
            images_to_download.append((img, src))

    all_local = True
    # 下载图片进度条
    if images_to_download:
        pbar = tqdm(images_to_download, desc=f"下载图片 ({file})", unit="img", leave=False)
        for img, src in pbar:
            filename = download_image(src, new_img_dir, file, pbar)
            if filename:
                html_name = os.path.splitext(file)[0]  # 去掉.html后缀
                img["src"] = f"img/{html_name}/{filename}"
            else:
                all_local = False
                break
        pbar.close()

    if not all_local:
        tqdm.write(f"⚠️ 跳过文件 {file}，存在下载失败的图片")
        continue

    # 所有img标签都为本地，替换路径为wordpress的图片路径
    new_soup = BeautifulSoup(str(soup), "html.parser")
    for img in new_soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("img/"):
            # 从路径中提取文件名（去掉img/目录部分）
            fname = os.path.basename(src)
            img["src"] = f"/wp-content/uploads/{fname}"

    with open(os.path.join(new_html_dir, file), "w", encoding="utf-8") as f:
        f.write(str(new_soup))
    tqdm.write(f"✅ 完成处理: {file}")

input("✅ 第一步完成，按任意键继续执行第二步...")
