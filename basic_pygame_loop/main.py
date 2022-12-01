import pygame

pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((640, 480))

while running:
    screen.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    clock.tick(60)
    pygame.display.flip()
    screen.fill((255, 255, 255))

pygame.quit()
