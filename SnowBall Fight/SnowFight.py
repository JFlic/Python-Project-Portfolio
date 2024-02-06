if __name__ == "__main__":
    pass

import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Snow Ball Fight")
clock = pygame.time.Clock()
over_font = pygame.font.Font('freesansbold.ttf', 64)
green_font = pygame.font.Font('freesansbold.ttf', 32)
winner_font = pygame.font.Font('freesansbold.ttf',32)

#player setup
class Player:
    def __init__(self,player_pos,player_hitbox,player_direction,
                 player_img,player_bulletImg,player_can_angle,
                 p_bullet_startX, p_bullet_startY, player_bullet_ang, p_dirX,
                 p_dirY,p_bullet_count,player_b_hitbox,p_pretime,playerType):

        self.player_pos = player_pos
        self.player_hitbox = player_hitbox
        self.player_direction = player_direction
        self.player_img = player_img
        self.player_bulletImg = player_bulletImg
        self.player_can_angle = player_can_angle
        self.p_bullet_startX = p_bullet_startX
        self.p_bullet_startY = p_bullet_startY
        self.player_bullet_ang = player_bullet_ang
        self.p_dirX = p_dirX
        self.p_dirY = p_dirY
        self.p_bullet_count = p_bullet_count
        self.player_b_hitbox = player_b_hitbox
        self.p_pretime = p_pretime
        self.playerType = playerType


player = Player([100, 600],pygame.Rect(1100 + 25,
                100 + 25, 50, 50),90,pygame.image.load("game images/player1.png")
                ,pygame.image.load("game images/Green_Snowball.png"),
                0, 0, 0, 0, 0, 0, 0, pygame.Rect(0 + 20,
                0 + 20, 20, 20), pygame.time.get_ticks(),'player')

player2 = Player([1100, 100],pygame.Rect(1100 + 25,
                100 + 25, 50, 50),90,pygame.image.load("game images/player2.png")
                ,pygame.image.load("game images/Red_Snowball.png"),
                0, 0, 0, 0, 0, 0, 0, pygame.Rect(0 + 20,
                0 + 20, 20, 20), pygame.time.get_ticks(), 'player2')

player_right = False
player_left = False
player_up = False
player_down = False

player_right2 = False
player_left2 = False
player_up2 = False
player_down2 = False

#Enemy setup

class bullets:
    def __init__(self,bulletX,bulletY,bulletAngle,Xdirection,Ydirection,
                 hitbox, hitboxX, hitboxY,canDelet,bulletType):
        self.bulletX = bulletX
        self.bulletY = bulletY
        self.bulletAngle = bulletAngle+90
        self.Xdirection = Xdirection
        self.Ydirection = Ydirection
        self.hitbox = hitbox
        self.hitboxX = hitboxX
        self.hitboxY = hitboxY
        self.canDelet = canDelet
        self.bulletType = bulletType

List_of_bullets = []

def update_tank(x, y, tank_img, tank_direction):
    tank_img = pygame.transform.rotozoom(tank_img, tank_direction, 1)
    tank_rect = tank_img.get_rect(center=(x, y))
    screen.blit(tank_img, tank_rect)

def update_bullets(x, y, angle, Snow_ball):
    bullet_rotated = pygame.transform.rotozoom(Snow_ball, angle+180, 1)
    bullet_rect = bullet_rotated.get_rect(center=(x, y))
    screen.blit(bullet_rotated, bullet_rect)

def inside_wall_check(bullet_list):
    for bullets in bullet_list:
        if (bullets.bulletX > 805 and bullets.bulletX < 895):
            if (bullets.bulletY > 150 and bullets.bulletY < 225):
                bullet_list.remove(bullets)
        if (bullets.bulletX > 805 and bullets.bulletX < 995):
            if (bullets.bulletY > 225 and bullets.bulletY < 295):
                bullet_list.remove(bullets)
        if (bullets.bulletX > 305 and bullets.bulletX < 395):
            if (bullets.bulletY < 545 and bullets.bulletY > 475):
                bullet_list.remove(bullets)
        if (bullets.bulletX > 205 and bullets.bulletX < 395):
            if (bullets.bulletY < 475 and bullets.bulletY > 410):
                bullet_list.remove(bullets)

