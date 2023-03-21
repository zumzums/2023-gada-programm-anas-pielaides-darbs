import pygame
import random
from pygame.locals import *
import sqlite3

pygame.init()

#spēļu konstantes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WIDTH = 400
HEIGHT = 500
x_player_position = 170
y_player_position = 400
platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [190, 260, 70, 10], [85, 170, 70, 10], [200, 50, 70, 10]]
jump = False
# [85, 370, 70, 10][265, 320, 70, 10][265, 130, 70, 10] [200, 50, 70, 10]
y_change = 0
x_change = 0
player_speed = 4
score = 0
high_score = 0
game_over = False

# speles bildes
player = pygame.transform.scale(pygame.image.load("doodleman.png"), (40, 70))


fps = 60
font = pygame.font.Font("freesansbold.ttf", 16)
gameOver_font = pygame.font.Font("freesansbold.ttf", 36)
timer = pygame.time.Clock()

# izveidoju ekranu
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Dawdle jumpo')

# collision
def check_collision(rect_list, j):
    global x_player_position
    global y_player_position
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([x_player_position + 10, y_player_position + 60, 20, 9]) and jump == False and y_change > 0:
            j = True
    return j


# updatoju speletaja y poziciju (leciens)
def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = 0.4
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos

# updeito platformu poziciju un kustibu uz augsu
def update_platforms (platform_list, y_pos, ychange):
    global score
    if y_pos < 300 and y_change < 0:
        for i in range (len(platform_list)):
            platform_list[i][1] -= ychange
    else:
        pass
    for item in range(len(platform_list)):
        if platform_list[item][1] > 500:
            platform_list[item] = [random.randint(10, 320), random.randint(-50, -10), 70, 10]
            score += 1
    return platform_list

# speles loop
running = True 
while running == True:
    timer.tick(fps)
    screen.fill(WHITE)
    screen.blit(player, (x_player_position, y_player_position))
    blocks = []
    # uzzime score
    score_text = font.render('Score: ' + str(score), True, BLACK)
    screen.blit(score_text, (320, 20))
    # uzime high score
    high_score_text = font.render('High score: ' + str(high_score), True, BLACK)
    screen.blit(high_score_text, (282, 40))

    if score < 5:
        instruction_text = gameOver_font.render('Move with "a" and "d"', True, GREY)
        screen.blit(instruction_text, (10, 100))

    if y_player_position < 300 and y_change < 0:
        for i in range (len(blocks)):
            blocks[i][1] -= y_change

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # uzzime platformas    
    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, BLACK, platforms[i], 0, 2)
        blocks.append(block)

# speletaja kustiba pa labi un pa  kreisi un restart
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and game_over:
        game_over = False
        score = 0
        x_player_position = 170
        y_player_position = 400
        platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [190, 260, 70, 10], [85, 170, 70, 10], [200, 50, 70, 10]]

    if keys[pygame.K_d]:
        x_change = player_speed
    if keys[pygame.K_a]:
        x_change = -player_speed
    

# parbauda game over
    if y_player_position < 440:
 # updato speletaju
        y_player_position = update_player(y_player_position)
    else:
        game_over = True
        y_change = 0
        x_change = 0
        GameOver_text = gameOver_font.render('GAME OVER', True, GREY, WHITE)
        screen.blit(GameOver_text, (94, 160))
        GameOver_text = font.render('to play again press "space"', True, GREY, WHITE)
        screen.blit(GameOver_text, (100, 200))

    # parbauda collision
    jump = check_collision(blocks, jump)
    # updeito platformas
    platforms = update_platforms(platforms, y_player_position, y_change)

    # ja game over, saglabā high score un izdara update datubāzē
    if game_over:
        if score > high_score:
            high_score = score
# lai nevar no laukuma iziet
    if x_player_position < 0:
        x_player_position = 0
    elif x_player_position > 356:
        x_player_position = 356
    if y_player_position < 0:
        y_player_position = 0

    x_player_position += x_change

    # speletaja virziens 
    if x_change > 0:
        player =pygame.transform.scale(pygame.image.load("doodleman.png"), (40, 70))
    elif x_change < 0:
        player = pygame.transform.flip(pygame.transform.scale(pygame.image.load("doodleman.png"), (40, 70)), 1, 0)

    # highscore
    if score > high_score:
        high_score = score
    pygame.display.flip()

pygame.quit()


