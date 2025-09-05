@echo off
chcp 65001 >nul
title 大文件检查工具

REM 设置当前目录为脚本所在目录
cd /d "%~dp0"

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python，请确保已安装Python并添加到系统PATH中
    echo.
    pause
    exit /b 1
)

REM 检查Python脚本是否存在
if not exist "check_large_files.py" (
    echo 错误：未找到check_large_files.py文件
    echo.
    pause
    exit /b 1
)

REM 运行Python脚本
python check_large_files.py

REM 如果Python脚本出错，显示错误信息
if %errorlevel% neq 0 (
    echo.
    echo 程序执行出现错误，错误代码：%errorlevel%
    pause
)

exit /b 0
