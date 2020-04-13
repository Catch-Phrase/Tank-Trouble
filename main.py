import pygame as pg
import math as m

vec = pg.Vector2

# Screen Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 128, 255)
GREEN = (44, 201, 48)
PINK = (255, 20, 147)

# Game Constants
WALLS = 10
FIRST_WALL_X = 100
FIRST_WALL_Y = 25
WALL_SPACE = (WINDOW_WIDTH - FIRST_WALL_X * 2) // WALLS
X_VEC = vec(0, 1)
Y_VEC = vec(1, 0)

# Bullet Constants
BULLET_RAD = 7
BULLET_SPEED = 5
AMMUNITION = 3

# Tank Constnts
TANK_SPEED = 2
TANK_ROTATION_SPEED = 2

# Graphics Setup
pg.init()
pg.font.init()
pg.mixer.init()
size = WINDOW_WIDTH, WINDOW_HEIGHT
screen = pg.display.set_mode(size)
pg.display.set_caption("Tank Trouble")
clock = pg.time.Clock()

def get_font(font_size):
    return pg.font.SysFont('consolas', font_size)

# Sprite Loading
green_tank = pg.image.load('green tank.png').convert()
green_tank.set_colorkey(PINK)
red_tank = pg.image.load('red tank.png').convert()
red_tank.set_colorkey(PINK)

green_tank_icon = pg.image.load('green tank icon.png').convert()
green_tank_icon.set_colorkey(PINK)
red_tank_icon = pg.image.load('red tank icon.png').convert()
red_tank_icon.set_colorkey(PINK)

g_tank_width = green_tank.get_rect().width
g_tank_height = green_tank.get_rect().height
r_tank_width = red_tank.get_rect().width
r_tank_height = red_tank.get_rect().height

g_icon_width = green_tank_icon.get_rect().width
g_icon_height = green_tank_icon.get_rect().height
r_icon_width = red_tank_icon.get_rect().width
r_icon_height = red_tank_icon.get_rect().height


def menu_background():
    pg.mouse.set_visible(True)
    # background image
    menu_img = pg.image.load('menu background.jpg')
    screen.blit(menu_img, (0, 0))

    # title text
    menu_title_text = get_font(120).render('Tank Trouble', True, BLACK, WHITE)
    menu_title_text_rect = menu_title_text.get_rect()
    menu_title_text_rect.center = (int(WINDOW_WIDTH / 2), 100)
    screen.blit(menu_title_text, menu_title_text_rect)

    # game modes text
    menu_mode_text = get_font(110).render('Play', True, BLACK, WHITE)
    menu_mode_text_rect = menu_mode_text.get_rect()
    menu_mode_text_rect.center = (WINDOW_WIDTH//6, WINDOW_HEIGHT//2)
    screen.blit(menu_mode_text, menu_mode_text_rect)

    pg.display.flip()

    return menu_mode_text_rect


def name_choose_screen_background():
    pg.mouse.set_visible(True)
    screen.fill(WHITE)

    play_button = get_font(100).render("PLAY", True, BLACK)
    play_button_rect = play_button.get_rect()
    play_button_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 6))

    screen.blit(play_button, play_button_rect)

    instr_text = get_font(70).render("Enter Names", True, BLACK)
    instr_text_rect = instr_text.get_rect()
    instr_text_rect.center = (int(WINDOW_WIDTH / 2), play_button_rect.bottom + 50)

    screen.blit(instr_text, instr_text_rect)

    return play_button_rect


def end_screen_background(winner, names):
    pg.mouse.set_visible(True)
    screen.fill(WHITE)

    if winner == 'Green':
        end_screen_title = get_font(100).render(names[0] + " Wins!", True, BLACK)
    else:
        end_screen_title = get_font(100).render(names[1] + " Wins!", True, BLACK)

    end_screen_title_rect = end_screen_title.get_rect()
    end_screen_title_rect.center = (int(WINDOW_WIDTH / 2), 150)
    screen.blit(end_screen_title, end_screen_title_rect)

    new_game_text = get_font(80).render('Play Again', True, BLACK)
    new_game_text_rect = new_game_text.get_rect()
    new_game_text_rect.center = (int(WINDOW_WIDTH / 2), 350)
    screen.blit(new_game_text, new_game_text_rect)

    return_to_main_text = get_font(80).render('Main Menu', True, BLACK)
    return_to_main_text_rect = return_to_main_text.get_rect()
    return_to_main_text_rect.center = (int(WINDOW_WIDTH / 2), 550)
    screen.blit(return_to_main_text, return_to_main_text_rect)

    leave_game_text = get_font(50).render('Leave Game', True, BLACK)
    leave_game_text_rect = leave_game_text.get_rect()
    leave_game_text_rect.center = (int(WINDOW_WIDTH / 4), 750)
    screen.blit(leave_game_text, leave_game_text_rect)

    return [new_game_text_rect, return_to_main_text_rect, leave_game_text_rect]


