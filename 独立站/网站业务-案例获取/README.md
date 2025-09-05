这个项目是针对https://csprojectedu.com/的内容爬取框架，分为三个阶段

### playwright_spider.py
关闭所有图片加载，主要负责html内容抓取

### one_step.py
根据html抓取自媒体内容比如图片，然后修改图片路径为上传到wordpress后的相对路径

### two_step.py
转换newdata目录下所有html文件的内容为WordPress RSS导入要求的示例文件（RSS 2.0格式）

图片要单独上传