# Premium Golf 2 By: Josh Hamburger
#
# This is a game of 2d golf that takes
# some inspiration from Super Stickman Golf.
# The objective of the game is to aim, choose power,
# and shoot the ball until it gets into the hole.
# The majority of assets are taken from
# Kenny Game Assets, which can be found
# at kenny.nl/assets
#
# Last modified: June 21st, 2017

import pygame,sys,random,math
#leveldata holds the level class and a list of all levels
from leveldata import *
pygame.init()
pygame.key.set_repeat(1)

size = width , height = 875,595
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Premium Golf 2')

#set colours and fonts
black = [22,22,29]
white = [255,255,255]
font = pygame.font.SysFont("CopperplateGothic",22)
bigfont = pygame.font.SysFont("CopperplateGothic",40,True)
winfont = pygame.font.SysFont("Forte",27)
bigwinfont = pygame.font.SysFont("Forte",40)

#set various variables
strokes = 0
angle_rotation = 0
x_speed = 0
y_speed = 0
slowdown = 0.1
power = 1
powertimer = 0
game_state = "menu"
increase = True
solid = True
lheight = height
x_camera = 0
score = 0
mouse_click = False
current_level = -1
clouds = []
x_mouse = 0
y_mouse = 0
timer = 0
can_click = True

#Set up image codes list that will be used for retriving levels
#and setting each block to the right image
imagecodes = ["O",")","=","(","X","^","l","n"]

#set codes for comparison of strokes to par
par_codes = [[-4,"Condor"],[-3,"Albatross"],[-2,"Eagle"],[-1,"Birdie"],[0,"At Par"],[+1,"Bogey"],[+2,"Double-Bougy"],[+3,"Triple-Bougy"],[+4,"Quadruple-Bougy"]]

#get images and set rects
img_ball = pygame.image.load("Ball/img_ball.png")
ball = img_ball.get_rect()

img_arrow = pygame.image.load("Ball/img_arrow.png")
arrow = img_arrow.get_rect()

img_hole = pygame.image.load("Hole/hole.png").convert_alpha()
img_flag = pygame.image.load("Hole/flag.png").convert_alpha()
img_pole = pygame.image.load("Hole/pole.png").convert_alpha()
score_background = pygame.image.load("GUI/img_score.png").convert_alpha()
score_paper = pygame.image.load("GUI/score_paper.png").convert_alpha()
button_up = pygame.image.load("GUI/button_up.png").convert_alpha()
button_down = pygame.image.load("GUI/button_down.png").convert_alpha()
button_locked = pygame.image.load("GUI/button_locked.png").convert_alpha()
img_cloud = pygame.image.load("GUI/cloud.png").convert_alpha()
img_sky = pygame.image.load("GUI/sky.png").convert_alpha()
logo = pygame.image.load("GUI/logo.png").convert_alpha()
img_congratulations = pygame.image.load("GUI/congratulations.png").convert_alpha()
img_a = pygame.image.load("GUI/img_a.png").convert_alpha()
img_d = pygame.image.load("GUI/img_d.png").convert_alpha()
img_left = pygame.image.load("GUI/img_left.png").convert_alpha()
img_right = pygame.image.load("GUI/img_right.png").convert_alpha()
img_spacebar = pygame.image.load("GUI/img_spacebar.png").convert_alpha()

#Hold info for each block in the current course         
class Block:
    def __init__(self,pos,width,height,solid,code=False):
        self.pos = self.left,self.top = pos
        self.width = width
        self.height = height
        self.solid = solid
        if code != False:
            self.img = pygame.image.load(tileset+"/"+code+".png").convert_alpha()
        else:
            self.img = False
        self.code = code
        self.right = self.left + self.width
        self.bottom = self.top + self.height

