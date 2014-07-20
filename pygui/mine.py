#!/usr/bin/env python
import pygame
import random
from os import _exit as exit
import autopy
SCREEN_SIZE=((500,380),(380,480),(520,520),(830,600))
global Mine,Total
Total=10
POS_x,POS_y=30,100
SOUND={}
def load():
    pygame.mixer.music.load(r"data/sound/bg.mp3")
    pygame.mixer.music.play(-1)                     #play background music
    for i in ('menu','bom','sucess','failed'):
        SOUND[i]=pygame.mixer.Sound(r"data/sound/"+i+'.org')
def play_sound(name):
    try:
        SOUND[name].play()
    except:
        pass
pygame.init()                                           #初始化pygame为使用硬件做准备
pygame.display.set_mode(SCREEN_SIZE[1])                 #必须使用这句，否则ImageDict无法初始化
ImageDict = {}
ImageDict['bgphoto']  = pygame.image.load('data/image/bg.jpg').convert()
ImageDict['button_0'] = pygame.image.load('data/image/button_0.png').convert_alpha()
ImageDict['button_1'] = pygame.image.load('data/image/button_1.png').convert_alpha()
ImageDict['button_2'] = pygame.image.load('data/image/button_2.png').convert_alpha()
ImageDict['face_0'] = pygame.image.load('data/image/face_0.jpg').convert_alpha()
ImageDict['face_1'] = pygame.image.load('data/image/face_1.jpg').convert_alpha()
ImageDict['face_2'] = pygame.image.load('data/image/face_2.jpg').convert_alpha()
ImageDict['mine_0'] = pygame.image.load('data/image/mine_0.png').convert_alpha()
ImageDict['mine_1'] = pygame.image.load('data/image/mine_1.png').convert_alpha()
ImageDict['mark_0'] = pygame.image.load('data/image/mark_0.png').convert_alpha()
ImageDict['mark_1'] = pygame.image.load('data/image/mark_1.png').convert_alpha()
logo_photo          = pygame.image.load('data/image/logo.png').convert_alpha()
pygame.display.set_icon(logo_photo)
class WrapMine:
    '''
		初始化一个窗口
    '''
    def __init__(self,s,flag=None,t=None):
        global size
        self.t=t
        size=s
        self.Mine,self.Total=0,0
        self.screen = pygame.display.set_mode(SCREEN_SIZE[size],0,32)     #创建窗口
        pygame.display.set_caption("WrapMine v0.0.2")               #设置窗口标题
        self.screen.fill((255,255,255))                             #填充背景为白色
        self.screen.blit(ImageDict['face_0'],(SCREEN_SIZE[size][0]/2-30,30))#把开始的图片载入
        self._init(flag)
    def _init(self,flag):
        global size
        self.matrix=[]
        for i in range(size+9):
            for j in range(int(size**2.5)+9):
                self.screen.blit(ImageDict['button_0'],(POS_x+j*32,POS_y+32*i))#10行10
        if flag and size==1:#仅仅支持Level 1的初始化
            self.matrix=[[[1,0],[1,0],[1,0],[0,0],[0,0],[1,0],[0,0],[1,0],[0,0],[0,0]],                     #1
                         [[0,0],[1,0],[0,0],[0,0],[1,0],[0,0],[1,0],[0,0],[1,0],[0,0]],                     #2
                         [[0,0],[1,0],[0,0],[0,0],[1,0],[0,0],[0,0],[0,0],[1,0],[0,0]],                     #3
                         [[1,0],[1,0],[1,0],[0,0],[0,0],[1,0],[0,0],[1,0],[0,0],[0,0]],                     #4
                         [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[1,0],[0,0],[0,0],[0,0]],                     #5
                         [[0,0],[0,0],[0,0],[1,0],[0,0],[1,0],[0,0],[0,0],[0,0],[0,0]],                     #6
                         [[0,0],[0,0],[0,0],[1,0],[0,0],[1,0],[0,0],[0,0],[0,0],[0,0]],                     #7
                         [[0,0],[0,0],[0,0],[1,0],[0,0],[1,0],[0,0],[0,0],[0,0],[0,0]],                     #8
                         [[0,0],[0,0],[0,0],[0,0],[1,0],[0,0],[0,0],[0,0],[0,0],[0,0]],                     #9
                         [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],                     #10
                         ]
            self.Total=25    #地雷数量
        else:
            for i in range(size+9):
                a=[]
                for j in range(int(size**2.5+9)):
                    a.append([0,0])
                self.matrix.append(a)
            for i in range(size*10*5/3):
                x=random.randint(0,int(size**2.5)+8)
                y=random.randint(0,size+8)
                self.matrix[y][x][0]=1
            self.Total=size*10*5/3
        self.font        =  pygame.font.SysFont("arial", 16)                #初始化字体为16号，Aril字体
        self.font_height =  self.font.get_linesize()
        text=self.font.render("Flags:%d/%d           By-shellvon"%(self.Mine,self.Total),True,(0,0,0),(255,255,255))
        self.screen.blit(text,(POS_x,SCREEN_SIZE[size][1]-50))#将text载入窗口，坐标在左下角
    def recushow(self,row,col):
        '''
            递归show
        '''
        pass
            
        
    def set_know(self,row,col):
        '''
            知道
        '''
        global size
        if -1<row<size+9 and -1<col<int(size**2.5+9):
            if self.matrix[row][col][0]==1:
                self.screen.blit(ImageDict['mine_1'],(POS_x+col*32,POS_y+row*32))
                pygame.display.update(pygame.rect.Rect((POS_x+col*32, POS_y+row*32), (32,32)))
            else:
                self.screen.blit(ImageDict['button_1'],(POS_x+col*32,POS_y+row*32))
                pygame.display.update(pygame.rect.Rect((POS_x+col*32, POS_y+row*32), (32,32)))
                self.matrix[row][col][1]=-1         #打开后
                n = self.checkAll(row,col)
                if n!=0:
                    text = self.font.render(str(n),True,(0,0,0),(255,255,255))#更改左下角显示的文字
                    self.screen.blit(text,(POS_x+col*32+10, POS_y+row*32+5))
                    pygame.display.update(pygame.rect.Rect((POS_x+col*32+10, POS_y+row*32+5), (32,32)))
         
    
    def fail(self):
        """
			游戏已经结束
        """
        global size
        self.screen.blit(ImageDict['face_1'],(SCREEN_SIZE[size][0]/2-30,30))#载入游戏失败时候的哭脸
        #打印出所有地雷位置
        for row in range(size+9):
            for col in range(int(size**2.5+9)):
                if self.matrix[row][col][0]==1:#是地雷
                    if self.matrix[row][col][1]==1:#标记过
                        self.screen.blit(ImageDict['mark_0'],(POS_x+col*32, POS_y+row*32))
                    else:
                        self.screen.blit(ImageDict['mine_0'],(POS_x+col*32, POS_y+row*32))
                     
                else:							#不是地雷
                    if self.matrix[row][col][1]==1:#标记过
                        self.screen.blit(ImageDict['mark_1'],(POS_x+col*32, POS_y+row*32))
                    else:
                        self.screen.blit(ImageDict['button_2'],(POS_x+col*32, POS_y+row*32))
        pygame.display.update()
        if size==1 and self.t:#如果选择的是1级而且是special的话。就会弹出俩个对话框
            autopy.alert.alert("Yes,I LOVE YOU",'Love','a','b')
            autopy.alert.alert("Do you love me? \nPlease choose the anwser")
        key=autopy.alert.alert("Want to again?",'Question','ok','cancel')
        if key:
            run()
        else:
            exit(0)

        
    def _check_one(self,row,col):
        """
            检查row行，col列。时候含有Mine。返回True or False
        """
        if -1<row<int(size+9) and -1<col<int(size**2.5+9):
            if self.matrix[row][col][0]==1:
                return True
        return False
    def checkAll(self,row,col):
        """
            统计row,col周围有多少个Mine
        """
        f=self._check_one
        return sum((f(row-1, col-1),f(row-1, col),f(row-1, col+1),f(row, col-1),f(row, col+1),f(row+1, col-1),f(row+1, col),f(row+1, col+1)))
    def run(self):
        global size
        pygame.display.update()
        self.count=0
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    exit(0)
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_ESCAPE:                      #如果按ESC键也可以退回
                        exit(0)
                if e.type==pygame.MOUSEBUTTONDOWN:                  #鼠标事件
                    press_mouse=pygame.mouse.get_pressed()          #返回一个三元组。表示鼠标左，中。右键的使用状态
                    if press_mouse[0]==1:                           #按住左键
                        pos_mouse=pygame.mouse.get_pos()            #获取鼠标位置
                        if POS_x<=pos_mouse[0]<=POS_x+int(size**2.5+9)*32 and POS_y<=pos_mouse[1]<=POS_y+(size+9)*32:#判断该位置时候合法
                            col = int((pos_mouse[0]-POS_x)/32)      #获得col
                            row = int((pos_mouse[1]-POS_y)/32)      #获得row
                            if self.matrix[row][col][0]==1:        #遇到地雷
                                self.fail()                         #游戏结束
                                self.set_know(row,col)
                                break
                            elif self.matrix[row][col][0]==0:       #如果不是地雷
                                #self.recushow(row,col)
                                self.set_know(row,col)

                               
                                                                    #递归调用打开周围
                    if press_mouse[2]==1:                           #鼠标右键状态
                        pos_mouse=pygame.mouse.get_pos()
                        if POS_x<=pos_mouse[0]<=POS_x+int(size**2.5+9)*32 and POS_y<=pos_mouse[1]<=POS_y+(size+9)*32:#判断该位置时候合法
                            col = int((pos_mouse[0]-POS_x)/32)      #获得col
                            row = int((pos_mouse[1]-POS_y)/32)      #获得row
                            if self.matrix[row][col][1]==0:         #如果是初始化状态
                                self.matrix[row][col][1]=1          #标记为已处理
                                self.Mine+=1                             #MineFlags+1
                                if self.matrix[row][col][0]==1:
                                    self.count+=1
                                    print self.count,'Chose'
                                self.screen.blit(ImageDict['mark_0'],(POS_x+col*32, POS_y+row*32))
                                pygame.display.update(pygame.rect.Rect((POS_x+col*32, POS_y+row*32), (32,32)))#局部更新
                                text = self.font.render('Score:'+str(self.Mine)+'/'+str(self.Total)+'   ',True,(0,0,0),(255,255,255))#更改左下角显示的文字
                                self.screen.blit(text,(POS_x,SCREEN_SIZE[size][1]-50))                                #填充文本
                                pygame.display.update()             #更新画面
                            elif self.matrix[row][col][1]==1:          #之前放过旗帜在这里
                                self.matrix[row][col][1]=0          #切换为初始状态
                                self.Mine-=1                             #用户取消这个MineFlags
                                if self.matrix[row][col][0]==1:
                                    self.count-=1
                                
                                self.screen.blit(ImageDict['button_0'],(POS_x+col*32, POS_y+row*32))
                                pygame.display.update(pygame.rect.Rect((POS_x+col*32, POS_y+row*32), (32,32)))#局部更新'''
                                text = self.font.render('Flags:'+str(self.Mine)+'/'+str(self.Total)+'   ',True,(0,0,0),(255,255,255))#更改左下角显示的文字
                                self.screen.blit(text,(POS_x,SCREEN_SIZE[size][1]-50))                                #填充文本
                                pygame.display.update()             #更新画面。否则的话，之前做的就没有效果了
                    if self.count==self.Total:
                        self.screen.blit(ImageDict['face_2'],(SCREEN_SIZE[size][0]/2-30,30))#载入游戏Success
                        pygame.display.update()
                        key=autopy.alert.alert("Want to again?",'Question','ok','cancel')
                        if key:
                            run()
                        else:
                            exit(0)
                        return

