import pygame
import sys
import math

pygame.init()

# ---------------- SCREEN SETUP ----------------
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Automatic Coconut Harvest Animation")

# ---------------- COLORS ----------------
SKY = (135, 206, 235)
SUN = (255, 255, 0)
MOUNTAIN1 = (107, 142, 35)
MOUNTAIN2 = (85, 107, 47)
FIELD = (124, 252, 0)
TREE_TRUNK = (160, 82, 45)
LEAF = (0, 128, 0)
MAN = (0, 0, 0)
COCONUT = (139, 69, 19)
GRASS = (0, 100, 0)
CROW = (30,30,30)

clock = pygame.time.Clock()

# ---------------- MAN VARIABLES ----------------
man_x, man_y = 100, 450
man_holding = False

# ---------------- COCONUT POSITIONS ----------------
coconuts = [(655,200),(670,210),(645,215),(660,190),(680,225)]
plucked_index = None
coconut_on_ground = False

# ---------------- SPEED VARIABLES ----------------
WALK_SPEED = 2
CLIMB_SPEED = 2
COCONUT_FALL_SPEED = 2

# ---------------- SUN BLINK VARIABLES ----------------
sun_radius = 50
sun_growing = True

# ---------------- CROW MOVEMENT VARIABLES ----------------
crow1_x = 50
crow2_x = 250
crow3_x = 450
crow_speed = 2

# ---------------- FRAME BASED ANIMATION CONTROL ----------------
# Algorithm: Frame based animation using stage logic
stage = 0


# ---------------- SUN DRAWING ----------------
def draw_sun():
    global sun_radius, sun_growing

    # Algorithm: Midpoint Circle (concept) → drawing circle
    pygame.draw.circle(screen, SUN, (120,90), sun_radius)

    # Algorithm: Bresenham Line concept → sun rays
    for angle in range(0,360,30):
        x1 = 120 + int(math.cos(math.radians(angle))*(sun_radius+5))
        y1 = 90 + int(math.sin(math.radians(angle))*(sun_radius+5))
        x2 = 120 + int(math.cos(math.radians(angle))*(sun_radius+18))
        y2 = 90 + int(math.sin(math.radians(angle))*(sun_radius+18))

        pygame.draw.line(screen,SUN,(x1,y1),(x2,y2),2)

    # blinking animation
    if sun_growing:
        sun_radius += 1
        if sun_radius >= 55:
            sun_growing = False
    else:
        sun_radius -= 1
        if sun_radius <= 45:
            sun_growing = True


# ---------------- DRAW CROW ----------------
def draw_crow(x,y):

    # Algorithm: Bresenham Line concept
    pygame.draw.arc(screen,CROW,(x,y,20,10),math.pi,2*math.pi,2)
    pygame.draw.arc(screen,CROW,(x+15,y,20,10),math.pi,2*math.pi,2)


# ---------------- MOVE CROWS ----------------
def update_crows():
    global crow1_x,crow2_x,crow3_x

    # Algorithm: 2D Translation Transformation
    crow1_x += crow_speed
    crow2_x += crow_speed
    crow3_x += crow_speed

    if crow1_x > WIDTH:
        crow1_x = -40
    if crow2_x > WIDTH:
        crow2_x = -40
    if crow3_x > WIDTH:
        crow3_x = -40


# ---------------- BACKGROUND ----------------
def draw_background():

    screen.fill(SKY)

    draw_sun()

    # Algorithm: Polygon Filling → mountains
    pygame.draw.polygon(screen,MOUNTAIN1,[(0,300),(150,180),(300,300)])
    pygame.draw.polygon(screen,MOUNTAIN2,[(200,300),(400,150),(600,300)])
    pygame.draw.polygon(screen,MOUNTAIN1,[(500,300),(700,180),(900,300)])

    # Algorithm: Scan Line Fill → paddy field
    pygame.draw.rect(screen,FIELD,(0,420,WIDTH,HEIGHT-420))

    # Algorithm: Bresenham Line concept → grass
    for i in range(0,WIDTH,6):
        pygame.draw.line(screen,GRASS,(i,420),(i+3,395),2)
        pygame.draw.line(screen,GRASS,(i+3,395),(i+6,420),2)

    draw_crow(crow1_x,80)
    draw_crow(crow2_x,120)
    draw_crow(crow3_x,60)


