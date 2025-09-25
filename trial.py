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
    cookies = {"_journey_session": r"092w3pyayALznLj6CA7Aaj4DO7RjIIwmeimOZ8eHpulRZ5x3kv2r0W0SZHarO1yo3jiCiHYLQrhaVrcC3p4OcZSCRIRbVoGe8vuU1Bb8plgxVQEPl6tCE47qo2PSZte9ww21hw2x9uDGD24KpCc0iJpfz90NzyW5NCV2Wi%2FJEmnnuSgHJKZ4Y3%2F35TKMJ%2FyJO88LIFcitIfSCA0MctnoeuUsu644Z6D4BLSlqzAXsiUG7mhnKZRpwKATQcyGU12Hzx0x4HQyY2xVnheKaViAaPzu5NG1fOWUin4y5IHlOpAD1HWSaNsljdwMYVkXiA01Vx19HYQmGA9dbeuTlwPCY44tsGwZdGox4oD2VhmhxuvT06bfjdsoe7TfKYIyYSD%2BldMhHTCYI7P2FxHnIc2qaQj3bCRs5GhRfcgg89nlWTCxws%2Fm25ujYAnFW%2BKWJoQuXNtmyHWCN9az%2BiZfNvd%2Bs%2FZivB9IXPai6SA9whFAC5YTDUe9QplEwVfZUt0K7t4FAr98qyA8vlNXj3AIFQ0TlCct0psUD3xm24guO9T0oMbPK8ripwAU6uM2uq03FXqbdnxhLLufKddJP4snwRP15kh7iuz43xGqwEvff1UxAC8qDkrKPlsgBA84cG8J49qmljwmXyFkHR%2BRsW788pKOFGwCC%2BHXwNH8%2FmA3HvSLGcJFhsN%2F0%2BXXuT9vGZJJPtMbqlHRjaNDWaeR0BbcfTION%2BZFZBrzistOqQS4c7U1c1pZHcihPXRtLb6Y3j7mX%2BJCXhabyOEgq3zvmrVQfCOfuPe5lAj5aNNSxNCRqktFfbKBmWqUj4xpkndyNZO%2BJVodLdq7l5iyyaOv48NN%2FrjgIw0kf8gBB%2Bwjf4G648hZA8go9mGv74tpTsY86FkhwTMgc9xja1B01XIRVPBxpW25OllcW5745%2FtV9GdL41QoLFeD%2BcxxqibZ6yez--EUDjz31NKlVnWKSI--QisV846%2FmMvo3Muup3pLuA%3D%3D","cf_clearance": r"KdngfPEjYvAcZVIPdO_BQd2VaSMk2.R1eQSdyYxDVHk-1758554060-1.2.1.1-yIu17y2sr1zjYQC4k1Oi5IavrMHsI.k0k84j_nT5Nkbe7SIs0S2h0VlASENZW3TGr6Q5_OI2Na3Qv_O5HLcEf5UxSUF6l3OBZd5.sQwkYyLbVWVK20BUwcU9ZDdMdFBPITQfnU6WVxc_3PxHdcF9VzNcuuOPywPB9sj3gGO0AZeufjPdQrEBpa_kvU6.fpbU2_Q_hXQ0lj_b4.JvOypWvfRo3WB4E58KGev1AhbcZ9Q","cfz_zaraz-analytics": r"%7B%22_cfa_clientId%22%3A%7B%22v%22%3A%2258739887188831110%22%2C%22e%22%3A1789878230677%7D%2C%22_cfa_sId%22%3A%7B%22v%22%3A%2225866942546196180%22%2C%22e%22%3A1758555860032%7D%7D", "fs_uid": r"#ARN0J#f87ac407-1907-487c-8362-82dce0ad5254:48c55142-d7c4-4492-b1be-e7cc3872a5a9:1758444081917::2#/1789878222"}
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