def main_menu():
    mouse_pos_menu = (0, 0)
    menu_finish = False

    while not menu_finish:
        menu_play_button = menu_background()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos_menu = pg.mouse.get_pos()

        if menu_play_button.collidepoint(mouse_pos_menu):
            menu_finish = True


def name_choose_screen():
    color_inactive = BLACK
    color_active = RED

    color1 = color_inactive
    active1 = False
    name1 = ''

    color2 = color_inactive
    active2 = False
    name2 = ''

    input_box1 = pg.Rect(0, int(WINDOW_HEIGHT * 0.4), 250, 100)
    input_box1.centerx = int(WINDOW_WIDTH / 2)

    input_box2 = pg.Rect(0, int(WINDOW_HEIGHT * 0.6), 250, 100)
    input_box2.centerx = int(WINDOW_WIDTH / 2)

    while True:
        play_button_rect = name_choose_screen_background()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos

                    if play_button_rect.collidepoint(mouse_pos):
                        return [name1, name2]

                    if input_box1.collidepoint(mouse_pos):
                        active1 = not active1
                    else:
                        active1 = False

                    if active1:
                        color1 = color_active
                    else:
                        color1 = color_inactive

                    if input_box2.collidepoint(mouse_pos):
                        active2 = not active2
                    else:
                        active2 = False

                    if active2:
                        color2 = color_active
                    else:
                        color2 = color_inactive

            if event.type == pg.KEYDOWN:
                if active1:
                    if event.key == pg.K_RETURN:
                        name1 = ''
                    elif event.key == pg.K_BACKSPACE:
                        name1 = name1[:-1]
                    else:
                        name1 += event.unicode

                if active2:
                    if event.key == pg.K_RETURN:
                        name2 = ''
                    elif event.key == pg.K_BACKSPACE:
                        name2 = name2[:-1]
                    else:
                        name2 += event.unicode

        text_name1 = get_font(80).render(name1, True, BLACK)
        text_name2 = get_font(80).render(name2, True, BLACK)

        width = max(200, text_name1.get_width() + 10)
        input_box1.w = width
        input_box1.centerx = int(WINDOW_WIDTH / 2)
        screen.blit(text_name1, (input_box1.x + 5, input_box1.y + 5))
        pg.draw.rect(screen, color1, input_box1, 2)

        width = max(200, text_name2.get_width() + 10)
        input_box2.w = width
        input_box2.centerx = int(WINDOW_WIDTH / 2)
        screen.blit(text_name2, (input_box2.x + 5, input_box2.y + 5))
        pg.draw.rect(screen, color2, input_box2, 2)

        pg.display.flip()
        clock.tick(60)


def build_walls():
    vertical_wall_list = []
    for i in range(WALLS + 1):
        col = []
        wall_x = FIRST_WALL_X + WALL_SPACE * i
        for j in range(WALLS):
            wall = pg.draw.line(screen, WHITE, (wall_x, FIRST_WALL_Y + WALL_SPACE * j),
                                (wall_x, FIRST_WALL_Y + WALL_SPACE * (j + 1)), 7)
            col.append([wall.copy(), False])
        vertical_wall_list.append(col)

    horizontal_wall_list = []
    for i in range(WALLS + 1):
        row = []
        wall_y = FIRST_WALL_Y + WALL_SPACE * i
        for j in range(WALLS):
            wall = pg.draw.line(screen, WHITE, (FIRST_WALL_X + WALL_SPACE * j, wall_y),
                                (FIRST_WALL_X + WALL_SPACE * (j + 1), wall_y), 7)
            row.append([wall.copy(), False])
        horizontal_wall_list.append(row)

    return vertical_wall_list, horizontal_wall_list


