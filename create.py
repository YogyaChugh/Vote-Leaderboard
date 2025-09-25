import json
import datetime

users = []
for i in range(1,1193):
    with open(f"pages/{i}.json") as ff:
        data = json.load(ff)
    for da in data["users"]:
        id = da["id"]
        display_name = da["display_name"]
        votes_count = da["votes_count"]
        avatar = da["avatar"]
        r = users
        pos = 0
        for dj in users:
            if da["id"] == dj["id"]:
                doit = True
                break
            if da["votes_count"]<dj['votes_count']:
                pos+=1
            else:
                break
        users = users[:pos]
        users.append({"id": da["id"],"votes_count": da["votes_count"],"display_name": da["display_name"],"avatar": da["avatar"]})
        users.extend(r[pos:])
    print(f"Page: {i}")

with open("fallback.json",'w') as jfile:
    now = datetime.datetime.now()
    json.dump({"users": users,"time": str(now),"count": 1193},jfile)