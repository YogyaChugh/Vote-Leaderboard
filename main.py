import requests
import json
import pygame
import sys
import asyncio
import io
import threading
import appdirs
import os
import math
import webbrowser
from os import listdir
from os.path import isfile, join

data_dir = appdirs.user_data_dir("Vote-Leaderboard")
data_dir = os.path.join(data_dir, "pages")
file_main = os.makedirs(data_dir, exist_ok=True)
file_main = data_dir

onlyfiles = [f for f in listdir(file_main) if isfile(join(file_main, f))]

pygame.init()

prev_users = []
users = []

DONE = False
working = True
online = True

font2 = pygame.font.SysFont("Arial",30)
font3 = pygame.font.SysFont("Arial",20)
cookies = {"_journey_session": r"092w3pyayALznLj6CA7Aaj4DO7RjIIwmeimOZ8eHpulRZ5x3kv2r0W0SZHarO1yo3jiCiHYLQrhaVrcC3p4OcZSCRIRbVoGe8vuU1Bb8plgxVQEPl6tCE47qo2PSZte9ww21hw2x9uDGD24KpCc0iJpfz90NzyW5NCV2Wi%2FJEmnnuSgHJKZ4Y3%2F35TKMJ%2FyJO88LIFcitIfSCA0MctnoeuUsu644Z6D4BLSlqzAXsiUG7mhnKZRpwKATQcyGU12Hzx0x4HQyY2xVnheKaViAaPzu5NG1fOWUin4y5IHlOpAD1HWSaNsljdwMYVkXiA01Vx19HYQmGA9dbeuTlwPCY44tsGwZdGox4oD2VhmhxuvT06bfjdsoe7TfKYIyYSD%2BldMhHTCYI7P2FxHnIc2qaQj3bCRs5GhRfcgg89nlWTCxws%2Fm25ujYAnFW%2BKWJoQuXNtmyHWCN9az%2BiZfNvd%2Bs%2FZivB9IXPai6SA9whFAC5YTDUe9QplEwVfZUt0K7t4FAr98qyA8vlNXj3AIFQ0TlCct0psUD3xm24guO9T0oMbPK8ripwAU6uM2uq03FXqbdnxhLLufKddJP4snwRP15kh7iuz43xGqwEvff1UxAC8qDkrKPlsgBA84cG8J49qmljwmXyFkHR%2BRsW788pKOFGwCC%2BHXwNH8%2FmA3HvSLGcJFhsN%2F0%2BXXuT9vGZJJPtMbqlHRjaNDWaeR0BbcfTION%2BZFZBrzistOqQS4c7U1c1pZHcihPXRtLb6Y3j7mX%2BJCXhabyOEgq3zvmrVQfCOfuPe5lAj5aNNSxNCRqktFfbKBmWqUj4xpkndyNZO%2BJVodLdq7l5iyyaOv48NN%2FrjgIw0kf8gBB%2Bwjf4G648hZA8go9mGv74tpTsY86FkhwTMgc9xja1B01XIRVPBxpW25OllcW5745%2FtV9GdL41QoLFeD%2BcxxqibZ6yez--EUDjz31NKlVnWKSI--QisV846%2FmMvo3Muup3pLuA%3D%3D","cf_clearance": r"KdngfPEjYvAcZVIPdO_BQd2VaSMk2.R1eQSdyYxDVHk-1758554060-1.2.1.1-yIu17y2sr1zjYQC4k1Oi5IavrMHsI.k0k84j_nT5Nkbe7SIs0S2h0VlASENZW3TGr6Q5_OI2Na3Qv_O5HLcEf5UxSUF6l3OBZd5.sQwkYyLbVWVK20BUwcU9ZDdMdFBPITQfnU6WVxc_3PxHdcF9VzNcuuOPywPB9sj3gGO0AZeufjPdQrEBpa_kvU6.fpbU2_Q_hXQ0lj_b4.JvOypWvfRo3WB4E58KGev1AhbcZ9Q","cfz_zaraz-analytics": r"%7B%22_cfa_clientId%22%3A%7B%22v%22%3A%2258739887188831110%22%2C%22e%22%3A1789878230677%7D%2C%22_cfa_sId%22%3A%7B%22v%22%3A%2225866942546196180%22%2C%22e%22%3A1758555860032%7D%7D", "fs_uid": r"#ARN0J#f87ac407-1907-487c-8362-82dce0ad5254:48c55142-d7c4-4492-b1be-e7cc3872a5a9:1758444081917::2#/1789878222"}