#defining obstacle positions
player_wall1 = pygame.Rect(800, 225, 200, 75)
player_wall2 = pygame.Rect(800, 150, 100, 75)
enemy_wall1 = pygame.Rect(200, 400, 200, 75)
enemy_wall2 = pygame.Rect(300, 475, 100, 75)


player_win = False
enemy_win = False
running = True
running_Start = True

while running:

    screen.fill((118, 211, 222))

    pygame.draw.rect(screen, (18, 160, 176), enemy_wall1)
    pygame.draw.rect(screen, (18, 160, 176), enemy_wall2)
    pygame.draw.rect(screen, (18, 160, 176), player_wall1)
    pygame.draw.rect(screen, (18, 160, 176), player_wall2)


    while running_Start:
        screen.fill((118, 211, 222))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_Start = False
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running_Start = False

        over_text = over_font.render("Welcome to Snow Ball Fight!", True, (255, 255, 255))
        green_text = green_font.render("Move the green player with W,A,S,D and shoot with Q", True, (255, 255, 255))
        red_text = green_font.render("Move the red player with arrow keys and shoot with P", True, (255, 255, 255))
        start_text = over_font.render("Press space to start", True, (255, 255, 255))
        screen.blit(over_text, (140, 75))
        screen.blit(green_text,(170, 225))
        screen.blit(red_text, (170, 325))
        screen.blit(start_text, (280, 450))
        pygame.display.update()

    if enemy_win:
        over_text = over_font.render("Red Wins!", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        player_right, player_left, player_up, player_down = False, False, False, False

    if player_win:
        over_text = over_font.render("Green wins!", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        player_right, player_left, player_up, player_down = False, False, False, False

    #makes red x button work
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #player movement
        if not player_win and not enemy_win:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player_left = True
                if event.key == pygame.K_d:
                    player_right = True
                if event.key == pygame.K_w:
                    player_up = True
                if event.key == pygame.K_s:
                    player_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player_left = False
                if event.key == pygame.K_d:
                    player_right = False
                if event.key == pygame.K_w:
                    player_up = False
                if event.key == pygame.K_s:
                    player_down = False

            # player1 movement
            if not player_win and not enemy_win:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_left2 = True
                    if event.key == pygame.K_RIGHT:
                        player_right2 = True
                    if event.key == pygame.K_UP:
                        player_up2 = True
                    if event.key == pygame.K_DOWN:
                        player_down2 = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player_left2 = False
                    if event.key == pygame.K_RIGHT:
                        player_right2 = False
                    if event.key == pygame.K_UP:
                        player_up2 = False
                    if event.key == pygame.K_DOWN:
                        player_down2 = False

            if event.type == pygame.KEYUP:
               if event.key == pygame.K_p:
                   if not player_win and not enemy_win:
                       current_time = pygame.time.get_ticks()
                       if current_time - player2.p_pretime > 2000:
                           player2.p_bullet_count = 0
                       if current_time - player2.p_pretime > 300:
                           if player2.p_bullet_count < 5:
                               player2.p_pretime = current_time
                               player2.p_bullet_startX = (player2.player_pos[0])
                               player2.p_bullet_startY = (player2.player_pos[1])
                               b_hitboxX = math.sin(math.radians(player2.player_bullet_ang))
                               b_hitboxY = math.cos(math.radians(player2.player_bullet_ang))
                               player2.can_delete = False
                               List_of_bullets.append(bullets(
                                player2.p_bullet_startX, player2.p_bullet_startY, player2.player_bullet_ang +90,
                                player2.p_dirX, player2.p_dirY,
                                player2.player_b_hitbox, b_hitboxX, b_hitboxY, player2.can_delete,"player2"))

                               player2.p_bullet_count += 1

            if event.type == pygame.KEYUP:
               if event.key == pygame.K_q:
                   if not player_win and not enemy_win:
                       current_time = pygame.time.get_ticks()
                       if current_time - player.p_pretime > 2000:
                           player.p_bullet_count = 0
                       if current_time - player.p_pretime > 300:
                           if player.p_bullet_count < 5:
                               player.p_pretime = current_time
                               player.p_bullet_startX = (player.player_pos[0])
                               player.p_bullet_startY = (player.player_pos[1])
                               b_hitboxX = math.sin(math.radians(player.player_bullet_ang))
                               b_hitboxY = math.cos(math.radians(player.player_bullet_ang))
                               player.can_delete = False
                               List_of_bullets.append(bullets(
                                player.p_bullet_startX, player.p_bullet_startY, player.player_bullet_ang +90,
                                player.p_dirX, player.p_dirY,
                                player.player_b_hitbox, b_hitboxX, b_hitboxY, player.can_delete,"player"))

                               player.p_bullet_count += 1

    inside_wall_check(List_of_bullets)

    player_mov_sp = 1
    # player movement and direction
    if player_right2:
        player2.player_pos[0] += player_mov_sp
        player2.player_direction = 0
        player2.player_bullet_ang = 0
    if player_left2:
        player2.player_pos[0] -= player_mov_sp
        player2.player_direction = 180
        player2.player_bullet_ang = 180
    if player_down2:
        player2.player_pos[1] += player_mov_sp
        player2.player_direction = 270
        player2.player_bullet_ang = 270
    if player_up2:
        player2.player_pos[1] -= player_mov_sp
        player2.player_direction = 90
        player2.player_bullet_ang = 90

    if player_right2 and player_up2:
        player2.player_direction = 45
        player2.player_bullet_ang = 45
    if player_right2 and player_down2:
        player2.player_direction = 315
        player2.player_bullet_ang = 315
    if player_left2 and player_up2:
        player2.player_direction = 125
        player2.player_bullet_ang = 125
    if player_left2 and player_down2:
        player2.player_direction =  225
        player2.player_bullet_ang = 225

    if player2.player_pos[0] > 1175:
        player2.player_pos[0] = 1175
    if player2.player_pos[0] < 25:
        player2.player_pos[0] = 25
    if player2.player_pos[1] > 675:
        player2.player_pos[1] = 675
    if player2.player_pos[1] < 25:
        player2.player_pos[1] = 25

    #

    if player_right:
        player.player_pos[0] += player_mov_sp
        player.player_direction = 0
        player.player_bullet_ang = 0
    if player_left:
        player.player_pos[0] -= player_mov_sp
        player.player_direction = 180
        player.player_bullet_ang = 180
    if player_down:
        player.player_pos[1] += player_mov_sp
        player.player_direction = 270
        player.player_bullet_ang = 270
    if player_up:
        player.player_pos[1] -= player_mov_sp
        player.player_direction = 90
        player.player_bullet_ang = 90

    if player_right and player_up:
        player.player_direction = 45
        player.player_bullet_ang = 45
    if player_right and player_down:
        player.player_direction = 315
        player.player_bullet_ang = 315
    if player_left and player_up:
        player.player_direction = 125
        player.player_bullet_ang = 125
    if player_left and player_down:
        player.player_direction =  225
        player.player_bullet_ang = 225

    if player.player_pos[0] > 1175:
        player.player_pos[0] = 1175
    if player.player_pos[0] < 25:
        player.player_pos[0] = 25
    if player.player_pos[1] > 675:
        player.player_pos[1] = 675
    if player.player_pos[1] < 25:
        player.player_pos[1] = 25

    # bullet bounce
    p_bullet_speed = 5.0
    for bullet in List_of_bullets:
        if not player_win and not enemy_win:
            if (bullet.bulletX < 1200 and bullet.bulletX > 0) and (bullet.bulletY < 700 and bullet.bulletY > 0):
                    if bullet.bulletAngle == 270:
                        bullet.bulletX = bullet.bulletX
                        bullet.bulletY = bullet.bulletY - p_bullet_speed
                    if bullet.bulletAngle == 450:
                        bullet.bulletX = bullet.bulletX
                        bullet.bulletY = bullet.bulletY + p_bullet_speed
                    if bullet.bulletAngle == 360:
                        bullet.bulletX = bullet.bulletX - p_bullet_speed
                        bullet.bulletY = bullet.bulletY
                    if bullet.bulletAngle == 180:
                        bullet.bulletX = bullet.bulletX + p_bullet_speed
                        bullet.bulletY = bullet.bulletY
                    if bullet.bulletAngle == 225:
                        bullet.bulletX = bullet.bulletX + p_bullet_speed
                        bullet.bulletY = bullet.bulletY - p_bullet_speed
                    if bullet.bulletAngle == 405:
                        bullet.bulletX = bullet.bulletX - p_bullet_speed
                        bullet.bulletY = bullet.bulletY + p_bullet_speed
                    if bullet.bulletAngle == 305:
                        bullet.bulletX = bullet.bulletX - p_bullet_speed
                        bullet.bulletY = bullet.bulletY - p_bullet_speed
                    if bullet.bulletAngle == 495:
                        bullet.bulletX = bullet.bulletX + p_bullet_speed
                        bullet.bulletY = bullet.bulletY + p_bullet_speed

                    update_bullets(bullet.bulletX, bullet.bulletY, bullet.bulletAngle, pygame.image.load("game images/Green_Snowball.png"))
            else:
                List_of_bullets.remove(bullet)

    # Snowballs hitting Snowballs
    for bullet in List_of_bullets:
        for next_bullet in List_of_bullets:
            if next_bullet.bulletType != bullet.bulletType:
                distance = math.sqrt((next_bullet.bulletX - bullet.bulletX) ** 2 + (next_bullet.bulletY - bullet.bulletY) ** 2)
                if distance != 0 and distance < 8:
                    List_of_bullets.remove(next_bullet)
                    List_of_bullets.remove(bullet)

    # player wall collitions
    collision_tolerance = 5
    if player.player_hitbox.colliderect(player_wall1):
        if abs((player_wall1.top) - player.player_hitbox.bottom) < collision_tolerance:
            player.player_pos[1] -= player_mov_sp
        if abs(player_wall1.bottom - player.player_hitbox.top) < collision_tolerance:
            player.player_pos[1] += player_mov_sp
        if abs(player_wall1.right - player.player_hitbox.left) < collision_tolerance:
            player.player_pos[0] += player_mov_sp
        if abs(player_wall1.left - player.player_hitbox.right) < collision_tolerance:
            player.player_pos[0] -= player_mov_sp
    if player.player_hitbox.colliderect(player_wall2):
        if abs(player_wall2.top - player.player_hitbox.bottom) < collision_tolerance:
            player.player_pos[1] -= player_mov_sp
        if abs(player_wall2.right - player.player_hitbox.left) < collision_tolerance:
            player.player_pos[0] += player_mov_sp
        if abs(player_wall2.left - player.player_hitbox.right) < collision_tolerance:
            player.player_pos[0] -= player_mov_sp
    if player.player_hitbox.colliderect(enemy_wall1):
        if abs(enemy_wall1.top - player.player_hitbox.bottom) < collision_tolerance:
            player.player_pos[1] -= player_mov_sp
        if abs(enemy_wall1.bottom - player.player_hitbox.top) < collision_tolerance:
            player.player_pos[1] += player_mov_sp
        if abs(enemy_wall1.right - player.player_hitbox.left) < collision_tolerance:
            player.player_pos[0] += player_mov_sp
        if abs(enemy_wall1.left - player.player_hitbox.right) < collision_tolerance:
            player.player_pos[0] -= player_mov_sp
    if player.player_hitbox.colliderect(enemy_wall2):
        if abs(enemy_wall2.bottom - player.player_hitbox.top) < collision_tolerance:
            player.player_pos[1] += player_mov_sp
        if abs(enemy_wall2.right - player.player_hitbox.left) < collision_tolerance:
            player.player_pos[0] += player_mov_sp
        if abs(enemy_wall2.left - player.player_hitbox.right) < collision_tolerance:
            player.player_pos[0] -= player_mov_sp


    if player2.player_hitbox.colliderect(player_wall1):
        if abs((player_wall1.top) - player2.player_hitbox.bottom) < collision_tolerance:
            player2.player_pos[1] -= player_mov_sp
        if abs(player_wall1.bottom - player2.player_hitbox.top) < collision_tolerance:
            player2.player_pos[1] += player_mov_sp
        if abs(player_wall1.right - player2.player_hitbox.left) < collision_tolerance:
            player2.player_pos[0] += player_mov_sp
        if abs(player_wall1.left - player2.player_hitbox.right) < collision_tolerance:
            player2.player_pos[0] -= player_mov_sp
    if player2.player_hitbox.colliderect(player_wall2):
        if abs(player_wall2.top - player2.player_hitbox.bottom) < collision_tolerance:
            player2.player_pos[1] -= player_mov_sp
        if abs(player_wall2.right - player2.player_hitbox.left) < collision_tolerance:
            player2.player_pos[0] += player_mov_sp
        if abs(player_wall2.left - player2.player_hitbox.right) < collision_tolerance:
            player2.player_pos[0] -= player_mov_sp
    if player2.player_hitbox.colliderect(enemy_wall1):
        if abs(enemy_wall1.top - player2.player_hitbox.bottom) < collision_tolerance:
            player2.player_pos[1] -= player_mov_sp
        if abs(enemy_wall1.bottom - player2.player_hitbox.top) < collision_tolerance:
            player2.player_pos[1] += player_mov_sp
        if abs(enemy_wall1.right - player2.player_hitbox.left) < collision_tolerance:
            player2.player_pos[0] += player_mov_sp
        if abs(enemy_wall1.left - player2.player_hitbox.right) < collision_tolerance:
            player2.player_pos[0] -= player_mov_sp
    if player2.player_hitbox.colliderect(enemy_wall2):
        if abs(enemy_wall2.bottom - player2.player_hitbox.top) < collision_tolerance:
            player2.player_pos[1] += player_mov_sp
        if abs(enemy_wall2.right - player2.player_hitbox.left) < collision_tolerance:
            player2.player_pos[0] += player_mov_sp
        if abs(enemy_wall2.left - player2.player_hitbox.right) < collision_tolerance:
            player2.player_pos[0] -= player_mov_sp

    player.player_hitbox = pygame.Rect(player.player_pos[0] - 27, player.player_pos[1] - 27, 55, 54)
    update_tank(player.player_pos[0], player.player_pos[1], player.player_img, player.player_direction)

    player2.player_hitbox = pygame.Rect(player2.player_pos[0] - 27, player2.player_pos[1] - 27, 55, 54)
    update_tank(player2.player_pos[0], player2.player_pos[1], player2.player_img, player2.player_direction)


    for bullet in List_of_bullets:
        if bullet.bulletType == player.playerType:
            Distance = math.sqrt((bullet.bulletX - player2.player_pos[0]) ** 2 + (bullet.bulletY - player2.player_pos[1]) ** 2)
            if Distance < 38:
                 player_win = True
        if bullet.bulletType == player2.playerType:
            Distance = math.sqrt((bullet.bulletX - player.player_pos[0]) ** 2 + (bullet.bulletY - player.player_pos[1]) ** 2)
            if Distance < 38:
                 enemy_win = True

    clock.tick(100)
    pygame.display.update()
