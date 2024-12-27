import pygame
import time
import random
import json

# Inicializar o pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Configurações iniciais
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Arquivo para salvar o HighScore
HIGH_SCORE_FILE = "highscore.json"

# Função para carregar o HighScore
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("highscore", 0)
    except FileNotFoundError:
        return 0

# Função para salvar o HighScore
def save_high_score(highscore):
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump({"highscore": highscore}, file)

# Variáveis do jogo
high_score = load_high_score()
def snake_game():
    global high_score
    game_over = False
    game_close = False

    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = 0, 0

    snake_list = []
    snake_length = 1

    score = 0

    # Posicionar as maçãs
    apple_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    apple_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    green_apple = None
    green_apple_timer = None

    while not game_over:

        while game_close:
            display.fill(BLACK)
            font = pygame.font.SysFont(None, 26)
            msg = font.render("GAME OVER! Pressione C para jogar novamente ou Q para sair", True, RED)
            display.blit(msg, [WIDTH / 10, HEIGHT / 2.5])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        snake_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        display.fill(BLACK)

        pygame.draw.rect(display, RED, [apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE])

        if green_apple:
            pygame.draw.rect(display, GREEN, [green_apple[0], green_apple[1], BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        for segment in snake_list:
            pygame.draw.rect(display, WHITE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, WHITE)
        highscore_text = font.render(f"HighScore: {high_score}", True, WHITE)
        display.blit(score_text, [10, 10])
        display.blit(highscore_text, [10, 40])

        pygame.display.update()

        # Comer a maçã vermelha
        if x == apple_x and y == apple_y:
            apple_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            apple_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
            score += 1

        # Comer a maçã verde
        if green_apple and x == green_apple[0] and y == green_apple[1]:
            green_apple = None
            green_apple_timer = None
            snake_length += 1
            score += 10

        # Adicionar maçã verde aleatoriamente
        if not green_apple and random.random() < 0.01:
            green_apple = [
                round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
                round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            ]
            green_apple_timer = time.time()

        # Remover a maçã verde após 15 segundos
        if green_apple and time.time() - green_apple_timer > 15:
            green_apple = None
            green_apple_timer = None

        clock.tick(15)

        if score > high_score:
            high_score = score
            save_high_score(high_score)

    pygame.quit()
    quit()

snake_game()
