## 爬PDF文件(速度有点慢)
### 思路

> 爬取PDF文件的思路是用**selenium+PhantomJS**先生成大截图，然后一段一段的截取。

## 用[crawlBaiduWenku.py](https://github.com/vict-cn/crawlBaiduWenku/blob/master/crawlBaiduWenku.py)来爬取
**特别提示：有时候因为网速原因会报错，可以考虑重新运行一遍。**
> 会生成一个文件夹， 里面含有**PDF的所有图片(默认格式为png)和一个PDF文件**。
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/2019121015054964.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTU3ODYwMA==,size_16,color_FFFFFF,t_70)

### 局限

 1. 清晰度不高
 2. 可以把png图片都转化为doc/txt格式

> 上述的两个问题也是这个项目后来的发展方向

**虽然清晰度不高，但是成功率挺高的。而且样式与之前差不多。**
