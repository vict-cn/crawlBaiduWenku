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
        r=requests.get(url,headers=header)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print('有错误')
        
def get_pic_html(wenku_id):
    pic_url="https://wenku.baidu.com/browse/getbcsurl?doc_id=" + wenku_id + "&pn=1&rn=99999&type=ppt"
    return getHTMLText(pic_url)

def jud_pic(wenku_id,info_ls):
    html=get_pic_html(wenku_id)
    pic_ls=re.findall('&png=.*?-.*?&jpg=(.*?)-(.*?)",*?"page":(\d*?)}',html)
    for i in pic_ls:
        x=int(i[0])
        y=i[1]
        if y:
            y=int(i[1])
        else:
            y=0
        if y-x>0:   #此处的可能出现小bug，最后一个图片有可能xxxx
            info_ls.append([i[0],i[1],i[2]])
    if len(info_ls):
        return True
    else:
        return False
            
def pick_pic(wenku_id,info_ls,wenku_title):
    if not os.path.exists(wenku_title):
        os.mkdir(wenku_title)
    html=get_pic_html(wenku_id)
    img_start_url=re.findall(r'"zoom".*?"(.*?pn=)\d*?(&.*?jpg=)',html)[0]
    for i,item in enumerate(info_ls):
        url=img_start_url[0].replace('\\','')+item[2]+img_start_url[1]+item[0]+'-'+item[1]
        filename='{}/{}.png'.format(wenku_title,item[2])
        with open(filename,'wb')as f:
            img=requests.get(url,headers=header)
            f.write(img.content)
    print('文件保存在{}下'.format(wenku_title))
    
if __name__=='__main__':
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    url=input('请输入网址：')
    html=getHTMLText(url)
    wenku_title=re.findall("\'title\'.*?\'(.*?)\'",html)[0]
    wenku_id=re.findall("'docId'.*?'(.*?)'",html)[0]
    info_ls=[]
    flags=jud_pic(wenku_id,info_ls)
    pick_pic(wenku_id,info_ls,wenku_title)
    
    