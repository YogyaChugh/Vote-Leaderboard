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
import datetime

data_dir = appdirs.user_data_dir("Vote-Leaderboard")
data_dir = os.path.join(data_dir, "pages")
file_main = os.makedirs(data_dir, exist_ok=True)
file_main = data_dir

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE = str(os.path.abspath(sys._MEIPASS))
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

onlyfiles = [f for f in os.listdir(file_main) if os.path.isfile(os.path.join(file_main, f))]

pygame.init()

prev_users = []
users = []
rectsdude = {}

DONE = False
working = True
online = True
REFETCH_ALLOW = True
COMPLETED = False
REFETCHED = False
SCREEN_UPDATED = True
TIMEJI = ""
TOTAL_PAGES = 1

font2 = pygame.font.SysFont("Arial",30)
font3 = pygame.font.SysFont("Arial",20)
cookies = {"_journey_session": r"","cf_clearance": r"","cfz_zaraz-analytics": r"", "fs_uid": r""}


def fetchprev(ev):
    global COMPLETED, prev_users, TIMEJI, SCREEN_UPDATED, TOTAL_PAGES, BASE
    COMPLETED = False
    prev_users = []
    if os.path.exists(os.path.join(data_dir,"fallback.json")):
        with open(os.path.join(data_dir,"fallback.json")) as ffff:
            somedata = json.load(ffff)
            TIMEJI = somedata["time"]
            TOTAL_PAGES = somedata["count"]
            for k in somedata["users"]:
                if ev.is_set():
                    return
                img = requests.get(k["avatar"]).content
                img = io.BytesIO(img)
                try:
                    img = pygame.image.load(img)
                except:
                    img = requests.get("https://ca.slack-edge.com/T0266FRGM-U015ZPLDZKQ-gf3696467c28-512").content
                    img = io.BytesIO(img)
                    img = pygame.image.load(img)
                img = pygame.transform.scale(img,(50,50))
                if k["display_name"].strip()!="":
                    try:
                        prev_users.append({"id": k["id"],"votes_count": k["votes_count"],"display_name": font2.render(k["display_name"],True,(0,0,0)),"votes_count_render": font2.render(str(k["votes_count"]),True,(0,0,0)),"avatar": img})
                        SCREEN_UPDATED = True
                    except:
                        continue
    else:
        with open(os.path.join(BASE,"fallback.json")) as ffff:
            somedata = json.load(ffff)
            TIMEJI = somedata["time"]
            TOTAL_PAGES = somedata["count"]
            for k in somedata["users"]:
                if ev.is_set():
                    return
                img = requests.get(k["avatar"]).content
                img = io.BytesIO(img)
                try:
                    img = pygame.image.load(img)
                except:
                    img = requests.get("https://ca.slack-edge.com/T0266FRGM-U015ZPLDZKQ-gf3696467c28-512").content
                    img = io.BytesIO(img)
                    img = pygame.image.load(img)
                img = pygame.transform.scale(img,(50,50))
                if k["display_name"].strip()!="":
                    try:
                        prev_users.append({"id": k["id"],"votes_count": k["votes_count"],"display_name": font2.render(k["display_name"],True,(0,0,0)),"votes_count_render": font2.render(str(k["votes_count"]),True,(0,0,0)),"avatar": img})
                        SCREEN_UPDATED = True
                    except:
                        continue
    COMPLETED = True
    REFETCHED = False
    

def update(event, page_num, total):
    global prev_users, working, online, cookies, users, SCREEN_UPDATED
    working = True
    online = True
    for number in range(total):
        if event.is_set():
            return
        try:
            a = requests.get(f"https://summer.hackclub.com/api/v1/users?page={page_num+number}",cookies=cookies, timeout=10)
            if a.status_code==503:
                try:
                    a = requests.get("https://www.example.com",cookies=cookies, timeout=4)
                    online = True
                except:
                    online = False
                working = False
                event.set()
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
            event.set()
            return
        done = False
        if event.is_set():
            DONE = True
            return
        for k in b["users"]:
            doit = False
            img = requests.get(k["avatar"]).content
            img = io.BytesIO(img)
            try:
                img = pygame.image.load(img)
            except:
                img = requests.get("https://ca.slack-edge.com/T0266FRGM-U015ZPLDZKQ-gf3696467c28-512").content
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
                    SCREEN_UPDATED = True
                except:
                    continue
            prev_users.extend(r[pos:])
            if event.is_set():
                done = True
                break
    DONE = True


