import pygame
from pygame.locals import *

pygame.init()

# Configurations
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
FPS = 60

# Colors
WHITE = (255, 255, 255)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apprendre le français - Aventure")

# Player setup
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# Map setup (simple grid with grass tiles)
map_data = [[0 for _ in range(WIDTH // TILE_SIZE)] for _ in range(HEIGHT // TILE_SIZE)]

# PNJ setup
pnj_pos_1 = [300, 300]
pnj_pos_2 = [500, 400]
conversation_active = False
conversation_text = ""
user_input = ""
input_active = False
choice_active = False
show_bubble = False
bubble_text = ""
current_pnj = None

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if input_active:
                if event.key == K_RETURN:
                    if current_pnj == 1:
                        bubble_text = f"Enchanté, {user_input}!"
                    elif current_pnj == 2:
                        bubble_text = f"Merci, moi c'est les pâtes b!"
                    input_active = False
                    conversation_active = False
                    show_bubble = True
                elif event.key == K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            elif choice_active:
                if event.key == K_y:
                    input_active = True
                    choice_active = False
                    user_input = ""
                elif event.key == K_n:
                    conversation_active = False
                    choice_active = False

    keys = pygame.key.get_pressed()
    if not input_active and not choice_active:
        if keys[K_UP]:
            player_pos[1] -= player_speed
        if keys[K_DOWN]:
            player_pos[1] += player_speed
        if keys[K_LEFT]:
            player_pos[0] -= player_speed
        if keys[K_RIGHT]:
            player_pos[0] += player_speed

    # Check proximity to PNJs
    player_rect = pygame.Rect(player_pos[0], player_pos[1], TILE_SIZE, TILE_SIZE)
    pnj_rect_1 = pygame.Rect(pnj_pos_1[0], pnj_pos_1[1], TILE_SIZE, TILE_SIZE)
    pnj_rect_2 = pygame.Rect(pnj_pos_2[0], pnj_pos_2[1], TILE_SIZE, TILE_SIZE)

    if player_rect.colliderect(pnj_rect_1.inflate(40, 40)):
        if keys[K_e] and not input_active and not choice_active:
            conversation_active = True
            choice_active = True
            conversation_text = "Bonjour ! Comment tu t'appelles ?"
            current_pnj = 1

    if player_rect.colliderect(pnj_rect_2.inflate(40, 40)):
        if keys[K_e] and not input_active and not choice_active:
            conversation_active = True
            choice_active = True
            conversation_text = "Quel est ton plat préféré ?"
            current_pnj = 2

    # Rendering
    screen.fill(WHITE)
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
            else:
                pygame.draw.rect(screen, DARK_GREEN, rect)

    pygame.draw.rect(screen, BLUE, (*player_pos, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, RED, (*pnj_pos_1, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, RED, (*pnj_pos_2, TILE_SIZE, TILE_SIZE))

    font = pygame.font.SysFont(None, 36)
    if conversation_active:
        pygame.draw.rect(screen, WHITE, (40, HEIGHT - 120, WIDTH - 80, 100))
        pygame.draw.rect(screen, BLACK, (40, HEIGHT - 120, WIDTH - 80, 100), 2)
        text_surface = font.render(conversation_text, True, BLACK)
        screen.blit(text_surface, (50, HEIGHT - 100))

        if choice_active:
            choice_surface = font.render("Voulez-vous répondre ? (Y/N)", True, BLACK)
            screen.blit(choice_surface, (50, HEIGHT - 60))
        if input_active:
            input_surface = font.render(user_input, True, BLACK)
            screen.blit(input_surface, (50, HEIGHT - 60))

    if show_bubble:
        if current_pnj == 1:
            bubble_rect = pygame.Rect(pnj_pos_1[0] - 50, pnj_pos_1[1] - 70, 200, 50)
        elif current_pnj == 2:
            bubble_rect = pygame.Rect(pnj_pos_2[0] - 50, pnj_pos_2[1] - 70, 200, 50)
        pygame.draw.rect(screen, WHITE, bubble_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, bubble_rect, 2, border_radius=10)
        bubble_surface = font.render(bubble_text, True, BLACK)
        screen.blit(bubble_surface, (bubble_rect.x + 10, bubble_rect.y + 10))

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
