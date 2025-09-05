### Browseruse

我想首先访问https://csprojectedu.com/，网站然后点击每篇显示的文章的标题（这样才能看到完整文章），然后保存xpath为//*[@id="posts"]/article的标签和标签里面的所有html代码到当前目录的html文件（文件名六位大小写字母数字随机），然后返回继续点击下一篇的文章，直到这一页的点击完成，然后在下面点击翻页直到所有文章都抓取完毕。请帮我把这个任务用英文整理成提供给browseruse的描述


### playwright
我想首先访问https://csprojectedu.com/，然后点击显示的每篇文章的标题（xpath是"//a[@class='post-title-link']"，保存文章的标题（就是这个xpath的text()用于后面保存取文件名，注意帮我去除windows系统文件名不支持的字符），点击后会打开这篇文章全文，我想保存xpath为//*[@id="posts"]/article的标签和标签里面的所有html代码到data目录下的html文件（文件名用前面保存的标题），然后返回继续点击下一篇的文章，直到这一页的点击完成，然后在下面点击翻页（a[@class='extend next']）直到所有文章都抓取完毕。
请帮我实现playwright代码