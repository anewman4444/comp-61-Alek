
import pygame
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Epic Flying Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 48)

# Player class
class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.radius = 20
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.velocity = 0

        if self.y < self.radius:
            self.y = self.radius
            self.velocity = 0

    def jump(self):
        self.velocity = self.lift

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, int(self.y)), self.radius)

# Pipe class
class Pipe:
    def __init__(self):
        self.width = 80
        self.gap = 200
        self.x = WIDTH
        self.top = random.randint(50, HEIGHT - self.gap - 50)
        self.bottom = self.top + self.gap
        self.speed = 4

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top))
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, self.width, HEIGHT - self.bottom))

    def off_screen(self):
        return self.x + self.width < 0

    def hits(self, player):
        if player.x + player.radius > self.x and player.x - player.radius < self.x + self.width:
            if player.y - player.radius < self.top or player.y + player.radius > self.bottom:
                return True
        return False

# Main game function
def game():
    player = Player()
    pipes = []
    score = 0
    frame_count = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    game()  # Restart game

        if not game_over:
            player.update()
            frame_count += 1

            if frame_count % 90 == 0:
                pipes.append(Pipe())

            for pipe in pipes:
                pipe.update()
                pipe.draw()
                if pipe.hits(player):
                    game_over = True
                if pipe.x + pipe.width < player.x and not getattr(pipe, 'scored', False):
                    score += 1
                    pipe.scored = True

            pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        player.draw()

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            over_text = font.render("Game Over! Press R to Restart", True, BLACK)
            over_text_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(over_text, over_text_rect)

        pygame.display.update()

# Start the game
game()
pygame.quit()