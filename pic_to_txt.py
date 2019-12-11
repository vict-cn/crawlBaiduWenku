from aip import AipOcr
import os
import math

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
    
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
                ls.append([i['words'],i['location']['top'],i['location']['left'],i['location']['width']])
                if 3<len(i['words'])<7:
                    font_size=i['location']['width']//len(i['words'])
    write_to_file(ls,filename,font_size)

def write_to_file(ls,filename,font_size):
    with open(filename+'.txt','w',encoding='utf-8')as f:
        flags=False
        s=0
        for num,text in enumerate(ls):
            before_space=text[2]//font_size
            if flags:
                s=text[2]-s
                before_space=s//font_size
            f.write(' '*before_space)
            f.write(text[0])
            try:
                if math.fabs(ls[num][1]-ls[num+1][1])>5: #同一行的top相差不会很大
                    f.write('\n')
                    s=0
                    flags=False
                else:
                    flags=True
            except:
                pass
            
if __name__=='__main__':
    filename=''
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    parse_text(filename)
    

    
    
    