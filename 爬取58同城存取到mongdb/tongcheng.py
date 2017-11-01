from bs4 import BeautifulSoup
import requests

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
            'catagory': cat,
            'link': 'http://bj.58.com'+str(link)
        }
        results.append(data)
    return results

#results = get_channel_links(start_url)
#print(results[0]['link'])
