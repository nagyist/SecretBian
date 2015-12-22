import threading
import pygame
import copy

b_loc = [(298, 275), (399, 275), (400, 275), (298, 351), (399, 351)]
g_loc = [(800, 275), (901, 275), (1002, 275), (800, 351), (901, 351), (1002, 351)]
        
class mythread (threading.Thread):
    def __init__(self, threadID, surface, b_img, g_img):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.surface = surface
        self.b_img = b_img
        self.g_img = g_img
        self.img_alpha = 0
    
    def run(self, party, index):
        global b_loc, g_loc
        
        # if party == blue
        if 0 == party:
            new_policy_img = copy.deepcopy(b_img)
            loc = b_loc[index]
        # else party == green
        else:
            new_policy_img = copy.deepcopy(g_img)
            loc = g_loc[index]
            
        if img_alpha < 255:
            self.img_alpha += 5
            new_policy_img.set_alpha(img_alpha)
            self.surface.blit(new_policy_img, loc)