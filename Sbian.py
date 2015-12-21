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
yes_btn_image = 'Image/button1_100x50.gif'
no_btn_image = 'Image/button2_100x50.gif'
bian_image = 'Image/bian_60x45.jpg'

background = pygame.image.load(background_image_filename).convert()
blue_flag  = pygame.image.load(blue_flag_image).convert()
green_flag = pygame.image.load(green_flag_image).convert()
blue_flag_alpha  = pygame.image.load(blue_flag_image).convert()
green_flag_alpha = pygame.image.load(green_flag_image).convert()
bullet_alpha     = pygame.image.load(bullet_image).convert()
investigation_alpha = pygame.image.load(investigation_image).convert()
bian = pygame.image.load(bian_image).convert()
up_arrow = pygame.image.load(up_arrow_image).convert()
yes_btn = pygame.image.load(yes_btn_image).convert()
no_btn = pygame.image.load(no_btn_image).convert()

blue_flag_s = pygame.transform.scale(blue_flag, (60, 45))
green_flag_s = pygame.transform.scale(green_flag, (60, 45))

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

r1_loc  = (920, 655)
r2_loc  = (620, 655)
r3_loc  = (320, 655)
r4_loc  = (0, 435)
r5_loc  = (0, 135)
r6_loc  = (320, 0)
r7_loc  = (620, 0)
r8_loc  = (920, 0)
r9_loc  = (1340, 135)
r10_loc = (1340, 435)

#id 0~2, left to right or up to down
po1_loc  = [(850, 550), (950, 550), (1050, 550)]
po2_loc  = [(550, 550), (650, 550), (750, 550)]
po3_loc  = [(250, 550), (350, 550), (450, 550)]
po4_loc  = [(100, 355), (100, 430), (100, 505)]
po5_loc  = [(100, 130), (100, 205), (100, 280)]
po6_loc  = [(250, 60), (350, 60), (450, 60)   ]
po7_loc  = [(550, 60), (650, 60), (750, 60)   ]
po8_loc  = [(850, 60), (950, 60), (1050, 60)  ]
po9_loc  = [(1190, 130), (1190, 205), (1190, 280)]
po10_loc = [(1190, 355), (1190, 430), (1190, 505)]

status_loc = (390, 250)

player_num = 10
policy_card_num = 3
president = -1
chancellor = -1
pre_president = -1
pre_chancellor = -1
human_player = -1
#mode == 0, ini. mode == 1, after select president candidate
#mode == 2, for human select chancellor.
#mode == 3, for computer select chancellor.
#mode == 4, president and chancellor candidate is done.
#mode == 5, election result
mode = 0

#positive: blue party, negative: green party
party_score = []
policy_card_loc = [po1_loc, po2_loc, po3_loc, po4_loc, po5_loc, po6_loc, po7_loc, po8_loc, po9_loc, po10_loc]
player_name_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
player_name_loc  = [p1_loc, p2_loc, p3_loc, p4_loc, p5_loc, p6_loc, p7_loc, p8_loc, p9_loc, p10_loc]
role_loc  = [r1_loc, r2_loc, r3_loc, r4_loc, r5_loc, r6_loc, r7_loc, r8_loc, r9_loc, r10_loc]
# 2: bian, 1: green, 0:blue
player_role = [0] * player_num
arrow_loc = list(player_name_loc)
yes_btn_loc = [0] * player_num
no_btn_loc = [0] * player_num
#1: Accepted, 0: No
election_ch = [0] * player_num

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
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

def role_to_image(rid):
    if 0 == rid:
        return blue_flag_s
    elif 1 == rid:
        return green_flag_s
    elif 2 == rid:
        return bian
    
