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
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def check_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y

paddle1 = Paddle(30, HEIGHT // 2 - 50)
paddle2 = Paddle(WIDTH - 40, HEIGHT // 2 - 50)
ball = Ball(WIDTH // 2, HEIGHT // 2)

score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)

def update_score():
    global score1, score2
    if ball.rect.left <= 0:
        score2 += 1
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed_x = -ball.speed_x
    if ball.rect.right >= WIDTH:
        score1 += 1
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed_x = -ball.speed_x

def render_score():
    score_text1 = font.render(str(score1), True, WHITE)
    score_text2 = font.render(str(score2), True, WHITE)
    screen.blit(score_text1, (WIDTH // 4, 10))
    screen.blit(score_text2, (3 * WIDTH // 4, 10))

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
    if keys[pygame.K_UP] and paddle2.rect.top > 0:
        paddle2.move(up=True)
    if keys[pygame.K_DOWN] and paddle2.rect.bottom < HEIGHT:
        paddle2.move(up=False)

    ball.move()
    ball.check_collision(paddle1, paddle2)
    update_score()

    screen.fill(BLACK)
    paddle1.draw(screen)
    paddle2.draw(screen)
    ball.draw(screen)
    render_score()
    pygame.display.flip()
    pygame.time.Clock().tick(60)