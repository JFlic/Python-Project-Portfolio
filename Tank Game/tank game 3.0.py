if __name__ == "__main__":
    pass

import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Tank Game 3.0")
clock = pygame.time.Clock()
over_font = pygame.font.Font('freesansbold.ttf', 64)
winner_font = pygame.font.Font('freesansbold.ttf',32)

#player setup
class Player:
    def __init__(self,player_pos,player_hitbox,player_direction,
                 player_img,player_canImg,player_bulletImg,player_can_angle,
                 p_bullet_startX, p_bullet_startY, p_dirX,
                 p_dirY,p_bullet_count,player_b_hitbox,p_pretime):

        self.player_pos = player_pos
        self.player_hitbox = player_hitbox
        self.player_direction = player_direction
        self.player_img = player_img
        self.player_canImg = player_canImg
        self.player_bulletImg = player_bulletImg
        self.player_can_angle = player_can_angle
        self.p_bullet_startX = p_bullet_startX
        self.p_bullet_startY = p_bullet_startY
        self.p_dirX = p_dirX
        self.p_dirY = p_dirY
        self.p_bullet_count = p_bullet_count
        self.player_b_hitbox = player_b_hitbox
        self.p_pretime = p_pretime

player = Player([1100, 100],pygame.Rect(1100 + 25,
                100 + 25, 50, 50),90,pygame.image.load("tank body.png"),
                pygame.image.load("tank gun.png"),pygame.image.load("bullet.png"),
                0, 0, 0, 0, 0, 0, pygame.Rect(0 + 10,
                0 + 10, 10, 10), pygame.time.get_ticks())

player_right = False
player_left = False
player_up = False
player_down = False

#Enemy setup
class Enemy:
    def __init__(self,enemy_pos,enemy_hitbox_angle,enemy_direction,
                 enemy_img,enemy_canimg,enemy_bulletImg,
                 enemy_detection,enemy_detected,e_detection_dirX, e_detection_dirY,
                 e_bullet_startX,e_bullet_startY,e_dirX, e_dirY, e_bullet_count,
                 enemy_b_hitbox,e_pretime,enemy_hitbox,enemy_detection_timer,
                 enemy_bullet_timer,enemy_firing,enemy_box_detection):

        self.enemy_pos = enemy_pos
        self.enemy_hitbox_angle = enemy_hitbox_angle
        self.enemy_direction = enemy_direction
        self.enemy_img = enemy_img
        self.enemy_canimg = enemy_canimg
        self.enemy_bulletImg = enemy_bulletImg
        self.enemy_detection = enemy_detection
        self.enemy_detected = enemy_detected
        self.e_detection_dirX = e_detection_dirX
        self.e_detection_dirY = e_detection_dirY
        self.e_bullet_startX = e_bullet_startX
        self.e_bullet_startY = e_bullet_startY
        self.e_dirX = e_dirX
        self.e_dirY = e_dirY
        self.e_bullet_count = e_bullet_count
        self.enemy_b_hitbox = enemy_b_hitbox
        self.e_pretime = e_pretime
        self.enemy_hitbox = enemy_hitbox
        self.enemy_detection_timer = enemy_detection_timer
        self.enemy_bullet_timer = enemy_bullet_timer
        self.enemy_firing = enemy_firing
        self.enemy_box_detection = enemy_box_detection


enemy1 = Enemy([100, 600],0,90,pygame.image.load("enemy tank body.png"),
               pygame.image.load("enemy tank cannon.png"),pygame.image.load("bullet.png"),
               [],False,0,0,0,0,0,0,0,
               pygame.Rect(0 + 10, 0 + 10, 10, 10),
               pygame.time.get_ticks(),
               pygame.Rect(100 + 25, 600 + 25, 50, 50),
               pygame.time.get_ticks(),pygame.time.get_ticks(),False,
               pygame.Rect(0+10, 0+10, 10, 10))

enemy_right = False
enemy_left = False
enemy_up = False
enemy_down = False

enemy_moving_up = True
enemy_moving_down = False
enemy_moving_right = False
enemy_moving_left = False