def update(event, page_num, total):
    global prev_users, working, online, cookies, users
    working = True
    online = True
    for number in range(total):
        print(f"Doing for page {page_num+number}")
        try:
            a = requests.get(f"https://summer.hackclub.com/api/v1/users?page={page_num+number}",cookies=cookies, timeout=10)
            if a.status_code==503:
                try:
                    a = requests.get("https://www.example.com",cookies=cookies, timeout=4)
                    online = True
                except:
                    online = False
                working = False
                return
            else:
                b = json.loads(a.content)
                try:
                    if b["error"] == "Page out of bounds":
                        return
                except:
                    pass
        except requests.exceptions.Timeout:
            working = False
            return
        done = False
        if event.is_set():
            DONE = True
            return
        for k in b["users"]:
            doit = False
            img = requests.get(k["avatar"]).content
            img = io.BytesIO(img)
            img = pygame.image.load(img)
            img = pygame.transform.scale(img,(50,50))
            r = prev_users
            pos = 0
            for i in prev_users:
                if event.is_set():
                    doit = True
                    break
                if k["id"] == i["id"]:
                    doit = True
                    break
                if k["votes_count"]<i['votes_count']:
                    pos+=1
                else:
                    break
            if doit:
                break
            prev_users = r[:pos]
            if k["display_name"].strip()!="":
                try:
                    prev_users.append({"id": k["id"],"votes_count": k["votes_count"],"display_name": font2.render(k["display_name"],True,(0,0,0)),"votes_count_render": font2.render(str(k["votes_count"]),True,(0,0,0)),"avatar": img})
                    users.append({"id": k["id"],"votes_count": k["votes_count"],"display_name": k["display_name"],"avatar": k["avatar"]})
                except:
                    continue
            prev_users.extend(r[pos:])
            if event.is_set():
                done = True
                break
        with open(f"{file_main}/{page_num+number}.json",'w') as fil:
            json.dump({"users": users},fil)
    DONE = True


def something(event):
    print("started")
    global cookies, online, working, onlyfiles, prev_users
    total_pages = 0
    i = 0
    try:
        a = requests.get("https://summer.hackclub.com/api/v1/users?page=1",cookies=cookies, timeout=10)
        if a.status_code==503:
            try:
                a = requests.get("https://www.example.com",cookies=cookies)
                online = True
            except:
                online = False
            working = False
        else:
            b = json.loads(a.content)
            total_pages = b['pagination']['pages']
    except requests.exceptions.Timeout:
        working = False
    if working:
        threads = []
        while i<total_pages:
            t = threading.Thread(target=update, args=(event, i,20))
            t.start()
            threads.append(t)
            i+=20
        for h in threads:
            h.join()
    else:
        for dd in onlyfiles:
            with open(os.path.join(data_dir,dd)) as df:
                b = json.load(df)
                for k in b["users"]:
                    doit = False
                    img = requests.get(k["avatar"]).content
                    img = io.BytesIO(img)
                    img = pygame.image.load(img)
                    img = pygame.transform.scale(img,(50,50))
                    r = prev_users
                    pos = 0
                    for i in prev_users:
                        if event.is_set():
                            doit = True
                            break
                        if k["id"] == i["id"]:
                            doit = True
                            break
                        if k["votes_count"]<i['votes_count']:
                            pos+=1
                        else:
                            break
                    if doit:
                        break
                    prev_users = r[:pos]
                    if k["display_name"].strip()!="":
                        try:
                            prev_users.append({"id": k["id"],"votes_count": k["votes_count"],"display_name": font2.render(k["display_name"],True,(0,0,0)),"votes_count_render": font2.render(str(k["votes_count"]),True,(0,0,0)),"avatar": img})
                        except:
                            continue
                    prev_users.extend(r[pos:])
                    if event.is_set():
                        done = True
                        break
            if event.is_set():
                break
    print("ended")

