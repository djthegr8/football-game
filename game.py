import sys
from csv import reader, writer
from time import sleep
import pygame
from pygame.locals import *

pygame.init()
FNAME = 'score.csv'
player1_score = 0
player2_score = 0

# Naming the game.
pygame.display.set_caption("Football Game")

width = 1200
height = 700

ground = pygame.display.set_mode((width, height))

# Font sizes.
font_s = pygame.font.SysFont("Arial", 25)
font_m = pygame.font.SysFont("Arial", 50)
font_l = pygame.font.SysFont("Arial", 80)

# Colours
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (56, 123, 255)

# Round won messages.
p1_scores = font_m.render("Player 1 scores !", True, red)
p2_scores = font_m.render("Player 2 scores !", True, red)

# Importing images for players, football, field
c1 = pygame.image.load("righty.png")
c2 = pygame.image.load("lefty.png")
ball = pygame.image.load("football.png")
background = pygame.image.load("football field.jpg").convert()
goal1 = pygame.image.load("post.jpg").convert()
goal2 = pygame.image.load("post2.jpg").convert()
ground.blit(background, [0, 0])
ft1 = font_m.render('Play', True, red)
ft2 = font_m.render('View history', True, red)
ground.blit(ft1, [100, 50])
ground.blit(ft2, [250, 50])
k, sh = False, False
while True:
    for action in pygame.event.get():
        if action.type == pygame.MOUSEBUTTONDOWN:
            # print(mouse)
            if 150 > mouse[0] > 50 and 110 > mouse[1] > 54:
                k = True
            if 520 > mouse[0] > 250 and 110 > mouse[1] > 54:
                sh = True
    if k:
        break
    if sh:
        with open(FNAME, 'r') as f1:
            csv_r = list(reader(f1))
            str_tbp = ""
            off = 40
            for i in range(len(csv_r)):
                print('dog')
                fsr = font_s.render(f"Player {csv_r[i][0]} won", True, red)
                ground.blit(fsr, [300, 200 + (i * off)])
        sh = False
    mouse = pygame.mouse.get_pos()
    pygame.display.update()

ground.blit(ball, [0, 0])
ground.blit(c1, [0, 0])
ground.blit(c2, [0, 0])
ground.blit(goal1, [0, 0])
ground.blit(goal2, [0, 0])

pygame.display.flip()

ball_area = ball.get_rect()
c1_area = c1.get_rect()
c2_area = c2.get_rect()
g1_area = goal1.get_rect()
g2_area = goal2.get_rect()
br = background.get_rect()
# Defining the starting point of the ball
ball_area.left = 600
ball_area.top = 350
IFST = False
# Starting point of player 1
c1_area.left = 160
c1_area.top = 280

# Starting point of player 2
c2_area.left = 1033
c2_area.top = 280

# Location of post 1
g1_area.left = 35
g1_area.top = 257

# Location of post 2
g2_area.left = 1100
g2_area.top = 257

speed = [1, 1]


def move_p1():
    keystroke = pygame.key.get_pressed()

    if keystroke[K_a]:
        c1_area.move_ip((-1, 0))
    if keystroke[K_d]:
        c1_area.move_ip((1, 0))
    if keystroke[K_s]:
        c1_area.move_ip((0, 1))
    if keystroke[K_w]:
        c1_area.move_ip((0, -1))


def player_2_move():
    keystroke = pygame.key.get_pressed()

    if keystroke[K_LEFT]:
        c2_area.move_ip((-1, 0))
    if keystroke[K_RIGHT]:
        c2_area.move_ip((1, 0))
    if keystroke[K_DOWN]:
        c2_area.move_ip((0, 1))
    if keystroke[K_UP]:
        c2_area.move_ip((0, -1))


def ball_exit():
    if ball_area.left < 0 or ball_area.right > width:
        speed[0] = -speed[0]
    if ball_area.top < 0 or ball_area.bottom > height:
        speed[1] = -speed[1]


