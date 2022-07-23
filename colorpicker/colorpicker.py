import pygame
from slider import Slider

pygame.init()

width = 500
height = 500
background = (255,255,255)

run = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drawing Program")

slider = Slider(max_value=255,h=20,w=5,value=255,x_box=height/2-150,y_box=300,h_box=20,w_box=300,box_color=(0,0,0),slider_color=(100,100,100),box_border_size=2)
slider2 = Slider(max_value=255,h=20,w=5,value=255,x_box=height/2-150,y_box=350,h_box=20,w_box=300,box_color=(0,0,0),slider_color=(100,100,100),box_border_size=2)
slider3 = Slider(max_value=255,h=20,w=5,value=255,x_box=height/2-150,y_box=400,h_box=20,w_box=300,box_color=(0,0,0),slider_color=(100,100,100),box_border_size=2)



while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    screen.fill(background)

    slider.update(mouse,click)
    slider.draw(screen=screen)
    slider2.update(mouse,click)
    slider2.draw(screen=screen)
    slider3.update(mouse,click)
    slider3.draw(screen=screen)

    pygame.draw.rect(screen,(slider.value,slider2.value,slider3.value),(height/2-50,150,100,100))

    clock.tick(60)
    pygame.display.update()

pygame.quit()
