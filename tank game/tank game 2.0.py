if __name__ == "__main__":
    pass

import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Tank Game 2.0")
clock = pygame.time.Clock()
over_font = pygame.font.Font('freesansbold.ttf', 64)
winner_font = pygame.font.Font('freesansbold.ttf',32)

# Image setup
player_pos = [1100, 100]
player_hitbox = pygame.Rect(player_pos[0] + 25, player_pos[1] + 25, 50, 50)
player_direction = 90
player_img = pygame.image.load("tank body.png")
player_canimg = pygame.image.load("tank gun.png")
player_bulletImg = pygame.image.load("bullet.png")

player_bullets = []

p_bullet_startX, p_bullet_startY = 0, 0
p_dirX, p_dirY = 0, 0
p_bullet_count = 0
player_b_hitbox = pygame.Rect(p_bullet_startX + 10, p_bullet_startY + 10, 10, 10)
p_pretime = pygame.time.get_ticks()


enemy_pos = [100, 600]
enemy_hitbox_angle = 0
enemy_direction = 90
enemy_img = pygame.image.load("enemy tank body.png")
enemy_canimg = pygame.image.load("enemy tank cannon.png")
enemy_bulletImg = pygame.image.load("bullet.png")

enemy_bullets = []
enemy_detection = []
enemy_detected = False
e_detection_dirX, e_detection_dirY = 0, 0

e_bullet_startX, e_bullet_startY = 0, 0
e_dirX, e_dirY = 0, 0
e_bullet_count = 0
enemy_b_hitbox = pygame.Rect(e_bullet_startX + 10, e_bullet_startY + 10, 10, 10)
e_pretime = pygame.time.get_ticks()

enemy_hitbox = pygame.Rect(enemy_pos[0] + 25, enemy_pos[1] + 25, 50, 50)
enemy_detection_timer = pygame.time.get_ticks()
enemy_bullet_timer = pygame.time.get_ticks()
enemy_firing = False
enemy_box_detection = pygame.Rect(e_bullet_startX+10, e_bullet_startY+10, 10, 10)

player_wall1 = pygame.Rect(800, 225, 200, 75)
player_wall2 = pygame.Rect(800, 150, 100, 75)
enemy_wall1 = pygame.Rect(200, 400, 200, 75)
enemy_wall2 = pygame.Rect(300, 475, 100, 75)
player_can_angle = 0
enemy_can_angle = 0

def update_tank(x, y, tank_img, tank_direction):
    tank_img = pygame.transform.rotozoom(tank_img, tank_direction, 1)
    tank_rect = tank_img.get_rect(center=(x, y))
    screen.blit(tank_img, tank_rect)

def update_can(x, y, cannon_img, angle):
    cannon_rotated = pygame.transform.rotozoom(cannon_img, angle+180, 0.8)
    cannon_rect = cannon_rotated.get_rect(center=(x, y))
    screen.blit(cannon_rotated, cannon_rect)

def update_bullets(x, y, angle):
    bullet_rotated = pygame.transform.rotozoom(player_bulletImg, angle+180, 1)
    bullet_rect = bullet_rotated.get_rect(center=(x, y))
    screen.blit(bullet_rotated, bullet_rect)

def inside_wall_check(bullet_list):
    for bullets in bullet_list:
        if (bullets[0] > 805 and bullets[0] < 895):
            if (bullets[1] > 150 and bullets[1] < 225):
                bullet_list.remove(bullets)
        if (bullets[0] > 805 and bullets[0] < 995):
            if (bullets[1] > 225 and bullets[1] < 295):
                bullet_list.remove(bullets)
        if (bullets[0] > 305 and bullets[0] < 395):
            if (bullets[1] < 545 and bullets[1] > 475):
                bullet_list.remove(bullets)
        if (bullets[0] > 205 and bullets[0] < 395):
            if (bullets[1] < 475 and bullets[1] > 410):
                bullet_list.remove(bullets)

