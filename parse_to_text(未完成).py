from aip import AipOcr
import requests
import os

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
filename='冷链物流企业排名'
APP_ID = '17956307'
API_KEY = 'SfXrfdIysZE6HUPm5p8eYQ3P'
SECRET_KEY = 'O1TaCxmQ9EbMHDOQsp740cM6DxHVgLiK'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)    
def parse_text(filename):
    options = {
            'detect_direction': "true",
            "detect_risk": "false",
    }
    ls=[]
    for i in os.walk(filename).__next__()[2]:
        if '.png' in i:
            image = get_file_content('{}/{}'.format(filename,i))
            result=client.accurate(image,options)
            for i in result['words_result']:
                ls.append([i['words'],i['location']['top']])
    write_to_file(ls,filename)

def write_to_file(ls,filename):
    with open(filename+'.txt','w',encoding='utf-8')as f:
        for num,text in enumerate(ls):
            try:
                if ls[num] != ls[num+1]:
                    f.write(text[0]+'\n')
                else:
                    f.write(text[0])
            except:
                pass
            
if __name__=='__main__':
    filename='冷链物流企业排名'
    APP_ID = '17956307'
    API_KEY = 'SfXrfdIysZE6HUPm5p8eYQ3P'
    SECRET_KEY = 'O1TaCxmQ9EbMHDOQsp740cM6DxHVgLiK'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    parse_text(filename)
    
    

    
    
    