@echo off
setlocal

:: 固定压缩文件名
set ZIP_NAME=OmniIP.zip
set REMOTE_HOST=8.210.22.195
set REMOTE_USER=root
set REMOTE_PORT=22
set REMOTE_DIR=/root/SynchronizedDirectory/

:: 1. 压缩当前目录
echo [*] Compressing current directory into %ZIP_NAME%...
powershell Compress-Archive -Path * -DestinationPath "%ZIP_NAME%" -Force

:: 2. 上传文件
if exist "%ZIP_NAME%" (
    echo [*] Uploading %ZIP_NAME% to %REMOTE_HOST%:%REMOTE_DIR% via port %REMOTE_PORT%...
    scp -P %REMOTE_PORT% -o StrictHostKeyChecking=no "%ZIP_NAME%" %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_DIR%

    if %ERRORLEVEL%==0 (
        echo [*] Upload successful. Cleaning up...
        del "%ZIP_NAME%"
    ) else (
        echo [!] Upload failed.
    )
) else (
    echo [!] Compression failed.
)

endlocal
pause