def something(event, ffthread):
    global cookies, online, working, onlyfiles, prev_users, TIMEJI, REFETCHED, TOTAL_PAGES, BASE
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
            TOTAL_PAGES = b['pagination']['pages']
    except requests.exceptions.Timeout:
        working = False
    if working:
        threads = []
        while i<total_pages:
            t = threading.Thread(target=update, args=(event, i,100))
            t.start()
            threads.append(t)
            i+=100
        for h in threads:
            h.join()
        TIMEJI = datetime.datetime.now()
        with open(f"{data_dir}/fallback.json",'w') as fil:
            now = datetime.datetime.now()
            json.dump({"users": users,"time": str(now),"count": TOTAL_PAGES},fil)
        REFETCHED = False
    else:
        prev_users = []
        event.clear()
        ffthread = threading.Thread(target=fetchprev, args=(event,))
        ffthread.start()
        ffthread.join()
    


async def main():
    global online, working, prev_users, DONE, COMPLETED, REFETCHED, TIMEJI, SCREEN_UPDATED, rectsdude, REFETCH_ALLOW, TOTAL_PAGES, BASE
    top = 0
    bottom = 40
    pagenum = 0
    bg = pygame.image.load(os.path.join(BASE,"assets/background.png"))
    font = pygame.font.Font(os.path.join(BASE,"assets/PlaypenSans-Bold.ttf"),60)
    leftarrow = pygame.image.load(os.path.join(BASE,"assets/leftji.png"))
    github = pygame.image.load(os.path.join(BASE,"assets/github.png"))
    logo = pygame.image.load(os.path.join(BASE, "assets/shell.png"))
    leftrect = leftarrow.get_rect()
    leftrect.topleft = (965,580)
    rightarrow = pygame.transform.rotate(leftarrow,180)
    rightrect = rightarrow.get_rect()
    rightrect.topleft = (1040,580)

    screen = pygame.display.set_mode((1100,619))
    pygame.display.set_caption("Vote Leaderboard")
    pygame.display.set_icon(logo)
    heading = font.render("Vote Leaderboard", True, (94,60,48))

    base_rect = pygame.Rect(210,150,700,70)

    end_event = threading.Event()
    sigma = threading.Thread(target=something,args=(end_event,))
    ffthread = threading.Thread(target=fetchprev, args=(end_event,))
    ffthread.start()
    clock = pygame.time.Clock()
    base_minus = 0
    updating = font2.render("Updating ...",True,(0,0,0))
    notworking = font3.render("SOM currently down ! Fetching previous data ...",True,(0,0,0))
    offline = font3.render("No Internet Connection",True,(0,0,0))
    
    rety = pygame.Rect(950,20,130,40)
    rety2 = pygame.Rect(950,530,130,40)
    tryt = font3.render("Refetch",True,(255,255,255))
    dabe = pygame.Rect(91, 560, 45, 45)
    profile = pygame.image.load(os.path.join(BASE,"assets/profile.png"))
    afff = pygame.Rect(25,560,50,50)
    def update_screen():
        global rectsdude
        change = font3.render(f"Page: {pagenum+1}", True,(255,255,255))
        rectsdude = {}
        cret = font3.render(f"Last Fetch: {TIMEJI}",True,(0,0,0))
        loading = font2.render("Loading ...",True,(255,255,255))
        screen.blit(bg,(0,0))
        screen.blit(heading, (280,5- base_minus))
        # pygame.draw.rect(screen, (0,0,0),(10, 560, 70,50),border_radius=20)
        # pygame.draw.rect(screen, (0,0,0),(10, 560, 70,50),4,border_radius=20)
        pygame.draw.rect(screen, (44, 42, 49), (91, 560, 45, 45),border_radius=10)
        screen.blit(github, (91,560))
        screen.blit(profile,(25,560))
        if REFETCH_ALLOW and prev_users!=[]:
            pygame.draw.rect(screen,(79,32,15),rety,border_radius=15)
            pygame.draw.rect(screen,(169,122,87),rety,2,15)
            screen.blit(tryt,(983,30))
        pygame.draw.rect(screen,(79,32,15),rety2,border_radius=15)
        pygame.draw.rect(screen,(169,122,87),rety2,2,15)
        screen.blit(change,(970,540))
        screen.blit(leftarrow,leftrect)
        screen.blit(rightarrow,rightrect)
        if not DONE and working and REFETCHED:
            screen.blit(updating, (480,100-base_minus))
        if not working and online and not DONE and REFETCHED:
            screen.blit(notworking, (350,100-base_minus))
        if not online and REFETCHED:
            screen.blit(offline, (430,100-base_minus))
        if not REFETCHED:
            screen.blit(cret, (380,100-base_minus))
        k = 0
        val = math.floor(top)
        d = prev_users.copy()
        for val in range((pagenum*20),(pagenum*20)+20):
            if val<len(d):
                pygame.draw.rect(screen,(0,0,0),(base_rect[0],base_rect[1]+(k*90) - base_minus,base_rect[2],base_rect[3]),3,20)
                temp = font2.render(f"#{val+1}",True,(0,0,0))
                screen.blit(temp,((base_rect[0]+10,base_rect[1]+18+(k*90)- base_minus)))
                screen.blit(d[val]["avatar"],(base_rect[0]+90,base_rect[1]+10+(k*90)- base_minus))
                screen.blit(d[val]["display_name"],(base_rect[0]+180,base_rect[1]+18+(k*90)- base_minus))
                rectsdude[val] = d[val]["display_name"].get_rect()
                rectsdude[val].topleft = (base_rect[0]+180,base_rect[1]+18+(k*90)- base_minus)
                screen.blit(d[val]["votes_count_render"],(base_rect[0]+620,base_rect[1]+18+(k*90)- base_minus))
                k+=1
                val+=1
            else:
                pygame.draw.rect(screen,(79,32,15),(base_rect[0],base_rect[1]+(k*90) - base_minus,base_rect[2],base_rect[3]),border_radius=15)
                pygame.draw.rect(screen,(169,122,87),(base_rect[0],base_rect[1]+(k*90) - base_minus,base_rect[2],base_rect[3]),2,15)
                screen.blit(loading,(base_rect[0]+270,base_rect[1]+18+(k*90)- base_minus))
    
    while True:
        if SCREEN_UPDATED:
            update_screen()
            SCREEN_UPDATED = False


        events = pygame.event.get()
        mousepos = pygame.mouse.get_pos()
        inone = False
        baby = False
        if rety.collidepoint(mousepos) and REFETCH_ALLOW and prev_users!=[]:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            inone = True
        for p in rectsdude:
            if rectsdude[p].collidepoint(mousepos):
                pygame.draw.line(screen,(0,0,0),(rectsdude[p][0],rectsdude[p][1]+32),(rectsdude[p][0]+rectsdude[p][2],rectsdude[p][1]+32),3)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                inone = True
                baby = True
        if leftrect.collidepoint(mousepos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            inone = True
        if rightrect.collidepoint(mousepos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            inone = True
        if dabe.collidepoint(mousepos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            inone = True
        if afff.collidepoint(mousepos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            inone = True
        if not inone:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if baby:
                baby = False
                update_screen()
        for event in events:
            if event.type==pygame.QUIT:
                screen.blit(bg,(0,0))
                add = font2.render("Closing ...",True,(0,0,0))
                screen.blit(add,(500,20))
                pygame.display.update()
                end_event.set()
                try:
                    ffthread.join()
                except:
                    pass
                try:
                    sigma.join()
                except:
                    pass
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                if len(prev_users)!=0:
                    if event.y<0:
                        if len(prev_users) - (pagenum*20)>20:
                            if base_rect[1]+(20*90)-base_minus>667:
                                base_minus += 80
                                update_screen()
                        elif len(prev_users) - (pagenum*20)>0:
                            if base_rect[1]+((len(prev_users) - (pagenum*20))*90)-base_minus>667:
                                base_minus += 80
                                update_screen()
                        
                            
                    elif event.y>=0:
                        if base_minus>=80:
                            base_minus -= 80
                            update_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rety.collidepoint(event.pos) and REFETCH_ALLOW and prev_users!=[]:
                    REFETCH_ALLOW = False
                    update_screen()
                    end_event.set()
                    try:
                        sigma.join()
                    except:
                        pass
                    try:
                        ffthread.join()
                    except:
                        pass
                    end_event.clear()
                    REFETCH_ALLOW = True
                    prev_users = []
                    working = True
                    online = True
                    DONE = False
                    REFETCHED = True
                    update_screen()
                    sigma = threading.Thread(target=something,args=(end_event, ffthread))
                    sigma.start()
                if pygame.MOUSEWHEEL not in events:
                    for ad in rectsdude:
                        if (rectsdude[ad].collidepoint(event.pos)):
                            webbrowser.open(f"https://summer.hackclub.com/users/{prev_users[ad]["id"]}")
                if leftrect.collidepoint(event.pos) and pagenum!=0:
                    pagenum-=1
                    update_screen()
                elif rightrect.collidepoint(event.pos) and pagenum!=TOTAL_PAGES:
                    pagenum+=1
                    update_screen()
                if dabe.collidepoint(event.pos):
                    webbrowser.open("https://github.com/YogyaChugh/Vote-Leaderboard.git")
                if afff.collidepoint(mousepos):
                    webbrowser.open("https://github.com/YogyaChugh")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and pagenum!=0:
                    pagenum-=1
                    update_screen()
                if event.key == pygame.K_RIGHT and pagenum!=TOTAL_PAGES:
                    pagenum+=1
                    update_screen()

        if DONE:
            end_event.set()
            sigma.join()
            
        if COMPLETED:
            ffthread.join()

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
