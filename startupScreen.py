# -*- coding: utf-8 -*-

import pygame
from pygame_widgets.button import Button

startGame = False

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def clickStart():
    global startGame
    startGame = True

def get_font(size):
    # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
    
#startupScreen -> show the startup screen
def startupScreen():
    
    global startGame
    startGame = False
    
#    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
    
    #show a button that says start
    #show a button that says exit
    #start is hit - return true
    #if exit is hit - return false
    
    screen2=pygame.display.set_mode([1920, 1080])
    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(960, 300), 
                       text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(960, 600), 
                       text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    

    events = pygame.event.get()
    run = True
    while run == True:
        pygame.time.delay(5)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        if run == True:
            #pygame.display.update()
            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen2)
            events = pygame.event.get()
            pygame.display.update()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        startGame = True

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.display.quit()
                        pygame.quit()

            if startGame is True:
                run = False

    return startGame