class bullets:
    def __init__(self,bulletX,bulletY,bulletAngle,Xdirection,Ydirection,
                 bounce,hitbox, hitboxX, hitboxY, canDelet,bulletType):
        self.bulletX = bulletX
        self.bulletY = bulletY
        self.bulletAngle = bulletAngle+90
        self.Xdirection = Xdirection
        self.Ydirection = Ydirection
        self.bounce = bounce
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

def update_can(x, y, cannon_img, angle):
    cannon_rotated = pygame.transform.rotozoom(cannon_img, angle+180, 0.8)
    cannon_rect = cannon_rotated.get_rect(center=(x, y))
    screen.blit(cannon_rotated, cannon_rect)

def update_bullets(x, y, angle):
    bullet_rotated = pygame.transform.rotozoom(player.player_bulletImg, angle+180, 1)
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

def bullets_bounce(bullet_list):
    for bullets in bullet_list:
        bullets.hitbox = pygame.Rect(bullets.hitboxX + bullets.bulletX, bullets.hitboxY + bullets.bulletY, 5, 5)
        if bullets.hitbox.colliderect(player_wall1):
            if abs(player_wall1.top - bullets.hitbox.bottom) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "horiz"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(player_wall1):
            if abs(player_wall1.bottom - bullets.hitbox.top) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "horiz"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(player_wall1):
            if abs(player_wall1.right - bullets.hitbox.left) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "vert"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(player_wall1):
            if abs(player_wall1.left - bullets.hitbox.right) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "vert"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(player_wall2):
            if abs(player_wall2.top - bullets.hitbox.bottom) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "horiz"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(player_wall2):
            if abs(player_wall2.left - bullets.hitbox.right) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "vert"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(player_wall2):
            if abs(player_wall2.right - bullets.hitbox.left) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "vert"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(enemy_wall1):
            if abs(enemy_wall1.top - bullets.hitbox.bottom) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "horiz"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(enemy_wall1):
            if abs(enemy_wall1.bottom - bullets.hitbox.top) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "horiz"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(enemy_wall1):
            if abs(enemy_wall1.right - bullets.hitbox.left) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "vert"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(enemy_wall1):
            if abs(enemy_wall1.left - bullets.hitbox.right) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "vert"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(enemy_wall2):
            if abs(enemy_wall2.bottom - bullets.hitbox.top) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "horiz"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(enemy_wall2):
            if abs(enemy_wall2.left - bullets.hitbox.right) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "vert"
                else:
                    bullets.canDelet = True
        if bullets.hitbox.colliderect(enemy_wall2):
            if abs(enemy_wall2.right - bullets.hitbox.left) < collision_tolerance:
                if bullets.bounce == "none":
                    bullets.bounce = "vert"
                else:
                    bullets.canDelet = True
    for bullets in bullet_list:
        if bullets.canDelet:
            bullet_list.remove(bullets)

#defining obstacle positions
player_wall1 = pygame.Rect(800, 225, 200, 75)
player_wall2 = pygame.Rect(800, 150, 100, 75)
enemy_wall1 = pygame.Rect(200, 400, 200, 75)
enemy_wall2 = pygame.Rect(300, 475, 100, 75)

player_win = False
enemy_win = False
running = True

