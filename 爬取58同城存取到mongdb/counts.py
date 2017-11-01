import time
from page_parsing import url_list

while True:
    #find函数是在mongo数据库中进行查询
    print(url_list.find().count())
    time.sleep(5)