# 一些抓取后发现的问题需要对抓取结果进行处理，一般都会更新到抓取代码里
from grab_csprojectedu.csprojectedu_main import filter_hexo_render_string
import os,re

'''
因为抓取的文章里面可能出现{{这样的字符，会导致Blog系统报错，所以在抓取后需要用这个脚本处理    
'''

def replace_placeholder_in_files(directory):
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.md'):  # 只处理以 .md 结尾的文件
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding="utf-8") as file:
                content = file.read()

            # 将 {{ 替换为空字符串
            content = filter_hexo_render_string(content)
            # 保存替换后的内容回原文件
            with open(filepath, 'w', encoding="utf-8") as file:
                file.write(content)

def rm_whitechar_of_files(directory):
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.md'):  # 只处理以 .md 结尾的文件
            filepath = os.path.join(directory, filename)
            new_filpath = os.path.join(directory, re.sub(r'\s+', '', filename))
            os.rename(filepath,new_filpath)

def replace_title_by_filename(directory):
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.md'):  # 只处理以 .md 结尾的文件
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding="utf-8") as file:
                content = file.read()
            # 文件名和title必须保持一致
            content = content.split("\n")
            content[1] = "title: " + filename.rsplit(".",1)[0]
            content = "\n".join(content)
            # 保存替换后的内容回原文件
            with open(filepath, 'w', encoding="utf-8") as file:
                file.write(content)

# 传入目录路径，例如 '_posts' 文件夹的路径
directory = '_posts'
# replace_placeholder_in_files(directory)
replace_title_by_filename(directory)
# rm_whitechar_of_files(directory)