#Button class handles all buttons
class Button():
    def __init__(self,x,y,width,height,on_state,text,font,lockable=False):
        self.size = size
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.on_state = on_state
        self.text = font.render(text,1,white)
        self.click = False
        self.lockable = lockable
    #This function tests to see what image the button should display, and if the button is being clicked
    def draw_button(self):
        global mouse_click
        self.click = False
        if game_state == self.on_state:
            #Check if the continue button should be locked or not
            if (0 <= current_level < len(levels)-1) == False and self.lockable:
                centre(pygame.transform.scale(button_locked,(self.width,self.height)),self.x, self.y)
            else:
                #Check if the mouse is on the button
                if self.x-self.width/2 < x_mouse < self.x+self.width/2 and self.y-self.height/2 < y_mouse < self.y+self.height/2:
                    centre(pygame.transform.scale(button_down,(self.width,self.height)),self.x, self.y)
                    if mouse_click == True:
                        self.click = True
                        mouse_click = False
                else:
                    centre(pygame.transform.scale(button_up,(self.width,self.height)),self.x, self.y)
                    
            #Centre button text on button
            centre(self.text, self.x, self.y)

#Cloud class handles variables for the coulds that appear in the game menus
class Cloud():
    def __init__(self):
        self.size = random.randint(75,250)
        self.img = pygame.transform.scale(img_cloud,(int(self.size*1.3),int(self.size*1.3)))
        self.speed = self.size/40
        self.y = self.size * 3 - 200
        self.x = width + self.size

#Retrieve a level from the list of levels, and turn it into a list of blocks
#aswell as set find the position of the ball
def get_level(level_num):
    tempblocks = []
    #Set blocks at edges of levels to avoid the ball going offscreen
    tempblocks.append(Block((0,-100),lwidth,100,True))
    tempblocks.append(Block((-100,0),100,lheight,True))
    tempblocks.append(Block((0,lheight),lwidth,100,True))
    tempblocks.append(Block((lwidth,0),100,lheight,True))
    temprow = 0
    #Go through all character in the list of level blocks
    for row in levels[level_num].blocks:
        tempcol = 0
        for col in row:
            #Compare each block to the block codes
            for i in imagecodes:
                if col == i:
                    #Create the block with the correct block id, and solidity accordingly
                    if col == "^" or col == "n" or col == "l":
                        tempblocks.append(Block((tempcol*35,temprow*35),35,35,False,i))
                    else:
                        tempblocks.append(Block((tempcol*35,temprow*35),35,35,True,i))
                #Find position of ball
                elif col == "B":
                    ball.x = tempcol*35 + 35/2
                    ball.bottom = (temprow+1)*35-1
            tempcol += 1
        temprow += 1
    return tempblocks, ball.x, ball.bottom

#Check if the ball has hit the side of a block
def check_side(side, block):
    if ball.top < block.bottom and ball.bottom > block.top:
        if side == "right":
            if x_speed < 0 and block.img != "(":
                if ball.left <= block.right and ball.right > block.left:
                    return True
        elif side == "left":
            if x_speed > 0 and block.img != ")":
                if ball.right >= block.left and ball.right < block.right:
                    return True

#Centre a source on a coordinate
def centre(source, xmid, ymid):
    screen.blit(source, (xmid-source.get_width()/2,ymid-source.get_height()/2))

#Draw the ball (while accounting for the camera position)
def drawBall():
    screen.blit(img_ball,(ball.left-x_camera,ball.top))

#Change that absolute value of a number
def changeAbs(val,posval):
    if val < 0:
        posval = -posval
    return posval

#Create all buttons
buttons = []
buttons.append(Button(545,400,200,50,"hole","Next Level",font))
buttons.append(Button(315,400,200,50,"hole","Main Menu",font))
buttons.append(Button(width/2,200,400,85,"menu","Continue",bigfont,True))
buttons.append(Button(width/2,300,400,85,"menu","New Game",bigfont))
buttons.append(Button(width/2,400,400,85,"menu","Instructions",bigfont))
buttons.append(Button(width/2,500,400,85,"menu","Quit",bigfont))
buttons.append(Button(width/2,405,300,80,"win","Main Menu",bigfont))
buttons.append(Button(width/2,530,400,80,"instructions","Main Menu",bigfont))

