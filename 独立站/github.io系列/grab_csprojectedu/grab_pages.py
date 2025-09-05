import os
import re
import random
import pickle
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import html2text as ht
from tqdm import tqdm

# 初始化 HTML 转 Markdown 工具
text_maker = ht.HTML2Text()

# 全局变量
ARCHIVE_URL = "https://csprojectedu.com/archives"
POSTS_DIR = "_posts"
TITLE2DATE_FILE = "title2date_dict.pk"
LAST_PK_FILE = "last.pk"

# 确保输出目录存在
os.makedirs(POSTS_DIR, exist_ok=True)


def get_html(url):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        )
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


def parse_datetime(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def is_noise_line(line):
    return (
        all(c.isspace() for c in line) or
        re.match(r'^\s*\d+\s*$', line) or
        line.strip() == "|"
    )


def sanitize_filename(name):
    name = re.sub(r'[\\/:\*\?"<>|]', '', name)
    return re.sub(r'\s+', '', name)


def filter_hexo_conflict(text):
    return (text
            .replace("{{", "_two big parantheses_")
            .replace("}}", "_two big parantheses_")
            .replace("{%", "_big paranthese with percent sign_"))


def standardize_md(md_text, title, date, tag, title2date):
    lines = [
        line for line in md_text.split("\n")
        if not is_noise_line(line)
    ]
    result_text = filter_hexo_conflict("\n".join(lines))

    # 日期处理与记录
    if title in title2date:
        date = title2date[title]
    else:
        year, rest = date.split("-", 1)
        year = int(year)
        year = max(2019, year - random.randint(1, 5)) if year >= 2023 else min(2023, year + random.randint(0, 2023 - year))
        date = f"{year}-{rest}"
        title2date[title] = date

    front_matter = f"---\ntitle: {title}\ndate: {date}\ntags: {tag}\n---\n"
    return front_matter + result_text


def load_pickle(file_path, default=None):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
    return default if default is not None else {}


def save_pickle(file_path, obj):
    with open(file_path, "wb") as f:
        pickle.dump(obj, f)


def process_archive_page(page, success_titles, title2date):
    url = ARCHIVE_URL if page == 1 else f"{ARCHIVE_URL}/page/{page}/"
    soup = BeautifulSoup(get_html(url), 'html.parser')
    new_count = 0

    for h1 in soup.select('h1.post-title'):
        title_raw = h1.text
        title = sanitize_filename(title_raw)

        if "作业代写" in title or title in success_titles:
            continue

        tag = title.split("：")[0] if "：" in title else "其他"
        save_path = os.path.join(POSTS_DIR, f"{title}.md")

        if os.path.exists(save_path):
            continue

        article_url = "https://csprojectedu.com" + h1.a['href']
        article_soup = BeautifulSoup(get_html(article_url), 'html.parser')

        content_html = article_soup.select_one('div.post-body').prettify()
        md_text = text_maker.handle(content_html)
        date_str = article_soup.select_one('time[itemprop="dateCreated"]')['datetime']
        date = parse_datetime(date_str)

        md_final = standardize_md(md_text, title, date, tag, title2date)

        with open(save_path, 'w', encoding="utf-8") as f:
            f.write(md_final)

        new_count += 1

    return new_count


def main():
    title2date = load_pickle(TITLE2DATE_FILE, {})
    last_titles = list(load_pickle(LAST_PK_FILE, {}).keys())

    try:
        start_str, end_str = input(">请输入起始抓取页码和结束页码（不含），用英文逗号分隔: ").strip().split(",")
        start_page = int(start_str)
        end_page = int(end_str)
    except ValueError:
        print("输入格式错误，应为：起始页码,结束页码（例如 1,5）")
        return

    total_new = 0
    with tqdm(total=end_page - start_page) as pbar:
        for page in range(start_page, end_page):
            new_count = process_archive_page(page, last_titles, title2date)
            total_new += new_count
            save_pickle(TITLE2DATE_FILE, title2date)
            pbar.update(1)

    print(f"[+] 新增文章 {total_new} 篇")


if __name__ == "__main__":
    main()
