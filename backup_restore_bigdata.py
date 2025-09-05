import os
import zipfile
import tempfile
import json
import typer
import shutil
import socks
import httplib2
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

app = typer.Typer()

ARCHIVE_NAME = "bigdata_backup.zip"
MANIFEST_FILE = "manifest.json"
GDRIVE_FOLDER_ID = "YOUR_FOLDER_ID_HERE"  # 替换为你的Google Drive文件夹ID


def find_bigdata_dirs(root="."):
    bigdata_paths = []
    for dirpath, dirnames, _ in os.walk(root):
        for dirname in dirnames:
            if dirname == "bigdata":
                rel_path = os.path.relpath(os.path.join(dirpath, dirname), root)
                bigdata_paths.append(rel_path)
    return bigdata_paths


def zip_bigdata_dirs(bigdata_dirs, archive_path):
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for rel_path in bigdata_dirs:
            for foldername, _, filenames in os.walk(rel_path):
                for filename in filenames:
                    full_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(full_path, start=os.getcwd())
                    zipf.write(full_path, arcname)
        # 写 manifest
        with tempfile.NamedTemporaryFile('w+', delete=False) as mf:
            json.dump(bigdata_dirs, mf)
            mf.flush()
            zipf.write(mf.name, MANIFEST_FILE)


def create_proxy_http():
    proxy_info = httplib2.ProxyInfo(
        proxy_type=socks.PROXY_TYPE_SOCKS5,
        proxy_host='127.0.0.1',
        proxy_port=10808
    )
    return httplib2.Http(proxy_info=proxy_info)


def upload_to_drive(file_path, folder_id):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    http = create_proxy_http()
    gauth.credentials = gauth.credentials.authorize(http)
    drive = GoogleDrive(gauth)

    file_drive = drive.CreateFile({
        'parents': [{'id': folder_id}],
        'title': os.path.basename(file_path)
    })
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    typer.echo(f"✅ Uploaded to Google Drive with ID: {file_drive['id']}")


@app.command()
def backup():
    bigdata_dirs = find_bigdata_dirs()
    if not bigdata_dirs:
        typer.echo("❌ No 'bigdata' directories found. Backup skipped.")
        raise typer.Exit()

    typer.echo("📂 Found the following 'bigdata' directories:")
    for path in bigdata_dirs:
        typer.echo(f" - {path}")

    typer.echo("📦 Zipping...")
    zip_bigdata_dirs(bigdata_dirs, ARCHIVE_NAME)

    typer.echo("☁️ Uploading to Google Drive...")
    upload_to_drive(ARCHIVE_NAME, GDRIVE_FOLDER_ID)

    os.remove(ARCHIVE_NAME)
    typer.echo("✅ Backup completed.")


if __name__ == "__main__":
    app()
