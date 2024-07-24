from cnocr import CnOcr
import json
from PIL import ImageFont, ImageDraw, Image  
import cv2
import time
import numpy as np
import re
import math 
import os
img_fp = r'screenshot.png'
ROI = (826,862,280,320)
img = cv2.imread(img_fp)
img = img[ROI[0]:ROI[1],ROI[2]:ROI[3]]
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('img',img)
cv2.waitKey(0)
img = cv2.resize(img,None,fx=4,fy=4)
cv2.imshow('img',img)
cv2.waitKey(0)
#img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8),iterations=1)
#img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8),iterations=3)
#img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8),iterations=1)
cv2.imshow('img',img)
cv2.waitKey(0)

img = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8),iterations=2)

cv2.imshow('img',img)
cv2.imwrite("temp.jpg",img)
cv2.waitKey(0)

img_fp = r'temp.jpg'
ocr = CnOcr(rec_model_name='en_PP-OCRv3')  # 识别模型使用繁体识别模型
out = ocr.ocr(img_fp)
print(out)
