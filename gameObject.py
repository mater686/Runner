# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:30:50 2023

@author: boleymax000
"""

import random
import pygame

class gameObject:
    x = 0
    y = 0
    w = 0
    h = 0
    vel = 0
    screen_width = 1920
    screen_height = 1080
    def __init__(self, x, y, w, h, vel):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = vel
        
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
    def getRect(self):
        return pygame.Rect(self.x,self.y,self.w,self.h)

        
class enemyObject(gameObject):
    
    wait = 100        
    def moveTowardsTarget(self, target):
        if self.wait > 0:
            self.wait -= 1
        else:
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