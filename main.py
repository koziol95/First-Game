import pygame
import random
import os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RUN AWAY")

UFO_WIDTH, UFO_HEIGHT = 55, 40
ROCK_WIDTH, ROCK_HEIGHT = 20, 20

# Kolory
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60

# Obrazy
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Space.png")), (WIDTH, HEIGHT))

UFO_IMAGE = pygame.image.load(os.path.join("Assets", "UFO.png"))
UFO = pygame.transform.scale(UFO_IMAGE, (UFO_WIDTH, UFO_HEIGHT))

ROCK_IMAGE = pygame.image.load(os.path.join("Assets", "Rock.png"))
ROCK = pygame.transform.scale(ROCK_IMAGE, (ROCK_WIDTH, ROCK_HEIGHT))

VEL = 5

def draw_window(ufo, rocks):
    WIN.blit(SPACE, (0, 0))
    
    for rock in rocks:
        WIN.blit(ROCK, (rock["rect"].x, rock["rect"].y))
    
    WIN.blit(UFO, (ufo.x, ufo.y))

    pygame.display.update()

def UFO_HANDLE_MOVEMENT(keys_pressed, ufo):
    if keys_pressed[pygame.K_LEFT] and ufo.x - VEL + ufo.width > 0 + 50:  # LEWO
        ufo.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and ufo.x + VEL < WIDTH - 50:  # PRAWO
        ufo.x += VEL
    if keys_pressed[pygame.K_UP] and ufo.y - VEL > 0 - 5:  # GÓRA
        ufo.y -= VEL
    if keys_pressed[pygame.K_DOWN] and ufo.y + VEL + ufo.height < HEIGHT + 2:  # DÓŁ
        ufo.y += VEL

def ROCK_MOVEMENT(rocks):
    for rock in rocks:
        rock["rect"].x += rock["vel"][0]
        rock["rect"].y -= rock["vel"][1]

        if rock["rect"].y <= 0 or rock["rect"].y + ROCK_HEIGHT >= HEIGHT:
            rock["vel"][1] *= -1

        if rock["rect"].x <= 0 or rock["rect"].x + ROCK_WIDTH >= WIDTH:
            rock["vel"][0] *= -1

def main():
    ufo = pygame.Rect(WIDTH // 2, HEIGHT // 2, UFO_WIDTH, UFO_HEIGHT)
    rocks = [{"rect": pygame.Rect(110, 110, ROCK_WIDTH, ROCK_HEIGHT), "vel": [3, 3]}]
    clock = pygame.time.Clock()
    run = True
    time_counter = 0

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        UFO_HANDLE_MOVEMENT(keys_pressed, ufo)

        time_counter += 1
        if time_counter == 3 * FPS:
            time_counter = 0
            new_rock = {
                "rect": pygame.Rect(111, 110, ROCK_WIDTH, ROCK_HEIGHT),
                "vel": [random.randint(-3, 3), random.randint(-3, 3)]
            }
            rocks.append(new_rock)

        ROCK_MOVEMENT(rocks)

        draw_window(ufo, rocks)

    pygame.quit()

if __name__ == "__main__":
    main()
