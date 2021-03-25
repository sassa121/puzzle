from enum import IntEnum
import random
import cv2
import numpy as np
from time import sleep
from pygame import mixer


"""
from kbhit import *
atexit.register(set_normal_term)
set_curses_term()
"""
"""
from PIL import Image

im = Image.open("./image.jpg")
# 画像読み込み

im_crop = im.crop((0, 0, 41, 41))
im_crop.save('./reddrop.jpg')
im_crop = im.crop((164, 0, 205, 41))
im_crop.save('./bluedrop.jpg')
im_crop = im.crop((41, 41, 82, 82))
im_crop.save('./greendrop.jpg')
im_crop = im.crop((123, 41, 164, 82))
im_crop.save('./yellowdrop.jpg')
im_crop = im.crop((0, 82, 41, 123))
im_crop.save('./purpledrop.jpg')
im_crop = im.crop((164, 82, 205, 123))
im_crop.save('./pinkdrop.jpg')
# img[top : bottom, left : right]

"""
DROP_times = 1.2
im_RED = cv2.imread("./images/reddrop.png")
im_GREEN = cv2.imread("./images/greendrop.png")
im_BLUE = cv2.imread("./images/bluedrop.png")
im_PURPLE = cv2.imread("./images/purpledrop.png")
im_YELLOW = cv2.imread("./images/yellowdrop.png")
im_PINK = cv2.imread("./images/pinkdrop.png")
im_NONE = cv2.imread("./images/nonedrop.png")
im_BACK = cv2.imread("./images/back6.png")
im_CHARA = cv2.imread("./images/183.png")
"""
im_RED2 = cv2.imread("./images/reddrop2.png")
im_GREEN2 = cv2.imread("./images/greendrop2.png")
im_BLUE2 = cv2.imread("./images/bluedrop2.png")
im_PURPLE2 = cv2.imread("./images/purpledrop2.png")
im_YELLOW2 = cv2.imread("./images/yellowdrop2.png")
im_PINK2 = cv2.imread("./images/pinkdrop2.png")
"""

def highlight(img, alpha=1.5, beta=0.0):
        # 積和演算を行う。
    dst = alpha * img + beta
    # [0, 255] でクリップし、uint8 型にする。
    return np.clip(dst, 0, 255).astype(np.uint8)
def scale_to_width(img, width):
    """幅が指定した値になるように、アスペクト比を固定して、リサイズする。
    """
    h, w = img.shape[:2]
    height = round(h * (width / w))
    dst = cv2.resize(img, dsize=(width, height))

    return dst



im_RED2 = highlight(im_RED)
im_GREEN2 = highlight(im_GREEN)
im_BLUE2 = highlight(im_BLUE)
im_YELLOW2 = highlight(im_YELLOW)
im_PURPLE2 = highlight(im_PURPLE)
im_PINK2 = highlight(im_PINK)



BOARD_WIDTH = 7
BOARD_HEIGHT = 6
DROP_SIZE = 41
ERASE_CHAIN_COUNT = 3
combo=0
cursorX=0
cursorY=0
im_BACK = scale_to_width(im_BACK, BOARD_WIDTH*DROP_SIZE)
#im_BACK = cv2.resize(im_BACK,(BOARD_WIDTH*DROP_SIZE,BOARD_HEIGHT*DROP_SIZE))
im_RED = cv2.resize(im_RED,(DROP_SIZE,DROP_SIZE))
im_BLUE = cv2.resize(im_BLUE,(DROP_SIZE,DROP_SIZE))
im_GREEN = cv2.resize(im_GREEN,(DROP_SIZE,DROP_SIZE))
im_YELLOW = cv2.resize(im_YELLOW,(DROP_SIZE,DROP_SIZE))
im_PURPLE = cv2.resize(im_PURPLE,(DROP_SIZE,DROP_SIZE))
im_PINK = cv2.resize(im_PINK,(DROP_SIZE,DROP_SIZE))
im_CHARA = cv2.resize(im_CHARA,(DROP_SIZE,DROP_SIZE))
colorlist = [im_RED,im_BLUE,im_GREEN,im_YELLOW ,im_PURPLE, im_PINK,im_CHARA]
colorlist2 = [im_RED2,im_BLUE2,im_GREEN2,im_YELLOW2 ,im_PURPLE2, im_PINK2]
holding = False
finished = False
light = False
class Color(IntEnum):
    NONE = -1
    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3
    PURPLE = 4
    PINK = 5
    MAX = 6
