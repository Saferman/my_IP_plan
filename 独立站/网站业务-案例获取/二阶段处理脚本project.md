帮我实现python代码，，请提供代码就好了，不用自己去运行或者检查目录是否存在： 
新建一个newdata目录和newdata/img目录
第一步帮我预处理data目录下所有的html文件：

- 检查html里面的所有img标签的src是img/开头还是http开头，如果是http开头则下载资源到data/img目录下，注意文件名和后缀保持一致，并在下载完成后后替换img标签的src问本地相对路径。如果是img/开头检查data/img目录是否存在对应的资源文件。全部处理完成后后，如果所有的img标签的src都是指向本地资源则继续处理：把html文件里所有img标签的src路径为/wp-content/uploads/资源文件名，把这个html保存到newdata目录下，然后把涉及的img标签的资源从data/img复制到newdata/img目录下

第二步：
转换newdata目录下所有html文件的内容为WordPress RSS导入要求的示例文件（RSS 2.0格式），只生成一个RSS文件，其中html的内容和RSS的XML标签对应关系如下：
- 标题信息来自html的class为post-title的h1标签的text（需要去除空白字符）
- 正文内容来自header标签和footer标签之间的内容源码（不含header和footer标签）
- pubDate从2016年-2025年不同日期随机生成（保持RFC 2822格式），尽可能保证2016-2025每年都有并且每年数量差不多


请在第一步结束后input暂停一下然后再第二步