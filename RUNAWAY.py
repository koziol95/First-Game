import pygame
import random
import os
import time

#=============================================
pygame.font.init()
pygame.mixer.init()

#=============================================

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RUNAWAY")
UFO_WIDTH, UFO_HEIGHT = 55, 40
ROCK_WIDTH, ROCK_HEIGHT = 20, 20

UFO_HIT = pygame.USEREVENT + 1

# Colors
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

ROCK_IMAGE = pygame.image.load(os.path.join("Assets", "Rock.png"))
ROCK = pygame.transform.scale(ROCK_IMAGE, (ROCK_WIDTH, ROCK_HEIGHT))

EXPLOSION_IMAGES = []
for i in range(1, 8):
    image = pygame.image.load(os.path.join("Assets", str(i) + ".png"))
    EXPLOSION_IMAGES.append(image)

BLACK_HOLE_IMAGE = pygame.image.load(os.path.join("Assets", "black_hole.png"))
BLACK_HOLE = pygame.transform.scale(BLACK_HOLE_IMAGE,(60, 60))

# ==================================================================

# Font
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 80)
HEALTH_FONT = pygame.font.SysFont("comicsans", 20)
COUNTDOWN_FONT = pygame.font.SysFont("comicsans", 60)
SCORE_FONT = pygame.font.SysFont("comicsans", 20)

# Sound
HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Impact.mp3"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("Assets", "explosion.mp3"))

# ===================================================================

# txt
HIGH_SCORES_FILE = "Tablica wyników.txt"

VEL = 5

# /////////////////////////////////////////////////////////////////////
def draw_window(ufo, rocks, ufo_health, score):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(BLACK_HOLE, (95, 95))

    for rock in rocks:
        WIN.blit(ROCK, (rock["rect"].x, rock["rect"].y))

    WIN.blit(UFO, (ufo.x, ufo.y))
    ufo_health_text = HEALTH_FONT.render("Health: " + str(ufo_health), 1, WHITE)
    WIN.blit(ufo_health_text, (10, 10))
    Score = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
    WIN.blit(Score, (WIDTH - Score.get_width() - 10, 10))

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


def collision(ufo, rocks):
    for rock in rocks:
        if ufo.colliderect(rock["rect"]):
            pygame.event.post(pygame.event.Event(UFO_HIT))
            rocks.remove(rock)
            return True
    return False


def explosion_animation(ufo):
    explosion_frame_delay = 150
    explosion_frame_count = 7
    explosion_x = ufo.x - 70
    explosion_y = ufo.y - 70

    for i in range(explosion_frame_count):
        WIN.blit(EXPLOSION_IMAGES[i], (explosion_x, explosion_y))
        pygame.display.update()
        time.sleep(explosion_frame_delay / 1000)
    ufo.x = -1000
    ufo.y = -1000


def draw_game_over(scores):
    draw_text = GAME_OVER_FONT.render("GAME OVER", 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    


def draw_countdown(counter):
    WIN.blit(SPACE, (0, 0))
    draw_text = COUNTDOWN_FONT.render(str(counter), 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()


def draw(text):
    draw_text = GAME_OVER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2,
                         HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def save_high_scores(scores, score):
    scores.append((score, get_player_name()))
    scores.sort(reverse=True)
    sores = scores[:10]
    with open(HIGH_SCORES_FILE, "w") as file:
        for score in scores:
            file.write(str(score[0]) + "\t" + score[1] + "\n")


def load_high_scores():
    scores = []
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, "r") as file:
            for line in file:
                score_parts = line.strip().split("\t")  # Podział linii na części po znaku "\t"
                if len(score_parts) == 2:
                    score = int(score_parts[0])
                    name = score_parts[1]
                    scores.append((score, name))
    scores.sort(reverse=True)
    scores = scores[:10]
    return scores


def draw_high_scores(scores):
    y_offset = 150
    high_scores_title = SCORE_FONT.render("High Scores", 1, WHITE)
    WIN.blit(high_scores_title, (WIDTH // 2 - high_scores_title.get_width() // 2, 50))
    for i, score in enumerate(scores):
        score_text = SCORE_FONT.render(str(score), 1, WHITE)
        WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset + i * 30))
    pygame.display.update()

def draw_enter_name():
    WIN.blit(SPACE, (0, 0))
    draw_text = COUNTDOWN_FONT.render("Enter your name:", 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()

def get_player_name():
    name = ""
    text_input_active = True

    while text_input_active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    text_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        WIN.blit(SPACE, (0, 0))
        draw_text = COUNTDOWN_FONT.render("Enter your name:", 1, WHITE)
        WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))

        name_text = COUNTDOWN_FONT.render(name, 1, WHITE)
        WIN.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + name_text.get_height() // 2))
        pygame.display.update()
        
    return name

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#===================================================================================================================

def main():
    ufo = pygame.Rect(WIDTH // 2, HEIGHT // 2, UFO_WIDTH, UFO_HEIGHT)
    rocks = [{"rect": pygame.Rect(110, 110, ROCK_WIDTH, ROCK_HEIGHT), "vel": [3, 3]}]
    clock = pygame.time.Clock()
    run = True
    time_counter = 0
    game_over = False
    score = 0
    scores = load_high_scores()
    ufo_health = 3

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

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
        if collision(ufo, rocks):
            ufo_health -= 1
            HIT_SOUND.play()
            if ufo_health <= 0:
                EXPLOSION_SOUND.play()
                explosion_animation(ufo)
                game_over = True

        draw_window(ufo, rocks, ufo_health, score)

        if game_over:
            draw_game_over(scores)
            pygame.time.delay(2000)
            scores.sort(reverse=True)
            scores = scores[:10]
            save_high_scores(scores, score)

            WIN.blit(SPACE, (0, 0))
            pygame.display.update()

            draw_high_scores(scores)
            pygame.time.delay(5000)

            counter = 5
            while counter > 0:
                draw_countdown(counter)
                pygame.time.delay(1000)
                counter -= 1
            draw_countdown(counter)
            pygame.time.delay(1000)
            counter -= 1

            

            run = False
        score += 1


    main()
if __name__ == "__main__":
    main()