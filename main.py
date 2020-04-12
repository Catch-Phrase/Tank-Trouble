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
BULLET_SPEED = 1
AMMUNITION = 3

# Tank Constnts
TANK_SPEED = 1


# Graphics Setup
pg.init()
pg.font.init()
pg.mixer.init()
size = WINDOW_WIDTH, WINDOW_HEIGHT
screen = pg.display.set_mode(size)
pg.display.set_caption("Tank Trouble")
clock = pg.time.Clock()

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


def check_collision_x(bullet_pos, ver_walls):
    return False


def check_collision_y(bullet_pos, hor_walls):
    return False

print(vec(1,0).rotate(90000))


green_pos = vec(FIRST_WALL_X + WALL_SPACE // 2, FIRST_WALL_Y + WALL_SPACE // 2)
green_dir = vec(0, 1)
red_pos = vec(WINDOW_WIDTH - FIRST_WALL_X - WALL_SPACE // 2, int(FIRST_WALL_Y + WALL_SPACE * (WALLS - 0.5)))
red_dir = vec(0, 1)

green_bullets = []
red_bullets = []
for i in range(AMMUNITION):
    x_g = 250 - i * 50
    y_g = (WINDOW_HEIGHT + FIRST_WALL_Y + WALL_SPACE * WALLS) // 2 + 40
    green_bullets.append([vec(x_g, y_g), vec(0, 0)])

    x_r = WINDOW_WIDTH - x_g
    y_r = y_g
    green_bullets.append([vec(x_r, y_r), vec(0, 0)])

ammo_used_g = 0
ammo_used_r = 0

green_rotation = 90
red_rotation = 90

green_max_size = (g_tank_width**2 + g_tank_height**2)**0.5
red_max_size = (g_tank_width**2 + g_tank_height**2)**0.5

finish = False
while not finish:
    ver_walls, hor_walls = build_level_1()

    green_rotation_x = int(m.cos(m.radians(green_rotation)) * 100 + 0.5)//100
    green_rotation_y = int(m.sin(m.radians(green_rotation)) * 100 + 0.5)//100
    green_rotation_vec = vec(green_rotation_x, green_rotation_y)
    green_rotate = green_dir.angle_to(green_rotation_vec)
    if green_dir.x != 0:
        green_rotation = m.atan(green_dir.y/green_dir.x)
    else:
        green_rotation = 180 - green_dir.y*90

    green_tank = pg.transform.rotate(green_tank, green_rotate)

    red_rotation_x = int(m.cos(m.radians(red_rotation)) *100 + 0.5)//100
    red_rotation_y = int(m.sin(m.radians(red_rotation)) *100 + 0.5)//100
    red_rotation_vec = vec(red_rotation_x, red_rotation_y)
    red_rotate = red_dir.angle_to(red_rotation_vec)
    if red_dir.x != 0:
        red_rotation = m.atan(red_dir.y/red_dir.x)
    else:
        red_rotation = 180 - red_dir.y

    screen.blit(green_tank, green_pos - vec(g_tank_width//2, g_tank_height//2))
    screen.blit(red_tank, red_pos - vec(r_tank_width//2, r_tank_height//2))

    icon_y = (WINDOW_HEIGHT + FIRST_WALL_Y + WALL_SPACE * WALLS) // 2 - 20

    screen.blit(green_tank_icon, vec(250, icon_y) - vec(g_icon_width // 2, g_icon_height // 2))
    screen.blit(red_tank_icon, vec(WINDOW_WIDTH - 250, icon_y) - vec(r_icon_width // 2, r_icon_height // 2))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finish = True

    keyboard = pg.key.get_pressed()

    if keyboard[pg.K_UP]:
        green_pos += green_dir * TANK_SPEED
    if keyboard[pg.K_DOWN]:
        green_pos -= green_dir * TANK_SPEED
    if keyboard[pg.K_LEFT]:
        print('turn left')
        green_dir = green_dir.rotate(-1)
    if keyboard[pg.K_RIGHT]:
        print('turn right')
        green_dir = green_dir.rotate(1)

    if keyboard[pg.K_w]:
        red_pos += red_dir * TANK_SPEED
    if keyboard[pg.K_s]:
        red_pos -= red_dir * TANK_SPEED
    if keyboard[pg.K_a]:
        green_pos += green_dir * TANK_SPEED
    if keyboard[pg.K_d]:
        green_pos += green_dir * TANK_SPEED


    for i in green_bullets:
        i[0] += i[1] * BULLET_SPEED
        pixel_pos = (int(i[0].x), int(i[0].y))
        bullet_rect = pg.draw.circle(screen, BLACK, pixel_pos, BULLET_RAD, BULLET_RAD)

    if green_bullets[0][0].y <= BULLET_RAD or green_bullets[0][0].y >= WINDOW_HEIGHT - BULLET_RAD:
        green_bullets[0][1] = green_bullets[0][1].reflect(X_VEC)

    if green_bullets[0][0].x <= BULLET_RAD or green_bullets[0][0].x >= WINDOW_WIDTH - BULLET_RAD:
        green_bullets[0][1] = green_bullets[0][1].reflect(Y_VEC)

    if check_collision_x(green_bullets[0][0], ver_walls):
        green_bullets[0][1] = green_bullets[0][1].reflect(Y_VEC)

    if check_collision_y(green_bullets[0][0], hor_walls):
        green_bullets[0][1] = green_bullets[0][1].reflect(X_VEC)

    pg.display.flip()

    clock.tick(60)
