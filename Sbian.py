import random
import time
import threading
import pygame
from sys import exit

screen_width = 1400
screen_height = 700
policy_alpha = 70
arrow_alpha = 100

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Secret Bian')

background_image_filename = 'Image/Nostalgy.gif'
blue_flag_image = 'Image/blue_flag_100x75.jpg'
green_flag_image = 'Image/green_flag_100x75.jpg'
bullet_image = 'Image/bullet__100x75.jpg'
investigation_image = 'Image/investigation_100x75.png'
up_arrow_image = 'Image/arrow_30x30.gif'

background = pygame.image.load(background_image_filename).convert()
blue_flag  = pygame.image.load(blue_flag_image).convert()
green_flag = pygame.image.load(green_flag_image).convert()
blue_flag_alpha  = pygame.image.load(blue_flag_image).convert()
green_flag_alpha = pygame.image.load(green_flag_image).convert()
bullet_alpha     = pygame.image.load(bullet_image).convert()
investigation_alpha = pygame.image.load(investigation_image).convert()
up_arrow = pygame.image.load(up_arrow_image).convert()

left_arrow = pygame.transform.rotate(up_arrow, 90)
down_arrow = pygame.transform.rotate(up_arrow, 180)
right_arrow = pygame.transform.rotate(up_arrow, 270)
up_arrow2 = pygame.image.load(up_arrow_image).convert()
left_arrow2 = pygame.transform.rotate(up_arrow, 90)
down_arrow2 = pygame.transform.rotate(up_arrow, 180)
right_arrow2 = pygame.transform.rotate(up_arrow, 270)

up_arrow2.set_alpha(arrow_alpha)
left_arrow2.set_alpha(arrow_alpha)
down_arrow2.set_alpha(arrow_alpha)
right_arrow2.set_alpha(arrow_alpha)
blue_flag_alpha.set_alpha(policy_alpha)
green_flag_alpha.set_alpha(policy_alpha)
bullet_alpha.set_alpha(policy_alpha)
investigation_alpha.set_alpha(policy_alpha)

p1  = u"小鷹"
p2  = u"小賣"
p3  = u"小熊"
p4  = u"小倉"
p5  = u"小力"
p6  = u"小站"
p7  = u"小魚"
p8  = u"小鯨"
p9  = u"小冏"
p10 = u"小牆"

p1_loc  = (990, 675)
p2_loc  = (690, 675)
p3_loc  = (390, 675)
p4_loc  = (0, 490)
p5_loc  = (0, 190)
p6_loc  = (390, 0)
p7_loc  = (690, 0)
p8_loc  = (990, 0)
p9_loc  = (1360, 190)
p10_loc = (1360, 490)

status_loc = (390, 250)

player_num = 10
president = -1
chancellor = -1
pre_president = -1
pre_chancellor = -1
human_player = -1
#mode == 0, ini. mode == 1, after select president candidate
#mode == 2, for human select chancellor.
#mode == 3, for computer select chancellor.
mode = 0

#positive: blue party, negative: green party
party_score = []
player_name_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
player_name_loc  = [p1_loc, p2_loc, p3_loc, p4_loc, p5_loc, p6_loc, p7_loc, p8_loc, p9_loc, p10_loc]
player_role = [0] * 10
arrow_loc = list(player_name_loc)

BLACK = (0, 0, 0)
RED = (255, 0, 0)

policy_interval_gap = 100

def write(msg="pygame is cool", color= (0,0,0), size = 14):
    myfont = pygame.font.Font("wqy-zenhei.ttf", size)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext 

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
            
