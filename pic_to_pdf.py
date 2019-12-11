# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 13:39:39 2019

@author: lwdnx
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,portrait
'''文件只用写入'''

def pic_to_pdf(filename):
    if '.pdf' not in filename:
        filename=filename+'.pdf'
    c = canvas.Canvas(filename)
    (w,h) = portrait(A4)
    for i in range(2):
        while True :
            try:
                c.drawImage(str(i+1)+'.png',0,0,w,h)
                c.showPage()
                break
            except:
                pass
    c.save()
    print('文件保存为{}.pdf'.format(filename))
    
if __name__=='__main__':
    filename=''
    pic_to_pdf(filename)
