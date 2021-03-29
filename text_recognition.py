# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:57:54 2021

@author: YasmineMnb
"""
import os
import cv2
import numpy as np
from pathlib import Path
import time
#%%

def detect_cotil_text(img, file_name = "test"):

    ## since "closed" is loger we jsut look at the end of the area it could be in
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_ROI = gray_img[0:20,66:76]
    _, binary_roi = cv2.threshold(gray_ROI,127,255,cv2.THRESH_BINARY)

    if 255 in binary_roi:
        return "Closed"

    ## focusing at the area where i expect the text
    ## (not actually nassery after finding the exact pixels, but makes sanity
    ## checks easyer)
    gray_ROI = gray_img[0:22,18:62]
    _, binary_roi = cv2.threshold(gray_ROI,127,255,cv2.THRESH_BINARY)

    ## looking at a pixel on the lower part of the "p" in open
    if binary_roi[19,15] == 255:
        return "Open"
    ## looking at a pixel on the upper part of the "k" in hook
    elif binary_roi[11,34] == 255:
        return "Hook"

#%% testing dir
directory = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\taged results\result_imgs\200915_contin_low_L"
lst = os.listdir(directory)
for file_name in lst:
    full = directory + "\\" + file_name
    img = cv2.imread(full, cv2.IMREAD_COLOR)
    state  = detect_cotil_text(img, file_name)
    print(file_name+"  ---   "+state)
    ## show the part of the img with the text
#    ROI = img[0:22,18:76]
#    cv2.namedWindow(file_name, cv2.WINDOW_NORMAL)
#    cv2.imshow(file_name , ROI)

    #%%


def crop_text_roi(img, window_name="croped"):
    ROI = img[0:22,18:62]


    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#    for i in range(3):
#        for j in range(3):
#            cv2.circle(ROI, (8+j,13+i), 1, (0, 5, 250), -1)


    cv2.circle(ROI, (34,11), 1, (0, 5, 250), -1)
    cv2.imshow(window_name , ROI)
    cv2.waitKey(1)
    return ROI

hook_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\taged results\result_imgs\200827_contin_low_R\7284_CROPED_1.jpg"
open_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\taged results\result_imgs\200827_contin_low_R\7284_CROPED_5.jpg"
closed_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\taged results\result_imgs\200827_contin_low_R\7284_CROPED_3.jpg"

h_img = cv2.imread(hook_path, cv2.IMREAD_COLOR)
o_img = cv2.imread(open_path, cv2.IMREAD_COLOR)
c_img = cv2.imread(closed_path, cv2.IMREAD_COLOR)

#crop_text_roi(h_img, "H")
#crop_text_roi(c_img, "C")
#crop_text_roi(o_img, "O")

#%%


def sim():
    pos = (20,20)
    font = 1
    font_size = 1
    font_thickness = 1

    cv2.putText(img, cot_stage, pos, font, font_size,(90,255,30),font_thickness)
