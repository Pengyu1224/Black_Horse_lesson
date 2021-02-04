import requests
from bs4 import BeautifulSoup
import pandas as pd
#得到页面内容并转化为BS对象
def get_page_content(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(url,headers=headers,timeout=10)
    content = html.text
    #通过content创建BS对象
    soup = BeautifulSoup(content,'html.parser')
    return soup

#解析当前页面内容
def analysis(soup):
    #找到具备完整投诉信息的类
    temp = soup.find('div',class_='tslb_b')
    tr_list = temp.find_all('tr')#找到所有的行
    #创建DataFrame,对要爬取数据的各字段进行命名
    df = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
    
    for tr in tr_list:
        #提取汽车各项投诉信息,解析各字段，放入DataFrame中
        info = {}
        td_list = tr.find_all('td')#找到一行中所有的列
        if len(td_list) >0:#第一行中没有td，进行判断，其余有数据的都有多个td
            id, brand, car_model, type, desc, problem, datetime, status = \
                td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            info["id"], info["brand"], info["car_model"], info["type"], info["desc"], info["problem"], info["datetime"], info["status"] = \
                id, brand, car_model, type, desc, problem, datetime, status
            df = df.append(info,ignore_index=True)
    return df
page_num = 30 #需要获取多少页信息
basic_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'#不带页码后缀的网页链接
result = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
#循环将每页信息写入DF
for i in range(page_num):
    url = basic_url+str(i+1)+'.shtml'#加上页码后缀组成每一页的完整链接
    soup = get_page_content(url)
    df = analysis(soup)
    result = result.append(df)
#提取结果保存为csv文件
result.to_csv('car_complain.csv',index=False)