while running:

    screen.fill((205, 183, 158))

    pygame.draw.rect(screen, (155, 133, 108), enemy_wall1)
    pygame.draw.rect(screen, (155, 133, 108), enemy_wall2)
    pygame.draw.rect(screen, (155, 133, 108), player_wall1)
    pygame.draw.rect(screen, (155, 133, 108), player_wall2)

    if enemy_win:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        win2 = winner_font.render("You lose", True, (255, 255, 255))
        screen.blit(win2, (200, 260))

    if player_win:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        win2 = winner_font.render("You win", True, (255, 255, 255))
        screen.blit(win2, (200, 260))

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

        # angling player cannon
        if event.type == pygame.MOUSEMOTION:
            if not player_win and not enemy_win:
                mx, my = pygame.mouse.get_pos()
                player.p_dirX, player.p_dirY = mx - player.player_pos[0], my - player.player_pos[1]
                length = math.hypot(player.p_dirX, player.p_dirY)
                b_dirX = math.sin(math.radians(player.player_can_angle)) * 50
                b_dirY = math.cos(math.radians(player.player_can_angle)) * 50
                player.p_bullet_startX = (b_dirX + player.player_pos[0])
                player.p_bullet_startY = (b_dirY + player.player_pos[1])

                if length == 0.0:
                    player.p_dirX, player.p_dirY = 0, -1
                else:
                    player.p_dirX, player.p_dirY = (player.p_dirX) / length, player.p_dirY / length
                player.player_can_angle = math.degrees(math.atan2(player.p_dirX, player.p_dirY))

        # player bullet fire
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not player_win and not enemy_win:
                current_time = pygame.time.get_ticks()
                if current_time - player.p_pretime > 2000:
                    player.p_bullet_count = 0
                if current_time - player.p_pretime > 300:
                    if player.p_bullet_count < 5:
                        player.p_pretime = current_time
                        b_dirX = math.sin(math.radians(player.player_can_angle)) * 50
                        b_dirY = math.cos(math.radians(player.player_can_angle)) * 50
                        player.p_bullet_startX = (b_dirX + player.player_pos[0])
                        player.p_bullet_startY = (b_dirY + player.player_pos[1])
                        player.player_bullet_ang = player.player_can_angle
                        b_hitboxX = math.sin(math.radians(player.player_bullet_ang))
                        b_hitboxY = math.cos(math.radians(player.player_bullet_ang))
                        player.player_b_hitbox = pygame.Rect(b_hitboxX + player.p_bullet_startX,
                                                             b_hitboxY + player.p_bullet_startY,10, 8)
                        player.bounce = "none"
                        player.can_delete = False
                        List_of_bullets.append(bullets(
                            player.p_bullet_startX, player.p_bullet_startY, player.player_bullet_ang +90,
                             player.p_dirX, player.p_dirY, player.bounce,
                             player.player_b_hitbox, b_hitboxX, b_hitboxY, player.can_delete,"player"))
                        player.p_bullet_count += 1

    inside_wall_check(List_of_bullets)

    # player movement and direction
    player_mov_sp = 1
    if player_right:
        player.player_pos[0] += player_mov_sp
        player.player_direction = 90
    if player_left:
        player.player_pos[0] -= player_mov_sp
        player.player_direction = 270
    if player_down:
        player.player_pos[1] += player_mov_sp
        player.player_direction = 180
    if player_up:
        player.player_pos[1] -= player_mov_sp
        player.player_direction = 0

    if player_right and player_up:
        player.player_direction = 135
    if player_right and player_down:
        player.player_direction = 45
    if player_left and player_up:
        player.player_direction = 45
    if player_left and player_down:
        player.player_direction = 135

    if player.player_pos[0] > 1175:
        player.player_pos[0] = 1175
    if player.player_pos[0] < 25:
        player.player_pos[0] = 25
    if player.player_pos[1] > 675:
        player.player_pos[1] = 675
    if player.player_pos[1] < 25:
        player.player_pos[1] = 25

    # bullet bounce
    p_bullet_speed = 1.5
    for bullet in List_of_bullets:
        if bullet.bulletType == "player":
            p_bullet_speed = 1.5
        else:
            p_bullet_speed = 0.03
        if not player_win and not enemy_win:
            if (bullet.bulletX < 1200 and bullet.bulletX > 0) and (bullet.bulletY < 700 and bullet.bulletY > 0):
                if bullet.bounce == "none":
                    bullet.bulletX = bullet.bulletX + bullet.Xdirection * p_bullet_speed
                    bullet.bulletY = bullet.bulletY + bullet.Ydirection * p_bullet_speed
                    bullet.bounce = "none"
                    if (bullet.bulletX > 1200 or bullet.bulletX < 0):
                        bullet.bounce = "vert"
                    if (bullet.bulletY > 700 or bullet.bulletY < 0):
                        bullet.bounce = "horiz"
                    update_bullets(bullet.bulletX, bullet.bulletY, bullet.bulletAngle)

                if bullet.bounce == "horiz":
                    bullet.bulletX = bullet.bulletX + bullet.Xdirection * p_bullet_speed
                    bullet.bulletY = bullet.bulletY - bullet.Ydirection * p_bullet_speed
                    bullet.bounce = "horiz"
                    update_bullets(bullet.bulletX, bullet.bulletY, -bullet.bulletAngle)
                    bullet.hitbox = pygame.Rect(bullet.hitboxX + bullet.bulletX, bullet.hitboxY + bullet.bulletY, 5, 5)

                if bullet.bounce == "vert":
                    bullet.bulletX = bullet.bulletX - bullet.Xdirection * p_bullet_speed
                    bullet.bulletY = bullet.bulletY + bullet.Ydirection * p_bullet_speed
                    bullet.bounce = "vert"
                    update_bullets(bullet.bulletX, bullet.bulletY, -bullet.bulletAngle)
                    bullets.hitbox = pygame.Rect(bullet.hitboxX + bullet.bulletX, bullet.hitboxY + bullet.bulletY, 5, 5)

            else:
                List_of_bullets.remove(bullet)

    # bullets hitting bullets
    for bullet in List_of_bullets:
        for next_bullet in List_of_bullets:
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

    bullets_bounce(List_of_bullets)

    player.player_hitbox = pygame.Rect(player.player_pos[0] - 27, player.player_pos[1] - 27, 55, 54)
    update_tank(player.player_pos[0], player.player_pos[1], player.player_img, player.player_direction)
    update_can(player.player_pos[0], player.player_pos[1], player.player_canImg, player.player_can_angle)

    #Getting position of enemy tank relative to player
    enemy1.e_detection_dirX, enemy1.e_detection_dirY = player.player_pos[0]-enemy1.enemy_pos[0], player.player_pos[1]-enemy1.enemy_pos[1]

    # Enemy tank predicting player
    if player_right == True:
        enemy1.e_detection_dirX += 100
    if player_left == True:
        enemy1.e_detection_dirX -= 100
    if player_up == True:
        enemy1.e_detection_dirY -= 100
    if player_down == True:
        enemy1.e_detection_dirY += 100


    enemy_length = math.hypot(enemy1.e_detection_dirX, enemy1.e_detection_dirY)
    if enemy_length == 0.0:
        enemy1.e_detection_dirX, enemy1.e_detection_dirY = 0, -1
    else:
        enemy1.e_detection_dirX, enemy1.e_detection_dirY = enemy1.e_detection_dirX / enemy_length, enemy1.e_detection_dirY / enemy_length
    enemy1.enemy_hitbox_angle = math.degrees(math.atan2(-enemy1.e_detection_dirY, enemy1.e_detection_dirX))

    enemy_current_time = pygame.time.get_ticks()
    if enemy_current_time - enemy1.enemy_detection_timer > 500:
        enemy1.enemy_detection_timer = enemy_current_time
        enemy1.enemy_detectionX, enemy1.enemy_dectectionY = enemy1.enemy_pos[0], enemy1.enemy_pos[1]

        detection_stop = 0
        enemy1.e_detection_dirX, enemy1.e_detection_dirY =\
        player.player_pos[0] - enemy1.enemy_detectionX,player.player_pos[1] - enemy1.enemy_dectectionY

        if enemy1.e_detection_dirX == 0.0:
            enemy1.e_detection_dirX, enemy1.e_detection_dirY = 0, 1
        else:
            enemy1.e_detection_dirX, enemy1.e_detection_dirY = enemy1.e_detection_dirX/enemy_length, enemy1.e_detection_dirY/enemy_length
        enemy1.enemy_detection.append([enemy1.enemy_detectionX, enemy1.enemy_dectectionY, enemy1.e_detection_dirX, enemy1.e_detection_dirY, enemy_length, detection_stop])

    detection_speed = 10
    for boxes in enemy1.enemy_detection:

        if (boxes[4] > boxes[5]):
            boxes[5] += 10
            boxes[0] = boxes[0] + boxes[2] * detection_speed
            boxes[1] = boxes[1] + boxes[3] * detection_speed
            detection = pygame.Rect(boxes[0], boxes[1], 10, 10)
            if detection.colliderect(player_wall1):
                enemy1.enemy_detected = True
            if detection.colliderect(player_wall2):
                enemy1.enemy_detected = True
            if detection.colliderect(enemy_wall1):
                enemy1.enemy_detected = True
            if detection.colliderect(enemy_wall2):
                enemy1.enemy_detected = True

            # pygame.draw.rect(screen, (0, 0, 0), detection)
        else:
            enemy1.enemy_detected = False
            enemy1.enemy_detection.remove(boxes)


    enemy_reload_time = pygame.time.get_ticks()


    enemy_bullet_count = 0
    for boxes in enemy1.enemy_detection:
        if (boxes[4] < boxes[5]):
            if enemy1.enemy_detected == False:
                enemy1.enemy_firing = True

    enemy_bullet_time = pygame.time.get_ticks()
    if enemy1.enemy_firing:
        if enemy_bullet_time - enemy1.enemy_bullet_timer > 2000:
            enemy1.e_bullet_count = 0

        if enemy_bullet_time - enemy1.enemy_bullet_timer > 300:
            if enemy1.e_bullet_count < 5:
                enemy1.enemy_bullet_timer = enemy_bullet_time
                enemy1.e_dirX = math.sin(math.radians(enemy1.enemy_hitbox_angle + 90)) * 50
                enemy1.e_dirY = math.cos(math.radians(enemy1.enemy_hitbox_angle + 90)) * 50
                enemy1.e_bullet_startX = (enemy1.e_dirX + enemy1.enemy_pos[0])
                enemy1.e_bullet_startY = (enemy1.e_dirY + enemy1.enemy_pos[1])
                enemy1.enemy_bullet_ang = enemy1.enemy_hitbox_angle
                e_hitboxX = math.sin(math.radians(enemy1.enemy_bullet_ang))
                e_hitboxY = math.cos(math.radians(enemy1.enemy_bullet_ang))
                enemy1.enemy_b_hitbox = pygame.Rect(e_hitboxX + enemy1.e_bullet_startX, e_hitboxY + enemy1.e_bullet_startY, 10, 8)
                enemy1.bounce = "none"
                can_delete = False
                List_of_bullets.append(bullets(enemy1.e_bullet_startX,
                    enemy1.e_bullet_startY, enemy1.enemy_bullet_ang,
                    enemy1.e_dirX,enemy1.e_dirY, enemy1.bounce, enemy1.enemy_b_hitbox,
                    e_hitboxX, e_hitboxY, can_delete,"enemy"))
                enemy1.e_bullet_count += 1
        else:
            enemy1.enemy_firing = False


    # enemy bullet bounce check
    if not player_win and not enemy_win:
        if enemy_moving_up:
            if enemy1.enemy_pos[1] < 100:
                enemy_moving_up = False
                enemy_moving_right = True
            else:
                enemy1.enemy_pos[1] -= player_mov_sp

        if enemy_moving_right:
            if enemy1.enemy_pos[0] > 1100:
                enemy_moving_right = False
                enemy_moving_down = True
            else:
                enemy1.enemy_pos[0] += player_mov_sp

        if enemy_moving_down:
            if enemy1.enemy_pos[1] > 600:
                enemy_moving_down = False
                enemy_moving_left = True
            else:
                enemy1.enemy_pos[1] += player_mov_sp

        if enemy_moving_left:
            if enemy1.enemy_pos[0] < 100:
                enemy_moving_left = False
                enemy_moving_up = True
            else:
                enemy1.enemy_pos[0] -= player_mov_sp


    enemy1.enemy_hitbox = pygame.Rect(enemy1.enemy_pos[0] - 27, enemy1.enemy_pos[1] - 27, 55, 54)
    update_tank(enemy1.enemy_pos[0], enemy1.enemy_pos[1], enemy1.enemy_img, enemy1.enemy_direction)
    update_can(enemy1.enemy_pos[0], enemy1.enemy_pos[1], enemy1.enemy_canimg, enemy1.enemy_hitbox_angle + 90)

    for bullet in List_of_bullets:
        Distance1 = math.sqrt((bullet.bulletX - player.player_pos[0]) **2 +(bullet.bulletY - player.player_pos[1])**2)
        Distance2 = math.sqrt((bullet.bulletX - enemy1.enemy_pos[0]) ** 2 + (bullet.bulletY - enemy1.enemy_pos[1]) ** 2)

        if Distance1 < 38:
            enemy_win = True
        if Distance2 < 38:
            player_win = True

    if enemy_win:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        win2 = winner_font.render("You lose", True, (255, 255, 255))
        screen.blit(win2, (200, 260))
        player_right, player_left, player_up,player_down = False, False, False, False

    if player_win:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        win2 = winner_font.render("You win", True, (255, 255, 255))
        screen.blit(win2, (200, 260))
        player_right, player_left, player_up, player_down = False, False, False, False

    pygame.display.update()
