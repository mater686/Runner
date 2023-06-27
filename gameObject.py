# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:30:50 2023

@author: boleymax000
"""

import random
import pygame

pygame.mixer.init()

class gameObject:
    x = 0
    y = 0
    w = 0
    h = 0
    vel = 0
    dashtimer = 0
    dashenergy = 0.01
    timer = 0
    currentvel = 0
    currentvel2 = 0
    isdashing = False
    screen_width = 1920
    screen_height = 1080
    rcolor = 0
    gcolor = 0
    bcolor = 0
    def __init__(self, x, y, w, h, vel, dashtimer, timer, isdashing, rcolor, bcolor, gcolor):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = vel
        self.dashtimer = dashtimer
        self.timer = timer
        self.isdashing = isdashing
        self.rcolor = rcolor
        self.gcolor = gcolor
        self.bcolor = bcolor
        self.currentvel = self.vel
        
    def moveRight(self):
        if (self.x < self.screen_width - self.vel):
            self.x += self.vel

    def moveLeft(self):
        if (self.x > self.vel):
            self.x -= self.vel
            
    def moveUp(self):
        if (self.y > self.vel):
            self.y -= self.vel
    
    def moveDown(self):
        if (self.y < self.screen_height - self.vel):
            self.y += self.vel
            
    def slowDown(self):
        self.vel = 3
        
    def startDash(self):
        self.rcolor = 69
        self.gcolor = 100
        self.bcolor = 200
        self.isdashing = True
        self.currentvel2 = self.vel
        self.vel += 10
                    
    def endDash(self):
        self.rcolor = 255
        self.gcolor = 255
        self.bcolor = 255
        self.vel = self.currentvel2
        self.isdashing = False
        
    def Dash(self, deltaTime):
        if self.isdashing == True:
            
            self.timer += deltaTime
            if self.timer >= 3:
                gameObject.endDash(self)
            
           
        
        
    def getRect(self):
        return pygame.Rect(self.x,self.y,self.w,self.h)

        
class enemyObject(gameObject):
    
    wait = 1
    live = 10000      
    rcolor = 255
    gcolor = 0
    bcolor = 0
    #def __init__(self, x, y, w, h, vel):
        #gameObject.__init__(self,x,y,w,h,vel)
        #self.rcolor = random.randint(1,255)
        #self.gcolor = random.randint(1,255)
        #self.bcolor = random.randint(1,255)
    def moveTowardsTarget(self, target):
        if self.wait > 0:
            self.wait -= 1
        else:
            self.live -= 1
            if self.x > target.x:
                self.x = self.x - self.vel
            if self.y > target.y:
                self.y = self.y - self.vel
            if self.x < target.x:
                self.x = self.x + self.vel
            if self.y < target.y:   
                self.y = self.y + self.vel
                
class powerUP():
        x = random.randint(100, 1820)
        y = random.randint(100, 980)
        w = 10
        h = 10                                                
        px = random.randint(100, 1820)
        py = random.randint(100, 980)
        
class DeltaTime():
    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000