import pyautogui
import time
import win32gui
from control import *
from dectector import *
import sys
from scrcpy import *

'''
畫面位置偵測 首頁 道具背包 道館 道館寶可夢 團體戰道館 
進到要守的道館後=>啟動=>檢查血量

'''
scrcpy = Scrcpy()
scrcpy.start()
notFoundCount = 0
winControler = WindowControl()#"SM-A5260"
mouseControler = MouseControl()
winControler.bring_window_to_front()

while True:
    winControler.bring_window_to_front()
    img = winControler.background_screenshot()
    _,bboxes = health(img)
    berry_amount = berry(img)
    if berry_amount == None:
        notFoundCount += 1
    else:
        notFoundCount = 1 if notFoundCount > 1 else 0
    print("berries:",berry_amount)

    if notFoundCount > 3 and len(bboxes) >1:
        print("道館")
        mouseControler.intoPKM()
        time.sleep(0.3)
        continue
    elif notFoundCount > 3 and len(bboxes) == 1:
        print("太遠了")
        time.sleep(0.3)
        continue
    elif notFoundCount == 0 and len(bboxes) == 1:
        print("道館寶可夢")
    else:
        print("???")
        time.sleep(0.3)
        continue

    
    for b in bboxes:
        cv2.rectangle(img, (b[0], b[1]), (b[2], b[3]), (0, 0, 0), 2)
        print("health:",b[-1])
        if b[-1] <0.5:
            print("Feeding")
            mouseControler.feedPKM()

    mouseControler.dragPKM()
    #cv2.imshow('img',cv2.resize(img,None,fx=0.7,fy=0.7))
    #cv2.imwrite('screenshot.png',img)
    
