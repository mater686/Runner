# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 13:55:40 2023

@author: boleymax000
"""

import pygame
import random
import gameObject


pygame.init()
pygame.mixer.init()

screen_width=1920
screen_height=1080
screen=pygame.display.set_mode([screen_width, screen_height])
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
x = 250
y = 250
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
enemyx = 20
enemyy = 20 
enemy_width = 15
enemy_hight = 15
enemy_vel = 15
points = 0
white = 255, 255, 255
timer = 0
currentenemies = 1
enemies = []
point_pickup = pygame.mixer.Sound("C:/Users/maxim/Practice/ChaChing.mp3")
#drawing and collideing logic
def RectLogic(scr, mainObject, powerUP):
    global points
    global enemies
    global point_pickup
    pygame.init()
    scr.fill((0, 0, 0))
    score(scr, mainObject)        
    playerrec = pygame.draw.rect(scr, (255, 255, 255), (mainObject.x, mainObject.y, mainObject.w, mainObject.h))
    for enemy in enemies:
        enemyrec = pygame.draw.rect(scr, (255, 0, 0), (enemy.x, enemy.y, enemy.w, enemy.h))
        enemycollide = pygame.Rect.colliderect(playerrec, enemyrec)
        
        if enemycollide:
            points = points - 5
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
    
    pygame.display.update()
    if powerUPcollide:
        powerUP.x = random.randint(100, 1820)
        powerUP.y = random.randint(100, 980)
        mainObject.vel = mainObject.vel + 2
    pointsup = pygame.Rect.colliderect(playerrec, pointpowerup)
    if pointsup:
        powerUP.px = random.randint(100, 1820)
        powerUP.py = random.randint(100, 980)
        point_pickup.play()
        points += 5
    

#scorechangeing        
def scoresystem(mainObject):
    global timer
    global points
    global currentenemies
    dt = clock.tick() / 1000
    timer += dt
    enemy = gameObject.enemyObject(0, 0, 10, 10, 1)
    
    if timer > 1:
        points = points + 1
        timer = 0
        
    if points < 0:
        points = 0
        mainObject.vel = 3
        
    if points > (currentenemies + 1) * 10:
        currentenemies += 1
        enemies.append(enemy)
        enemy.x = random.randint(100,1820)
        enemy.y = random.randint(100,980)
    

#score UI        
def score(scr, mainObject):
    global points
    font = pygame.font.Font('BULKYPIX.TTF', 32)
    text = font.render(f'{points}', True, white)
    textRect = text.get_rect()
    textRect.center = (fontx // 1, fonty // 2)
    scr.blit(text, textRect)
    scoresystem(mainObject)  

#player movement        
def movement(events, mainObject):

    global playerLeft
    global playerRight
    global playerUp
    global playerDown
    global playerSpeed
    global currentspeed
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
    
            
    return rVal                

def enemySpawn(mainObject):
    global timer2
    dt2 = clock.tick() / 1000
    timer2 += dt2
    if timer2 > 1:
       enemies.append (gameObject.enemyObject(0, 0, 10, 10, 1))
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
            
            
            
#where I put all functions
def main():
    global points      
    screen_width=1920
    screen_height=1080
    mainObject = gameObject.gameObject(250,250,15,15,3)
    powerUP = gameObject.powerUP()
    screen = pygame.display.set_mode([screen_width, screen_height])
    
    pygame.display.set_caption("Runner")
    run = True
    events = pygame.event.get()
    RectLogic(screen, mainObject, powerUP)
    while run == True:
        pygame.time.delay(5)
        RectLogic(screen, mainObject, powerUP)             
        run = movement(events,mainObject)
        events = pygame.event.get()
        enemySpawn(mainObject)
    pygame.quit()
    
main()