class Direction(IntEnum):
    DIRECTION_RIGHT = 0
    DIRECTION_DOWN = 1
    DIRECTION_MAX = 2
print(im_NONE)
board = np.zeros((BOARD_HEIGHT,BOARD_WIDTH))
#checked = np.zeros((BOARD_HEIGHT,BOARD_WIDTH))
#toErase = np.zeros_like(board, dtype=np.bool)

for i in range(BOARD_HEIGHT):
    for j in range(BOARD_WIDTH):
        board[i][j] = random.randrange(0,int(Color.MAX))

board=[[1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1]
]
fall = np.zeros_like(board, dtype=np.bool)

def combosound():        
    mixer.init()  
         #初期化
    if combo <= 38:
        mixer.music.load("./sound/se_006p0"+ str(combo).zfill(2)+".ogg")
    else:
        mixer.music.load("./sound/se_006p039.ogg")
    mixer.music.play(1)
    
    """
    sounds = []
    sounds.append(mixer.Sound("./sound/se_006p001.ogg"))
    sounds.append(mixer.Sound("./sound/se_006p002.ogg"))
    for sound in sounds:
        sound.play()
    #同時に鳴らすとき
    """

def puzzlesound():        
    mixer.init()  
    mixer.music.load("./sound/se_004.ogg")
    mixer.music.play(1)
def checkChain ( _i, _j,toErase,checked,board,color):
    
    if(_i<0 or _i>=BOARD_HEIGHT or _j<0 or _j>=BOARD_WIDTH or checked[_i][_j]==1 or toErase[_i][_j]==False or board[_i][_j]!=color or board[_i][_j]==int(Color.NONE)):
        pass
        
    
    else:
        
        checked[_i][_j]=1
        checkChain( _i-1, _j,toErase,checked,board,color)
        checkChain( _i+1, _j,toErase,checked,board,color)
        checkChain( _i, _j-1,toErase,checked,board,color)
        checkChain( _i, _j+1,toErase,checked,board,color)
    
def eraseconnectDrops(checked):
    global combo 
    for i in range(4):
        draw(40)
    for i in range (BOARD_HEIGHT):
        for j in range (BOARD_WIDTH):  
            if checked[i][j]== 1:
                board[i][j]= int(Color.NONE)
    combo += 1
    combosound()
    for i in range(5):
        draw(40)
    
    

def eraseDrops():
    global light
    light = False
    toErase = np.zeros_like(board, dtype=np.bool)
    for i in range (BOARD_HEIGHT-ERASE_CHAIN_COUNT+1):
        for j in range (BOARD_WIDTH):
            for n in range(1,ERASE_CHAIN_COUNT):
                
                if board[i][j] != board[i+n][j] :
                    break
                if n==ERASE_CHAIN_COUNT-1:
                    toErase[i:i+ERASE_CHAIN_COUNT,j:j+1]=True
                    
                  
    for i in range (BOARD_HEIGHT):
        for j in range (BOARD_WIDTH-ERASE_CHAIN_COUNT+1):           
            for n in range(1,ERASE_CHAIN_COUNT):
                if board[i][j] != board[i][j+n]:
                    break
                if n==ERASE_CHAIN_COUNT-1:
                    toErase[i:i+1,j:j+ERASE_CHAIN_COUNT]=True
    #print(toErase)
    checked = np.zeros((BOARD_HEIGHT,BOARD_WIDTH))
    
    for i in reversed(range(BOARD_HEIGHT)):
        for j in range (BOARD_WIDTH):  
            if checked[i][j]==0 and toErase[i][j]==True:
                checkChain(i,j,toErase,checked,board,board[i][j])
                eraseconnectDrops(checked)
                
            
 


