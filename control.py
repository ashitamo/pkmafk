import win32gui
import win32ui
import win32con
import time
import numpy as np
import cv2
from dectector import health
import pyautogui

class WindowControl:
    def __init__(self, window_name='SM-G975F'):
        self.window_name = window_name
        self.width, self.height = int(720//1.5),int(1520//1.5)
    
    def background_screenshot(self):
        offest = (0, 0)
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width+offest[0], self.height+offest[1])
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.width+offest[0], self.height+offest[1]) , dcObj, (0,0), win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img = img.reshape(self.height+offest[1], self.width+offest[0], 4)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return img

    def get_hwnd(self):
        self.hwnd = win32gui.FindWindow(None, self.window_name)
    def get_window_position(self):
        self.get_hwnd()
        if self.hwnd:
            rect = win32gui.GetWindowRect(self.hwnd)
            cr = win32gui.GetClientRect(self.hwnd)
            return rect,cr
        else:
            return None
    def bring_window_to_front(self):
        self.get_hwnd()
        if self.hwnd:
            try:
                win32gui.SystemParametersInfo(win32con.SPI_SETANIMATION, 0)
                win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(self.hwnd)
                win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                win32gui.SetWindowPos(self.hwnd,None,0,0,self.width,self.height,win32con.SWP_NOMOVE|win32con.SWP_NOZORDER)
            except Exception as e:
                print(e)
class MouseControl:
    def __init__(self):
        pass
    def dragPKM(self):
        pyautogui.moveTo(300, 300)
        pyautogui.dragTo(100,300,duration=0.3)
        time.sleep(1)
    
    def feedPKM(self):
        time.sleep(1)
        pyautogui.moveTo(240,770)
        time.sleep(0.1)
        pyautogui.click(240,770)
        time.sleep(1)
    def intoPKM(self):
        pyautogui.click(250,580)
        time.sleep(2)
if __name__ == '__main__':
    controler = WindowControl("SM-A5260")
    controler.bring_window_to_front()
    mouseControler = MouseControl()
    #while True:
        
    #time.sleep(0.1)
    #print(controler.get_window_position())
    #while True:
    # pyautogui.moveTo(300, 300)
    # pyautogui.dragTo(100,300,duration=0.3)
    # time.sleep(1.5)
    img = controler.background_screenshot()
    mouseControler.dragPKM()
    mouseControler.feedPKM()
    _,bboxes = health(img)
    for b in bboxes:
        cv2.rectangle(img, (b[0], b[1]), (b[2], b[3]), (0, 0, 0), 2)
        print(b[-1])
    cv2.imshow('img',cv2.resize(img,None,fx=0.7,fy=0.7))
    
    cv2.imwrite('screenshot.png',img)
    #cv2.waitKey(0)
