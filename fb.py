import pygame
import numpy as np

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
GRAVITY = 0.3
JUMP_FORCE = -5
PIPE_SPAWN_INTERVAL = 120
PIPE_SPEED = 2

# Initialize game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

# Create player
player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT / 2
player_velocity_y = 0
player_width = 20
player_height = 20

# Create pipes
pipes = []
pipe_spawn_counter = 0
pipe_width = 20
pipe_height = 2000

# Game loop
game_over = False
game_started = False
while not game_over:
  # Handle events
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          game_over = game_started
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE and not game_started:
              game_started = True
          if event.key == pygame.K_SPACE and game_started:
              player_velocity_y = JUMP_FORCE
  
  # Update player
  player_velocity_y += GRAVITY
  player_y += player_velocity_y
  if player_y > SCREEN_HEIGHT:
      game_over = True
  
  # Update pipes
  pipe_spawn_counter += 1
  if pipe_spawn_counter == PIPE_SPAWN_INTERVAL:
      pipe_spawn_counter = 0
      gap_y = np.random.randint(100, SCREEN_HEIGHT - 100)
      pipes.append((SCREEN_WIDTH, gap_y - pipe_height))
      pipes.append((SCREEN_WIDTH, gap_y + 100))
  for i, (pipe_x, pipe_y) in enumerate(pipes):
      pipes[i] = (pipe_x - PIPE_SPEED, pipe_y)
      if pipe_x < -pipe_width:
          pipes.pop(i)
          i -= 1
  
  # Check collision with pipes
  for pipe_x, pipe_y in pipes:
      if (
          pipe_x < player_x + player_width
          and pipe_x + pipe_width > player_x
          and pipe_y < player_y + player_height
          and pipe_y + pipe_height > player_y
      ):
          game_over = True
  
  # Draw game
  screen.fill((0, 0, 0))
  if not game_started:
      text = font.render("Press space bar to start", True, (255, 255, 255))
      screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
  else:
      pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
      for pipe_x, pipe_y in pipes:
          pygame.draw.rect(screen, (0, 255, 0), (pipe_x, pipe_y, pipe_width, pipe_height))
  pygame.display.flip()
  clock.tick(60)
