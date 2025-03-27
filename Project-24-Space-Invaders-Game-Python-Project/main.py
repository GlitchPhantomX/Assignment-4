import pygame
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5

enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemies = []

for i in range(5):
    enemy_x = random.randint(0, width - enemy_width)
    enemy_y = random.randint(50, 150)
    enemies.append([enemy_x, enemy_y])

bullet_width = 5
bullet_height = 10
bullets = []
bullet_speed = 7

running = True
while running:
    screen.fill(black)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        bullets.append([player_x + player_width // 2, player_y])

    pygame.draw.rect(screen, white, (player_x, player_y, player_width, player_height))

    for enemy in enemies:
        pygame.draw.rect(screen, red, (enemy[0], enemy[1], enemy_width, enemy_height))
        enemy[1] += enemy_speed
        if enemy[1] > height:
            enemy[1] = random.randint(-100, -40)
            enemy[0] = random.randint(0, width - enemy_width)

    for bullet in bullets:
        bullet[1] -= bullet_speed
        pygame.draw.rect(screen, white, (bullet[0], bullet[1], bullet_width, bullet_height))
        if bullet[1] < 0:
            bullets.remove(bullet)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
