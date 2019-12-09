import requests
import re
import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,portrait
from PIL import Image
from selenium import webdriver
import time

def getHTMLText(url):
    try:
        r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print('有错误')  

def parse_doc(html): #这一块是重点
    result = ''
    url_list = re.findall('(https.*?0.json.*?)\\\\x22}', html)
    url_list = [addr.replace("\\\\\\/", "/") for addr in url_list]
    print(url_list)
    for url in url_list[:-5]:
        content = getHTMLText(url)
        y = 0
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', content)
        for item in txtlists:
            if not y== item[1]:   #一行都有一个标记值，可用标记值来判断是否元素在同一行
                y=item[1]   
                n='\n'           #若是y与标记值不相等，等则行，用'\n'
            else:
                n=''             #若是y与标记值相等，则不换行，用''
            result+=n            #连接时先连接n,再连接文字，这样可以很好的处理换行。
            result += item[0].encode('utf-8').decode('unicode_escape', 'ignore')
    return result

def main():
    url=input('请输入你要获取百度文库的URL连接：')
    html=getHTMLText(url)
    wenku_title=re.findall("\'title\'.*?\'(.*?)\'",html)[0]
    wenku_type=re.findall("\'docType\'.*?\'(.*?)\'",html)[0]
    wenku_id=re.findall("'docId'.*?'(.*?)'",html)[0]
    result=parse_doc(html)
    filename=wenku_title+'.doc'
    with open(filename,'w',encoding='utf-8')as f:
        f.write(result)
    print('文件保存为{}.doc'.format(wenku_title))

main()