def draw_player_name():
    global player_name_list, president, chancellor

    for i in range(player_num):
        if i == president:
            if 0 <= president <= 2 or 5 <= president <= 7:
                screen.blit(write(player_name_list[i]+u" 總統", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
            else:
                screen.blit(write(player_name_list[i], BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
                screen.blit(write(u"總統", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]+20))
        elif i == chancellor:
            if 0 <= president <= 2 or 5 <= president <= 7:
                screen.blit(write(player_name_list[i]+u" 院長", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
            else:
                screen.blit(write(player_name_list[i], BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
                screen.blit(write(u"院長", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]+20))
        else:
            screen.blit(write(player_name_list[i], BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))

# find human player
def findhp(pnlist):
    for i in range(player_num):
        if pnlist[i] == u"小鷹":
            return i

def id_to_arrow__image(id):
    if 0 <= id <= 2:
        return down_arrow2
    elif 3 <= id <= 4:
        return left_arrow2
    elif 5 <= id <= 7:
        return up_arrow2
    elif 8 <= id <= 9:
        return right_arrow2
    
            
def draw_select_chancellor():
    screen.blit(write(u"%s 總統，您要選誰當院長呢？"%p1, BLACK, 20), status_loc)
    
    for i in range(player_num):
        if i in [president, pre_president, pre_chancellor]:
            continue
        screen.blit(id_to_arrow__image(i), arrow_loc[i])
            
def select_chancellor_ai():
    candidate = []
    
    # if blue party
    if 0 == player_role[president]:
        for i in range(player_num):
            if i in [president, pre_president, pre_chancellor]:
                continue
            elif party_score[president][i] < -1:
                continue
            elif -1 == party_score[president][i]:
                candidate.append(i)
            elif 0 == party_score[president][i]:
                candidate.extend([i]*3)
            elif 1 == party_score[president][i]:
                candidate.extend([i]*9)
            else: # party_score[i] > 1
                candidate.extend([i]*27)
    # if green party
    else:
        for i in range(player_num):
            if i in [president, pre_president, pre_chancellor]:
                continue
            elif party_score[president][i] > 1:
                continue
            elif 1 == party_score[president][i]:
                candidate.append(i)
            elif 0 == party_score[president][i]:
                candidate.extend([i]*3)
            elif -1 == party_score[president][i]:
                candidate.extend([i]*9)
            else: # party_score[i] < -1
                candidate.extend([i]*27)
    
    if 0 == len(candidate):
        for i in range(player_num):
            if i in [president, pre_president, pre_chancellor]:
                continue
            else:
                candidate.append(i)
    
    random.shuffle(candidate)
    
    return candidate[0]

def ini_arrow_loc():
    for i in range(player_num):
        if 0 <= i <= 2:
            arrow_loc[i] = (arrow_loc[i][0], arrow_loc[i][1]-50)
        elif 3 <= i <= 4:
            arrow_loc[i] = (arrow_loc[i][0]+50, arrow_loc[i][1])
        elif 5 <= i <= 7:
            arrow_loc[i] = (arrow_loc[i][0], arrow_loc[i][1]+50)
        elif 8 <= i <= 9:
            arrow_loc[i] = (arrow_loc[i][0]-50, arrow_loc[i][1])
    
def main():
    global player_role, mode, player_name_list, president, chancellor, human_player

    first = 1
    # index 0: bian, 1~3: green party, 4~9: blue party
    player_ini_role = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    random.shuffle(player_name_list)
    ini_arrow_loc()
    human_player = findhp(player_name_list)
    
    while True:
        if 1 == first:
            random.shuffle(player_ini_role)
            for i in range(player_num):
                if 0 == i:
                    # 2 == bian role
                    player_role[player_ini_role[i]] = 2
                elif 0 < i < 4:
                    # 1 == green party
                    player_role[player_ini_role[i]] = 1
                else:
                    # 0 == blue party
                    player_role[player_ini_role[i]] = 0
                party_score.append([0]*player_num)
            first = 0
        if 0 == mode:
            president = random.randint(0, player_num-1)
            chancellor = -1
            #president = human_player
            mode = 1
    
        if 1 == mode:
            if president == human_player:
                mode = 2
            else:
                chancellor = select_chancellor_ai()
                mode = 3
    
        fill_background()
        draw_policy_table()
        draw_player_name()
        if 2 == mode:
            draw_select_chancellor()
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