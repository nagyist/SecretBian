import random
import time
import threading
import pygame
from sys import exit

screen_width = 1400
screen_height = 700

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Secret Bian')

background_image_filename = 'Image/Nostalgy.gif'

background = pygame.image.load(background_image_filename).convert()

#treasure_b.set_alpha(treasure_alpha)

def fill_background():
    for y in range(0, screen_height, background.get_height()):
        for x in range(0, screen_width, background.get_width()):
            screen.blit(background, (x, y))
       
def main():
    while True:
        fill_background()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    #if f_x <= mouseX <= f_x+button1.get_width() and f_y <= mouseY <= f_y+button1.get_height():
                    #    break            
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()