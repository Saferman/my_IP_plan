#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大文件检查工具
检查当前目录及所有子目录下是否存在大于等于50MB的文件
"""

import os
import sys
from pathlib import Path


def format_size(size_bytes):
    """将字节大小格式化为可读的格式"""
    if size_bytes >= 1024 * 1024 * 1024:  # GB
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    elif size_bytes >= 1024 * 1024:  # MB
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes >= 1024:  # KB
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} bytes"


def check_large_files(directory_path, size_limit_mb=50):
    """
    检查目录下的大文件
    
    Args:
        directory_path: 要检查的目录路径
        size_limit_mb: 文件大小限制（MB），默认50MB
    
    Returns:
        list: 包含大文件信息的列表
    """
    size_limit_bytes = size_limit_mb * 1024 * 1024  # 转换为字节
    large_files = []
    
    try:
        # 遍历目录及所有子目录
        for root, dirs, files in os.walk(directory_path):
            # 跳过常见的系统和版本控制目录
            skip_dirs = ['.git', '__pycache__', '.vscode', '.idea', 'node_modules', '.pytest_cache']
            for skip_dir in skip_dirs:
                if skip_dir in dirs:
                    dirs.remove(skip_dir)
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # 获取文件大小
                    file_size = os.path.getsize(file_path)
                    
                    # 如果文件大小超过限制
                    if file_size >= size_limit_bytes:
                        # 计算相对路径
                        relative_path = os.path.relpath(file_path, directory_path)
                        large_files.append({
                            'path': relative_path,
                            'size': file_size,
                            'size_formatted': format_size(file_size)
                        })
                        
                except (OSError, IOError) as e:
                    # 处理无法访问的文件（如权限问题）
                    print(f"警告：无法访问文件 {file_path}: {e}")
                    continue
                    
    except Exception as e:
        print(f"扫描目录时发生错误: {e}")
        return []
    
    return large_files


def main():
    """主函数"""
    print("=" * 60)
    print("大文件检查工具")
    print("=" * 60)
    print(f"正在检查当前目录及所有子目录下大于等于50MB的文件...")
    print("(跳过目录: .git, __pycache__, .vscode, .idea, node_modules, .pytest_cache)")
    print()
    
    # 获取当前工作目录
    current_dir = os.getcwd()
    print(f"检查目录: {current_dir}")
    print()
    
    # 检查大文件
    large_files = check_large_files(current_dir)
    
    if large_files:
        # 发现大文件，输出告警信息
        print("⚠️  告警：发现以下大文件（≥50MB）:")
        print("=" * 60)
        
        # 按文件大小降序排列
        large_files.sort(key=lambda x: x['size'], reverse=True)
        
        for i, file_info in enumerate(large_files, 1):
            print(f"{i:2d}. {file_info['path']}")
            print(f"    大小: {file_info['size_formatted']}")
            print()
        
        print(f"总计发现 {len(large_files)} 个大文件")
        print("=" * 60)
        print("建议：请检查这些大文件是否需要清理或移动到其他位置")
        
    else:
        # 没有发现大文件
        print("✅ 一切正常")
        print("当前目录及所有子目录下没有发现大于等于50MB的文件")
    
    print()
    print("=" * 60)
    
    # 等待用户按回车键退出
    try:
        input("按回车键退出程序...")
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"程序执行出错: {e}")
        input("按回车键退出...")
        sys.exit(1)
