import random
import time
import threading
import pygame
from sys import exit

screen_width = 1400
screen_height = 700
policy_alpha = 90

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Secret Bian')

background_image_filename = 'Image/Nostalgy.gif'
blue_flag_image = 'Image/blue_flag_100x75.jpg'
green_flag_image = 'Image/green_flag_100x75.jpg'
bullet_image = 'Image/bullet__100x75.jpg'
investigation_image = 'Image/investigation_100x75.png'

background = pygame.image.load(background_image_filename).convert()
blue_flag  = pygame.image.load(blue_flag_image).convert()
green_flag = pygame.image.load(green_flag_image).convert()
blue_flag_alpha  = pygame.image.load(blue_flag_image).convert()
green_flag_alpha = pygame.image.load(green_flag_image).convert()
bullet_alpha     = pygame.image.load(bullet_image).convert()
investigation_alpha = pygame.image.load(investigation_image).convert()

blue_flag_alpha.set_alpha(policy_alpha)
green_flag_alpha.set_alpha(policy_alpha)
bullet_alpha.set_alpha(policy_alpha)
investigation_alpha.set_alpha(policy_alpha)

BLACK = (0, 0, 0)
RED = (255, 0, 0)

policy_interval_gap = 100

def fill_background():
    for y in range(0, screen_height, background.get_height()):
        for x in range(0, screen_width, background.get_width()):
            screen.blit(background, (x, y))

def draw_green_table():
    row_num = 3
    width = 1
   
    (mid_w, mid_h) = (screen_width/2, screen_height/2)
    x = mid_w + policy_interval_gap - 1
    y = mid_h - green_flag.get_height() - 1
    
    #row line
    for i in range(0, row_num):
        pygame.draw.line(screen, BLACK, (x, y + i*(green_flag.get_height()+1)), (x + 3*(green_flag.get_width()+1), y + i*(green_flag.get_height()+1)), width)
    
    #column line
    for i in range(0, row_num+1):
        pygame.draw.line(screen, BLACK, (x + i*(green_flag.get_width()+1), y), (x + i*(green_flag.get_width()+1), y + 2*(green_flag.get_height()+1)), width)
        
    victory_x = x + 2*(green_flag.get_width()+1) + 1
    victory_y = y + green_flag.get_height()+2
    
    pre_victory_x = victory_x-1-green_flag.get_width()
    
    x4 = pre_victory_x-1-green_flag.get_width()
    
    x3 = x + (row_num - 1)*(green_flag.get_width()+1)+1
    
    pygame.draw.rect(screen, RED, (pre_victory_x, victory_y, green_flag.get_width(), green_flag.get_height()))
    pygame.draw.rect(screen, RED, (victory_x, victory_y, green_flag.get_width(), green_flag.get_height()))
    
    screen.blit(bullet_alpha, (x3, y))
    screen.blit(investigation_alpha, (x4, victory_y))
    screen.blit(bullet_alpha, (pre_victory_x, victory_y))
    screen.blit(green_flag_alpha, (victory_x, victory_y))
    
def draw_blue_table():
    row_num = 3
    width = 1
   
    (mid_w, mid_h) = (screen_width/2, screen_height/2)
    x = mid_w - policy_interval_gap - 3*(blue_flag.get_width() + 1)
    y = mid_h - blue_flag.get_height() - 1
    
    #row line
    for i in range(0, row_num-1):
        pygame.draw.line(screen, BLACK, (x, y + i*(blue_flag.get_height()+1)), (x + 3*(blue_flag.get_width()+1), y + i*(blue_flag.get_height()+1)), width)
    
    pygame.draw.line(screen, BLACK, (x, y + 2*(blue_flag.get_height()+1)), (x + 2*(blue_flag.get_width()+1), y + 2*(blue_flag.get_height()+1)), width)
    
    #column line
    for i in range(0, row_num):
        pygame.draw.line(screen, BLACK, (x + i*(blue_flag.get_width()+1), y), (x + i*(blue_flag.get_width()+1), y + 2*(blue_flag.get_height()+1)), width)
    
    pygame.draw.line(screen, BLACK, (x + row_num*(blue_flag.get_width()+1), y), (x + row_num*(blue_flag.get_width()+1), y + blue_flag.get_height()+1), width)
    
    victory_x = x + blue_flag.get_width()+1 + 1
    victory_y = y + blue_flag.get_height()+2
    
    screen.blit(blue_flag_alpha, (victory_x, victory_y))
    
def draw_policy_table():
    draw_blue_table()
    draw_green_table()
            
def main():
    while True:
        fill_background()
        draw_policy_table()
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