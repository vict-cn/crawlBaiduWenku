## 爬取DOC文件
### 用[crawlBaiduWenku.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/crawlBaiduWenku.py)爬取

> 会生成doc文件
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210155026637.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210185834929.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)

图一效果还不错

但是！！碰到带图片的那就没法看了

### 用[parse_to_pic.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/parse_to_pic.py)获取doc中的图片

> 生成一个文件夹，里面含有程序能够获取的图片(默认为png格式)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210192931863.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)

但是这种方法有时候无效，需要使用者稍加选择，是在不行就用[Screenshot_to_pdf.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/Screenshot_to_pdf.py)文件生成截图（迫不得已）

### 描述

 1. 若是doc文件为纯文本，则可以使用[crawlBaiduWenku.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/crawlBaiduWenku.py)或者[parse_to_doc.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/parse_to_doc.py)获得doc文件。
 2. 若是doc有图片，可以尝试使用[parse_to_pic](https://github.com/vict-cn/crawlBaiduWenku/blob/master/parse_to_pic.py).py。
 3. 若是上述两者无效，可以选择使用[Screenshot_to_pdf.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/Screenshot_to_pdf.py)文件