#Game loop        
while True:
    #User inputs
    for event in pygame.event.get():
        #Exit the game if the user closes the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        #Get the position of the mouse
        if event.type == pygame.MOUSEMOTION:
            x_mouse, y_mouse = pygame.mouse.get_pos()

        #Check if the mouse has made a full click (down and up)
        mouse_click = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            can_click = True
        if event.type == pygame.MOUSEBUTTONUP and can_click == True:
            mouse_click = True
            can_click = False
    
        keys = pygame.key.get_pressed()
        
        #Set various variables when the player chooses the power of their shot
        if keys[pygame.K_SPACE] and game_state == "power":
            angle_rotation = 0
            x_speed *= power/5
            y_speed *= power/5
            pygame.key.set_repeat(1)
            game_state = "moving"
            strokes += 1
            shot_text = font.render("Strokes: "+str(strokes)+"    Par:  "+str(par),1,black)
            
        #Set the ball speed and gamestate when the player choose their aim 
        elif game_state == "aiming":
            if keys[pygame.K_SPACE]:
                x_speed = -angle_rotation/10
                y_speed = -9 + abs(x_speed)
                pygame.key.set_repeat(0)
                game_state = "power"
            #Rotate the arrow when aiming
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                angle_rotation = min(angle_rotation+1,90)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                angle_rotation = max(angle_rotation-1,-90)

    #General game code
    
    #Set camera position on the ball while keeping the camera on the screen
    if game_state in ["moving","power","aiming"]:
        x_camera = max(min(ball.left-width/2,lwidth-width),0)
        
    #Change animations of the arrow when selecting power
    if game_state == "power":
        #power goes up to 8 then down, looping
        if powertimer <= 0:
            if increase == True:
                power += 1
            elif increase == False:
                power -= 1
            if power == 1 or power == 8:
                increase = not increase
            powertimer = 5
        powertimer -= 1
        #The image of the arrow changes to represent power
        img_arrow = pygame.image.load("Ball/img_arrow_animate"+str(int(power))+".png").convert_alpha()

    #Move the ball
    if game_state == "moving":
        ball.right += int(x_speed)
        ball.bottom = min(ball.bottom+y_speed,height)

    #Decide whether the ball is ready for another shot
    if int(x_speed) == 0 and y_speed == 0 and game_state == "moving":
        game_state = "aiming"
        img_arrow = pygame.image.load("Ball/img_arrow.png").convert_alpha()

    #Stop the ball from moving too fast and risking clipping
    if abs(y_speed) > 8:
        y_speed = changeAbs(y_speed,8)

    #Ball physics
    air = True
    if game_state == "moving":
        for block in blocks:
            if block.solid == True:
                #Set a few relevant temporary variables
                d_top = abs(ball.bottom - block.top)
                d_left = abs(block.left - ball.right)
                d_right = abs(ball.left - block.right)
                d_bottom = abs(block.bottom - ball.top)

                #Check top of block
                if d_top < d_left and d_top < d_right:
                    if y_speed >= 0:
                        if ball.bottom >= block.top and ball.top < block.bottom and ball.right >= block.left and ball.left <= block.right:
                            ball.bottom = block.top
                            if int(y_speed) != 0:
                                y_speed = int(y_speed*-0.34)
                                x_speed = int(x_speed*0.8)
                            else:
                                x_speed *= 0.95
                            air = False
                            if block.code == "X":
                                ball.top -= 35

                #Check bottom of block             
                if d_bottom < d_left and d_bottom < d_right:
                    if y_speed < 0:
                        if ball.top <= block.bottom and ball.bottom > block.top and ball.right > block.left and ball.left < block.right:
                            ball.top = block.bottom
                            y_speed *= -1

                #Check left side of block
                if check_side("left",block) == True:
                    ball.right = block.left
                    x_speed = changeAbs(x_speed,min(abs(x_speed)*0.5,2))*-1
                        
                #Check right side of block
                if check_side("right",block) == True:
                    ball.left = block.right
                    x_speed = changeAbs(x_speed,min(abs(x_speed)*0.5,2))*-1
                    
        #Change yspeed in the air
        if ball.bottom != lheight and air == True:
            y_speed = y_speed+slowdown

    #Handle the ball going in the hole
    if game_state in ["moving","aiming"]:
        if ball.left >= x_hole and ball.left <= x_hole + 21 and y_hole+35 > ball.bottom >= y_hole:
            x_speed = 0
            y_speed = 0
            if current_level == len(levels)-1:
                game_state = "win"
            else:
                game_state = "hole"
                
                #Calculate the name of score in comparison to par
                partext = ""
                if strokes == 1:
                    partext = "Hole In One"
                else:
                    for code in par_codes:
                        if code[0] == strokes - par:
                            partext = code[1]
                            break
                if partext == "":
                    if strokes - par < 0:
                        partext= str(-1*(strokes-par))+"  Under Par"
                    else:
                        partext= str(strokes - par)+"  Over Par"
                #Set text for end of the level
                wintexttop = bigwinfont.render(partext+"!",1,black)
                wintextmiddle = winfont.render("Level: "+str(levelnum)+"    Strokes: "+str(strokes)+"    Par: "+str(par),1,black)
                wintextbottom = winfont.render("Total Strokes:   "+str(score+strokes),1,black)
            #Reset strokes and set total score
            score += strokes
            strokes = 0

    #Move the ball into the hole     
    if game_state == "hole":
        ball.y += 1
    
    #Calculate the position of the arrow (after rotation)
    final_arrow = pygame.transform.rotate(img_arrow, angle_rotation)
    arrow.top = int(ball.top + img_ball.get_height()/2 - final_arrow.get_height()/2)
    arrow.left = int(ball.left + img_ball.get_width()/2 - final_arrow.get_width()/2)

    #Create, move, and delete clouds on the menus      
    if game_state in ["menu","win","instructions"]:
        if random.randint(1,17) == 1:
            clouds.append(Cloud())
        for c in clouds:
            c.x -= c.speed
            if c.x + int(c.size*1.3) <= 0:
                clouds.remove(c)
                
    #Button checking

    #Back to menu from win screen
    if game_state == "win":
        if buttons[6].click == True:
            game_state = "menu"
            mouse_click = False

    #Menu buttons            
    if game_state == "menu":
        #New game
        if buttons[3].click == True:
            game_state = "aiming"
            current_level = 0
            strokes = 0
            img_arrow = pygame.image.load("Ball/img_arrow.png").convert_alpha()
            lwidth = levels[0].width
            par = levels[0].par
            tileset = levels[0].tileset
            levelnum = levels[0].num
            x_hole = levels[0].x_hole
            y_hole = levels[0].y_hole
            background = pygame.image.load(levels[current_level].tileset+"/background.png").convert_alpha()
            shot_text = font.render("Strokes: "+str(strokes)+"    Par:  "+str(par),1,black)
            blocks, ball.x, ball.bottom = get_level(0)
            score = 0
        #Continue Game
        elif buttons[2].click == True and 0 <= current_level < len(levels)-1:
            strokes = 0
            current_level += 1
            lwidth = levels[current_level].width
            par = levels[current_level].par
            tileset = levels[current_level].tileset
            levelnum = levels[current_level].num
            x_hole = levels[current_level].x_hole
            y_hole = levels[current_level].y_hole
            background = pygame.image.load(levels[current_level].tileset+"/background.png").convert_alpha()
            img_arrow = pygame.image.load("Ball/img_arrow.png").convert_alpha()
            blocks, ball.x, ball.bottom = get_level(current_level)
            game_state = "aiming"
            shot_text = font.render("Strokes: "+str(strokes)+"    Par:  "+str(par),1,black)
        #Quit Game
        elif buttons[5].click == True:
            pygame.quit()
            sys.exit()
        #View Instructions
        elif buttons[4].click == True:
            game_state = "instructions"

    #Instructiosn back to main menu
    if game_state == "instructions":
        if buttons[7].click == True:
            game_state = "menu"
            
    if game_state == "hole":
        #Next Level
        if buttons[0].click == True:
            strokes = 0
            current_level += 1
            lwidth = levels[current_level].width
            par = levels[current_level].par
            tileset = levels[current_level].tileset
            levelnum = levels[current_level].num
            x_hole = levels[current_level].x_hole
            y_hole = levels[current_level].y_hole
            background = pygame.image.load(levels[current_level].tileset+"/background.png").convert_alpha()
            img_arrow = pygame.image.load("Ball/img_arrow.png").convert_alpha()
            blocks, ball.x, ball.bottom = get_level(current_level)
            game_state = "aiming"
            shot_text = font.render("Strokes: "+str(strokes)+"    Par:  "+str(par),1,black)
        #Back to Main Menu
        if buttons[1].click == True:
            game_state = "menu"
            mouse_click = False
            
    #Draw game elements

    #Draw menu clouds
    if game_state in ["menu","win","instructions"]:
        screen.blit(img_sky, (0,0))
        for c in clouds:
            screen.blit(c.img, (c.x, c.y))

    #Draw game logo on main menu      
    if game_state == "menu":
        centre(logo, width/2, 80)

    #Draw the elements of the win screen
    if game_state == "win":
        centre(img_congratulations, width/2, 75)
        screen.blit(score_background, (0,38))
        centre(bigwinfont.render("Final Score:  "+str(score),1,black), width/2, 270)

    #Draw instructions
    elif game_state == "instructions":
        centre(img_a, width/2-75, 100)
        centre(img_d, width/2+75, 100)
        centre(img_left, width/2-75, 250)
        centre(img_right, width/2+75, 250)
        centre(img_spacebar, width/2, 420)
        centre(bigfont.render("Aim Ball",1,black), width/2, 25)
        centre(font.render("+",1,black), width/2, 100)
        centre(font.render("OR",1,black), width/2, 175)
        centre(font.render("+",1,black), width/2, 250)
        centre(bigfont.render("Shoot / Select Power",1,black), width/2, 340)

    #Draw course elements (Ajusted for camera)     
    elif game_state in ["power","aiming","moving","hole"]:
        screen.blit(background, (0-x_camera*1.1,0))
        #All blocks and tiles
        for block in blocks:
            if block.img != False:
                screen.blit(block.img,(block.left-x_camera,block.top))
        #Hole
        screen.blit(img_hole, (x_hole+7-x_camera,y_hole-1))
        screen.blit(img_pole, (x_hole-x_camera+14,y_hole-35))
        screen.blit(img_flag, (x_hole-x_camera+14,y_hole-70))

    #Draw ball/arrow and other stationary level aspects
    if game_state in ["power","aiming","moving"]:   
        drawBall()
        #Arrow
        if game_state != "moving":
            screen.blit(final_arrow,(arrow.left-x_camera,arrow.top))
        #Score display
        screen.blit(score_paper, (0,0))
        screen.blit(shot_text, (12,10))
        
    #Draw info after a level is completed
    elif game_state == "hole":
        screen.blit(score_background, (0,0))
        centre(wintexttop, width/2, 190)
        centre(wintextmiddle, width/2, 250)
        centre(wintextbottom, width/2, 310)

    #Draw buttons if they are in the current game state
    for bt in buttons:
        bt.draw_button()

    pygame.display.flip()

