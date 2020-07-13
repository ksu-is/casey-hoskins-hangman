import pygame
import os

pygame.init()
winHeight = 480
winWidth = 700
win=pygame.display.set_mode((winWidth,winHeight))

hangmanPics = pygame.image.load('hangman-guigame/hangman0.png')

x = 50
y = 50

print("The CWD is " + os.getcwd())
win.blit(hangmanPics, (x,y))

pygame.display.update()
clock.tick(60)