# -*- coding: utf-8 -*-
# 小说文本后处理
# 智能处理，输出txt,epub
import configparser
#基础检查下非法文本

#记录上一行的代码
last_line=0
def validate_line_jp(text):
	if text=="\n":
		return 4
	text=text.strip()
	if text=="(" or text==")" or text=="[" or text=="]" or text=="《" or text=="》":
		return 1
	elif text=="・":
		return 2
	elif len(text)==1:
		return 3
	else:
		return 0


def main(inidir="core.ini"):
	conf = configparser.ConfigParser()
	conf.read(inidir, encoding="utf-8")
	bookdir=conf["site"]["title"]+"-"+conf["site"]["author"]
	newbook=""
	with open(bookdir+f"/{bookdir}.txt",'r',encoding='utf-8') as f:
		line=f.readline()
		newbook+=line
		while True:
			line=f.readline()
			if not line:
				break
			if conf["cfg"]["language"]=="zh":
				pass
			elif conf["cfg"]["language"]=="jp":
				num=validate_line_jp(line)
				new_line=line.strip()
				if num==0 and last_line!=1:
					newbook+="\n"+new_line
				elif num==1:
					newbook+=new_line
				elif num==2:
					newbook+="!"
				elif num==3:
					newbook+=new_line
				elif num==4:
					newbook+="\n"
				else:
					newbook+=new_line
				last_line=num
			elif conf["cfg"]["language"]=="en":
				pass
			else:
				print("不支持的文件语言设置")
				break
	print(f'正在整理{conf["site"]["title"]}')
	with open(bookdir+f"/{bookdir}.txt",'w',encoding='utf-8') as f:
		f.write(newbook)
	print(f'{conf["site"]["title"]}整理完毕')

if __name__ == '__main__':
	main("失踪する猫.ini")