def bullets_bounce(bullet_list):
    for bullets in bullet_list:
        bullets[6] = pygame.Rect(bullets[7] + bullets[0], bullets[8] + bullets[1], 5, 5)
        if bullets[6].colliderect(player_wall1):
            if abs(player_wall1.top - bullets[6].bottom) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "horiz"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(player_wall1):
            if abs(player_wall1.bottom - bullets[6].top) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "horiz"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(player_wall1):
            if abs(player_wall1.right - bullets[6].left) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "vert"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(player_wall1):
            if abs(player_wall1.left - bullets[6].right) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "vert"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(player_wall2):
            if abs(player_wall2.top - bullets[6].bottom) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "horiz"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(player_wall2):
            if abs(player_wall2.left - bullets[6].right) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "vert"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(player_wall2):
            if abs(player_wall2.right - bullets[6].left) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "vert"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(enemy_wall1):
            if abs(enemy_wall1.top - bullets[6].bottom) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "horiz"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(enemy_wall1):
            if abs(enemy_wall1.bottom - bullets[6].top) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "horiz"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(enemy_wall1):
            if abs(enemy_wall1.right - bullets[6].left) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "vert"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(enemy_wall1):
            if abs(enemy_wall1.left - bullets[6].right) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "vert"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(enemy_wall2):
            if abs(enemy_wall2.bottom - bullets[6].top) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "horiz"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(enemy_wall2):
            if abs(enemy_wall2.left - bullets[6].right) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "vert"
                else:
                    bullets[9] = True
        if bullets[6].colliderect(enemy_wall2):
            if abs(enemy_wall2.right - bullets[6].left) < collision_tolerance:
                if bullets[5] == "none":
                    bullets[5] = "vert"
                else:
                    bullets[9] = True
    for bullets in bullet_list:
        if bullets[9]:
            bullet_list.remove(bullets)

player_right = False
player_left = False
player_up = False
player_down = False

enemy_right = False
enemy_left = False
enemy_up = False
enemy_down = False

enemy_moving_up = True
enemy_moving_down = False
enemy_moving_right = False
enemy_moving_left = False

