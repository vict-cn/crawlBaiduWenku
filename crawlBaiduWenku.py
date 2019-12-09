import requests
import re
import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,portrait
from PIL import Image
from selenium import webdriver
import time

'''
    获得百度文库的图片："https://wenku.baidu.com/browse/getbcsurl?doc_id=" + wenku_id + "&pn=1&rn=99999&type=ppt"
    
    txt :'https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=' + wenku_id
    
    
    大佬写的果然不一样，希望自己以后也能够写出这样的项目出来，感觉这其中包含的东西有点奇妙，编码与反编码之间的关系时间令人捉摸不透。
    
    缺点：很少有自己的想法，基本上都是照搬大佬的文件，（因为啥也不知道啊）
        对一部分doc文件不适用,对pdf文件，有的可以保存下来，有的不行。可能是百度文库拒绝了访问
        此外，也不能爬取需要VIP文档的后续部分。
    
    优点：了解了百度文库的组成（真尼玛的沙雕，也不知道为啥要搞这么麻烦，感觉这个大佬就是百度出来的）。
    
    
doc文件中貌似可以获得添加图片。先保存再说。
'''

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

def getWebInfo(soup):
    pass

def parse_doc(html): #这一块是重点
    result = ''
    url_list = re.findall('(https.*?0.json.*?)\\\\x22}', html)
    url_list = [addr.replace("\\\\\\/", "/") for addr in url_list]
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
            result += i['c'].replace('\\r', '\r').replace('\\n', '\n')
    return result

def parse_other(wenku_id,wenku_title):
    content_url = "https://wenku.baidu.com/browse/getbcsurl?doc_id=" + wenku_id + "&pn=1&rn=99999&type=ppt"
    html=getHTMLText(content_url)
    img_url_ls=re.findall(r'"zoom".*?"(.*?)"',html)
    img_url_ls=[i.replace('\\','') for i in img_url_ls]
    if not os.path.exists(wenku_title):   #这种写法可能存在已经存在文件的情况，不过影响不大。
#        shutil.rmtree(wenku_title)       # 其实不要这句最好,得不到的不一定要毁灭。
        os.mkdir(wenku_title)
        
    for i,j in enumerate(img_url_ls):
        filename='{}/第{}页图片.jpg'.format(wenku_title,i+1)
        with open(filename,'wb')as f:
            img=requests.get(j)
            f.write(img.content)
    print('图片保存在{} 文件夹内'.format(wenku_title))

def write_to_file(result,filename,flags,wenku_title):
    if flags:
        if not os.path.exists(wenku_title):
            os.mkdir(wenku_title)
        with open(wenku_title+'/'+filename,'a',encoding='utf-8')as f:
            f.write(result)
        print('文件保存在{}下的{}文件中'.format(wenku_title,filename))
    else:
        with open(filename,'a',encoding='utf-8')as f:
            f.write(result)
        print('文档保存在{} 文件中'.format(filename))

def jud_pic(wenku_id,info_ls):
    html=get_pic_html(wenku_id)
#    url_ls=re.findall(r'"zoom".*?"(.*?)"',html)
#    jpg_ls=re.search'"zoom".*?"(.*?)&jpg',html)
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
            
def pick_pic(wenku_id,info_ls,wenku_title,flags):
    if flags:
        html=get_pic_html(wenku_id)
        img_start_url=re.findall(r'"zoom".*?"(.*?pn=)\d*?(&.*?jpg=)',html)[0]
        for i,item in enumerate(info_ls):
            url=img_start_url[0].replace('\\','')+item[2]+img_start_url[1]+item[0]+'-'+item[1]
            filename='{}/{}.jpg'.format(wenku_title,item[2])
            with open(filename,'wb')as f:
                img=requests.get(url,headers=header)
                
                f.write(img.content)
    else:
        return ''

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
        con_read(browser)
    screenshot(browser,wenku_title)


    
def main():
    url=input('请输入你要获取百度文库的URL连接：')
#    url='https://wenku.baidu.com/view/a85d12f7fc4ffe473268ab1a.html?from=search'
    html=getHTMLText(url)
    wenku_title=re.findall("\'title\'.*?\'(.*?)\'",html)[0]
    wenku_type=re.findall("\'docType\'.*?\'(.*?)\'",html)[0]
    wenku_id=re.findall("'docId'.*?'(.*?)'",html)[0]
    info_ls=[]
    flags=jud_pic(wenku_id,info_ls)
    if wenku_type=='txt': #doc文件应该可以插入文件，明天试下。
        result=parse_doc(html)
        write_to_file(result,wenku_title+'.txt',flags,wenku_title)
    elif wenku_type=='txt': #txt文件最好别插入文件
        result=parse_txt(wenku_id)
        write_to_file(result,wenku_title+'.txt')
        flags=False
    elif wenku_type=='pdf':#pdf文件初步为=txt+img ,后来为word然后转成pdf 
        parse_pdf(url,wenku_title)
    elif wenku_type=='xls':  #xls图片部分有可能与文字重合，这个暂时不知道怎么判断
#        result=parse_doc(html) 
        parse_other(wenku_id,wenku_title)
#        write_to_file(result,wenku_title+'.txt',flags,wenku_title)
    else:#这个适用于PPT
        flags=False  
        parse_other(wenku_id,wenku_title)
    pick_pic(wenku_id,info_ls,wenku_title,flags)
    
if __name__=='__main__':
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    main()
    
    
    
    
    