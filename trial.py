import requests
import pygame
import sys
import io
import json
import os
import appdirs
from requests.adapters import HTTPAdapter
import threading

s = requests.Session()
s.mount('https://summer.hackclub.com', HTTPAdapter(max_retries=5))

data_dir = appdirs.user_data_dir("Vote-Leaderboard")
data_dir = os.path.join(data_dir, "pages")
file_main = os.makedirs(data_dir, exist_ok=True)
file_main = data_dir

prev_users = []

def update(l,f):
    global prev_users
    cookies = {"_journey_session": r"","cf_clearance": r"","cfz_zaraz-analytics": r"", "fs_uid": r""}
    page = 1
    for i in range(l,l+f):
        if not os.path.exists(f"pages/{i}.json"):
            a = requests.get(f"https://summer.hackclub.com/api/v1/users?page={i}",cookies=cookies)
            if a.status_code!=503:
                b = json.loads(a.content)
                with open(f"pages/{i}.json",'w') as file:
                    json.dump(b,file)
                print("Page: ",i)

threads = []
for i in range(11):
    t = threading.Thread(target=update,args=(1160+(i*3)+1,3))
    t.start()
    threads.append(t)
for i in threads:
    i.join()
