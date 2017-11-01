from multiprocessing import Pool
from page_parsing import get_links_from, get_item_info
from tongcheng import get_channel_links
import pymongo
#获取所有频道页的主链接
start_url = 'http://bj.58.com/sale.shtml'
channel_links = get_channel_links(start_url)
all_channel_urls = [data['link'] for data in channel_links]
#print(all_channel_urls)

#定义每个频道爬取前100页的函数
def get_all_links_from(channel):
    #获取每个频道页的商品链接
    for num in range(1, 101):
        get_links_from(channel, num)

client = pymongo.MongoClient('localhost', 27017)
tongcheng = client['tongcheng']
url_list = tongcheng['url_lists']
#建立一个进程池，其中的processes参数可以设置进程的个数，一般来说，CPU是几核就设置多少
#不设置processes，会根据电脑自动分配
if __name__=='__main__':
    #pool = Pool(processes=4)
    pool = Pool()
    #不同进程爬取商品的url
    #pool.map(get_all_links_from, all_channel_urls)
    #不同进程爬取商品信息
    item_urls = [data['url'] for data in url_list.find()]
    pool.map(get_item_info, item_urls)