async def main():
    global online, working, prev_users, DONE
    top = 0
    bottom = 40
    bg = pygame.image.load("assets/background.png")
    font = pygame.font.Font("assets/PlaypenSans-Bold.ttf",60)

    screen = pygame.display.set_mode((1100,619))
    heading = font.render("Vote Leaderboard", True, (94,60,48))

    base_rect = pygame.Rect(210,150,700,70)

    end_event = threading.Event()
    sigma = threading.Thread(target=something,args=(end_event,))
    sigma.start()
    clock = pygame.time.Clock()
    base_minus = 0
    updating = font2.render("Updating ...",True,(0,0,0))
    notworking = font3.render("SOM currently down ! Showing previous data",True,(0,0,0))
    offline = font3.render("No Internet Connection",True,(0,0,0))
    
    rety = pygame.Rect(950,20,130,40)
    tryt = font3.render("Refetch",True,(255,255,255))

    while True:
        screen.blit(bg,(0,0))
        screen.blit(heading, (280,5- base_minus))
        pygame.draw.rect(screen,(79,32,15),rety,border_radius=15)
        pygame.draw.rect(screen,(169,122,87),rety,2,15)
        screen.blit(tryt,(983,30))
        if not DONE and working:
            screen.blit(updating, (480,100-base_minus))
        if not working and online:
            screen.blit(notworking, (360,100-base_minus))
        if not online:
            screen.blit(offline, (430,100-base_minus))
        k = 0
        rectsdude = {}
        val = math.floor(top)
        d = prev_users.copy()
        while val!=math.floor(bottom) and val<len(d):
            pygame.draw.rect(screen,(0,0,0),(base_rect[0],base_rect[1]+(val*90) - base_minus,base_rect[2],base_rect[3]),3,20)
            temp = font2.render(f"#{val+1}",True,(0,0,0))
            screen.blit(temp,((base_rect[0]+10,base_rect[1]+18+(val*90)- base_minus)))
            screen.blit(d[val]["avatar"],(base_rect[0]+90,base_rect[1]+10+(val*90)- base_minus))
            screen.blit(d[val]["display_name"],(base_rect[0]+180,base_rect[1]+18+(val*90)- base_minus))
            rectsdude[val] = d[val]["display_name"].get_rect()
            rectsdude[val].topleft = (base_rect[0]+180,base_rect[1]+18+(val*90)- base_minus)
            screen.blit(d[val]["votes_count_render"],(base_rect[0]+620,base_rect[1]+18+(val*90)- base_minus))
            k+=1
            val+=1


        events = pygame.event.get()
        mousepos = pygame.mouse.get_pos()
        inone = False
        if rety.collidepoint(mousepos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            inone = True
        for p in rectsdude:
            if rectsdude[p].collidepoint(mousepos):
                pygame.draw.line(screen,(0,0,0),(rectsdude[p][0],rectsdude[p][1]+32),(rectsdude[p][0]+rectsdude[p][2],rectsdude[p][1]+32),3)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                inone = True
        if not inone:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in events:
            if event.type==pygame.QUIT:
                end_event.set()
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                if len(prev_users)!=0:
                    if event.y<0:
                        if base_rect[1]+(len(prev_users)*90)-base_minus+20>667:
                            base_minus += 80
                            if bottom!=len(prev_users) and base_minus>160:
                                top +=0.5
                                bottom +=0.5
                    elif event.y>=0:
                        if base_minus!=0:
                            base_minus -= 80
                            if top!= 0:
                                top -=0.5
                                bottom -=0.5
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rety.collidepoint(event.pos):
                    end_event.set()
                    sigma.join()
                    end_event.clear()
                    prev_users = []
                    working = True
                    online = True
                    DONE = False
                    sigma = threading.Thread(target=something,args=(end_event,))
                    sigma.start()
                if pygame.MOUSEWHEEL not in events:
                    for ad in rectsdude:
                        if (rectsdude[ad].collidepoint(event.pos)):
                            webbrowser.open(f"https://summer.hackclub.com/users/{d[ad]["id"]}")

        if DONE:
            end_event.set()
            sigma.join()

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