def ball_collision():
    global IFST
    # player 1 and ball collision
    if c1_area.colliderect(ball_area) and not IFST:
        if c1_area.colliderect(ball_area.move(-speed[0], 0)):
            speed[1] = -speed[1]

        if c1_area.colliderect(ball_area.move(0, speed[1])):
            speed[0] = -speed[0]
        IFST = True
        sleep(0.00025)
        IFST = False
    # player 2 and ball collision
    if c2_area.colliderect(ball_area) and not IFST:
        if c2_area.colliderect(ball_area.move(-speed[0], 0)):
            speed[1] = -speed[1]
        if c2_area.colliderect(ball_area.move(0, speed[1])):
            speed[0] = -speed[0]
        IFST = True
        sleep(0.00025)
        IFST = False


def goal():
    # Scoring a goal for player 2
    if g1_area.colliderect(ball_area):
        if g1_area.colliderect(ball_area.move(-speed[0], 0)):
            speed[1] = -speed[1]

    if g1_area.colliderect(ball_area):
        if g1_area.colliderect(ball_area.move(0, speed[1])):
            speed[0] = -speed[0]

    # Scoring a goal for player 1
    if g2_area.colliderect(ball_area):
        if g2_area.colliderect(ball_area.move(-speed[0], 0)):
            speed[1] = -speed[1]
    if g2_area.colliderect(ball_area):
        if g2_area.colliderect(ball_area.move(0, speed[1])):
            speed[0] = -speed[0]


def player_exit():
    # Player 1 screen exit prevention.
    c1_area.clamp_ip(br)
    c2_area.clamp_ip(br)
    # Player 2 screen exit prevention.
    if c2_area.left > width:
        c2_area.right = 0

    if c2_area.right < 0:
        c2_area.left = width

    if c2_area.top > height:
        c2_area.bottom = 0

    if c2_area.bottom < 0:
        c2_area.top = height


def playgame():
    global player1_score
    global player2_score

    while True:

        # Score counting for player 1
        if g2_area.colliderect(ball_area):
            player1_score += 1
            ground.blit(p1_scores, [450, 190])
            ball_area.left = 500
            ball_area.top = 280
            c1_area.left = 160
            c1_area.top = 280
            c2_area.left = 1033
            c2_area.top = 280
            pygame.display.update()
            pygame.time.wait(2000)

        # Score counting for player 2
        if g1_area.colliderect(ball_area):
            player2_score += 1
            ground.blit(p2_scores, [450, 190])
            ball_area.left = 500
            ball_area.top = 280
            c1_area.left = 160
            c1_area.top = 280
            c2_area.left = 1033
            c2_area.top = 280
            pygame.display.update()
            pygame.time.wait(2000)

        # Creating scoreboard
        board1 = font_s.render("Player 1 : " + str(player1_score), True, black, blue)
        board2 = font_s.render("Player 2 : " + str(player2_score), True, black, blue)

        ball_area.move_ip(speed)

        ball_exit()
        goal()
        ball_collision()
        move_p1()
        player_2_move()
        player_exit()

        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if action.type == KEYDOWN:
                if action.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        if player1_score >= 3:
            with open(FNAME, 'a', newline='') as f2:
                csv_w = writer(f2)
                csv_w.writerow([1, ])
            pygame.quit()
            sys.exit()

        if (player2_score >= 3):
            with open(FNAME, 'a', newline='') as f2:
                csv_w = writer(f2)
                csv_w.writerow([2, ])
            pygame.quit()
            sys.exit()

        # Updating background
        ground.blit(background, [0, 0])
        ground.blit(goal1, g1_area)
        ground.blit(goal2, g2_area)
        ground.blit(c1, c1_area)
        ground.blit(c2, c2_area)
        ground.blit(board1, [50, 0])
        ground.blit(board2, [1000, 0])
        ground.blit(ball, ball_area)

        pygame.display.update()
        pygame.display.flip()


playgame()
