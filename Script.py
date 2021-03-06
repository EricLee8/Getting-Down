import pygame
import sys
import time
import random
import string
from pygame.locals import *
from pygame import font
from collections import deque
pygame.init()

#initialize parameters
ball_speed = 2#下降速度
lrspeed = 4 #左右移动速度
block_speed = 2#上升速度
level = 1
life = 3
score = 0
game_over = True
first_start = True

#basic set:
#resolution
bgsize = width, height = 520, 510
pygame.display.set_mode(bgsize)
#title!
pygame.display.set_caption('Getting down！')
#b&color
bg = (0,0,0)
ball_image = pygame.image.load('images/ball1.png')
score_file_const = open('data/Highest_Score.txt','r')
highest_score = int(score_file_const.read())
score_file_const.close()
user_file_const = open('data/name.txt','r')
name = user_file_const.read()
user_file_const.close()
background = pygame.image.load('images/background.jpg')

#Surface
screen = pygame.display.get_surface()
#color set
white = 255,255,255 #rgb
red = 255,0,0#for the block that adds a life
yellow = 230,230,50
blue = 0,0,255
light_orange = 255,165,0 #for dangerous block(which decreases life)
green = 0,255,0 #for the block that will crack
cyan2 = 0,238,238
Aquamarine1 = 127,255,152
gold = 255,215,0

#tool functions:
#打印文本内容的工具函数
def print_text(font,x,y,text,color=(255,255,255)):
	imgText = font.render(text,True,color) # 创建字体，三个参数是文本.抗锯齿.颜色
	screen.blit(imgText,(x,y)) #built screen 创建文本窗口
#升级的函数
def level_up(ball):
    global level,ball_speed,block_speed,lrspeed
    level += 1
    ball_speed += 0.5
    block_speed += 0.5
    ball.speed += 0.5
    lrspeed += 0.25
#判断落是否落在板子上以及板子是什么颜色并做出相应操作的函数：
def is_inboard(ball_1,que):
    global life, score
    for rec in que:
        #如果小球在挡板上
        #这语句里面的一些参数是为了判据更准确而一次次试出来的的，不然可能会出现穿模现象
        if (ball.rect.y+D>=rec.y-2 and ball.rect.y+D<=rec.y+12) and (ball.rect.x+D>=rec.x and ball.rect.x<=rec.x+rec.size[0]):
            if rec.color == green:
                score += 200
                que.remove(rec)
            elif rec.color == red:
                rec.color = white
                life += 1
            elif rec.color == light_orange:
                rec.color = white
                life -= 1
            return True
    return False
#copied codes
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass
def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.SysFont('arial',18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 10,
                    (screen.get_height() / 2) - 10,
                    500,500), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 150,
                    (screen.get_height() / 2) - 10,
                    380,50), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()
def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + str(current_string))
  real_string = ''
  while 1:
    inkey = get_key()
    print(inkey)
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + ''.join(current_string)) #list 转化为 string
  return ''.join(current_string)

