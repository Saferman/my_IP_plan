@echo off
setlocal

:: 设置变量
set ZIP_NAME=OmniIP.zip
set REMOTE_HOST=8.210.22.195
set REMOTE_USER=root
set REMOTE_PORT=22
set REMOTE_PATH=/root/SynchronizedDirectory/OmniIP.zip

:: 1. 下载压缩包
echo [*] Downloading %ZIP_NAME% from %REMOTE_HOST%...
scp -P %REMOTE_PORT% -o StrictHostKeyChecking=no %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH% "%ZIP_NAME%"

:: 2. 检查是否成功下载
if exist "%ZIP_NAME%" (
    echo [*] Extracting %ZIP_NAME% to current directory...
    powershell Expand-Archive -Path "%ZIP_NAME%" -DestinationPath "." -Force

    echo [*] Cleaning up...
    del "%ZIP_NAME%"
    echo [*] Done.
) else (
    echo [!] Download failed or ZIP file missing.
)

endlocal
pause
