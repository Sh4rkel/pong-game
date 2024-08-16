import csv
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 5

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.initial_speed_x = 5
        self.initial_speed_y = 5
        self.speed_x = self.initial_speed_x
        self.speed_y = self.initial_speed_y
        self.speed_increment = 0.5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def check_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.speed_x = -self.speed_x
            self.increase_speed()
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y

    def increase_speed(self):
        if self.speed_x > 0:
            self.speed_x += self.speed_increment
        else:
            self.speed_x -= self.speed_increment
        if self.speed_y > 0:
            self.speed_y += self.speed_increment
        else:
            self.speed_y -= self.speed_increment

    def reset_speed(self):
        self.speed_x = self.initial_speed_x
        self.speed_y = self.initial_speed_y

paddle1 = Paddle(30, HEIGHT // 2 - 50)
paddle2 = Paddle(WIDTH - 40, HEIGHT // 2 - 50)
ball = Ball(WIDTH // 2, HEIGHT // 2)

score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)

def save_final_score(player1_score, player2_score):
    with open('scores.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player1_score, player2_score])

def check_game_end():
    global score1, score2
    if score1 >= 10 or score2 >= 10:
        save_final_score(score1, score2)
        return True
    return False

def update_score():
    global score1, score2
    if ball.rect.left <= 0:
        score2 += 1
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.reset_speed()
        ball.speed_x = -ball.speed_x
    if ball.rect.right >= WIDTH:
        score1 += 1
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.reset_speed()
        ball.speed_x = -ball.speed_x
    if check_game_end():
        return True
    return False

def render_score():
    score_text1 = font.render(str(score1), True, WHITE)
    score_text2 = font.render(str(score2), True, WHITE)
    screen.blit(score_text1, (WIDTH // 4, 10))
    screen.blit(score_text2, (3 * WIDTH // 4, 10))

def ai_move(paddle, ball):
    if paddle.rect.centery < ball.rect.centery:
        paddle.move(up=False)
    elif paddle.rect.centery > ball.rect.centery:
        paddle.move(up=True)

def save_score(player1_score, player2_score):
    with open('scores.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player1_score, player2_score])

def load_scores():
    scores = []
    try:
        with open('scores.csv', mode='r') as file:
            reader = csv.reader(file)
            scores = list(reader)
    except FileNotFoundError:
        pass
    return scores

def draw_back_to_menu_button():
    back_font = pygame.font.Font(None, 50)
    back_text = back_font.render("Back to Menu", True, WHITE)
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(back_text, back_rect)
    return back_rect

def show_history():
    scores = load_scores()
    screen.fill(BLACK)
    history_font = pygame.font.Font(None, 50)
    y_offset = 100
    for score in scores:
        score_text = history_font.render(f"Player 1: {score[0]}(10) - Player 2: {score[1]}(10)", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 50
    back_rect = draw_back_to_menu_button()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return

def start_screen():
    screen.fill(BLACK)
    title_font = pygame.font.Font(None, 74)
    option_font = pygame.font.Font(None, 50)
    title_text = title_font.render("Pong Game", True, WHITE)
    pvp_text = option_font.render("Player vs Player", True, WHITE)
    pva_text = option_font.render("Player vs AI", True, WHITE)
    history_text = option_font.render("Show History", True, WHITE)

    pvp_rect = pvp_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pva_rect = pva_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    history_rect = history_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(pvp_text, pvp_rect)
    screen.blit(pva_text, pva_rect)
    screen.blit(history_text, history_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_rect.collidepoint(event.pos):
                    return "PVP"
                if pva_rect.collidepoint(event.pos):
                    return "PVA"
                if history_rect.collidepoint(event.pos):
                    show_history()
                    screen.fill(BLACK)
                    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
                    screen.blit(pvp_text, pvp_rect)
                    screen.blit(pva_text, pva_rect)
                    screen.blit(history_text, history_rect)
                    pygame.display.flip()

game_mode = start_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.rect.top > 0:
        paddle1.move(up=True)
    if keys[pygame.K_s] and paddle1.rect.bottom < HEIGHT:
        paddle1.move(up=False)
    if game_mode == "PVP":
        if keys[pygame.K_UP] and paddle2.rect.top > 0:
            paddle2.move(up=True)
        if keys[pygame.K_DOWN] and paddle2.rect.bottom < HEIGHT:
            paddle2.move(up=False)
    elif game_mode == "PVA":
        ai_move(paddle2, ball)

    ball.move()
    ball.check_collision(paddle1, paddle2)
    if update_score():
        game_mode = start_screen()

    screen.fill(BLACK)
    paddle1.draw(screen)
    paddle2.draw(screen)
    ball.draw(screen)
    render_score()
    pygame.display.flip()
    pygame.time.Clock().tick(60)