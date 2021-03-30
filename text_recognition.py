# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:57:54 2021

@author: YasmineMnb
"""
import os
import cv2
from ast import literal_eval
import pandas as pd



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

#%%


## load in the data from the .txt file
with open(r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\taged results\TEST.txt", "r") as tags_file:
    ## get the first line to init the dct for the data frame
    f_line = tags_file.readline()
    f_dct = literal_eval(f_line)
    ## init dataframe with dct keys + broken down file name and dict name
    ## (from the full_img_path)

    df = pd.DataFrame(columns=f_dct.keys())
    df["file_name"] = ""
    df["directory_name"] = ""

    df = df.append(f_dct, ignore_index=True)

    for line in tags_file:
        line = line.strip()
        dct = literal_eval(line)
        df = df.append(dct, ignore_index=True)

for i in range(len(df)):
    df["file_name"][i]=df["full_img_path"][i].split("\\")[-1]
    df["directory_name"][i]=df["full_img_path"][i].split("\\")[-2]

    #%%




mother_dir = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\taged results\result_imgs"

dir_lst = os.listdir(mother_dir)
for directory_name in dir_lst:
    directory_path = mother_dir + "\\" + directory_name
    file_lst = os.listdir(directory_path)
    for file_name in file_lst:
        full = directory_path + "\\" + file_name
        #%
        img = cv2.imread(full, cv2.IMREAD_COLOR)
        state  = detect_cotil_text(img, file_name)
        if state == None:
            continue
        print(file_name+"  ---   "+state)

        cur_dir_df = df[df["directory_name"]==directory_name]
        ind = cur_dir_df[cur_dir_df["file_name"]==file_name].index[0]

        df.loc[ind]["cot_stage"]=state



        ## show the part of the img with the text
    #    ROI = img[0:22,18:76]
    #    cv2.namedWindow(file_name, cv2.WINDOW_NORMAL)
    #    cv2.imshow(file_name , ROI)
