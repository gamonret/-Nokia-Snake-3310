
import pygame
import random
import sys
import math

pygame.init()

# NOKIA 3310 - SNAKE 2.4

WIDTH, HEIGHT = 520, 820
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NOKIA 3310 - SNAKE 2.4")
clock = pygame.time.Clock()

# COLORS
BG = (31, 39, 35)
BODY = (194, 199, 181)
BODY_LIGHT = (224, 226, 211)
BODY_DARK = (115, 124, 108)
EDGE = (79, 88, 76)

LCD = (163, 181, 126)
LCD_LIGHT = (190, 205, 151)

PIXEL = (42, 57, 34)
PIXEL_SOFT = (75, 91, 54)
WHITE = (240, 242, 225)

# FONTS
font_tiny = pygame.font.SysFont("consolas", 12, bold=True)
font_small = pygame.font.SysFont("consolas", 15, bold=True)
font_big = pygame.font.SysFont("consolas", 31, bold=True)
font_logo = pygame.font.SysFont("arial", 39, bold=True)

# PHONE
PHONE = pygame.Rect(55, 18, 410, 784)
LCD_FRAME = pygame.Rect(91, 155, 338, 302)
LCD_INNER = pygame.Rect(104, 168, 312, 276)

# GAME GRID
GRID_W = 20
GRID_H = 14
CELL = 15

GRID_X = 110
GRID_Y = 205

GRID_RECT = pygame.Rect(
    GRID_X, GRID_Y,
    GRID_W * CELL,
    GRID_H * CELL
)

# BUTTONS
MENU_RECT = pygame.Rect(119, 501, 80, 36)
OK_RECT = pygame.Rect(220, 501, 80, 36)
BACK_RECT = pygame.Rect(321, 501, 80, 36)

KEY_RECTS = {}

# GAME STATE
state = "boot"

boot_started = pygame.time.get_ticks()
boot_duration = 2400

snake = []
direction = (1, 0)
next_direction = (1, 0)

food = (10, 7)
score = 0
best = 0

move_accumulator = 0
move_interval = 155


def draw_text(surface, text, pos, fnt,
              color=PIXEL, center=False):

    image = fnt.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = pos
    else:
        rect.topleft = pos

    surface.blit(image, rect)


def rounded(surface, rect, color,
            radius=12, border=0, border_color=None):

    pygame.draw.rect(
        surface, color, rect,
        border_radius=radius
    )

    if border and border_color:
        pygame.draw.rect(
            surface, border_color, rect,
            border, border_radius=radius
        )


