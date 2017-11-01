import requests
from bs4 import BeautifulSoup
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
tongcheng = client['tongcheng']
url_list = tongcheng['url_lists']
item_info = tongcheng['item_info']
#为了防止每次运行代码时重复插入数据，可以每次插入前清空表
item_info.remove()
start_url = 'http://bj.58.com/sale.shtml'
def get_channel_links(url):
    results = []
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('#ymenu-side > ul > li > span > a')
    for i in range(len(links)):
        cat = links[i].text
        link = links[i].get('href')
        data = {
            'catagory':cat,
            'link': 'http://bj.58.com'+str(link)
        }
        results.append(data)
    return results

all_urls = [data['link'] for data in get_channel_links(start_url)]
#print(all_urls)
#who_sells代表是个人还是商家
#http://bj.58.com/shouji/1/pn1/?PGTID=0d300024-0000-1918-9eae-6ca4518e9a52&ClickID=1
def get_links_from(channel,pages,who_sells=0):
    #爬取这个频道的某一页，并解析出每个商品信息的url
    list_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #判断该页面是否有商品信息
    if soup.find('td','t'):
        for link in soup.select('td > a.t'):
            #print(link.get('href'),link.text)
            item_link = link.get('href').split('?')[0]
            if 'jump' not in item_link:
                url_list.insert_one({'url': item_link})
                print(item_link)
    else:
        pass

def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #判断不存在的即404页面
    #print(soup.find_all('script', type="text/javascript")[1])
    no_longer_exit= False
    for script in soup.find_all('script', type="text/javascript"):
        if script.get('src') is not None:
            if '404' in script.get('src').split('/'):
                no_longer_exit= True
    #no_longer_exit = '404' in soup.find_all('script', type="text/javascript")[1].get('src').split('/')
    if no_longer_exit:
        pass
    else:
        title = soup.title.text.strip()
        price = soup.select('span.price_now > i')[0].text if soup.find('span', 'price_now') else None
        address = soup.select('div.palce_li > span > i')[0].text if soup.find('div', 'palce_li') else None
        data = {
            'title': title,
            'price': price,
            'address': address,
            'url': url
        }
        item_info.insert_one(data)
        print(data)

#get_links_from(all_urls[0], 0, 0)
get_item_info('http://zhuanzhuan.58.com/detail/751793048516018180z.shtml')