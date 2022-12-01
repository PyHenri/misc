import pygame
from textinput import textbox
import json
import random

f = open("data.json")
data = json.load(f)
qa = data["data"][random.randint(0, len(data["data"]))]

pygame.init()
clock = pygame.time.Clock()
running = True
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont(None, 32)
background = (0, 0, 0)

box = textbox(screen, width/2 - 300/2, height/2, 300, 350, 50, font, (255, 255, 255), (255, 255, 255), (255, 255, 255))

while running:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                if qa["city"] == box.value:
                    qa = data["data"][random.randint(0, len(data["data"]))]
                    box.value = ""
                    background = (0, 100, 0)
                else:
                    box.value = qa["city"]
                    background = (100, 0, 0)

                
    rendered_surface = font.render(qa["country"], True, (255, 255, 255))
    screen.blit(rendered_surface, (width/2 - 300/2, height/2 - 50))
    box.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed(), events)

    clock.tick(60)
    pygame.display.flip()
    screen.fill(background)

pygame.quit()