def draw_gradient(surface, rect, top, bottom, radius=0):

    grad = pygame.Surface(
        (rect.width, rect.height),
        pygame.SRCALPHA
    )

    for y in range(rect.height):

        t = y / max(1, rect.height - 1)

        color = tuple(
            int(top[i] * (1 - t) + bottom[i] * t)
            for i in range(3)
        )

        pygame.draw.line(
            grad, color,
            (0, y), (rect.width, y)
        )

    if radius:

        mask = pygame.Surface(
            (rect.width, rect.height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            mask.get_rect(),
            border_radius=radius
        )

        grad.blit(
            mask, (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

    surface.blit(grad, rect.topleft)


def draw_button(surface, rect, label,
                sublabel=None, pressed=False):

    dy = 3 if not pressed else 1

    pygame.draw.rect(
        surface, EDGE,
        rect.move(0, 5),
        border_radius=9
    )

    pygame.draw.rect(
        surface, BODY_LIGHT,
        rect.move(0, dy),
        border_radius=9
    )

    pygame.draw.rect(
        surface, BODY_DARK,
        rect.move(0, dy),
        2,
        border_radius=9
    )

    inner = rect.inflate(-5, -5).move(0, dy)

    draw_gradient(
        surface, inner,
        (104, 114, 103),
        (47, 56, 50),
        7
    )

    pygame.draw.line(
        surface, (148, 157, 140),
        (inner.left + 7, inner.top + 3),
        (inner.right - 7, inner.top + 3),
        1
    )

    if label:
        draw_text(
            surface, label,
            (
                rect.centerx,
                rect.centery - (5 if sublabel else 0)
            ),
            font_small, WHITE, center=True
        )

    if sublabel:
        draw_text(
            surface, sublabel,
            (rect.centerx, rect.centery + 10),
            font_tiny,
            (203, 211, 188),
            center=True
        )


# PHONE DESIGN
def draw_phone():

    screen.fill(BG)

    pygame.draw.rect(
        screen, (12, 17, 14),
        PHONE.move(8, 10),
        border_radius=54
    )

    rounded(screen, PHONE, BODY_DARK, 54)

    rounded(
        screen, PHONE.inflate(-7, -7),
        BODY, 51, 2, (235, 236, 221)
    )

    pygame.draw.arc(
        screen, (245, 246, 231),
        (65, 25, 390, 760),
        195, 5.95, 3
    )

    pygame.draw.arc(
        screen, (132, 140, 124),
        (63, 28, 394, 758),
        0.2, 2.8, 2
    )

    # SPEAKER
    rounded(
        screen,
        pygame.Rect(205, 52, 110, 14),
        (112, 121, 106), 7
    )

    for x in range(214, 309, 8):
        pygame.draw.line(
            screen, (67, 77, 67),
            (x, 56), (x, 62), 2
        )

    # NOKIA LOGO
    draw_text(
        screen, "NOKIA",
        (260, 91), font_logo,
        (49, 65, 48), center=True
    )

    # DISPLAY
    rounded(screen, LCD_FRAME, (72, 82, 70), 17)

    rounded(
        screen, LCD_FRAME.inflate(-5, -5),
        (43, 54, 43), 14
    )

    rounded(
        screen, LCD_INNER,
        LCD, 8, 2, (202, 215, 163)
    )

    pygame.draw.line(
        screen, (213, 225, 173),
        (112, 174), (405, 174), 2
    )

    draw_text(screen, "NOKIA", (112, 179), font_tiny)
    draw_text(screen, "100%", (368, 179), font_tiny)

    # BUTTON LABELS
    draw_text(
        screen, "MENU", (165, 485),
        font_tiny, (78, 88, 75), center=True
    )

    draw_text(
        screen, "SELECT", (260, 485),
        font_tiny, (78, 88, 75), center=True
    )

    draw_text(
        screen, "BACK", (355, 485),
        font_tiny, (78, 88, 75), center=True
    )

    draw_button(screen, MENU_RECT, "MENU")
    draw_button(screen, OK_RECT, "OK")
    draw_button(screen, BACK_RECT, "BACK")

    # KEYPAD
    labels = [
        ("1", ""), ("UP", "ARROW"), ("3", "DEF"),
        ("LEFT", "ARROW"), ("5", "SELECT"), ("RIGHT", "ARROW"),
        ("7", "PQRS"), ("DOWN", "ARROW"), ("9", "WXYZ"),
        ("*", ""), ("0", "+"), ("#", "")
    ]

    start_x = 128
    start_y = 562

    key_w = 76
    key_h = 42

    gap_x = 17
    gap_y = 10

    KEY_RECTS.clear()

    direction_keys = {
        "UP": "up",
        "LEFT": "left",
        "RIGHT": "right",
        "DOWN": "down"
    }

    for i, (number, letters) in enumerate(labels):

        row, col = divmod(i, 3)

        rect = pygame.Rect(
            start_x + col * (key_w + gap_x),
            start_y + row * (key_h + gap_y),
            key_w, key_h
        )

        draw_button(screen, rect, number, letters)

        if number in direction_keys:
            KEY_RECTS[direction_keys[number]] = rect.copy()

    draw_text(
        screen, "3310",
        (260, 785), font_tiny,
        (101, 111, 96), center=True
    )


# SNAKE
def draw_pixel_snake():

    for i, (x, y) in enumerate(snake):

        rect = pygame.Rect(
            GRID_X + x * CELL + 1,
            GRID_Y + y * CELL + 1,
            CELL - 2, CELL - 2
        )

        color = PIXEL if i else (30, 45, 26)

        pygame.draw.rect(screen, color, rect)

        if i == 0:

            hx, hy = rect.center

            if direction == (1, 0):
                eyes = [(hx + 3, hy - 3), (hx + 3, hy + 3)]

            elif direction == (-1, 0):
                eyes = [(hx - 3, hy - 3), (hx - 3, hy + 3)]

            elif direction == (0, -1):
                eyes = [(hx - 3, hy - 3), (hx + 3, hy - 3)]

            else:
                eyes = [(hx - 3, hy + 3), (hx + 3, hy + 3)]

            for eye in eyes:
                pygame.draw.rect(
                    screen, LCD_LIGHT,
                    (*eye, 2, 2)
                )


def draw_food(ticks):

    if (ticks // 260) % 2 == 0:

        x, y = food

        rect = pygame.Rect(
            GRID_X + x * CELL + 3,
            GRID_Y + y * CELL + 3,
            9, 9
        )

        pygame.draw.rect(screen, PIXEL, rect)
        pygame.draw.rect(screen, PIXEL_SOFT, rect, 1)


# FOOD
def place_food():

    global food

    empty = [
        (x, y)
        for x in range(GRID_W)
        for y in range(GRID_H)
        if (x, y) not in snake
    ]

    if empty:
        food = random.choice(empty)


# START NEW GAME
def start_game():

    global snake, direction, next_direction
    global score, move_accumulator
    global move_interval, state

    snake = [
        (8, 7),
        (7, 7),
        (6, 7)
    ]

    direction = (1, 0)
    next_direction = (1, 0)

    score = 0
    move_accumulator = 0
    move_interval = 155

    place_food()

    state = "playing"


# PAUSE
def toggle_pause():

    global state

    if state == "playing":
        state = "paused"

    elif state == "paused":
        state = "playing"


# BACK TO MENU
def return_to_menu():

    global state

    state = "menu"


# GAME UPDATE
def update_game():

    global snake, direction
    global score, best, state, move_interval

    direction = next_direction

    hx, hy = snake[0]

    new_head = (
        hx + direction[0],
        hy + direction[1]
    )

    # WALL COLLISION
    if (
        new_head[0] < 0 or
        new_head[0] >= GRID_W or
        new_head[1] < 0 or
        new_head[1] >= GRID_H
    ):
        state = "gameover"
        return

    # SELF COLLISION
    if new_head in snake[:-1]:
        state = "gameover"
        return

    snake.insert(0, new_head)

    if new_head == food:

        score += 10
        best = max(best, score)

        move_interval = max(
            65,
            155 - (score // 50) * 10
        )

        place_food()

    else:
        snake.pop()


# DIRECTION CONTROL
def handle_direction(key):

    global next_direction

    mapping = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),

        pygame.K_w: (0, -1),
        pygame.K_s: (0, 1),
        pygame.K_a: (-1, 0),
        pygame.K_d: (1, 0),

        pygame.K_2: (0, -1),
        pygame.K_8: (0, 1),
        pygame.K_4: (-1, 0),
        pygame.K_6: (1, 0),

        pygame.K_KP2: (0, -1),
        pygame.K_KP8: (0, 1),
        pygame.K_KP4: (-1, 0),
        pygame.K_KP6: (1, 0)
    }

    if key in mapping:

        candidate = mapping[key]

        if candidate != (
            -direction[0],
            -direction[1]
        ):
            next_direction = candidate


# MOUSE BUTTONS
def handle_mouse(pos):

    if MENU_RECT.collidepoint(pos):

        if state in ("playing", "paused"):
            toggle_pause()

    elif BACK_RECT.collidepoint(pos):

        if state in ("playing", "paused", "gameover"):
            return_to_menu()

    elif OK_RECT.collidepoint(pos):

        # OK starts the game from the menu
        if state == "menu":
            start_game()

        # NEW: OK restarts after GAME OVER
        elif state == "gameover":
            start_game()

        # OK also resumes a paused game
        elif state == "paused":
            toggle_pause()

    elif state == "playing":

        for name, rect in KEY_RECTS.items():

            if rect.collidepoint(pos):

                key_map = {
                    "up": pygame.K_UP,
                    "down": pygame.K_DOWN,
                    "left": pygame.K_LEFT,
                    "right": pygame.K_RIGHT
                }

                handle_direction(key_map[name])
                break


# GAME SCREEN
def draw_game_screen(ticks):

    draw_text(
        screen, f"SCORE {score:03d}",
        (114, 190), font_tiny
    )

    draw_text(
        screen, f"HI {best:03d}",
        (350, 190), font_tiny
    )

    pygame.draw.rect(
        screen, (117, 137, 83),
        GRID_RECT, 1
    )

    for x in range(GRID_W + 1):

        px = GRID_X + x * CELL

        pygame.draw.line(
            screen, (151, 170, 113),
            (px, GRID_Y),
            (px, GRID_Y + GRID_H * CELL),
            1
        )

    for y in range(GRID_H + 1):

        py = GRID_Y + y * CELL

        pygame.draw.line(
            screen, (151, 170, 113),
            (GRID_X, py),
            (GRID_X + GRID_W * CELL, py),
            1
        )

    if state in ("playing", "paused", "gameover"):

        draw_food(ticks)
        draw_pixel_snake()

    if state == "menu":

        draw_text(
            screen, "SNAKE II",
            (260, 263), font_big, center=True
        )

        draw_text(
            screen, "CLASSIC 3310 EDITION",
            (260, 296), font_tiny, center=True
        )

        for i in range(8):

            x = 7 + i

            y = 9 + int(
                math.sin(ticks / 250 + i * 0.45) * 1.5
            )

            pygame.draw.rect(
                screen, PIXEL,
                (
                    GRID_X + x * CELL + 2,
                    GRID_Y + y * CELL + 2,
                    11, 11
                )
            )

        pygame.draw.rect(
            screen, PIXEL,
            (
                GRID_X + 16 * CELL + 3,
                GRID_Y + 9 * CELL + 3,
                9, 9
            )
        )

        draw_text(
            screen, "ENTER / OK TO PLAY",
            (260, 395), font_small, center=True
        )

    elif state == "paused":

        draw_text(
            screen, "PAUSED",
            (260, 300), font_big, center=True
        )

        draw_text(
            screen, "MENU / P TO RESUME",
            (260, 340), font_tiny, center=True
        )

        draw_text(
            screen, "BACK TO MAIN MENU",
            (260, 365), font_tiny, center=True
        )

    elif state == "gameover":

        draw_text(
            screen, "GAME OVER",
            (260, 290), font_big, center=True
        )

        draw_text(
            screen, f"YOUR SCORE: {score}",
            (260, 326), font_small, center=True
        )

        draw_text(
            screen, "OK = PLAY AGAIN",
            (260, 365), font_tiny, center=True
        )

    draw_text(
        screen, "CLICK ARROWS / KEYS 2 4 6 8",
        (260, 430), font_tiny,
        (71, 86, 55), center=True
    )


# MAIN LOOP
running = True

while running:

    dt = clock.tick(FPS)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            handle_mouse(event.pos)

        elif event.type == pygame.KEYDOWN:

            if state == "boot":
                state = "menu"

            elif state == "menu":

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):
                    start_game()

            elif state == "playing":

                if event.key in (
                    pygame.K_p,
                    pygame.K_ESCAPE
                ):
                    toggle_pause()

                else:
                    handle_direction(event.key)

            elif state == "paused":

                if event.key in (
                    pygame.K_p,
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):
                    toggle_pause()

                elif event.key == pygame.K_ESCAPE:
                    return_to_menu()

            elif state == "gameover":

                # Keyboard restart
                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):
                    start_game()

                elif event.key == pygame.K_ESCAPE:
                    return_to_menu()

    # BOOT SCREEN
    if (
        state == "boot"
        and ticks - boot_started >= boot_duration
    ):
        state = "menu"

    # SNAKE MOVEMENT
    if state == "playing":

        move_accumulator += dt

        if move_accumulator >= move_interval:

            update_game()
            move_accumulator = 0

    # DRAW
    draw_phone()

    if state == "boot":

        elapsed = ticks - boot_started

        pulse = (
            0.82 +
            0.18 * math.sin(elapsed / 150)
        )

        logo_color = (
            int(PIXEL[0] * pulse),
            int(PIXEL[1] * pulse),
            int(PIXEL[2] * pulse)
        )

        draw_text(
            screen, "NOKIA",
            (260, 274), font_big,
            logo_color, center=True
        )

        draw_text(
            screen, "Connecting people",
            (260, 310), font_tiny,
            PIXEL, center=True
        )

        for i in range(10):

            rect = pygame.Rect(
                185 + i * 18,
                350, 12, 8
            )

            if elapsed > i * 170:
                pygame.draw.rect(screen, PIXEL, rect)
            else:
                pygame.draw.rect(
                    screen, PIXEL_SOFT, rect, 1
                )

    else:

        draw_game_screen(ticks)

    pygame.display.flip()


pygame.quit()
sys.exit()