class Menu:
    _options=['Level1','Level2','Level3','Setting','exit']
    def __init__(self):
        load()
        self.screen = pygame.display.set_mode(SCREEN_SIZE[0],0,32)     #创建窗口
        pygame.display.set_caption("WrapMine v0.0.2")               #设置窗口标题
        self.screen.fill((255,255,255))#填充背景为白色
        self.screen.blit(ImageDict['bgphoto'],(0, 0))
        my_font=pygame.font.Font(r'data\font\default.ttf',32)
        text=my_font.render(u'Wrap Mine',True,(0,0,0),(255,255,255))
        self.screen.blit(text,(SCREEN_SIZE[0][1]/4-40,SCREEN_SIZE[0][0]/6))
        self.stat=0
    def _draw(self):
        pygame.font.init()
        my_font=pygame.font.Font(r'data\font\default.ttf',24)
        txt=('Level 1','Level 2','Level 3','Setting',' Quit  ')
        for i in range(5):
            if i==self.stat:
                t=my_font.render(txt[i],True,(0,20,255),(255,255,255))
                self.screen.blit(t,(SCREEN_SIZE[0][1]/4,SCREEN_SIZE[0][0]/5+40*(i+1)))
            else:
                t=my_font.render(txt[i],True,(0,0,0),(255,255,255))
                self.screen.blit(t,(SCREEN_SIZE[0][1]/4,SCREEN_SIZE[0][0]/5+40*(i+1)))
    def run(self):
        while 1:
            self._draw()
            pygame.display.update()
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    exit(0)
                elif e.type==pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.stat=(self.stat-1)%5
                        play_sound('menu')
                    elif e.key == pygame.K_DOWN:
                        self.stat=(self.stat+1)%5
                        play_sound('menu')
                    elif e.key == pygame.K_RETURN:
                        return self.stat#等级状态

