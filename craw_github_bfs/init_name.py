# coding =utf-8
import requests
import re
from time import sleep
from pickle import dump,load
from redis_util import RedisCache


logfile="init_names.pkl"
db = RedisCache()

names_list =[]
url_name_template = "https://github.com/search?p={0}&q={1}&type=Users"
name_pattern = re.compile(r"a href=\"\/(.*?)\"><img alt=")
def search_names():
    for search in [chr(i+ord('A')) for i in range(26)]:
        for page_i in range(1,101):
            while 1:
                url_name = url_name_template.format(page_i,search)
                name_page = requests.get(url_name).text
                page_names = re.findall(pattern=name_pattern,string=name_page)
                print(search,page_i,page_names)
                if len(page_names) > 0:
                    names_list.extend(page_names)
                    # sleep(0.3)
                    break
                else:
                    print("Error_retry after 1 min ...:",url_name)
                    sleep(60)
    all_names = list(set(names_list))
    with open(logfile,"wb") as f:
        dump(all_names,f)
    print("all crawed")

def init_names():
    with open(logfile,"rb") as f:
        names = load(f)
    print(names[:10])
    print(len(names)) # 20129
    db.empty_list()
    db.append_list(*names)
    print(db.size_list())


if __name__ == '__main__':
    # search_names()
    init_names()