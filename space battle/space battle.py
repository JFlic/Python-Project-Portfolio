if __name__ == "__main__":
    pass

import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("Space battle")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

rectangle_color = (255,255,255)
bullet_color = (255,255,0)
score_font = pygame.font.Font('freesansbold.ttf',32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

player1Img = pygame.image.load("rocket.png")

player1X = 0
player1Y = 300
player1_changeX = 0
player1_changeY = 0
score1 = 0
text1Y = 10
text1X = 10

number_of_bullets = 3

bullet_change1 = 5
bulletY1 = []
bulletX1 = []
bullet_state1 = []

for i in range(number_of_bullets):
    bulletY1.append(0)
    bulletX1.append(0)
    bullet_state1.append("ready")

bullet_change2 = -5
bulletY2 = []
bulletX2 = []
bullet_state2 = []

for i in range(number_of_bullets):
    bulletY2.append(0)
    bulletX2.append(0)
    bullet_state2.append("ready")


player2Img = pygame.image.load("spaceship (1).png")

player2X = 1200
player2Y = 300
player2_changeX = 0
player2_changeY = 0
score2 = 0
test2X = 1040
text2Y = 10

def player1(x,y,image):
    image_rot = pygame.transform.rotate(image, -90)
    screen.blit(image_rot,(x,y))

def player2(x,y,image):
    image_rot = pygame.transform.rotate(image, 90)
    screen.blit(image_rot,(x,y))

def bullet_fire1(x,y):
    bullet_state1[i] = "fire"
    bullet = pygame.draw.rect(screen, rectangle_color, pygame.Rect(x + 50, y + 30, 30, 5))

def bullet_fire2(x,y):
    bullet_state2[i] = "fire"
    bullet = pygame.draw.rect(screen, rectangle_color, pygame.Rect(x-25, y+30, 30, 5))

def total_score1(x,y):
    score = score_font.render("Score : " + str(score1), True, (255, 255, 255))
    screen.blit(score, (x, y))

def total_score2(x,y):
    score = score_font.render("Score : " + str(score2), True, (255,255,255))
    screen.blit(score,(x,y))

running = True
game_end = False

player1_left = False
player2_left = False

player1_right = False
player2_right = False

player1_up = False
player2_up = False

player1_down = False
player2_down = False

while running:

    screen.fill((0,0,0))
    pygame.draw.rect(screen, rectangle_color, pygame.Rect(595, 0, 5, 700))

    player1_changeX = 0
    player1_changeY = 0

    player2_changeX = 0
    player2_changeY = 0

    if score1 >= 10 or score2 >= 10:
        if score1 > score2:
            over_text = over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(over_text, (90, 200))
            win2 = score_font.render("ship 1 wins", True, (255, 255, 255))
            screen.blit(win2, (200, 260))

        if score2 > score1:
            over_text = over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(over_text, (700, 200))
            win2 = score_font.render("ship 2 wins",True,(255,255,255))
            screen.blit(win2,(820,260))

        game_end = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player1_left = True
            if event.key == pygame.K_d:
                player1_right = True
            if event.key == pygame.K_s:
                player1_down = True
            if event.key == pygame.K_w:
                player1_up = True
            if event.key == pygame.K_c:
                for i in range(number_of_bullets):
                    if bullet_state1[i] == "ready":
                        bulletY1[i] = player1Y
                        bulletX1[i] = player1X
                        bullet_fire1(bulletX1[i], bulletY1[i])
                        break

            if event.key == pygame.K_j:
                player2_left = True
            if event.key == pygame.K_l:
                player2_right = True
            if event.key == pygame.K_k:
                player2_down = True
            if event.key == pygame.K_i:
                player2_up = True
            if event.key == pygame.K_n:
                for i in range(number_of_bullets):
                    if bullet_state2[i] == "ready":
                        bulletY2[i] = player2Y
                        bulletX2[i] = player2X
                        bullet_fire2(bulletX2[i], bulletY2[i])
                        break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                player2_left = False
            if event.key == pygame.K_l:
                player2_right = False
            if event.key == pygame.K_k:
                player2_down = False
            if event.key == pygame.K_i:
                player2_up = False

            if event.key == pygame.K_a:
                player1_left = False
            if event.key == pygame.K_d:
                player1_right = False
            if event.key == pygame.K_s:
                player1_down = False
            if event.key == pygame.K_w:
                player1_up = False


    for i in range(number_of_bullets):
        if game_end == False:
            Distance = math.sqrt((bulletX1[i] - player2X) ** 2 + (bulletY1[i] - player2Y) ** 2)
            if bulletX1[i] > 1200:
                bulletX1[i] = 0
                bulletY1[i] = 0
                bullet_state1[i] = "ready"

            if bullet_state1[i] == "fire":
                bullet_fire1(bulletX1[i], bulletY1[i])
                bulletX1[i] += bullet_change1
            if Distance < 38:
                bullet_state1[i] = "ready"
                bulletX1[i] = 0
                bulletY1[i] = 0
                score1 += 1

    for i in range(number_of_bullets):
        if game_end == False:
            Distance = math.sqrt((bulletX2[i] - player1X) ** 2 + (bulletY2[i] - player1Y) ** 2)
            if bulletX2[i] < 0:
                bulletX2[i] = 1200
                bulletY2[i] = 1200
                bullet_state2[i] = "ready"

            if bullet_state2[i] == "fire":
                bullet_fire2(bulletX2[i], bulletY2[i])
                bulletX2[i] += bullet_change2
            if Distance < 38:
                bullet_state2[i] = "ready"
                bulletX2[i] = 1200
                bulletY2[i] = 1200
                score2 += 1

    if player1_left:
        player1_changeX = -3
    if player1_right:
        player1_changeX = 3
    if player1_up:
        player1_changeY = -3
    if player1_down:
        player1_changeY = 3

    if player1X <= 0:
        player1X = 0
    if player1X >= 535:
        player1X = 535
    if player1Y <= 0:
        player1Y = 0
    if player1Y >= 635:
        player1Y = 635

    if player2_left:
        player2_changeX = -3
    if player2_right:
        player2_changeX = 3
    if player2_up:
        player2_changeY = -3
    if player2_down:
        player2_changeY = 3

    if player2X >= 1140:
        player2X = 1140
    if player2X <= 600:
        player2X = 600
    if player2Y <= 0:
        player2Y = 0
    if player2Y >= 635:
        player2Y = 635

    player1X += player1_changeX
    player1Y += player1_changeY

    player2X += player2_changeX
    player2Y += player2_changeY

    player1(player1X, player1Y, player1Img)
    player2(player2X, player2Y, player2Img)
    total_score1(text1X, text1Y)
    total_score2(test2X, text2Y)

    pygame.display.update()