def setting():
    music_volume=100
    my_font=pygame.font.Font(r'data\font\default.ttf',32)
    vol_font=pygame.font.Font(r'data\font\default.ttf',24)
    while 1:
        screen = pygame.display.set_mode(SCREEN_SIZE[0],0,32)     #创建窗口
        pygame.display.set_caption("WrapMine v0.0.2")               #设置窗口标题
        screen.fill((255,255,255))#填充背景为白色
        screen.blit(ImageDict['bgphoto'],(0, 0))
        text=my_font.render(u'Setting',True,(0,0,0),(255,255,255))
        screen.blit(text,(SCREEN_SIZE[0][1]/4-40,SCREEN_SIZE[0][0]/6))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                exit(0)
            if event.type == pygame.KEYDOWN:
                #通过上向键来控制音量
                if event.key == pygame.K_RETURN:
                    run()
                if event.key == pygame.K_UP:  
                    music_volume += 10  
                    if (music_volume > 100):  
                        music_volume = 0  
                if event.key == pygame.K_DOWN:  
                    music_volume -= 10  
                    if (music_volume < 0):
                        music_volume = 100
                pygame.mixer.music.set_volume(music_volume / 100.0)
        vol=vol_font.render(u'Now Volume：%s'%int(music_volume),True,(0,0,0),(255,255,255))
        screen.blit(vol,(SCREEN_SIZE[0][1]/4-40,SCREEN_SIZE[0][0]/3))
        pygame.display.update()
    
def run():
    a=Menu()
    while 1:
        x=a.run()
        if x==0 or x==1 or x==2:
            t=0
            if x==0:
                t=autopy.alert.alert(u'Choose Special?','?','yes','no')
            if t:
                m=WrapMine(x+1,1,t)
            else:
                m=WrapMine(x+1)
            m.run()
        if x==3:
            #setting
            setting()
        if x==4:
            exit(0)
run()
