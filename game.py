""" 
A simple game. The player is a square that slides
around the screen collecting circles for points
"""

# Standard Modules
import random

# External Modules
import pygame
vec2 = pygame.math.Vector2

# Local Imports
# import shape_sprites

# def slider_game():
pygame.init()

FPS = 60
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (400, 400)

# Initialize the screen/display attributes

# Full screen on windows requires some special information
# when UI scaling is something other than 100%
""" import ctypes
ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
screen = pygame.display.set_mode(true_res, pygame.FULLSCREEN) """

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Slider")

BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(220, 40, 40)
GREEN = pygame.Color(40, 220, 40)


# Initialize entities for the single-scene game

# Debug font for displaying debug information
font = pygame.font.SysFont(None, 30)

# TODO: Pull player out to a entity/sprite class
player_size = player_width, player_height = (20, 20)
player_velocity = [0.0, 0.0]
player_accel = 20.0/100.0

player = pygame.sprite.Sprite()
player.image = pygame.Surface(player_size)
player.image.fill(RED)
player_center = [SCREEN_WIDTH/2.0, SCREEN_HEIGHT/2.0]
player.rect = player.image.get_rect(center=player_center)

all_sprites = pygame.sprite.Group(player)
food_sprites = pygame.sprite.Group()

# Initialize a clock object to be used by the game for various reasons
clock = pygame.time.Clock()

# Food related initialization
prev_spawn_time = 0
food_spawn_interval = 5000
food_score = 0


done = False

while not done:
  for event in pygame.event.get():   # User did something
    if event.type == pygame.QUIT:  # If user clicked close
      done = True   # Flag that we are done so we exit this loop
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        done = True

  # Update objects states
  def update_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      player_velocity[0] -= player_accel
    if keys[pygame.K_RIGHT]:
      player_velocity[0] += player_accel
    if keys[pygame.K_UP]:
      player_velocity[1] -= player_accel
    if keys[pygame.K_DOWN]:
      player_velocity[1] += player_accel

    if player.rect.right < 0:
      player_center[0] += (SCREEN_WIDTH + player_width)
    elif player.rect.left > SCREEN_WIDTH:
      player_center[0] -= (SCREEN_WIDTH + player_width)
    if player.rect.bottom < 0:
      player_center[1] += (SCREEN_HEIGHT + player_height)
    elif player.rect.top > SCREEN_HEIGHT:
      player_center[1] -= (SCREEN_HEIGHT + player_height)

    player_center[0] += player_velocity[0]
    player_center[1] += player_velocity[1]
    player.rect.center = player_center
  update_player()

  # TODO: Food spawn interval should be capped at a minimum value
  # TODO: Timer keeps running even when the game is paused by debugger
  game_time = pygame.time.get_ticks()
  dt = game_time - prev_spawn_time

  if dt > food_spawn_interval:
    new_food = pygame.sprite.Sprite()
    new_food.image = pygame.Surface((10, 10))
    new_food.image.fill(GREEN)
    edge_buffer = 20
    new_food_center = (
        random.randint(0 + edge_buffer, SCREEN_WIDTH - edge_buffer),
        random.randint(0 + edge_buffer, SCREEN_HEIGHT - edge_buffer))
    new_food.rect = new_food.image.get_rect(center=new_food_center)
    all_sprites.add(new_food)
    food_sprites.add(new_food)
    prev_spawn_time = game_time

  # Check if player collides and should consume any food
  collisions = pygame.sprite.spritecollide(player, food_sprites, True)
  for food in collisions:
    food_score += 1
    food_spawn_interval -= 100

  # Draw updated objects to the screen
  screen.fill(BLACK)
  all_sprites.draw(screen)
  food_score_text = font.render(str(food_score), False, GREEN)
  screen.blit(food_score_text, ((SCREEN_WIDTH-food_score_text.get_width())/2, 5))

  # Overlay any debug style text
  fps_text = font.render("{:.2f}".format(clock.get_fps()), False, GREEN)
  screen.blit(fps_text, (5, 5))

  # Go ahead and update the screen with what we've drawn.
  pygame.display.flip()
  clock.tick(FPS)

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()
