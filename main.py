import pygame
from random import randint
from Colors import Colors

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
LINE_HEIGHT = 70
DRAGON_VELOCITY = 6
FPS = 60

STARTING_LIVES = 5
STARTING_SCORE = 0
STARTING_COIN_SPEED = 5

def main():
    
    lives, score, coin_speed = reset_game_stats()

    display_surface = initialize_game(
        caption="Feed the Dragon"
    )

    font = pygame.font.Font("fonts/AttackGraffiti.ttf", 48)

    score_text, score_text_rect = load_text(
        font=font,
        text="SCORE: " + str(STARTING_SCORE),
        color=Colors.GREEN.value,
        background=Colors.LIGHT_GREEN.value,
        center=(WINDOW_WIDTH * 1/6, 30)
    )

    title_text, title_text_rect = load_text(
        font=font,
        text="FEED THE DRAGON",
        color=Colors.GREEN.value,
        background=Colors.WHITE.value,
        center=(WINDOW_WIDTH * 3/6, 30)
    )

    lives_text, lives_text_rect = load_text(
        font=font,
        text="LIVES: " + str(STARTING_LIVES),
        color=Colors.GREEN.value,
        background=Colors.LIGHT_GREEN.value,
        center=(WINDOW_WIDTH * 5/6, 30)
    )

    game_over_text, game_over_text_rect = load_text(
        font=font,
        text="GAMEOVER",
        color=Colors.GREEN.value,
        background=Colors.LIGHT_GREEN.value,
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    )

    continue_text, continue_text_rect = load_text(
        font=font,
        text="Press any key to play again",
        color=Colors.GREEN.value,
        background=Colors.LIGHT_GREEN.value,
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)
    )

    draw_full_screen_horizontal_line(
        display_surface=display_surface,
        line_height=LINE_HEIGHT,
        width=2
    )

    # Images
    dragon, dragon_rect = load_images(
        path="images/dragon.png",
        centerx=40,
        centery=(WINDOW_HEIGHT - LINE_HEIGHT) // 2
    )

    coin, coin_rect = load_images(
        path="images/coin.png",
        centerx=WINDOW_WIDTH - 32,
        centery=randint(LINE_HEIGHT + 32, (WINDOW_HEIGHT - LINE_HEIGHT) - 32)
    )

    # Sound
    coin_sound = pygame.mixer.Sound("sounds/coin_sound.wav")
    miss_sound = pygame.mixer.Sound("sounds/miss_sound.wav")
    miss_sound.set_volume(.1)
    pygame.mixer.music.load("sounds/ftd_background_music.wav")

    # Clock
    clock = pygame.time.Clock()

    pygame.mixer.music.play(-1, 0.0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and dragon_rect.top > LINE_HEIGHT:
            dragon_rect.centery -= DRAGON_VELOCITY
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and dragon_rect.bottom < WINDOW_HEIGHT:
            dragon_rect.centery += DRAGON_VELOCITY

        pygame.draw.line(display_surface, Colors.WHITE.value, (0, LINE_HEIGHT), (WINDOW_WIDTH, LINE_HEIGHT), 2)

        coin_rect.centerx -= coin_speed

        if dragon_rect.colliderect(coin_rect) or coin_rect.x <= 0:
            if coin_rect.x <= 0:
                lives -= 1
                miss_sound.play()
            else:
                score += 1
                coin_sound.play()
                coin_speed += .5

            coin_rect.centerx = WINDOW_WIDTH - 32
            coin_rect.centery = randint(LINE_HEIGHT + 32, (WINDOW_HEIGHT - LINE_HEIGHT) - 32)

        score_text = font.render("Score: " + str(score), True, Colors.GREEN.value, Colors.LIGHT_GREEN.value)
        lives_text = font.render("Lives: " + str(lives), True, Colors.GREEN.value, Colors.LIGHT_GREEN.value)

        if lives == 0:
            display_surface.blit(game_over_text, game_over_text_rect)
            display_surface.blit(continue_text, continue_text_rect)
            display_surface.blit(lives_text, lives_text_rect)
            pygame.display.update()

            pygame.mixer.music.stop()
            is_paused = True
            while is_paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_paused = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        is_paused = False
                        lives, score, coin_speed = reset_game_stats()

                        dragon_rect.centerx = 40
                        dragon_rect.centery = (WINDOW_HEIGHT - LINE_HEIGHT) // 2
                        pygame.mixer.music.play(-1, 0, 0)

        display_surface.fill(Colors.BLACK.value)

        display_surface.blit(score_text, score_text_rect)
        display_surface.blit(title_text, title_text_rect)
        display_surface.blit(lives_text, lives_text_rect)
        display_surface.blit(coin, coin_rect)
        display_surface.blit(dragon, dragon_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

def initialize_game(caption):
    pygame.init()
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(caption)

    return display_surface

def load_text(font, text, color, background, center):
    text = font.render(text, True, color, background)
    rect = text.get_rect()
    rect.center = center
    return text, rect

def draw_full_screen_horizontal_line(display_surface, line_height, width):
    pygame.draw.line(display_surface, Colors.WHITE.value, (0, line_height), (WINDOW_WIDTH, line_height), width)

def load_images(path, centerx, centery):
    image = pygame.image.load(path)
    rect = image.get_rect()
    rect.centerx = centerx
    rect.centery = centery
    return image, rect

def reset_game_stats():
    return STARTING_LIVES, STARTING_SCORE, STARTING_COIN_SPEED


main()