#class Ball
D = ball_image.get_height()
class Ball(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        #size & speed
        self.speed = speed
        self.image = ball_image
        #position:
        self.rect = self.image.get_rect()
        self.rect.y = 50
        self.rect.x = random.randint(200,300)

    def movedown(self):
        self.rect.y += self.speed
    def moveup(self):
        self.rect.y -= (block_speed)
    def moveleft(self):
        self.rect.x -= lrspeed
    def moveright(self):
        self.rect.x += lrspeed

#class rectangle:
#v1.2，增加了不同种的障碍物（通过随机数随机生成）
class rectangle:
    def __init__(self,pos_y=530):
        self.size = (random.randint(40,140),10)
        self.x = random.randint(50,350)
        self.y = pos_y
        self.type = random.randint(0,level+18)  #3+18=21>20，即第3级开始出现不同的障碍物
        if self.type<=20 or self.type>23: #normal
            self.color = white
        elif self.type == 21: #for adding life
            self.color = red
        elif self.type == 22: #for cracking
            self.color = green
        elif self.type == 23: #for decresing life
            self.color = light_orange
    def move(self):
        self.y -= block_speed


#实例化Clock()对象
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()
#初始化一个小球：
ball = Ball(ball_speed)
#初始化障碍物队列
q_block = deque([rectangle(300)])
q_block.append(rectangle())
#初始化默认字体和字体大小：
font1 = pygame.font.SysFont('arial',24)
font2 = pygame.font.SysFont('arial',60)
font3 = pygame.font.SysFont('arial',42)
font4 = pygame.font.SysFont('arial',36)
font5 = pygame.font.SysFont('arial',48)

#main process
while True:
    #get the event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:  #鼠标抬起(是从压下状态下抬起的意思，即一个click可以触发此事件)
            if game_over:
                game_over = False
                ball_speed = 1.5  # 下降速度
                lrspeed = 3.5  # 左右移动速度
                block_speed = 1.5  # 上升速度
                level = 1
                life = 3
                score = 0
                ball = Ball(ball_speed)

    #How to start the game
    if game_over:
        if first_start:
            print_text(font5,103,50,'GETTING DOWN!',cyan2)
            print_text(font4,42,130,'Remember, red is the color of life!',red)
            print_text(font4,42,180,'And orange is the color of danger!',light_orange)
            print_text(font4,29,230,'Also, green is the color of weakness!',green)
            print_text(font4, 120, 280, 'Maybe forgiveness?(x', green)
            print_text(font2,118,370,'Click to play!',white)
            clock.tick(60)
            pygame.display.flip()
            screen.blit(background,(0,0))
            continue
        else:
            screen.blit(background, (0, 0))
            q_block.clear()  #清空障碍物
            q_block.append(rectangle())
            print_text(font3,122,250,'Your score is: '+str(score),gold)
            print_text(font2, 130, 60, 'Game Over!', cyan2)
            print_text(font2, 45, 136, 'Click to play again!', cyan2)
            print_text(font3,151,340,'Highest Score:',Aquamarine1)
            print_text(font3,168,405,name+':  '+str(highest_score),Aquamarine1)
            clock.tick(60)
            pygame.display.flip()
            continue

    #生成及删除越界障碍物矩形
    #v1.2添加不同种的障碍物，在rectangle类的构造函数完成
    if q_block[len(q_block)-1].y<random.randint(270,400):
        q_block.append(rectangle()) #生成
    if q_block[0].y<0:
        q_block.popleft() #删除(为了节省空间并提高运行效率)
    for rec in q_block:
        rec.move() #移动障碍物

    #get key action:
    # 此函数用来取得所有键盘的状态，返回一个dict，键值为键盘名，值为True or False
    key_press = pygame.key.get_pressed()

    #处理小球、矩形的移动
    #判断小球是向上还是向下
    #v1.2判断小球落在的矩形是什么颜色并且做出相应行动
    if is_inboard(ball,q_block): #在板子上
        ball.moveup()
    else:
        ball.movedown()
    #判断小球是向左走还是向右走
    if key_press[K_LEFT] and ball.rect.x>10:
        ball.moveleft()
    elif key_press[K_RIGHT] and ball.rect.x+D<510:
        ball.moveright()

    #处理何时减少生命值、结束游戏：
    if ball.rect.y<0 or ball.rect.y>510:
        life -= 1
        ball = Ball(ball_speed)
    if life == 0:
        game_over = True
        first_start = False
        if score>highest_score:
            screen.fill((0,0,0))
            name = ask(screen, 'Please enter your name\n(English ONLY)')
            name_file = open('data/name.txt', 'w')
            name_file.write(name)
            name_file.close()
            highest_score = score
            score_file = open('data/Highest_Score.txt', 'w')
            score_file.write(str(score))
            score_file.close()
        continue

    #得分和升级
    score += 1
    if score%1000==0:
        level_up(ball)

    #fill the background
    screen.fill(bg)
    # set boundary
    pygame.draw.rect(screen, blue, (0, 0, 10, 510), 0)
    pygame.draw.rect(screen, blue, (510, 0, 10, 510), 0)
    pygame.draw.rect(screen, blue, (10, 0, 500, 10), 0)

    #很重要！！！！！！画面显示代码：
    screen.blit(background,(0,0))
    screen.blit(ball_image, ball.rect)
    for rec in q_block:
        pygame.draw.rect(screen,rec.color,(rec.x,rec.y,rec.size[0],rec.size[1]),0)
    print_text(font1,10,0,'Score:'+str(score),white)
    print_text(font1,220,0,'Level:'+str(level),white)
    print_text(font1,453,0,'Life:'+str(life),white)

    clock.tick(60)#每秒不超过x帧，即不超过x次图像处理（重新刷新）
    #将完整的显示更新到屏幕
    pygame.display.flip()
