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

# Images
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Space.png")), (WIDTH, HEIGHT))

UFO_IMAGE = pygame.image.load(os.path.join("Assets", "UFO.png"))
UFO = pygame.transform.scale(UFO_IMAGE, (UFO_WIDTH, UFO_HEIGHT))

ROCK_IMAGE = pygame. image.load(os.path.join("Assets", "Rock.png"))
ROCK = pygame.transform.scale(ROCK_IMAGE, (ROCK_WIDTH, ROCK_HEIGH))

###
VEL = 5


#=====================================================================
def draw_window(ufo):
    WIN.blit(SPACE, (0,0))

    WIN.blit(UFO, (ufo.x, ufo.y))

    pygame.display.update()

def UFO_HANDLE_MOVMENT(keys_pressed, ufo):
    if keys_pressed[pygame.K_LEFT] and ufo.x - VEL + ufo.width > 0 + 50:  # LEFT
        ufo.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and ufo.x + VEL  < WIDTH - 50 :  # RIGHT
        ufo.x += VEL
    if keys_pressed[pygame.K_UP] and ufo.y - VEL > 0 - 5:  # UP
        ufo.y -= VEL
    if keys_pressed[pygame.K_DOWN] and ufo.y + VEL + ufo.height < HEIGHT + 2:  # DOWN
        ufo.y += VEL


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

        keys_pressed = pygame.key.get_pressed()
        UFO_HANDLE_MOVMENT(keys_pressed, ufo)
        

    
        draw_window(ufo)

if __name__ == "__main__":
    main()