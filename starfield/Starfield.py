import random
import pygame
import math
from dataclasses import dataclass

SIZE = (400, 400)
MAX_LINE_LENGTH = 80

SPEED_MU = 20
MAX_SIZE = 3
WHITE = (255, 255, 255, 255)


@dataclass
class Star:
    pos: pygame.Vector2
    speed: pygame.Vector2
    size: int

    def update(self, screen, elapsed):
        pygame.draw.circle(screen, WHITE, self.pos, self.size)
        self.pos += elapsed * self.speed
        return int(self.pos.x) in range(SIZE[0]) and int(self.pos.y) in range(SIZE[1])

    def __sub__(self, other):
        return (self.pos - other.pos).length()


def map_distance_to_color(distance):
    if distance < MAX_LINE_LENGTH:
        g = int(255 * (1 - distance / MAX_LINE_LENGTH))
        return (g, g, g, g)
    return None


class StarField:

    def __init__(self, count=100):
        self._count = count
        self._stars = []
        self._respawn()

    def _respawn(self):
        for _ in range(self._count - len(self._stars)):
            star = Star(
                pos=pygame.Vector2(
                    random.randint(0, SIZE[0] - 1),
                    random.randint(0, SIZE[1] - 1),
                ),
                speed=pygame.Vector2(
                    random.gauss(0, SPEED_MU),
                    random.gauss(0, SPEED_MU),
                ),
                size=random.randint(1, MAX_SIZE),
            )
            self._stars.append(star)

    def update(self, screen, elapsed):
        remove = []
        lines = []
        for a in self._stars:
            for b in self._stars:
                if a is not b:
                    distance = a - b
                    color = map_distance_to_color(distance)
                    if color is not None:
                        lines.append((color, a.pos, b.pos))

        for color, a_pos, b_pos in sorted(lines, key=lambda line: line[0]):
            pygame.draw.line(screen, color, a_pos, b_pos)

        for star in self._stars:
            alive = star.update(screen, elapsed)
            if not alive:
                remove.append(star)
        for star in remove:
            self._stars.remove(star)
        self._respawn()


def main():
    pygame.init()
    pygame.display.set_caption("Star Geometry")

    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    star_field = StarField()

    running = True
    elapsed = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        star_field.update(screen, elapsed / 1000)
        pygame.display.flip()
        elapsed = clock.tick(60)


if __name__ == "__main__":
    main()