def build_level_1():
    screen.fill(WHITE)
    ver_walls, hor_walls = build_walls()

    # Outer Walls
    for i in range(WALLS):
        ver_walls[0][i][1] = True
        ver_walls[WALLS][i][1] = True

        hor_walls[0][i][1] = True
        hor_walls[WALLS][i][1] = True

    # Maze
    ver_walls[1][1][1] = True
    ver_walls[1][4][1] = True
    ver_walls[1][5][1] = True
    ver_walls[1][6][1] = True

    ver_walls[2][3][1] = True
    ver_walls[2][7][1] = True
    ver_walls[2][8][1] = True

    ver_walls[3][2][1] = True
    ver_walls[3][8][1] = True

    ver_walls[4][0][1] = True
    ver_walls[4][1][1] = True
    ver_walls[4][3][1] = True
    ver_walls[4][7][1] = True

    ver_walls[5][1][1] = True
    ver_walls[5][2][1] = True
    ver_walls[5][6][1] = True
    ver_walls[5][8][1] = True
    ver_walls[5][9][1] = True

    ver_walls[6][1][1] = True
    ver_walls[6][2][1] = True
    ver_walls[6][3][1] = True
    ver_walls[6][5][1] = True
    ver_walls[6][7][1] = True

    ver_walls[7][1][1] = True
    ver_walls[7][2][1] = True
    ver_walls[7][8][1] = True

    ver_walls[8][1][1] = True
    ver_walls[8][5][1] = True
    ver_walls[8][6][1] = True
    ver_walls[8][9][1] = True

    ver_walls[9][5][1] = True
    ver_walls[9][8][1] = True

    hor_walls[1][2][1] = True
    hor_walls[1][3][1] = True
    hor_walls[1][8][1] = True

    hor_walls[2][1][1] = True
    hor_walls[2][2][1] = True
    hor_walls[2][8][1] = True
    hor_walls[2][9][1] = True

    hor_walls[3][0][1] = True
    hor_walls[3][4][1] = True
    hor_walls[3][7][1] = True
    hor_walls[3][8][1] = True

    hor_walls[4][2][1] = True
    hor_walls[4][3][1] = True
    hor_walls[4][7][1] = True
    hor_walls[4][8][1] = True

    hor_walls[5][2][1] = True
    hor_walls[5][3][1] = True
    hor_walls[5][5][1] = True
    hor_walls[5][7][1] = True

    hor_walls[6][2][1] = True
    hor_walls[6][3][1] = True
    hor_walls[6][4][1] = True
    hor_walls[6][6][1] = True
    hor_walls[6][9][1] = True

    hor_walls[7][1][1] = True
    hor_walls[7][3][1] = True
    hor_walls[7][4][1] = True
    hor_walls[7][8][1] = True

    hor_walls[8][0][1] = True
    hor_walls[8][5][1] = True
    hor_walls[8][7][1] = True
    hor_walls[8][8][1] = True

    hor_walls[9][1][1] = True
    hor_walls[9][2][1] = True
    hor_walls[9][3][1] = True
    hor_walls[9][6][1] = True

    for row in ver_walls:
        for wall in row:
            if wall[1]:
                pg.draw.rect(screen, BLACK, wall[0])

    for col in hor_walls:
        for wall in col:
            if wall[1]:
                pg.draw.rect(screen, BLACK, wall[0])

    return ver_walls, hor_walls


