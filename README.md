# book_spider
通用小说爬虫

一个非常基础简单的爬虫。通过配置ini文件，可以爬取不同网站的小说。
spider.py 是爬虫
txteditor.py 是针对不同语言，对爬取的文本进行简单排版
这两个py全都是在一个ini文件里配置的

提供了日本轻小说网站 小説家になろう 与 中文网络小说站 和图书 的两个ini，爬这两个网站只需要修改对应的ini文件中的内容即可使用

其他小说网站需要提供ini文件里 必填 内容的数据。

使用时请修改py文件中，main函数调用的ini文件。