def draw_player_name():
    global player_name_list, president, chancellor, player_role

    # if human role is green party
    if 1 == player_role[human_player]:
        show_green_party = 1
    else:
        show_green_party = 0
    
    for i in range(player_num):
        if i == human_player:
            screen.blit(role_to_image(player_role[i]), role_loc[i])
        elif 1 == show_green_party and 1 == player_role[i]:
            screen.blit(role_to_image(player_role[i]), role_loc[i])
    
        if i == president:
            if 0 <= president <= 2 or 5 <= president <= 7:
                screen.blit(write(player_name_list[i]+u" 總統", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
            else:
                screen.blit(write(player_name_list[i], BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
                screen.blit(write(u"總統", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]+20))
        elif i == chancellor:
            if 0 <= chancellor <= 2 or 5 <= chancellor <= 7:
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

def id_to_arrow_image(id):
    if 0 <= id <= 2:
        return down_arrow
    elif 3 <= id <= 4:
        return left_arrow
    elif 5 <= id <= 7:
        return up_arrow
    elif 8 <= id <= 9:
        return right_arrow

def id_to_arrow_alpha_image(id):
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
    
    (MouseX, MouseY) = pygame.mouse.get_pos()
    
    for i in range(player_num):
        if i in [president, pre_president, pre_chancellor]:
            continue
        if arrow_loc[i][0] <= MouseX <= arrow_loc[i][0] + id_to_arrow_image(i).get_width() and arrow_loc[i][1] <= MouseY <= arrow_loc[i][1] + id_to_arrow_image(i).get_height():
            screen.blit(id_to_arrow_image(i), arrow_loc[i])
        else:
            screen.blit(id_to_arrow_alpha_image(i), arrow_loc[i])
            
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
    global arrow_loc
    
    for i in range(player_num):
        if 0 <= i <= 2:
            arrow_loc[i] = (arrow_loc[i][0], arrow_loc[i][1]-50)
        elif 3 <= i <= 4:
            arrow_loc[i] = (arrow_loc[i][0]+50, arrow_loc[i][1])
        elif 5 <= i <= 7:
            arrow_loc[i] = (arrow_loc[i][0], arrow_loc[i][1]+30)
        elif 8 <= i <= 9:
            arrow_loc[i] = (arrow_loc[i][0]-50, arrow_loc[i][1])

def draw_button(loc, str, image = yes_btn, size = 16):
    (mouseX, mouseY) = pygame.mouse.get_pos()
        
    fontx = loc[0]+ 47 - int(len(str)/2*12)
    fonty = loc[1]+15
    screen.blit(image, loc)
    if loc[0] <= mouseX <= loc[0]+image.get_width() and loc[1] <= mouseY <= loc[1]+image.get_height():
        screen.blit(write(str, BLUE, size), (fontx, fonty))
    else:
        screen.blit(write(str, BLACK, size), (fontx, fonty))            
            
def yes_no_btn():
    global arrow_loc, yes_btn_loc, no_btn_loc
    
    for i in range(player_num):
        if 0 <= i <= 2:
            yes_btn_loc[i] = (arrow_loc[i][0]-100, arrow_loc[i][1]-30)
            no_btn_loc[i] = (arrow_loc[i][0]+25, arrow_loc[i][1]-30)
        elif 3 <= i <= 4:
            yes_btn_loc[i] = (arrow_loc[i][0]+20, arrow_loc[i][1]-50)
            no_btn_loc[i] = (arrow_loc[i][0]+20, arrow_loc[i][1]+25)
        elif 5 <= i <= 7:
            yes_btn_loc[i] = (arrow_loc[i][0]-100, arrow_loc[i][1]+30)
            no_btn_loc[i] = (arrow_loc[i][0]+25, arrow_loc[i][1]+30)
        elif 8 <= i <= 9:
            yes_btn_loc[i] = (arrow_loc[i][0]-95, arrow_loc[i][1]-50)
            no_btn_loc[i] = (arrow_loc[i][0]-95, arrow_loc[i][1]+25)
        
def ini_loc():
    ini_arrow_loc()
    yes_no_btn()

def yes_no_ai(i, role):
    
    score = 0
    ele = 0
    
    # if blue
    if 0 == role:
        b = 1
        g = 0
    # if green
    else:
        b = 0
        g = 1
    
    if party_score[i][president] >= 2:
        score += 2
    elif party_score[i][president] <= -2:
        score -= 2
    else:
        score += party_score[i][president]
        
    if party_score[i][chancellor] >= 2:
        score += 2
    elif party_score[i][chancellor] <= -2:
        score -= 2
    else:
        score += party_score[i][chancellor]   
    
    r = random.randint(1, 16)
    if score >= 4:
        ele = b
    elif 3 == score:
        if r > 1:
            ele = b
        else:
            ele = g
    elif 2 == score:
        if r > 2:
            ele = b
        else:
            ele = g
    elif 1 == score:
        if r > 4:
            ele = b
        else:
            ele = g
    elif 0 == score:
        if r > 8:
            ele = b
        else:
            ele = g
    elif -1 == score:
        if r > 12:
            ele = b
        else:
            ele = g
    elif -2 == score:
        if r > 14:
            ele = b
        else:
            ele = g
    elif -3 == score:
        if r > 15:
            ele = b
        else:
            ele = g
    elif -4 <= score:
        ele = g
    
    return ele
    
def election_ai():
    global election_ch
    
    score = 0
    
    for i in range(player_num):
        if i == human_player:
            continue
        elif i in [president, chancellor]:
            election_ch[i] = 1
        else:
            election_ch[i] = yes_no_ai(i, player_role[i])

def election_result():
    global election_ch
    
    y_num = 0
    n_num = 0
    
    for i in range(player_num):
        if 1 == election_ch[i]:
            screen.blit(write(u"同意", BLACK, 20), arrow_loc[i])
            y_num += 1
        else:
            screen.blit(write(u"否決", RED, 20), arrow_loc[i])
            n_num += 1
            
    if y_num > n_num:
        screen.blit(write(u"同意：%d票，否決：%d票， %s 當總統， %s 當院長，通過"%(y_num, n_num, player_name_list[president], player_name_list[chancellor]), BLACK, 20), status_loc)
    else:
        screen.blit(write(u"同意：%d票，否決：%d票，政治協商破局"%(y_num, n_num), BLACK, 20), status_loc)
    
def main():
    global player_role, mode, player_name_list, president, chancellor, human_player
    
    first = 1
    # index 0: bian, 1~3: green party, 4~9: blue party
    player_ini_role = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    random.shuffle(player_name_list)
    ini_loc()
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
            for i in player_ini_role[1:4]:
                for j in player_ini_role[1:4]:
                    if i == j:
                        continue
                    party_score[i][j] = -60
            first = 0
        if 0 == mode:
            president = random.randint(0, player_num-1)
            chancellor = -1
            #president = human_player #For test only
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
        elif 3 == mode:
            if human_player != president and human_player != chancellor:
                screen.blit(write(u"%s 代表，您是否贊成 %s 當總統以及 %s 當院長？"%(player_name_list[human_player], player_name_list[president], player_name_list[chancellor]), BLACK, 20), status_loc)
                draw_button(yes_btn_loc[human_player],u"同意", yes_btn)
                draw_button(no_btn_loc[human_player],u"否決", no_btn)
            else:
                mode = 4
        elif 4 == mode:
            election_ai()
            mode = 5
        elif 5 == mode:
            election_result()
        # Test location
        #for i in range(player_num):
        #    screen.blit(yes_btn, yes_btn_loc[i])
        #    screen.blit(no_btn, no_btn_loc[i])
        # End test location
        # Test policy card
        #for i in range(player_num):
        #    for j in range(policy_card_num):
        #        screen.blit(green_flag, policy_card_loc[i][j])
        # End test policy card
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 2 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    for i in range(player_num):
                        if i in [president, pre_president, pre_chancellor]:
                            continue
                        if arrow_loc[i][0] <= MouseX <= arrow_loc[i][0] + id_to_arrow_image(i).get_width() and arrow_loc[i][1] <= MouseY <= arrow_loc[i][1] + id_to_arrow_image(i).get_height():
                            chancellor = i
                            mode = 4
                            break
                    break
                elif 3 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if yes_btn_loc[human_player][0] <= MouseX <= yes_btn_loc[human_player][0]+yes_btn.get_width() and yes_btn_loc[human_player][1] <= MouseY <= yes_btn_loc[human_player][1]+yes_btn.get_height():
                        election_ch[human_player] = 1
                        mode = 4
                    elif no_btn_loc[human_player][0] <= MouseX <= no_btn_loc[human_player][0]+no_btn.get_width() and no_btn_loc[human_player][1] <= MouseY <= no_btn_loc[human_player][1]+no_btn.get_height():
                        election_ch[human_player] = 0
                        mode = 4
                    break
                        
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()