import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

# Paddle
paddle_width = 100
paddle_height = 10
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - 40
paddle_speed = 10

# Ball
ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed_x = 4
ball_speed_y = -4

# Bricks
brick_rows = 6
brick_cols = 10
brick_width = screen_width // brick_cols
brick_height = 20
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * brick_width
        brick_y = row * brick_height
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game Over
game_over = False

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += paddle_speed

        # Ball movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with walls
        if ball_x <= 0 or ball_x >= screen_width - ball_radius:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y
        if ball_y >= screen_height:
            game_over = True

        # Ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        ball_rect = pygame.Rect(ball_x, ball_y, ball_radius * 2, ball_radius * 2)
        if paddle_rect.colliderect(ball_rect):
            ball_speed_y = -ball_speed_y

        # Ball collision with bricks
        for brick in bricks:
            if brick.colliderect(ball_rect):
                ball_speed_y = -ball_speed_y
                bricks.remove(brick)
                score += 10
                break

    # Drawing
    screen.fill(black)
    pygame.draw.rect(screen, white, paddle_rect)
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)

    for i, brick in enumerate(bricks):
        pygame.draw.rect(screen, colors[i // brick_cols], brick)

    # Draw score
    draw_text(f'Score: {score}', font, white, screen, screen_width // 2, 30)

    if game_over:
        draw_text('Game Over', font, white, screen, screen_width // 2, screen_height // 2)
        draw_text('Press R to Restart', font, white, screen, screen_width // 2, screen_height // 2 + 50)
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

    # Restart game
    keys = pygame.key.get_pressed()
    if game_over and keys[pygame.K_r]:
        ball_x = screen_width // 2
        ball_y = screen_height // 2
        ball_speed_y = -4
        paddle_x = (screen_width - paddle_width) // 2
        bricks = [pygame.Rect(col * brick_width, row * brick_height, brick_width, brick_height)
                  for row in range(brick_rows) for col in range(brick_cols)]
        score = 0
        game_over = False

pygame.quit()
sys.exit()
