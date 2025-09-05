import asyncio
import os
import re
import urllib.parse
import aiohttp
import csv
import playwright
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# CSV记录文件路径
RECORD_FILE = "scraping_records.csv"

# 合法化文件名
def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    return name.strip()[:100]

# 加载已抓取的记录
def load_scraped_records() -> set:
    records = set()
    if Path(RECORD_FILE).exists():
        with open(RECORD_FILE, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['status'] == '1':  # 只跳过成功抓取的
                    records.add(row['title'])
    return records

# 记录抓取状态
def record_scraping_status(title: str, status: int, error_msg: str = ""):
    file_exists = Path(RECORD_FILE).exists()
    with open(RECORD_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['title', 'status', 'error_message'])
        writer.writerow([title, status, error_msg])

# 处理图片文件名冲突
def resolve_duplicate_filename(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    i = 1
    while True:
        new_path = base_path.with_name(f"{base_path.stem}.{i}{base_path.suffix}")
        if not new_path.exists():
            return new_path
        i += 1

# 直接返回HTML，不处理图片
def process_html(html: str) -> str:
    return html

early_stop = False
# 主程序
async def scrape_all_articles():
    # 不再需要创建img目录，因为不下载图片
    Path("data").mkdir(parents=True, exist_ok=True)
    
    # 加载已抓取的记录
    scraped_records = load_scraped_records()
    print(f"📋 已加载 {len(scraped_records)} 条抓取记录")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # 创建上下文时禁用图片加载
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = await context.new_page()
        
        # 禁用图片加载
        await page.route("**/*.{png,jpg,jpeg,gif,svg,webp}", lambda route: route.abort())

        await page.goto("https://csprojectedu.com/")
        
        # 连续跳过计数器
        consecutive_skipped = 0
        max_consecutive_skipped = 5
        
        while True:
            article_links = await page.locator("//a[@class='post-title-link']").all()
            print(f"📄 Found {len(article_links)} articles.")

            for i in range(len(article_links)):
                article_links = await page.locator("//a[@class='post-title-link']").all()
                link = article_links[i]

                raw_title = await link.inner_text()
                clean_title = sanitize_filename(raw_title)
                
                # 检查是否已经抓取过
                if clean_title in scraped_records:
                    consecutive_skipped += 1
                    print(f"⏭️ 跳过已抓取的文章: {clean_title} (连续跳过: {consecutive_skipped})")
                    
                    # 检查是否连续跳过次数达到阈值
                    if early_stop and consecutive_skipped >= max_consecutive_skipped:
                        print(f"🎯 连续跳过 {max_consecutive_skipped} 篇文章，推断已抓取完所有更新内容")
                        print("🚀 程序提前退出，所有新内容已抓取完毕！")
                        await browser.close()
                        return
                    continue
                
                # 重置连续跳过计数器（发现新文章）
                consecutive_skipped = 0
                save_path = Path("data") / f"{clean_title}.html"

                print(f"➡️ Opening article: {clean_title}")
                
                try:
                    await asyncio.sleep(1)
                    await link.click()
                    await page.wait_for_selector('//*[@id="posts"]/article')

                    article_elem = await page.locator('//*[@id="posts"]/article').element_handle()
                    html = await article_elem.inner_html()

                    # 处理HTML（不下载图片）
                    updated_html = process_html(html)

                    # 保存 HTML
                    save_path.write_text(updated_html, encoding='utf-8')
                    print(f"✅ HTML saved to {save_path}")
                    
                    # 记录成功状态
                    record_scraping_status(clean_title, 1)
                    print(f"📝 记录成功状态: {clean_title}")

                except Exception as e:
                    error_msg = str(e)
                    print(f"❌ 抓取失败: {clean_title}, 错误: {error_msg}")
                    # 记录失败状态
                    record_scraping_status(clean_title, 0, error_msg)

                await asyncio.sleep(1)
                try:
                    await page.go_back()
                except playwright._impl._errors.TimeoutError:
                    print("❗️ 返回上一页失败，可能是页面某些组件加载非常缓慢导致问题")
                    continue
                await page.wait_for_selector("//a[@class='post-title-link']")

            next_button = page.locator("//a[@class='extend next']")
            if await next_button.count() == 0 or not await next_button.is_visible():
                print("🏁 No more pages.")
                break
            else:
                await asyncio.sleep(1)
                await next_button.click()
                await page.wait_for_selector("//a[@class='post-title-link']")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_all_articles())
