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
        
def parse_txt(wenku_id):
    content_url = 'https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=' + wenku_id
    content = getHTMLText(content_url)
    md5 = re.findall('"md5sum":"(.*?)"', content)[0]
    pn = re.findall('"totalPageNum":"(.*?)"', content)[0]
    rsign = re.findall('"rsign":"(.*?)"', content)[0]
    content_url = 'https://wkretype.bdimg.com/retype/text/' + wenku_id + '?rn=' + pn + '&type=txt' + md5 + '&rsign=' + rsign
    content = json.loads(getHTMLText(content_url))
    result = ''
    for item in content:
        for i in item['parags']:
            result += i['c'].replace('\r\n\r\n','\r\n')
    return result

def main():
    url=input('请输入你要获取百度文库的URL连接：')
    html=getHTMLText(url)
    wenku_title=re.findall("\'title\'.*?\'(.*?)\'",html)[0]
    wenku_type=re.findall("\'docType\'.*?\'(.*?)\'",html)[0]
    wenku_id=re.findall("'docId'.*?'(.*?)'",html)[0]
    result=parse_txt(wenku_id)  
    filename=wenku_title+'.txt'
    with open(filename,'w',encoding='utf-8')as f:
        f.write(result)
    print('文件保存为{}.txt'.format(wenku_title))

main()





