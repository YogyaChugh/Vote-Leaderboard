import requests
import json
import pygame
import sys

# page = 1
# a = requests.get("https://summer.hackclub.com/api/v1/users?page=1",cookies=cookies)
# b = json.loads(a.content)
# done = False
# while b['pagination']['page']!=b['pagination']['pages']:
#     for k in b["projects"]:
#         if k['id']==100:
#             print(k)
#             done = True
#             break
#     page = b['pagination']['page']+1
#     a = requests.get(f"https://summer.hackclub.com/api/v1/users?page={page}",cookies=cookies)
#     b = json.loads(a.content)
#     if done:
#         break


pygame.init()

bg = pygame.image.load("assets/background.png")
font = pygame.font.Font("assets/PlaypenSans-Bold.ttf",60)

screen = pygame.display.set_mode((1100,619))
heading = font.render("Vote Leaderboard", True, (94,60,48))

users = [{},{},{},{},{},{}]
base_rect = pygame.Rect(200,150,700,70)

while True:
    
    screen.blit(bg,(0,0))
    screen.blit(heading, (280,5))
    
    for i in range(len(users)):
        pygame.draw.rect(screen,(0,0,0),(base_rect[0],base_rect[1]+(i*90),base_rect[2],base_rect[3]),3,20)
    
    events = pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            sys.exit()
    
    pygame.display.update()
