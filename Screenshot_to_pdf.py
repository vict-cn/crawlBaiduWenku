# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 16:16:50 2019

@author: lwdnx
"""
import requests
import re
import os
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

def con_read(browser):  #点击继续阅读
    hidden_div = browser.find_element_by_css_selector('#html-reader-go-more')
    gotBtn = browser.find_element_by_css_selector('.moreBtn')
    actions = webdriver.ActionChains(browser)
    actions.move_to_element(hidden_div)
    actions.click(gotBtn)
    actions.perform()  
    time.sleep(20) 
    
def pic_crop(i,picture,browser,wenku_title):
    print('第{}页截图开始'.format(i))
    page_one = browser.find_element_by_id('pageNo-'+str(i))
    left = page_one.location['x']
    top = page_one.location['y']
    elementWidth = page_one.location['x'] + page_one.size['width']
    elementHeight = page_one.location['y'] + page_one.size['height']
    pic = picture.crop((left, top, elementWidth-50, elementHeight-50))
    pic.save('{}/第{}页图片.png'.format(wenku_title,i))
    time.sleep(2)
    print('第{}页截图成功'.format(i))

def pic_to_pdf(page_count,wenku_title):
    filename=wenku_title+'\\'+wenku_title+'.pdf'
    c = canvas.Canvas(filename)
    (w,h) = portrait(A4)
    print('开始写入pdf')
    for i in range(1,page_count+1):
        c.drawImage('{}/第{}页图片.png'.format(wenku_title,i),0,0,w,h)
        c.showPage()
    c.save()
    print('文件保存在{}文件夹下的{}.pdf中'.format(wenku_title,wenku_title))

def del_screen(wenku_title,page_count):
    print('开始删除截图')
    for i in range(2,page_count,3):
        os.remove('{}/第{}阶段截图.png'.format(wenku_title,i))
        if page_count%3==1 and page_count-2==i:
            os.remove('{}/第{}阶段截图.png'.format(wenku_title,i+1))
            break
    print('删除截图成功')
  
def screenshot(browser,wenku_title):
    if not os.path.exists(wenku_title):
        os.mkdir(wenku_title)
    page_count = int(browser.find_element_by_css_selector('.page-count').text[1:])
    print('开始截图')
    print()
    if page_count<=3:
        browser.save_screenshot('{}/第{}阶段截图.png'.format(wenku_title,1))
        picture=Image.open('{}/第{}阶段截图.png'.format(wenku_title,1))
        for i in range(1,page_count+1):
            pic_crop(i,picture,browser,wenku_title)
    else:
        for i in range(2,page_count,3):
            y_loc=browser.find_element_by_id('pageNo-{}'.format(str(i)))
            js="window.scrollTo(0,{})".format(str(y_loc.location['y']))
            browser.execute_script(js) 
            time.sleep(5)
            browser.save_screenshot('{}/第{}阶段截图.png'.format(wenku_title,i))
            
            picture=Image.open('{}/第{}阶段截图.png'.format(wenku_title,i))
            pic_crop(i-1,picture,browser,wenku_title)
            pic_crop(i,picture,browser,wenku_title)
            if page_count%3==2 and page_count==i: #爬取总也数为3*i+2中最后一页的情况
                pass
            else:
                pic_crop(i+1,picture,browser,wenku_title)
                
            if page_count%3==1 and page_count-2==i:    #爬取总页数为3*i+1中最后一页的情况
                y_loc=browser.find_element_by_id('pageNo-{}'.format(i+2))
                js="window.scrollTo(0,{})".format(str(y_loc.location['y']))
                browser.execute_script(js) 
                time.sleep(5)
                browser.save_screenshot('{}/第{}阶段截图.png'.format(wenku_title,i+1))
                picture=Image.open('{}/第{}阶段截图.png'.format(wenku_title,i+1))
                pic_crop(i+2,picture,browser,wenku_title)
                break
    pic_to_pdf(page_count,wenku_title)
    del_screen(wenku_title,page_count)

def parse_pdf(url,wenku_title):
    print('此过程较慢请稍后')
    browser=webdriver.PhantomJS()
    browser.get(url)
    browser.maximize_window()
    time.sleep(3)
    try:
        con_read(browser)
    except:
        pass
    screenshot(browser,wenku_title)

def main():
    url=input('请输入你要获取的网页：')
    html=getHTMLText(url)
    wenku_title=re.findall("\'title\'.*?\'(.*?)\'",html)[0]
    parse_pdf(url,wenku_title)
    
main()