''' created:2020.2.4
    author:huangxing
'''
import requests
import json
import re
from pymongo import MongoClient

def get_html(html):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response=requests.get(html,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        return None


def html_parse(response):
    if response == None:
        print('None')
    else:
        pattern=re.compile('<li data-rid="(\d+)".*?<h4>.*?data-bid=".*?">(.*?)</a>.*?data-eid=".*?">(.*?)</a>',re.S)
        items=pattern.findall(response)
        for item in items:
            yield {
                'book': item[1],
                'author': item[2]
            }


def save_html_parse(response):
    with open('qidian24xiaoshirexiaobang.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(response, ensure_ascii=False) + '\n')
        f.close()


def mongo_save(response):
    client = MongoClient()
    db = client.qidian24  # 数据库
    collection = db.xiaoshirexiaobang  # 集合
    result = collection.insert(response)  # 插入文档
    print(result)

if __name__ == '__main__':
    html=''
    for i in range(10):
        url='https://www.qidian.com/rank/hotsales?page='+str(i+1)

        html=(html+get_html(url))
    for item,i in zip(html_parse(html),range(200)):

        index={'index':i}
        item_1=dict(index,**item)
        save_html_parse((item_1))
        mongo_save(item_1)

        print(item_1)


