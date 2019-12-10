
# 爬取BaiduWenku

## 需求是发明之母
**下载文库的文档又不想花钱和积分**

> 如果你和我有一样的想法就往下看，只要几分钟就可以看完，从今以后可以白嫖99%的文库了
***
## 使用方法

 **1. 下载本文档(当然也可以选择不下载)** 
 		

> git clone https://github.com/vict-cn/BaiduWenkuSpider

 **2. 安装依赖项(如果这些库你都有，也可以不安装)**
 

>  - 先用cmd切换到requirements.txt路径
>
> - **pip install -r https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt**

 **3. 下载PhantomJS(本文档自带)**

> - 然后将其添加到环境变量，若是不知道怎么做的，可以看我的一篇博客，或者搜索 PhantomJS配置即可
>
> - 因为selenium高版本不支持PhantomJS了，所以我们这里选择安装低版本的selenium

 **4. 运行CrawlBaiduWenku.py文件**
 

> 此时你就会得到你想要的(大概率是可行的)，要是爬取的不太理想，请继续阅读

***
## 使用说明(若是不想看文字，可以直接看example文件夹内的实例，或者直接各文件的作用)

>  - 爬**TXT**文件，爬取效果最好，可以选择可以使用**prase_to_txt.py**文件或者**parse_to_doc.py**文件，有时候后者比前者的效果要好，会生成一个**txt/doc**文件。[查看TXT实例](https://github.com/vict-cn/crawlBaiduWenku/tree/master/example/TXT)

> - 爬**PPT**文件，会生成一个文件夹，里面有PPT的所有图片，要是想直接生成PPT，运行**pic_to_ppt.py**，想生成pdf,可以运行**pic_to_pdf**。[查看PPT实例](https://github.com/vict-cn/crawlBaiduWenku/tree/master/example/PPT)

> - 爬**pdf**文件，速度较慢，会生成一个文件夹，里面有PDF的所有图片加上合起来的PDF文件（文件清晰度不是很高，这个有待提高）。[查看PDF实例
](https://github.com/vict-cn/crawlBaiduWenku/tree/master/example/PDF)

>- 爬**xls**文件，若是xls中有表格时(xls难道不就是表格文件？里面不都是表格？有时候还真不是),会生成一个文件内有表格的图片，里面都是表格图片（有时候图片会是分散的），要想生成xls文件，需要导入百度的识别表格API（此处留个链接）。若xls中全是文字的话，运行**Screenshot_to_pdf.py**文件，生成图片（速度有点慢），然后用**pdf_to_text.py**文件生成**txt/doc**[。
查看XLS实例](https://github.com/vict-cn/crawlBaiduWenku/tree/master/example/XLS)

 > - 爬**doc**文件，大难题就是它，若是纯文本则可以直接运行**parse_to_doc.py**文件(效果还不错)，若是图片少的时候，直接运行**parse_to_doc.py**文件生成doc文件，然后稍加修改，若是图片多的时候，可以考虑运行**Screenshot_to_pdf.py**文件，来生成图片(这里应该是最大的一个bug)。[查看DOC实例](https://github.com/vict-cn/crawlBaiduWenku/tree/master/example/DOC)
***
## 各文件的作用

 1. [crawlBaiduWenku.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/crawlBaiduWenku.py)
 	

> - 可以爬取 TXT / PDF / DOC / XLS /PPT 文件，生成对应的文件。

 2. [parse_to_txt.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/parse_to_txt.py)
 

> - 可以爬取TXT /  PDF / DOC / XLS  文件，生成txt文件。
> - **爬取TXT文件的效果最好。**

3. [parse_to_doc.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/parse_to_doc.py)

> - 可以爬取TXT /  PDF / DOC / XLS 文件，生成doc文件。
> - **爬取DOC与TXT文件的效果最好(有时候爬TXT简直不要太好。)**

4. [Screenshot_to_pdf.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/Screenshot_to_pdf.py)
> - 可以爬 TXT / PDF / DOC / XLS /PPT 文件，生成对应的截图还有合起来的pdf文件。
> - 对所有文件有用，缺点是清晰度不是很好，但是看的清楚。

5. [pic_to_pdf.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/pic_to_pdf.py)
> - 把文件夹的图片转化为pdf文件。

6. [pic_to_xls.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/pic_to_xls.py)
> - 把文件夹的表格转化为xls文件。

7. [get_pic.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/get_pic.py)
>- 获得每个网页的图片(有的文档可能解析不出来)。

***
## 声明
**除非选择下载文件，否则很难得到原来一模一样的文件，而爬取文件没有定式，爬TXT非要用parse_to_txt.py之类的，还有大把方法可以使用，没准那个就适合你要爬取的文件呢？**