# ---------------- TREE ----------------
def draw_tree():

    # Algorithm: Bresenham Line Drawing concept
    pygame.draw.line(screen,TREE_TRUNK,(640,520),(645,450),8)
    pygame.draw.line(screen,TREE_TRUNK,(645,450),(650,370),8)
    pygame.draw.line(screen,TREE_TRUNK,(650,370),(655,300),8)
    pygame.draw.line(screen,TREE_TRUNK,(655,300),(660,230),8)
    pygame.draw.line(screen,TREE_TRUNK,(660,230),(665,170),6)

    pygame.draw.line(screen,LEAF,(665,170),(600,130),6)
    pygame.draw.line(screen,LEAF,(665,170),(720,130),6)
    pygame.draw.line(screen,LEAF,(665,170),(580,180),6)
    pygame.draw.line(screen,LEAF,(665,170),(740,180),6)


# ---------------- MAN ----------------
def draw_man():

    # Algorithm: Midpoint Circle concept → head
    pygame.draw.circle(screen,MAN,(man_x,man_y),6)

    # Algorithm: Bresenham Line concept → body parts
    pygame.draw.line(screen,MAN,(man_x,man_y+6),(man_x,man_y+28),3)
    pygame.draw.line(screen,MAN,(man_x,man_y+12),(man_x-10,man_y+18),3)
    pygame.draw.line(screen,MAN,(man_x,man_y+12),(man_x+10,man_y+18),3)
    pygame.draw.line(screen,MAN,(man_x,man_y+28),(man_x-10,man_y+42),3)
    pygame.draw.line(screen,MAN,(man_x,man_y+28),(man_x+10,man_y+42),3)

    if man_holding:
        pygame.draw.circle(screen,COCONUT,(man_x+12,man_y+18),8)


# ---------------- COCONUTS ----------------
def draw_coconuts():

    for idx,(x,y) in enumerate(coconuts):

        # Midpoint Circle concept
        if idx != plucked_index:
            pygame.draw.circle(screen,COCONUT,(x,y),8)

        elif not man_holding:
            pygame.draw.circle(screen,COCONUT,(x,y),8)


# ---------------- MAIN LOOP ----------------
running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_crows()

    # ----------- AUTOMATIC ANIMATION -----------
    # Algorithm: 2D Translation + Frame Animation

    if stage == 0:      # walk to tree
        if man_x < 640:
            man_x += WALK_SPEED
        else:
            stage = 1

    elif stage == 1:    # climb tree
        if man_y > 170:
            man_y -= CLIMB_SPEED
        else:
            stage = 2

    elif stage == 2:    # pluck coconut
        if plucked_index is None:
            plucked_index = 0
        stage = 3

    elif stage == 3:    # coconut falls
        if plucked_index is not None:
            x,y = coconuts[plucked_index]
            if y < 520:
                coconuts[plucked_index] = (x,y + COCONUT_FALL_SPEED)
            else:
                coconut_on_ground = True
                stage = 4

    elif stage == 4:    # climb down
        if man_y < 450:
            man_y += CLIMB_SPEED
        else:
            stage = 5

    elif stage == 5:    # pick coconut
        if coconut_on_ground:
            man_holding = True
        stage = 6

    elif stage == 6:    # walk away
        man_x += WALK_SPEED

    draw_background()
    draw_tree()
    draw_coconuts()
    draw_man()

    pygame.display.update()

pygame.quit()
sys.exit()