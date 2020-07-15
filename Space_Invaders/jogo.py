
# Jogo criado com base em um tutorial em video
# https://www.youtube.com/watch?v=FfWpgLFMI7w

import pygame
import math
from pygame import mixer

# inicia o pygame
pygame.init()

# cria a janela
tela = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background01.jpg")

# titulo e icone
pygame.display.set_caption("Space Invaders")
icone = pygame.image.load("space-invaders-icon.png")
pygame.display.set_icon(icone)

# player
playerimg = pygame.image.load("spaceship.png")
playerX = 368
playerY = 500
playerX_change = 0


def player(X, Y):
    tela.blit(playerimg, (X, Y))


# bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 500
bulletY_change = -5
bullet_state = "not fired"


def bullet_fire(X, Y):
    global bullet_state
    bullet_state = "fired"
    tela.blit(bulletimg, (X + 17, Y + 16))


# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enenmy = 13
for index in range(num_of_enenmy):
    enemyimg.append(pygame.image.load("alien.png"))
    enemyY.append(10)
    enemyX.append(20 * index * 6)
    enemyX_change.append(1)
    if enemyX[index] > 736:
        enemyX[index] = 640 - (120 * (index - 7))
        enemyY[index] = 10 + (60 * math.floor(index / 7))
        enemyX_change[index] = -1
    enemyY_change.append(60)
    # print("enemy number: " + str(index))
    # print("X: " + str(enemyX[index]))
    # print("Y: " + str(enemyY[index]))


def enemy(X, Y, index):
    tela.blit(enemyimg[index], (X, Y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False


score_value = 0
font_score = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 0
scoreY = 0


def show_score(X, Y):
    score = font_score.render("Score: " + str(score_value), True, (255, 255, 255))
    tela.blit(score, (X, Y))


font_over = pygame.font.Font("freesansbold.ttf", 80)


def game_over():
    over_text = font_over.render("GAME OVER", True, (255, 255, 255))
    tela.blit(over_text, (170, 250))


font_menu = pygame.font.Font("freesansbold.ttf", 50)
font_commands = pygame.font.Font("freesansbold.ttf", 30)


def menu_screen():
    menu_text1 = font_menu.render("Tottaly Not", True, (255, 255, 255))
    menu_text2 = font_menu.render("SPACE INVADERS", True, (255, 255, 255))
    commands_text1 = font_commands.render("Espaço: Atira", True, (255, 255, 255))
    commands_text2 = font_commands.render("Setas: Movimenta", True, (255, 255, 255))
    commands_text3 = font_commands.render("Para inciar aperte ESPAÇO", True, (255, 255, 255))

    tela.blit(menu_text1, (250, 100))
    tela.blit(menu_text2, (180, 150))
    tela.blit(commands_text1, (290, 400))
    tela.blit(commands_text2, (260, 450))
    tela.blit(commands_text3, (200, 500))


mixer.music.load("Space Funeral.mp3")
mixer.music.play(-1)

running = True
end = False
menu = True
while menu:
    tela.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu = False

    menu_screen()
    pygame.display.update()

while running:

    # cor da tela RGB
    tela.fill((0, 0, 0))

    tela.blit(background, (0, 0))

    # fechar a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            end = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            elif event.key == pygame.K_RIGHT:
                playerX_change = 3
            elif event.key == pygame.K_SPACE:
                if bullet_state == "not fired":
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX = playerX + playerX_change
    if playerX <= 0:
        playerX = 0
        playerX_change = 0
    elif playerX >= 736:
        playerX = 736
        playerX_change = 0

    if bulletY <= -32:
        bulletY = 500
        bulletX = 900
        bullet_state = "not fired"
    elif bullet_state == "fired":
        bullet_fire(bulletX, bulletY)
        bulletY += bulletY_change

    for index in range(num_of_enenmy):
        if iscollision(enemyX[index], enemyY[index], playerX, playerY):
            for index in range(num_of_enenmy):
                enemyY[index] = 700
                enemyX[index] = 1200
            game_over()
            running = False
            end = True
        elif enemyX_change[index] > 0:
            enemyX_change[index] = 1 + (score_value * 0.25)
        elif enemyX_change[index] < 0:
            enemyX_change[index] = -1 - (score_value * 0.25)
        enemyX[index] = enemyX[index] + enemyX_change[index]
        if enemyX[index] <= 0:
            enemyX_change[index] = 1 + (score_value * 0.25)
            enemyY[index] = enemyY[index] + enemyY_change[index]
        elif enemyX[index] > 736:
            enemyX_change[index] = -1 - (score_value * 0.25)
            enemyY[index] = enemyY[index] + enemyY_change[index]

        collision = iscollision(enemyX[index], enemyY[index], bulletX, bulletY)
        if collision:
            kill_sound = mixer.Sound("destroyed.wav")
            kill_sound.play()
            bulletY = 500
            bulletX = 900
            bullet_state = "not fired"
            score_value += 1
            enemyY[index] -= 690

        enemy(enemyX[index], enemyY[index], index)

    player(playerX, playerY)
    show_score(scoreX, scoreY)
    pygame.display.update()

while end:
    game_over()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False
