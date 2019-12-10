from aip import AipOcr
import requests
import os

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
    
def parse_table(filename):
    options = {
            'detect_direction': "true",
            "detect_risk": "false",
    }
    for i in os.walk(filename).__next__()[2]:
        if '.png' in i:
            image = get_file_content('{}/{}'.format(filename,i))
            result=client.tableRecognition(image,options)
            r=requests.get(result['result']['result_data'],headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
            fname='{}/{}.xls'.format(filename,i[:-4])
            with open(fname,'wb')as f:
                f.write(r.content)
            print('生成{}.xls成功'.format(i[:-4]))
            
if __name__=='__main__':
    filename='物流设备采购清单明细'
    APP_ID = '17956307'
    API_KEY = 'SfXrfdIysZE6HUPm5p8eYQ3P'
    SECRET_KEY = 'O1TaCxmQ9EbMHDOQsp740cM6DxHVgLiK'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    parse_table(filename)
    
    

    
    
    