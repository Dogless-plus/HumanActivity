# coding=utf-8

from requests.auth import HTTPBasicAuth
import requests
import pandas as pd
from os import mkdir,sep
import re
import json
from datetime import datetime
from redis_util import RedisCache
from time import sleep


authinfo = HTTPBasicAuth("user","passwd")    # todo :replace user,passwd here
name="wonderb0lt"
trace_folder = "trace"
info_folder = "info"
r = RedisCache()

try:
    mkdir(trace_folder)
except:
    pass
try:
    mkdir(info_folder)
except:
    pass

def fetchone_proxy():
    # one_proxy = {"https": "https://1.180.4.169:10519", }
    pass

def get_trace_info_one(name,proxy=None):
    url_trace_template = r"https://github.com/{0}"
    url_info_template="https://api.github.com/users/{0}"
    trace_pattern = re.compile(r"data-count=\"(.*?)\" data-date=\"(.*?)\"\/")
    text = requests.get(url_trace_template.format(name),proxies=proxy,auth = authinfo).text
    trace = re.findall(pattern=trace_pattern,string=text)

    info_page = requests.get(url_info_template.format(name),proxies=proxy,auth =authinfo).text
    info_dict = json.loads(info_page)
    use_info=info_dict["followers"],info_dict["following"],info_dict["location"],info_dict["public_gists"],info_dict["public_repos"]
    url_follower = info_dict["followers_url"]
    url_following = url_follower.replace("followers","following")
    follower_page = requests.get(url_follower,auth=authinfo).text
    followers = set( [item ["login"] for item in json.loads(follower_page)])
    # following_page = requests.get(url_following,auth=authinfo).text    #todo : reduce api times
    # followings = set( [item ["login"] for item in json.loads(following_page)])
    followings=set([])
    new_names = list(followers|followings)

    if len(trace) and len(use_info):
        pd.DataFrame(trace).to_csv(trace_folder+sep+name+".csv",header=None,index=False,encoding="utf-8")
        with open(info_folder+sep+name+".csx","wt") as f:
            f.write("|||".join([str(si) for si in use_info]))
        # print(trace)
        # print(new_names)
        real_newnames = [name for name in new_names if not r.isin_set(name)]
        print("new names for %s: %s/%s" %(name, len(real_newnames),len(new_names)))
        if real_newnames:
            r.append_list(*real_newnames)
        return "success"
    else:
        return "fail"

def fetch_worker():
    global r
    while r.size_list():
        tryloop = 14
        t0= datetime.now()
        name = r.lpop_list()
        if r.isin_set(name):
            continue
        while tryloop:
            try:
                status = get_trace_info_one(name)
                if status == "success":
                    r.push_set(name)
                else:
                    r.append_list(name)
                t1=datetime.now()
                print("[OK] ",name," timeused:",t1-t0," @",t1, "now n_names:",r.size_list())
                break
            except:
                sleep(3)
                r = None
                r = RedisCache()
                tryloop-=1
                print("tryloop:",tryloop,"@",name)
        if not tryloop:
            r.append_list(name)
            t1=datetime.now()
            print("[Warn] some error",name," @",t1,"now n_names:",r.size_list())

if __name__ == '__main__':
    fetch_worker()