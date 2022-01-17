# -*- coding: utf-8 -*-
# 泛用小说爬虫
import configparser
import requests
from requests.packages import urllib3
from lxml import etree
import os
from urllib import parse
from tqdm import trange
from lxml import html
import re

#检测是否有非法字符
def validateTitle(title):
	rstr = r"[\/\\\:\*\?\"\<\>\|]" # '/ \ : * ? " < > |'
	new_title = re.sub(rstr, "_", title) # 替换为下划线
	return new_title

#参数是爬虫的配置文件
def book_spider(inidir="core.ini"):
	conf = configparser.ConfigParser()
	conf.read(inidir, encoding="utf-8")  
	urllib3.disable_warnings()
	print(f'开始爬取 《{conf["site"]["title"]}》')
	bookdir=conf["site"]["title"]+"-"+conf["site"]["author"]
	#新建书籍目录
	os.makedirs(bookdir, exist_ok=True)
	send_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"}
	#书籍主页
	novel = requests.get(url=conf["site"]["booksite"],verify=False,headers=send_headers)
	xml=bytes(bytearray(novel.text, encoding='utf-8')) 
	#取得目录
	link_list = etree.HTML(xml)
	links=link_list.xpath(conf["path"]["list"])


	abstract_content="\n\n"
	#取得书籍概要
	if conf["path"]["abstract"]!="None":
		abstract=link_list.xpath(conf["path"]["abstract"])
		for i in abstract:
			if conf["cfg"]["space"]=="True":
				abstract_content+=("  "+i+"\n")
			else:
				abstract_content+=(i+"\n")

	books=[]
	books.append(["小说概要",abstract_content])

	#获取书籍内容
	for i in links:
		bookurl=""
		if conf["cfg"]["abs"]=="False":
			bookurl=parse.urljoin(conf["site"]["index"],i)
		else:
			bookurl=i
		bookcontent=requests.get(url=bookurl,verify=False,headers=send_headers)
		xml=bytes(bytearray(bookcontent.text, encoding='utf-8')) 
		bookcontents=etree.HTML(xml)
		#章节标题
		section_title=bookcontents.xpath(conf["bookcontents"]["title"])
		title=""
		for j in section_title:
			title=(j+"\n")
		#章节内容
		section_content=bookcontents.xpath(conf["bookcontents"]["content"])
		content=""
		for j in section_content:
			if conf["cfg"]["space"]=="True":
				content+=("  "+j+"\n")
			else:
				content+=(j+"\n")
		books.append([title,content])
		print(f"{title} _ 已接收")

	#根据设置倒转书本
	if conf["cfg"]["invert"]=="True":
		books.reverse()

	print(f'开始输出{conf["site"]["title"]}')

	if conf["cfg"]["type"]=="全本":
		with open(bookdir+f"/{bookdir}.txt",'w',encoding='utf-8') as f:
			f.write("书名："+conf["site"]["title"]+"\n\n")
			f.write("作者："+conf["site"]["author"]+"\n\n")
			for i in trange(len(books)):
				f.write(books[i][0])
				f.write(books[i][1])
				f.write("\n\n")
	elif conf["cfg"]["type"]=="章节":
		for i in trange(len(books)):
			newbook=validateTitle(books[i][0]).strip()
			with open(bookdir+f"/{newbook}.txt",'w',encoding='utf-8') as f:
				f.write(books[i][0])
				f.write(books[i][1])
	elif conf["cfg"]["type"]=="卷":
		pass
	print(f'{conf["site"]["title"]}输出完毕')

if __name__ == '__main__':
	book_spider("失踪する猫.ini")



# print(a)
# print(conf["site"]["booksite"])