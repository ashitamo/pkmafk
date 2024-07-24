import cv2
import numpy as np
import os
from typing import Callable
from cnocr import CnOcr
ocr = CnOcr(rec_model_name='en_PP-OCRv3')  # 识别模型使用繁体识别模型   
def berry(img,ROI = (826,862,280,320)):
    if type(img) == str:
        img = cv2.imread(img)
    img = img[ROI[0]:ROI[1],ROI[2]:ROI[3]]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img,None,fx=3,fy=3)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("temp.jpg",img)
    out = ocr.ocr("temp.jpg")
    for i in out:
        if i['text'] !='':
            try:
                return int(i['text'])
            except:
                continue
    return None

def health(img,ROI = (150,600)):
    if type(img) == str:
        img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    up = np.array([255, 110, 140])#248,90,123
    down = np.array([230, 70, 100])
    mask = cv2.inRange(img, down,up)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, hierarchy = cv2.findContours(mask[ROI[0]:ROI[1]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('img',img[ROI[0]:ROI[1]])
    # cv2.waitKey(0)
    #bboxes = [cv2.boundingRect(c) if cv2.contourArea(c) > 100 else None for c in contours]
    bboxes = []
    for c in contours:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        btnxn,btnyn = (x+w/2)/img.shape[1],(y+h)/img.shape[0]
        xn,yn,wn,hn = btnxn-0.08,btnyn-0.055,btnxn+0.08,btnyn+0.01
        x,y,w,h = int(xn*img.shape[1]),int(yn*img.shape[0]),int(wn*img.shape[1]),int(hn*img.shape[0])
        bboxes.append([x,y,w,h,area/((w-x)*(h-y))*2.95])
    return mask,bboxes

if __name__ == '__main__':
    img = cv2.imread(r'screenshot.png')
    mask,bboxes = health(img)
    print(berry(img))
    cv2.imshow('mask',mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    for bbox in bboxes:
        if bbox:
            cv2.rectangle(img, (bbox[0], bbox[1]+350), (bbox[2], bbox[3]+350), (0, 255, 0), 2)
            print(bbox[-1])
    cv2.imshow('cmask',cv2.resize(img,None,fx=0.7,fy=0.7))
    cv2.waitKey(0)