def draw(time,frame_num = 0):          


    boardpixel = np.zeros((BOARD_HEIGHT*DROP_SIZE,BOARD_WIDTH*DROP_SIZE,3), dtype=np.uint8)
    boardpixel[:,:,:] = im_NONE[0,0,:]
    for i in range (BOARD_HEIGHT):
        for j in range (BOARD_WIDTH):
            
            if board[i][j]>= 0 and fall[i][j]== True:
                if  i*DROP_SIZE-int(frame_num*DROP_SIZE)>=0:
                    boardpixel[i*DROP_SIZE-int(frame_num*DROP_SIZE):(i+1)*DROP_SIZE-int(frame_num*DROP_SIZE),j*DROP_SIZE:(j+1)*DROP_SIZE] =  colorlist[board[i][j]]
                else:        
                    boardpixel[0:(i+1)*DROP_SIZE-int(frame_num*DROP_SIZE),j*DROP_SIZE:(j+1)*DROP_SIZE] =  colorlist[board[i][j]][int(frame_num*DROP_SIZE):DROP_SIZE]
            elif board[i][j]>= 0 and fall[i][j]== False:
                boardpixel[i*DROP_SIZE:(i+1)*DROP_SIZE,j*DROP_SIZE:(j+1)*DROP_SIZE] =  colorlist[board[i][j]]
    #持っているドロップ色変更
    global light
    if cursorY>=0 and cursorY<BOARD_HEIGHT and cursorX>=0 and cursorX<BOARD_WIDTH and light == True:
        boardpixel[cursorY*DROP_SIZE:(cursorY+1)*DROP_SIZE,cursorX*DROP_SIZE:(cursorX+1)*DROP_SIZE] =  colorlist2[board[cursorY][cursorX]]
        
    #盤面を描画
    boardpixel = np.vstack([im_BACK,boardpixel])
        
    #cv2.imwrite("board.png",boardpixel)
    cv2.namedWindow("result")
    #img = cv2.imread("./board.png")
    #boardpixel= cv2.resize(boardpixel,(450,750))
    boardpixel = scale_to_width(boardpixel, 450)
    #img = cv2.resize(boardpixel, dsize=None, fx=1, fy=1)
    if combo >= 2:
        cv2.putText(boardpixel, 'Combo {}'.format(combo), (60, 180), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), thickness=15)
        cv2.putText(boardpixel, 'Combo {}'.format(combo), (60, 180), cv2.FONT_HERSHEY_SIMPLEX, 2.0, ( random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)), thickness=8)
    cv2.imshow("result",boardpixel)
    
    cv2.waitKey(time)
    #sleep(5)
    #cv2.destroyWindow("result")

def fallDrops():
    global fall 
    global combo
    flag = True
    while flag == True:
        flag = False
        fall = np.zeros_like(board, dtype=np.bool)
        for i in range (BOARD_HEIGHT-2,-1,-1):
            for j in range (BOARD_WIDTH):
                if board[i][j] != int(Color.NONE) and board[i+1][j] == int(Color.NONE):
                    board[i+1][j] = board[i][j] 
                    board[i][j] = int(Color.NONE)
                    fall[i+1][j] = True
                    
                    
        for j in range (BOARD_WIDTH):
            if board[0][j] == int(Color.NONE):
                if combo==49:
                    board[0][j] = 6
                else:
                    #board[0][j] =  random.randrange(0,int(Color.MAX))
                    board[0][j] = int(Color.BLUE)
                flag = True
                fall[0][j] = True
                
                
        if flag == True:   
         
            global finished
            finished = False
        
            for i in range(5):     
                draw(6,(4-i)*0.2)#40
def puzzle():
    global light
    light = True
    done = False
    while True:
        
        global cursorX,cursorY,holding
        
        key = cv2.waitKey(0)
        lastcursorY = cursorY
        lastcursorX = cursorX
        
        if cursorY > 0 and key == 119:#上w
            cursorY-=1
        elif cursorX > 0 and key == 97:#左a
            cursorX-=1
        elif cursorY < BOARD_HEIGHT-1 and key == 115:#下s
            cursorY+=1
        elif cursorX < BOARD_WIDTH-1 and key == 100:#右d
            cursorX+=1
        elif key == 13:
            holding =not holding
        if holding == True:
            temp = board[cursorY][cursorX]
            board[cursorY][cursorX] = board[lastcursorY][lastcursorX]
            board[lastcursorY][lastcursorX] = temp
            puzzlesound()
            if  cursorY!=lastcursorY or cursorX!=lastcursorX:
                done = True
                

        draw(10)
        if done == True and holding == False:
            break


if __name__ == "__main__":
    
    draw(10)
    while True:
        
        puzzle()
        while True:
            finished = True
            eraseDrops()
            fallDrops()
            if finished == True:
                combo = 0
                break

   
   
