# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 13:55:40 2023

@author: boleymax000
"""

import pygame
import pygame_widgets
from pygame_widgets.progressbar import ProgressBar

import random
import gameObject
import startupScreen
# constants
ENEMYDELTA = 22 # Time between new enemy spawns


#pygame.mixer.init()
pygame.mixer.init()
screen_width=1920
screen_height=1080 
x = 250
y = 250
mixer = pygame.mixer
fontx = screen_width / 2
fonty = 150
playerx = x
timer2 = 0
playery = y
width = 10
height = 10
playerLeft = 0
playerRight = 0
playerUp = 0
playerDown = 0
playerSpeed = 0
currentspeed = 0
currentspeed2 = 0
playerdash = 0
enemyx = 20
enemyy = 20 
enemy_width = 15
enemy_hight = 15
enemy_vel = 15
points = 0
white = 255, 255, 255
timer = 0
#dash constats 
dash_cooldown = 0
currentenemies = 1
enemies = []
mainObject = None

#drawing and collideing logic

def progress_max():
    global mainObject
    rval = 1
    if mainObject != None:
        rval = (3 - mainObject.timer)/3
    if rval < 0:
        rval = 0
    return rval

def RectLogic(scr, mainObject, powerUP, DeltaTime, events):
    global points
    global enemies
    global point_pickup
    global playerdash
    pygame.init()
    scr.fill((0, 0, 0))
    score(scr, mainObject, DeltaTime)   
    if mainObject.timer > 0 and mainObject.isdashing == False:
        mainObject.timer -= mainObject.dashenergy
        if mainObject.timer < 0:
            mainObject.timer = 0
    playerrec = pygame.draw.rect(scr, (mainObject.rcolor, mainObject.gcolor, mainObject.bcolor), (mainObject.x, mainObject.y, mainObject.w, mainObject.h))
    for enemy in enemies:
        enemyrec = pygame.draw.rect(scr, (255, 0, 0), (enemy.x, enemy.y, enemy.w, enemy.h))
        enemycollide = pygame.Rect.colliderect(playerrec, enemyrec)
        if enemycollide:
            if playerdash == 0:
                points = points - 5
                enemy.x = random.randint(100,1820)
                enemy.y = random.randint(100,980)
                
            if playerdash == 1:
                points += 1
                enemy.x = random.randint(100,1820)
                enemy.y = random.randint(100,980)
        enemyhit = enemiesHit(enemy, enemies)
        
        if enemyhit:
            points += 2
            enemy.x = random.randint(100,1820)
            enemy.y = random.randint(100,980)
            
    powerup = pygame.draw.rect(scr, (255, 255, 0), (powerUP.x, powerUP.y, powerUP.w, powerUP.h))
    pointpowerup = pygame.draw.rect(scr, (255, 0, 255), (powerUP.px, powerUP.py, powerUP.w, powerUP.h))
    powerUPcollide = pygame.Rect.colliderect(playerrec, powerup)
    

    pygame_widgets.update(events)
    pygame.display.update()
    
    if powerUPcollide:
        powerUP.x = random.randint(100, 1820)
        powerUP.y = random.randint(100, 980)
        mainObject.vel = mainObject.vel + 2
        
    pointsup = pygame.Rect.colliderect(playerrec, pointpowerup)
    
    if pointsup:
        powerUP.px = random.randint(100, 1820)
        powerUP.py = random.randint(100, 980)
        points += 5
    

#scorechangeing        
def scoresystem(mainObject, DeltaTime):
    global timer
    global points
    global currentenemies
    timer += gameObject.DeltaTime.dt
    enemy = gameObject.enemyObject(0, 0, 10, 10, 1, 0, 0, False, 0, 0, 0)
    
    if timer >= 3:
        points += 1
        timer = 0
        
    if points < 0:
        points = 0
        mainObject.vel = 3
        
    if points > ((currentenemies + 10000000) * 10):
        currentenemies += 1
        enemies.append(enemy)
        enemy.x = random.randint(100,1820)
        enemy.y = random.randint(100,980)
    

#score UI        
def score(scr, mainObject, DeltaTime):
    global points
    font = pygame.font.Font('BULKYPIX.TTF', 32)
    text = font.render(f'{points}', True, white)
    textRect = text.get_rect()
    textRect.center = (fontx // 1, fonty // 2)
    scr.blit(text, textRect)
    scoresystem(mainObject, DeltaTime)  

#player movement        
def movement(events, mainObject, DeltaTime):

    global playerLeft
    global playerRight
    global playerUp
    global playerDown
    global playerSpeed
    global currentspeed
    global currentspeed2
    global playerdash
    rVal = True
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerLeft = 1
            if event.key == pygame.K_RIGHT:
                playerRight = 1
            if event.key == pygame.K_UP:
                playerUp = 1
            if event.key == pygame.K_DOWN:
                playerDown = 1
            if event.key == pygame.K_LSHIFT:
                playerSpeed = 1
                currentspeed = mainObject.vel
            if event.key == pygame.K_SPACE and dash_cooldown == 0:
                playerdash = 1
                mainObject.startDash()
                currentspeed2 = mainObject.vel
            if event.key == pygame.K_ESCAPE:
                rVal = False
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerLeft = 0
            if event.key == pygame.K_RIGHT:
                playerRight = 0
            if event.key == pygame.K_UP:
                playerUp = 0
            if event.key == pygame.K_DOWN:
                playerDown = 0
            if event.key == pygame.K_LSHIFT:
                playerSpeed = 0
                mainObject.vel = currentspeed
            if event.key == pygame.K_SPACE:
                playerdash = 0
                mainObject.endDash()
                mainObject.vel = mainObject.currentvel2
                
    if playerRight==1:
        mainObject.moveRight()
    if playerLeft==1:
        mainObject.moveLeft()
    if playerUp == 1:
        mainObject.moveUp()
    if playerDown == 1:
        mainObject.moveDown()
    if playerSpeed == 1:
        mainObject.slowDown()
    if playerdash == 1:
        mainObject.Dash(DeltaTime.dt)
    
            
    return rVal                

def enemySpawn(mainObject, DeltaTime):
    global timer2
    global ENEMYDELTA
    timer2 += gameObject.DeltaTime.dt
    if timer2 > ENEMYDELTA:
       enemies.append(gameObject.enemyObject(0, 0, 10, 10, 1, 0, 0, False, 255, 255, 255))
       timer2 = 0
    for enemy in enemies:
        enemy.moveTowardsTarget(mainObject)
        
def enemiesHit(enemy, enemies):
    rVal = False
    for enemy2 in enemies:
        if enemy != enemy2:
            if pygame.Rect.colliderect(enemy.getRect(), enemy2.getRect()):
                rVal = True
                break
    return rVal
            
def game(screen):
    global mainObject
    pb = ProgressBar(screen, 1700, 1040, 175, 20, lambda: progress_max(), curved=True)
    pb.completedColour = (30, 144, 255)
    pygame.mouse.set_visible(False)

    mainObject = gameObject.gameObject(250,250,15,15,3, 0, 0, False, 255, 255, 255)
    powerUP = gameObject.powerUP()
    DeltaTime = gameObject.DeltaTime()
    
    pygame.display.set_caption("Runner")
    events = pygame.event.get()
    run = True
    while run == True:
        pygame.time.delay(5)
        RectLogic(screen, mainObject, powerUP, DeltaTime,events)             
        run = movement(events,mainObject, DeltaTime)
        if run == True:
            pygame_widgets.update(events)
            pygame.display.update()
            events = pygame.event.get()
            enemySpawn(mainObject, DeltaTime)

#where I put all functions
def main():
    global points
    global enemies
    pygame.init()
    screen_height=1080
    playGame = True
    while playGame is True:
        pygame.mouse.set_visible(True)
        playGame = startupScreen.startupScreen()
        if playGame is True:
            screen=pygame.display.set_mode([screen_width, screen_height])
            points = 0
            enemies = []
            game(screen)
    pygame.quit()
    
main()