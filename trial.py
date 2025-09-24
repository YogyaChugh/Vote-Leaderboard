import requests
import pygame
import sys
from PIL import Image


a = requests.get("https://avatars.slack-edge.com/2025-04-02/8691071291270_f5f10b1c28f09449f27a_original.jpg")

pygame.init()

screen = pygame.display.set_mode((1000,667))

image = Image.frombytes('RGBA', (128,128), a.content)
image.show()
c = image.copy().convert("RGBA")
b = pygame.image.fromstring(c.tobytes(),c.size,c.mode)
print(c.mode)
screen.blit(b,(100,200))

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
            
    pygame.display.update()