if __name__ == "__main__":
    pass

import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Tank Game 1.0")
clock = pygame.time.Clock()

playerImg = pygame.image.load("tank body.png")
playerX, playerY = 1000, 300

player_movement_rate = 1

player_right = False
player_left = False
player_up = False
player_down = False
player_direction = 0

def player(x, y, playerImg, tank_direction):
    playerImg = pygame.transform.rotozoom(playerImg, tank_direction, 1)
    player_rect = playerImg.get_rect(center=(x, y))
    screen.blit(playerImg, player_rect)


player_cannonImg = pygame.image.load("tank gun.png")
player_cannon_angle = 0
cannonX, cannonY = playerX, playerY
dirX, dirY = 0, 0

def player_cannon(player_cannonImg, angle):
    cannon_rotated = pygame.transform.rotozoom(player_cannonImg, angle-90, 0.8)
    cannon_rect_rotated = cannon_rotated.get_rect(center=(playerX, playerY))
    screen.blit(cannon_rotated, cannon_rect_rotated)

bulletImg = pygame.image.load("bullet.png")
player_bullets = 5
player_bullet_movement = 1.5
player_bullet_state = []
player_bulletX = []
player_bulletY = []
player_bullet_angle = []
bullet_dirX = []
bullet_dirY = []


for i in range(player_bullets):
    player_bulletX.append(0)
    player_bulletY.append(0)
    player_bullet_angle.append(0)
    player_bullet_state.append("ready")
    bullet_dirX.append(0)
    bullet_dirY.append(0)

def player_fire(x, y, angle):
    player_bullet_state[i] = "fire"
    bullet_rotated = pygame.transform.rotozoom(bulletImg, angle-90, 1)
    bullet_rect_rotated = bullet_rotated.get_rect(center=(x, y))
    screen.blit(bullet_rotated, bullet_rect_rotated)


enemyImg = pygame.image.load("enemy tank body.png")
enemyX, enemyY = 100, 350
previous_time = pygame.time.get_ticks()


def enemy(enemyX, enemyY, enemyImg):
    enemy_rect = playerImg.get_rect(center=(enemyX, enemyY))
    screen.blit(enemyImg, enemy_rect)

enemy_bullets = 5
enemy_bullet_state = []
enemy_bulletX = []
enemy_bulletY = []
enemy_bullet_angle = []
enemy_bullet_dirX = []
enemy_bullet_dirY = []

for i in range(enemy_bullets):
    enemy_bullet_state.append("ready")
    enemy_bulletX.append(0)
    enemy_bulletY.append(0)
    enemy_bullet_angle.append(0)
    enemy_bullet_dirX.append(0)
    enemy_bullet_dirY.append(0)

enemy_cannonImg = pygame.image.load("enemy tank cannon.png")
enemy_cannonX, enemy_cannonY = enemyX, enemyY
enemy_cannon_angle = 0
enemy_dirX, enemy_dirY = 0, 0
enemy_length = 0


def enemy_cannon(enemy_cannonImg, angle):
    enemy_cannon_rotated = pygame.transform.rotozoom(enemy_cannonImg, angle-90, 0.8)
    enemy_cannon_rect = enemy_cannon_rotated.get_rect(center=(enemyX, enemyY))
    screen.blit(enemy_cannon_rotated, enemy_cannon_rect)

def enemy_fire(enemyX, enemyY, angle):
    enemy_bullet_state[i] = "fire"
    bullet_rotated = pygame.transform.rotozoom(bulletImg, angle - 90, 1)
    bullet_rect_rotated = bullet_rotated.get_rect(center=(enemyX, enemyY))
    screen.blit(bullet_rotated, bullet_rect_rotated)