def game(counter, names):
    pg.mouse.set_visible(False)
    winner = 'Green'

    green_pos = vec(FIRST_WALL_X + WALL_SPACE // 2, FIRST_WALL_Y + WALL_SPACE // 2)
    green_dir = vec(0, 1)
    red_pos = vec(WINDOW_WIDTH - FIRST_WALL_X - WALL_SPACE // 2, int(FIRST_WALL_Y + WALL_SPACE * (WALLS - 0.5)))
    red_dir = vec(0, 1)

    green_bullets = []
    red_bullets = []
    for i in range(AMMUNITION):
        x_g = 250 - i * 50
        y_g = (WINDOW_HEIGHT + FIRST_WALL_Y + WALL_SPACE * WALLS) // 2 + 40
        green_bullets.append([vec(x_g, y_g), vec(0, 0), False])

        x_r = WINDOW_WIDTH - x_g
        y_r = y_g
        red_bullets.append([vec(x_r, y_r), vec(0, 0), False])

    ammo_used_g = 0
    ammo_used_r = 0

    green_max_size = (g_tank_width**2 + g_tank_height**2)**0.5
    red_max_size = (g_tank_width**2 + g_tank_height**2)**0.5

    finish = False
    while not finish:
        ver_walls, hor_walls = build_level_1()

        name1 = names[0]
        name2 = names[1]

        counter_name1 = get_font(40).render(' ' + name1 + ' ', True, BLACK)
        counter_name2 = get_font(40).render(' ' + name2 + ' ', True, BLACK)

        counter_name1_rect = counter_name1.get_rect()
        counter_name2_rect = counter_name2.get_rect()

        width_name1 = max(200, counter_name1.get_width() + 10)
        counter_name1_rect.w = width_name1
        counter_name1_rect.center = (int(WINDOW_WIDTH / 2 - width_name1 / 2), 770)
        screen.blit(counter_name1, counter_name1_rect)

        width_name2 = max(200, counter_name2.get_width() + 10)
        counter_name2_rect.w = width_name2
        counter_name2_rect.center = (int(WINDOW_WIDTH / 2 + width_name2 / 2), 770)
        screen.blit(counter_name2, counter_name2_rect)

        counter_num1 = get_font(50).render(' ' + str(counter[0]) + ' ', True, BLACK)
        counter_num1_rect = counter_num1.get_rect()
        counter_num1_rect.center = WINDOW_WIDTH // 2 - counter_num1_rect.width // 2, counter_name1_rect.bottom + counter_num1_rect.height//2 - 1
        screen.blit(counter_num1, counter_num1_rect)

        counter_num2 = get_font(50).render(' ' + str(counter[1]) + ' ', True, BLACK)
        counter_num2_rect = counter_num2.get_rect()
        counter_num2_rect.center = WINDOW_WIDTH // 2 + counter_num2_rect.width // 2, counter_name1_rect.bottom + counter_num2_rect.height//2 - 1
        screen.blit(counter_num2, counter_num2_rect)

        pg.draw.rect(screen, BLACK, counter_name1_rect, 2)
        pg.draw.rect(screen, BLACK, counter_name2_rect, 2)
        pg.draw.rect(screen, BLACK, counter_num1_rect, 2)
        pg.draw.rect(screen, BLACK, counter_num2_rect, 2)

        green_shoot = False
        red_shoot = False

        g_front_in_wall = False
        g_back_in_wall = False
        r_front_in_wall = False
        r_back_in_wall = False

        green_rotate = green_dir.angle_to(vec(0, 1))
        red_rotate = red_dir.angle_to(vec(0, 1))

        g_rotated = pg.transform.rotate(green_tank, green_rotate)
        r_rotated = pg.transform.rotate(red_tank, red_rotate)

        screen.blit(g_rotated, (int(green_pos.x - g_rotated.get_rect().width//2), int(green_pos.y - g_rotated.get_rect().height//2)))
        screen.blit(r_rotated, (int(red_pos.x - r_rotated.get_rect().width//2), int(red_pos.y - r_rotated.get_rect().height//2)))

        g_hitbox = g_rotated.get_rect()
        g_hitbox.center = int(green_pos.x), int(green_pos.y)

        green_angle = green_dir.angle_to(vec(1, 0))

        if 45 <= green_angle <= 135:
            g_hitbox_front = pg.Rect(g_hitbox.left, g_hitbox.top, g_hitbox.width, g_hitbox.height//2)
            g_hitbox_back = pg.Rect(g_hitbox.left, g_hitbox.top + g_hitbox.height//2, g_hitbox.width, g_hitbox.height//2)
        elif 135 <= green_angle <= 180 or -180 <= green_angle <= -135:
            g_hitbox_front = pg.Rect(g_hitbox.left, g_hitbox.top, g_hitbox.width//2, g_hitbox.height)
            g_hitbox_back = pg.Rect(g_hitbox.left + g_hitbox.width//2, g_hitbox.top, g_hitbox.width//2, g_hitbox.height)
        elif -135 <= green_angle <= -45:
            g_hitbox_front = pg.Rect(g_hitbox.left, g_hitbox.top + g_hitbox.height//2, g_hitbox.width, g_hitbox.height//2)
            g_hitbox_back = pg.Rect(g_hitbox.left, g_hitbox.top, g_hitbox.width, g_hitbox.height//2)
        elif -45 <= green_angle <= 45:
            g_hitbox_front = pg.Rect(g_hitbox.left + g_hitbox.width//2, g_hitbox.top, g_hitbox.width//2, g_hitbox.height)
            g_hitbox_back = pg.Rect(g_hitbox.left, g_hitbox.top, g_hitbox.width//2, g_hitbox.height)

        for i in ver_walls:
            for j in i:
                if g_hitbox_front.colliderect(j[0]) and j[1]:
                    g_front_in_wall = True
                elif g_hitbox_back.colliderect(j[0]) and j[1]:
                    g_back_in_wall = True

        for i in hor_walls:
            for j in i:
                if g_hitbox_front.colliderect(j[0]) and j[1]:
                    g_front_in_wall = True
                elif g_hitbox_back.colliderect(j[0]) and j[1]:
                    g_back_in_wall = True

        r_hitbox = r_rotated.get_rect()
        r_hitbox.center = int(red_pos.x), int(red_pos.y)

        red_angle = red_dir.angle_to(vec(1, 0))

        if 45 <= red_angle <= 135:
            r_hitbox_front = pg.Rect(r_hitbox.left, r_hitbox.top, r_hitbox.width, r_hitbox.height // 2)
            r_hitbox_back = pg.Rect(r_hitbox.left, r_hitbox.top + r_hitbox.height // 2, r_hitbox.width,
                                    r_hitbox.height // 2)
        elif 135 <= red_angle <= 180 or -180 <= red_angle <= -135:
            r_hitbox_front = pg.Rect(r_hitbox.left, r_hitbox.top, r_hitbox.width // 2, r_hitbox.height)
            r_hitbox_back = pg.Rect(r_hitbox.left + r_hitbox.width // 2, r_hitbox.top, r_hitbox.width // 2, r_hitbox.height)
        elif -135 <= red_angle <= -45:
            r_hitbox_front = pg.Rect(r_hitbox.left, r_hitbox.top + r_hitbox.height // 2, r_hitbox.width,
                                     r_hitbox.height // 2)
            r_hitbox_back = pg.Rect(r_hitbox.left, r_hitbox.top, r_hitbox.width, r_hitbox.height // 2)
        elif -45 <= red_angle <= 45:
            r_hitbox_front = pg.Rect(r_hitbox.left + r_hitbox.width // 2, r_hitbox.top, r_hitbox.width // 2,
                                     r_hitbox.height)
            r_hitbox_back = pg.Rect(r_hitbox.left, r_hitbox.top, r_hitbox.width // 2, r_hitbox.height)

        for i in ver_walls:
            for j in i:
                if r_hitbox_front.colliderect(j[0]) and j[1]:
                    r_front_in_wall = True
                elif r_hitbox_back.colliderect(j[0]) and j[1]:
                    r_back_in_wall = True

        for i in hor_walls:
            for j in i:
                if r_hitbox_front.colliderect(j[0]) and j[1]:
                    r_front_in_wall = True
                elif r_hitbox_back.colliderect(j[0]) and j[1]:
                    r_back_in_wall = True

        icon_y = (WINDOW_HEIGHT + FIRST_WALL_Y + WALL_SPACE * WALLS) // 2 - 20

        screen.blit(green_tank_icon, (150 - g_icon_width // 2, icon_y - g_icon_height // 2))
        screen.blit(red_tank_icon, (WINDOW_WIDTH - 150 - r_icon_width // 2, icon_y - r_icon_height // 2))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    green_shoot = True
                if event.key == pg.K_SPACE:
                    red_shoot = True

        keyboard = pg.key.get_pressed()

        if keyboard[pg.K_UP] and not g_front_in_wall:
            green_pos += green_dir * TANK_SPEED
        if keyboard[pg.K_DOWN] and not g_back_in_wall:
            green_pos -= green_dir * TANK_SPEED
        if keyboard[pg.K_LEFT]:
            green_dir = green_dir.rotate(-TANK_ROTATION_SPEED)
        if keyboard[pg.K_RIGHT]:
            green_dir = green_dir.rotate(TANK_ROTATION_SPEED)

        if keyboard[pg.K_w] and not r_front_in_wall:
            red_pos += red_dir * TANK_SPEED
        if keyboard[pg.K_s] and not r_back_in_wall:
            red_pos -= red_dir * TANK_SPEED
        if keyboard[pg.K_a]:
            red_dir = red_dir.rotate(-2)
        if keyboard[pg.K_d]:
            red_dir = red_dir.rotate(2)

        green_bullet_rects = []
        for i in green_bullets:
            i[0] += i[1] * BULLET_SPEED
            pixel_pos = (int(i[0].x), int(i[0].y))
            green_bullet_rects.append(pg.draw.circle(screen, BLACK, pixel_pos, BULLET_RAD, 0))

        red_bullet_rects = []
        for i in red_bullets:
            i[0] += i[1] * BULLET_SPEED
            pixel_pos = (int(i[0].x), int(i[0].y))
            red_bullet_rects.append(pg.draw.circle(screen, BLACK, pixel_pos, BULLET_RAD, 0))

        if green_shoot and ammo_used_g < AMMUNITION:
            g_cannon = vec(g_tank_height//2 * green_dir.x, g_tank_height//2 * green_dir.y)
            green_bullets[ammo_used_g][0] = vec(green_pos.x + g_cannon.x, green_pos.y + g_cannon.y)
            green_bullets[ammo_used_g][1] = green_dir
            green_bullets[ammo_used_g][2] = True
            ammo_used_g += 1

        if red_shoot and ammo_used_r < AMMUNITION:
            r_cannon = vec(r_tank_height//2 * red_dir.x, r_tank_height//2 * red_dir.y)
            red_bullets[ammo_used_r][0] = vec(red_pos.x + r_cannon.x, red_pos.y + r_cannon.y)
            red_bullets[ammo_used_r][1] = red_dir
            red_bullets[ammo_used_r][2] = True
            ammo_used_r += 1

        for i in green_bullets:
            if i[0].x <= FIRST_WALL_X + (5 + BULLET_RAD):
                i[1] = i[1].reflect(Y_VEC)
            elif i[0].x >= WINDOW_WIDTH - FIRST_WALL_X - (5 + BULLET_RAD):
                i[1] = i[1].reflect(Y_VEC)
            elif i[0].y <= FIRST_WALL_Y + (5 + BULLET_RAD):
                i[1] = i[1].reflect(X_VEC)
            elif i[0].y >= WALLS*WALL_SPACE + FIRST_WALL_Y - (5 + BULLET_RAD):
                i[1] = i[1].reflect(X_VEC)

        for i in red_bullets:
            if i[0].x <= FIRST_WALL_X + (5 + BULLET_RAD):
                i[1] = i[1].reflect(Y_VEC)
            elif i[0].x >= WINDOW_WIDTH - FIRST_WALL_X - (5 + BULLET_RAD):
                i[1] = i[1].reflect(Y_VEC)
            elif i[0].y <= FIRST_WALL_Y + (5 + BULLET_RAD):
                i[1] = i[1].reflect(X_VEC)
            elif i[0].y >= WALLS*WALL_SPACE + FIRST_WALL_Y - (5 + BULLET_RAD):
                i[1] = i[1].reflect(X_VEC)

        for i in range(len(green_bullet_rects)):
            if g_hitbox.colliderect(green_bullet_rects[i]) and not green_bullets[i][2]:
                finish = True
                winner = 'Red'
            elif r_hitbox.colliderect(green_bullet_rects[i]):
                finish = True
                winner = 'Green'

        for i in range(len(red_bullet_rects)):
            if g_hitbox.colliderect(red_bullet_rects[i]):
                finish = True
                winner = 'Red'
            elif r_hitbox.colliderect(red_bullet_rects[i]) and not red_bullets[i][2]:
                finish = True
                winner = 'Green'

        for i in green_bullets:
            if i[0].distance_to(green_pos) >= green_max_size:
                i[2] = False

        for i in red_bullets:
            if i[0].distance_to(red_pos) >= red_max_size:
                i[2] = False

        pg.display.flip()
        clock.tick(60)

    return winner


def end_screen(winner, names):
    button_pos = end_screen_background(winner, names)
    play_again_button = button_pos[0]
    main_menu_button = button_pos[1]
    leave_button = button_pos[2]
    mouse_pos_game = [0, 0]

    end_screen_finish = False

    while not end_screen_finish:
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos_game = pg.mouse.get_pos()

        if play_again_button.collidepoint(mouse_pos_game):
            return True

        if main_menu_button.collidepoint(mouse_pos_game):
            return False

        if leave_button.collidepoint(mouse_pos_game):
            pg.quit()


# Game

while True:
    main_menu()

    counter = [0, 0]
    new_game = True
    names = name_choose_screen()

    while new_game:

        winner = game(counter, names)

        if winner == 'Green':
            counter[0] += 1
        if winner == 'Red':
            counter[1] += 1

        new_game_two = end_screen(winner, names)

pygame.quit()




pg.quit()
