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

def parse_doc(html): #这一块是重点
    result = ''
    url_list = re.findall('(https.*?0.json.*?)\\\\x22}', html)
    url_list = [addr.replace("\\\\\\/", "/") for addr in url_list]
    for url in url_list[:-5]:
        content = getHTMLText(url)
        y = 0
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', content)
        for item in txtlists:
            if not y== item[1]:
                y=item[1]   
                n='\n'
            else:
                n=''      
            result+=n   
            result += item[0].encode('utf-8').decode('unicode_escape', 'ignore')
    return result

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

def parse_other(wenku_id,wenku_title):
    content_url = "https://wenku.baidu.com/browse/getbcsurl?doc_id=" + wenku_id + "&pn=1&rn=99999&type=ppt"
    html=getHTMLText(content_url)
    img_url_ls=re.findall(r'"zoom".*?"(.*?)"',html)
    img_url_ls=[i.replace('\\','') for i in img_url_ls]
    if not os.path.exists(wenku_title): 
        os.mkdir(wenku_title)
        
    for i,j in enumerate(img_url_ls):
        filename='{}/{}.png'.format(wenku_title,i+1)
        with open(filename,'wb')as f:
            img=requests.get(j)
            f.write(img.content)
    print('图片保存在{} 文件夹内'.format(wenku_title))

def write_to_file(result,filename):
    with open(filename,'a',encoding='utf-8')as f:
        f.write(result)
    print('文件保存在{}中'.format(filename))

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
    print('删除截图')

def screenshot(browser,wenku_title):
    if not os.path.exists(wenku_title):
        os.mkdir(wenku_title)
    page_count = int(browser.find_element_by_css_selector('.page-count').text[1:])
    for i in range(2,page_count,3):
        print('截图开始')
        y_loc=browser.find_element_by_id('pageNo-{}'.format(str(i)))
        js="window.scrollTo(0,{})".format(str(y_loc.location['y']))
        browser.execute_script(js) 
        time.sleep(5)
        browser.save_screenshot('{}/第{}阶段截图.png'.format(wenku_title,i))
        
        picture=Image.open('{}/第{}阶段截图.png'.format(wenku_title,i))
        pic_crop(i-1,picture,browser,wenku_title)
        pic_crop(i,picture,browser,wenku_title)
        if page_count%3==2 and page_count==i:
            pass
        else:
            pic_crop(i+1,picture,browser,wenku_title)
            
        if page_count%3==1 and page_count-2==i:
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
        con_read(browser)
    screenshot(browser,wenku_title)


    
def main():
    url=input('请输入你要获取百度文库的URL连接：')
    html=getHTMLText(url)
    wenku_title=re.findall("\'title\'.*?\'(.*?)\'",html)[0]
    wenku_type=re.findall("\'docType\'.*?\'(.*?)\'",html)[0]
    wenku_id=re.findall("'docId'.*?'(.*?)'",html)[0]
    if wenku_type=='doc': 
        result=parse_doc(html)
        write_to_file(result,wenku_title+'.doc')
    elif wenku_type=='txt':
        result=parse_txt(wenku_id)
        write_to_file(result,wenku_title+'.txt')
    elif wenku_type=='pdf':
        parse_pdf(url,wenku_title)
    elif wenku_type=='xls':
        parse_other(wenku_id,wenku_title)
    else:
        parse_other(wenku_id,wenku_title)
    
if __name__=='__main__':
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    main()
    
    
    
    
    