running = True
while running:

    screen.fill((205, 183, 158))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_right = True
            if event.key == pygame.K_d:
                player_left = True
            if event.key == pygame.K_w:
                player_up = True
            if event.key == pygame.K_s:
                player_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_right = False
            if event.key == pygame.K_d:
                player_left = False
            if event.key == pygame.K_w:
                player_up = False
            if event.key == pygame.K_s:
                player_down = False

        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
            dirX, dirY = mouseX-cannonX, mouseY-cannonY
            length = math.hypot(dirX, dirY)
            if length == 0.0:
                dirX, dirY = 0, -1
            else:
                dirX, dirY = dirX/length, dirY/length
            player_cannon_angle = math.degrees(math.atan2(-dirY, dirX))


        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(player_bullets):
                if player_bullet_state[i] == "ready":
                    player_bulletX[i], player_bulletY[i] = cannonX, cannonY
                    player_bullet_angle[i] = player_cannon_angle
                    bullet_dirX[i], bullet_dirY[i] = dirX, dirY
                    player_fire(player_bulletX[i], player_bulletY[i], player_bullet_angle[i])
                    break


    if player_right:
        playerX -= player_movement_rate
        player_direction = 90
    if player_left:
        playerX += player_movement_rate
        player_direction = 270
    if player_down:
        playerY += player_movement_rate
        player_direction = 180
    if player_up:
        playerY -= player_movement_rate
        player_direction = 0
    if player_right and player_up:
        player_direction = 45
    if player_right and player_down:
        player_direction = 135
    if player_left and player_up:
        player_direction = 315
    if player_left and player_down:
        player_direction = 225

    cannonX = playerX
    cannonY = playerY

    if playerX > 1175:
        playerX = 1175
    if playerX < 25:
        playerX = 25
    if playerY > 675:
        playerY = 675
    if playerY < 25:
        playerY = 25

    for i in range(player_bullets):
        if player_bulletX[i] < 0:
            player_bullet_state[i] = "ready"
        if player_bulletX[i] > 1200:
            player_bullet_state[i] = "ready"
        if player_bulletY[i] < 0:
            player_bullet_state[i] = "ready"
        if player_bulletY[i] > 700:
            player_bullet_state[i] = "ready"

        if player_bullet_state[i] == "fire":
            player_bulletX[i] = player_bulletX[i] + bullet_dirX[i] * player_bullet_movement
            player_bulletY[i] = player_bulletY[i] + bullet_dirY[i] * player_bullet_movement
            player_fire(player_bulletX[i], player_bulletY[i], player_bullet_angle[i])

    enemy_dirX, enemy_dirY = playerX - enemyX, playerY - enemyY
    enemy_length = math.hypot(enemy_dirX, enemy_dirY)
    if enemy_length == 0.0:
        enemy_dirX, enemy_dirY = 0, -1
    else:
        enemy_dirX, enemy_dirY = enemy_dirX / enemy_length, enemy_dirY / enemy_length
    enemy_cannon_angle = math.degrees(math.atan2(-enemy_dirY, enemy_dirX))

    for i in range(enemy_bullets):

        if enemy_bulletX[i] < 0:
            enemy_bullet_state[i] = "ready"
        if enemy_bulletY[i] < 0:
            enemy_bullet_state[i] = "ready"
        if enemy_bulletX[i] > 1200:
            enemy_bullet_state[i] = "ready"
        if enemy_bulletY[i] > 700:
            player_bullet_state[i] = "ready"

    for i in range(enemy_bullets):
        if enemy_bullet_state[i] == "ready":
            enemy_bulletX[i], enemy_bulletY[i] = enemyX, enemyY
            enemy_bullet_angle[i] = enemy_cannon_angle
            enemy_bullet_dirX[i], enemy_bullet_dirY[i] = enemy_dirX, enemy_dirY
            enemy_fire(enemy_bulletX[i], enemy_bulletY[i], enemy_bullet_angle[i])

    for i in range(enemy_bullets):
        if enemy_bullet_state[i] == "fire":
            enemy_bulletX[i] = enemy_bulletX[i] + enemy_bullet_dirX[i] * player_bullet_movement
            enemy_bulletY[i] = enemy_bulletY[i] + enemy_bullet_dirY[i] * player_bullet_movement
            enemy_fire(enemy_bulletX[i], enemy_bulletY[i], enemy_bullet_angle[i])


    enemy(enemyX, enemyY, enemyImg)
    enemy_cannon(enemy_cannonImg, enemy_cannon_angle)

    player(playerX, playerY, playerImg, player_direction)
    player_cannon(player_cannonImg, player_cannon_angle)

    pygame.display.update()