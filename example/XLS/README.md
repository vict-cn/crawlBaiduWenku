## 爬取XLS文件
### 用crawlBaiduWenku.py来爬取

> 会生成一个文件夹，里面含有所有xls文件的图片
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210151034157.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)
### 运行png_to_xls.py来转化png为xls
> 需要输入文件夹名称(上面可以得到)与APP_ID、API_KEY、SECRET_KEY（可以点击这个看怎么获得）
> 会在同目录生成xls文件。
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210151836830.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)

 **可以看到效果还不错(格式未识别)**

***但是！！！***

> 有的xls文件就不是这么友好了，比如下面这个文件
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210152640442.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)
> 它不会自动生成图片，**看这个排版，这难道不是doc文件？**
> 但是parse_to_doc有时候解析不出来(prase_to_txt可以，但是排版会乱)
> 这就会用到Screenshot_to_pdf.py来截图(参考PDF，速度较慢)，
> 然后使用pic_to_text.py来识别文字(点击)
> 
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20191210153559869.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)
### 推荐

 1. 判断文档的的表格是否完整
 2. 若是完整直接调用crawlBaiduWenku.py生成文件夹，然后运行pic_to_xls.py来生成表格
 3. 若是不完整，这就靠发挥了，是在不行直接截图然后识别，要是不想动，可以调用Screenshot_to_pdf.py来生成截图，然后在识别(此处应该有文件)。

### 局限

> - 还需要添加对图片文字识别的文件。
> - 精准度看照片的质量
> - 把多个xls文件合并为一个
