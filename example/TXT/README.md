## 爬TXT文件

### 用crawlBaiduWenku.py来爬取

> **运行之后会获得一个txt文件**
![效果还不错](https://img-blog.csdnimg.cn/20191210131354642.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)
>

### 也可以使用parse_to_txt.py（与上述一样）
### 有时候也可以用parse_to_doc.py

> 会获得一个doc文件（有时候内容为空）
> 使用这个的好处是：**有的文件显示效果比txt文件要好**
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210131807256.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210131854926.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)
> 

### 推荐

 1. 先使用parse_to_txt.py或者crawlBaiduWenku.py获取txt文件，与原文比对，若是就差几个空格，稍加修改即可
 2. 若是效果不好，可以尝试使用prase_to_doc.py来获取doc文件

**爬取txt比较简单，就介绍到这里**