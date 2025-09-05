import os


def func(path):
    # 创建一个文件列表以存储文件名
    files_list = []
    # 获取当前目录的所有文件（包括文件夹）
    files = os.listdir(path)

    # 获取当前目录的所有文件（包括文件夹）
    for i in files:
        # 判断当前对象是文件or文件夹
        if os.path.isdir(path + os.sep + i):
            # 是文件夹，则把文件夹的名字添加进目录中，得到新路径
            new_path = path + os.sep + i
            # 然后传入新路径递归执行函数
            files_list = func(new_path) + files_list
        else:
            # 是文件，直接把文件名添加进入文件列表
            with open(path + os.sep + i, "r") as file:
                s = file.readlines()
                r = s.find("secret")
                if r != -1:
                    files_list.append(i)
    # 递归结束，返回文件列表                  
    return files_list


files_list = func('files')
print(files_list)