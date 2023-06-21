import pygame
import random
import os
#=====================================================================


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RUN AWAY")

UFO_WIDTH, UFO_HEIGHT = 55, 40
ROCK_WIDTH , ROCK_HEIGH = 10, 10


# colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60

UFO_IMAGE = pygame.image.load(os.path.join("Assets", "UFO.png"))
UFO = pygame.transform.scale(UFO_IMAGE, (UFO_WIDTH, UFO_HEIGHT))

ROCK_IMAGE = pygame. image.load(os.path.join("Assets", "rock.png"))
ROCK = pygame.transform.scale(ROCK_IMAGE, (ROCK_WIDTH, ROCK_HEIGH))

#=====================================================================
def draw_window():
    WIN.fill(BLACK)
    WIN.blit(UFO, (WIDTH//2, HEIGHT//2))

    pygame.display.update()


def main():
    ufo = pygame.Rect(WIDTH//2, HEIGHT//2 , UFO_WIDTH, UFO_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

    
        draw_window()

if __name__ == "__main__":
    main()