game_over1 = False
game_over2 = False
running = True
while running:

    screen.fill((205, 183, 158))

    # obstacle
    pygame.draw.rect(screen, (155, 133, 108), enemy_wall1)
    pygame.draw.rect(screen, (155, 133, 108), enemy_wall2)
    pygame.draw.rect(screen, (155, 133, 108), player_wall1)
    pygame.draw.rect(screen, (155, 133, 108), player_wall2)

    if game_over1:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        win2 = winner_font.render("You lose", True, (255, 255, 255))
        screen.blit(win2, (200, 260))

    if game_over2:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        win2 = winner_font.render("You win", True, (255, 255, 255))
        screen.blit(win2, (200, 260))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player movement
        if not game_over1 and not game_over2:
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

        # angling cannon
        if event.type == pygame.MOUSEMOTION:
            if not game_over1 and not game_over2:
                mx, my = pygame.mouse.get_pos()
                p_dirX, p_dirY = mx-player_pos[0], my-player_pos[1]
                length = math.hypot(p_dirX, p_dirY)
                b_dirX = math.sin(math.radians(player_can_angle)) * 50
                b_dirY = math.cos(math.radians(player_can_angle)) * 50
                p_bullet_startX = (b_dirX + player_pos[0])
                p_bullet_startY = (b_dirY + player_pos[1])

                if length == 0.0:
                    p_dirX, p_dirY = 0, -1
                else:
                    p_dirX, p_dirY = (p_dirX)/length, p_dirY/length
                player_can_angle = math.degrees(math.atan2(p_dirX, p_dirY))


        #player bullet fire
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over1 and not game_over2:
                current_time = pygame.time.get_ticks()
                if current_time - p_pretime > 2000:
                    p_bullet_count = 0
                if current_time - p_pretime > 300:
                    if p_bullet_count < 5:
                        p_pretime = current_time
                        b_dirX = math.sin(math.radians(player_can_angle)) * 50
                        b_dirY = math.cos(math.radians(player_can_angle)) * 50
                        p_bullet_startX = (b_dirX + player_pos[0])
                        p_bullet_startY = (b_dirY + player_pos[1])
                        player_bullet_ang = player_can_angle
                        b_hitboxX = math.sin(math.radians(player_bullet_ang))
                        b_hitboxY = math.cos(math.radians(player_bullet_ang))
                        player_b_hitbox = pygame.Rect(b_hitboxX + p_bullet_startX, b_hitboxY + p_bullet_startY, 10, 8)
                        bounce = "none"
                        can_delete = False
                        player_bullets.append([p_bullet_startX, p_bullet_startY, player_bullet_ang, p_dirX,
                                               p_dirY, bounce, player_b_hitbox, b_hitboxX, b_hitboxY, can_delete])
                        p_bullet_count += 1


    inside_wall_check(player_bullets)
    inside_wall_check(enemy_bullets)

    # player movement and direction
    player_mov_sp = 1
    if player_right:
        player_pos[0] += player_mov_sp
        player_direction = 90
    if player_left:
        player_pos[0] -= player_mov_sp
        player_direction = 270
    if player_down:
        player_pos[1] += player_mov_sp
        player_direction = 180
    if player_up:
        player_pos[1] -= player_mov_sp
        player_direction = 0

    if player_right and player_up:
        player_direction = 135
    if player_right and player_down:
        player_direction = 45
    if player_left and player_up:
        player_direction = 45
    if player_left and player_down:
        player_direction = 135

    if player_pos[0] > 1175:
        player_pos[0] = 1175
    if player_pos[0] < 25:
        player_pos[0] = 25
    if player_pos[1] > 675:
        player_pos[1] = 675
    if player_pos[1] < 25:
        player_pos[1] = 25

    # bullet bounce
    p_bullet_speed = 1.5
    for bullets in player_bullets:
        if not game_over1 and not game_over2:
            if (bullets[0] < 1200 and bullets[0] > 0) and (bullets[1] < 700 and bullets[1] > 0):
                if bullets[5] == "none":
                    bullets[0] = bullets[0] + bullets[3] * p_bullet_speed
                    bullets[1] = bullets[1] + bullets[4] * p_bullet_speed
                    bullets[5] = "none"
                    if (bullets[0] > 1200 or bullets[0] < 0):
                        bullets[5] = "vert"
                    if (bullets[1] > 700 or bullets[1] < 0):
                        bullets[5] = "horiz"
                    update_bullets(bullets[0], bullets[1], bullets[2])

                if bullets[5] == "horiz":
                    bullets[0] = bullets[0] + bullets[3] * p_bullet_speed
                    bullets[1] = bullets[1] - bullets[4] * p_bullet_speed
                    bullets[5] = "horiz"
                    update_bullets(bullets[0], bullets[1], -bullets[2])
                    bullets[6] = pygame.Rect(bullets[7] + bullets[0], bullets[8] + bullets[1], 5, 5)

                if bullets[5] == "vert":
                    bullets[0] = bullets[0] - bullets[3] * p_bullet_speed
                    bullets[1] = bullets[1] + bullets[4] * p_bullet_speed
                    bullets[5] = "vert"
                    update_bullets(bullets[0], bullets[1], -bullets[2])
                    bullets[6] = pygame.Rect(bullets[7] + bullets[0], bullets[8] + bullets[1], 5, 5)

            else:
                player_bullets.remove(bullets)

    # bullets hitting bullets
    for bullets in player_bullets:
        for bullet in player_bullets:
            distance = math.sqrt((bullets[0] - bullet[0]) **2 + (bullets[1] - bullet[1]) **2)
            if distance != 0 and distance < 8:
                player_bullets.remove(bullets)
                player_bullets.remove(bullet)

    for bullets in player_bullets:
        for bullet in enemy_bullets:
            distance = math.sqrt((bullets[0] - bullet[0]) **2 + (bullets[1] - bullet[1]) **2)
            if distance != 0 and distance < 8:
                player_bullets.remove(bullets)
                enemy_bullets.remove(bullet)

    for bullets in enemy_bullets:
        for bullet in enemy_bullets:
            distance = math.sqrt((bullets[0] - bullet[0]) **2 + (bullets[1] - bullet[1]) **2)
            if distance != 0 and distance < 8:
                enemy_bullets.remove(bullets)
                enemy_bullets.remove(bullet)

    player_mov_sp = 1
    # player wall collitions
    collision_tolerance = 5
    if player_hitbox.colliderect(player_wall1):
        if abs((player_wall1.top) - player_hitbox.bottom) < collision_tolerance:
            player_pos[1] -= player_mov_sp
        if abs(player_wall1.bottom - player_hitbox.top) < collision_tolerance:
            player_pos[1] += player_mov_sp
        if abs(player_wall1.right - player_hitbox.left) < collision_tolerance:
            player_pos[0] += player_mov_sp
        if abs(player_wall1.left - player_hitbox.right) < collision_tolerance:
            player_pos[0] -= player_mov_sp
    if player_hitbox.colliderect(player_wall2):
        if abs(player_wall2.top - player_hitbox.bottom) < collision_tolerance:
            player_pos[1] -= player_mov_sp
        if abs(player_wall2.right - player_hitbox.left) < collision_tolerance:
            player_pos[0] += player_mov_sp
        if abs(player_wall2.left - player_hitbox.right) < collision_tolerance:
            player_pos[0] -= player_mov_sp
    if player_hitbox.colliderect(enemy_wall1):
        if abs(enemy_wall1.top - player_hitbox.bottom) < collision_tolerance:
            player_pos[1] -= player_mov_sp
        if abs(enemy_wall1.bottom - player_hitbox.top) < collision_tolerance:
            player_pos[1] += player_mov_sp
        if abs(enemy_wall1.right - player_hitbox.left) < collision_tolerance:
            player_pos[0] += player_mov_sp
        if abs(enemy_wall1.left - player_hitbox.right) < collision_tolerance:
            player_pos[0] -= player_mov_sp
    if player_hitbox.colliderect(enemy_wall2):
        if abs(enemy_wall2.bottom - player_hitbox.top) < collision_tolerance:
            player_pos[1] += player_mov_sp
        if abs(enemy_wall2.right - player_hitbox.left) < collision_tolerance:
            player_pos[0] += player_mov_sp
        if abs(enemy_wall2.left - player_hitbox.right) < collision_tolerance:
            player_pos[0] -= player_mov_sp

    # bullet walls bounce

    bullets_bounce(player_bullets)

    player_hitbox = pygame.Rect(player_pos[0] - 27, player_pos[1] - 27, 55, 54)
    update_tank(player_pos[0], player_pos[1], player_img, player_direction)
    update_can(player_pos[0], player_pos[1], player_canimg, player_can_angle)

    inside_wall_check(enemy_bullets)

    e_detection_dirX, e_detection_dirY = player_pos[0]-enemy_pos[0], player_pos[1]-enemy_pos[1]
    enemy_length = math.hypot(e_detection_dirX, e_detection_dirY)
    if enemy_length == 0.0:
        e_detection_dirX, e_detection_dirY = 0, -1
    else:
        e_detection_dirX, e_detection_dirY = e_detection_dirX / enemy_length, e_detection_dirY / enemy_length
    enemy_hitbox_angle = math.degrees(math.atan2(-e_detection_dirY, e_detection_dirX))

    enemy_current_time = pygame.time.get_ticks()
    if enemy_current_time - enemy_detection_timer > 500:
        enemy_detection_timer = enemy_current_time
        enemy_detectionX, enemy_dectectionY = enemy_pos[0], enemy_pos[1]

        detection_stop = 0
        e_detection_dirX, e_detection_dirY = player_pos[0] - enemy_detectionX, player_pos[1] - enemy_dectectionY
        if e_detection_dirX == 0.0:
            e_detection_dirX, e_detection_dirY = 0, 1
        else:
            e_detection_dirX, e_detection_dirY = e_detection_dirX/enemy_length, e_detection_dirY/enemy_length
        enemy_detection.append([enemy_detectionX, enemy_dectectionY, e_detection_dirX, e_detection_dirY, enemy_length, detection_stop])

    detection_speed = 10
    for boxes in enemy_detection:
        if (boxes[4] > boxes[5]):
            boxes[5] += 10
            boxes[0] = boxes[0] + boxes[2] * detection_speed
            boxes[1] = boxes[1] + boxes[3] * detection_speed
            detection = pygame.Rect(boxes[0], boxes[1], 10, 10)
            if detection.colliderect(player_wall1):
                enemy_detected = True
            if detection.colliderect(player_wall2):
                enemy_detected = True
            if detection.colliderect(enemy_wall1):
                enemy_detected = True
            if detection.colliderect(enemy_wall2):
                enemy_detected = True

        else:
            enemy_detected = False
            enemy_detection.remove(boxes)


    enemy_reload_time = pygame.time.get_ticks()

    enemy_bullet_count = 0
    for boxes in enemy_detection:
        if (boxes[4] < boxes[5]):
            if enemy_detected == False:
                enemy_firing = True

    enemy_bullet_time = pygame.time.get_ticks()
    if enemy_firing:
        if enemy_bullet_time - enemy_bullet_timer > 2000:
            e_bullet_count = 0

        if enemy_bullet_time - enemy_bullet_timer > 300:
            if e_bullet_count < 5:
                enemy_bullet_timer = enemy_bullet_time
                e_dirX = math.sin(math.radians(enemy_hitbox_angle+90)) * 50
                e_dirY = math.cos(math.radians(enemy_hitbox_angle+90)) * 50
                e_bullet_startX = (e_dirX + enemy_pos[0])
                e_bullet_startY = (e_dirY + enemy_pos[1])
                enemy_bullet_ang = enemy_hitbox_angle
                e_hitboxX = math.sin(math.radians(enemy_bullet_ang))
                e_hitboxY = math.cos(math.radians(enemy_bullet_ang))
                enemy_b_hitbox = pygame.Rect(e_hitboxX + e_bullet_startX, e_hitboxY + e_bullet_startY, 10, 8)
                bounce = "none"
                can_delete = False
                enemy_bullets.append([e_bullet_startX, e_bullet_startY, enemy_bullet_ang+90, e_dirX,
                                       e_dirY, bounce, enemy_b_hitbox, e_hitboxX, e_hitboxY, can_delete])
                e_bullet_count += 1
        else:
            enemy_firing = False

    e_bullet_speed = 0.03
    for bullets in enemy_bullets:
        if not game_over1 and not game_over2:
            if (bullets[0] < 1200 and bullets[0] > 0) and (bullets[1] < 700 and bullets[1] > 0):
                if bullets[5] == "none":
                    bullets[0] = bullets[0] + bullets[3] * e_bullet_speed
                    bullets[1] = bullets[1] + bullets[4] * e_bullet_speed
                    bullets[5] = "none"
                    if (bullets[0] > 1200 or bullets[0] < 0):
                        bullets[5] = "vert"
                    if (bullets[1] > 700 or bullets[1] < 0):
                        bullets[5] = "horiz"
                    update_bullets(bullets[0], bullets[1], bullets[2])

                if bullets[5] == "horiz":
                    bullets[0] = bullets[0] + bullets[3] * e_bullet_speed
                    bullets[1] = bullets[1] - bullets[4] * e_bullet_speed
                    bullets[5] = "horiz"
                    update_bullets(bullets[0], bullets[1], -bullets[2])
                    bullets[6] = pygame.Rect(bullets[7] + bullets[0], bullets[8] + bullets[1], 5, 5)

                if bullets[5] == "vert":
                    bullets[0] = bullets[0] - bullets[3] * e_bullet_speed
                    bullets[1] = bullets[1] + bullets[4] * e_bullet_speed
                    bullets[5] = "vert"
                    update_bullets(bullets[0], bullets[1], -bullets[2])
                    bullets[6] = pygame.Rect(bullets[7] + bullets[0], bullets[8] + bullets[1], 5, 5)

            else:
                enemy_bullets.remove(bullets)

    #enemy bullet bounce check
    bullets_bounce(enemy_bullets)
    if not game_over1 and not game_over2:
        if enemy_moving_up:
            if enemy_pos[1] < 100:
                enemy_moving_up = False
                enemy_moving_right = True
            else:
                enemy_pos[1] -= player_mov_sp

        if enemy_moving_right:
            if enemy_pos[0] > 1100:
                enemy_moving_right = False
                enemy_moving_down = True
            else:
                enemy_pos[0] += player_mov_sp

        if enemy_moving_down:
            if enemy_pos[1] > 600:
                enemy_moving_down = False
                enemy_moving_left = True
            else:
                enemy_pos[1] += player_mov_sp

        if enemy_moving_left:
            if enemy_pos[0] < 100:
                enemy_moving_left = False
                enemy_moving_up = True
            else:
                enemy_pos[0] -= player_mov_sp


    enemy_hitbox = pygame.Rect(enemy_pos[0] - 27, enemy_pos[1] - 27, 55, 54)
    update_tank(enemy_pos[0], enemy_pos[1], enemy_img, enemy_direction)
    update_can(enemy_pos[0], enemy_pos[1], enemy_canimg, enemy_hitbox_angle+90)

    for bullets in player_bullets:
        Distance1 = math.sqrt((bullets[0] - player_pos[0]) **2 +(bullets[1] - player_pos[1])**2)
        Distance2 = math.sqrt((bullets[0] - enemy_pos[0]) ** 2 + (bullets[1] - enemy_pos[1]) ** 2)

        if Distance1 < 38:
            game_over1 = True
        if Distance2 < 38:
            game_over2 = True

    for bullets in enemy_bullets:
        Distance1 = math.sqrt((bullets[0] - player_pos[0]) ** 2 + (bullets[1] - player_pos[1]) ** 2)
        Distance2 = math.sqrt((bullets[0] - enemy_pos[0]) ** 2 + (bullets[1] - enemy_pos[1]) ** 2)

        if Distance1 < 38:
            game_over1 = True
        if Distance2 < 38:
            game_over2 = True

    if game_over1:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        win2 = winner_font.render("You lose", True, (255, 255, 255))
        screen.blit(win2, (200, 260))
        player_right, player_left, player_up,player_down = False, False, False, False

    if game_over2:
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (90, 200))
        win2 = winner_font.render("You win", True, (255, 255, 255))
        screen.blit(win2, (200, 260))
        player_right, player_left, player_up, player_down = False, False, False, False

    pygame.display.update()