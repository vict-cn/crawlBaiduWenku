# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 19:07:20 2019

@author: lwdnx
"""

from aip import AipOcr
import requests

APP_ID = '17956307'
API_KEY = 'SfXrfdIysZE6HUPm5p8eYQ3P'
SECRET_KEY = 'O1TaCxmQ9EbMHDOQsp740cM6DxHVgLiK'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

options = {
        'detect_direction': "true",
#        'language_type': 'CHN_ENG',
        "detect_risk": "false",
}
image = get_file_content(str(i)+'.png')
result=client.basicGeneral(image,options)
with open('1.txt','a',encoding='utf-8')as f:
    for i in result['words_result']:
        f.write(i['words'])