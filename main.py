import pygame
import random
import os
#=====================================================================


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RUN AWAY")

UFO_WIDTH, UFO_HEIGHT = 55, 40
ROCK_WIDTH , ROCK_HEIGHT = 20, 20


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
ROCK = pygame.transform.scale(ROCK_IMAGE, (ROCK_WIDTH, ROCK_HEIGHT))

###
VEL = 5

ROCK_VEL = 3


#=====================================================================
def draw_window(ufo, rock):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(ROCK, (rock.x, rock.y))

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

def ROCK_MOVMENT(rock):
    global ROCK_VEL
    rock.x += ROCK_VEL
    rock.y -= 3
    

    if rock.y + ROCK_HEIGHT  >= HEIGHT or rock.y <= 0:  # Sprawdzanie kolizji z górną i dolną krawędzią
        rock.y *= -1*ROCK_VEL
    if rock.x + ROCK_WIDTH >= WIDTH or rock.x <= 0:  # Sprawdzanie kolizji z lewą i prawą krawędzią
        rock.x *= -1*ROCK_VEL

    


def main():
    ufo = pygame.Rect(WIDTH//2, HEIGHT//2 , UFO_WIDTH, UFO_HEIGHT)
    rock = pygame.Rect(101, 101, ROCK_WIDTH, ROCK_HEIGHT)
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
       # ROCK_MOVMENT(rock)
        

    
        draw_window(ufo, rock)

if __name__ == "__main__":
    main()