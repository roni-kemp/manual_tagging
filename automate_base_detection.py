# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:32:09 2020

@author: YasmineMnb
"""

import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
#%%

folder_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\first_last_imgs"
for dirname, dirnames, file_lst in os.walk(folder_path):
#    print(dirname)

    for file in file_lst:
        file_path = os.path.join(dirname, file)

        thresholded(file_path)
        k = cv2.waitKey(500) & 0xFF
        if k == 27: # Esc KEY
            print("Exiting! you stoped...")
            break
#            cv2.destroyAllWindows()



#%%

file = os.path.join(dirname, file_lst[0])
def thresholded(file_path):
    img = cv2.imread(file_path)#,0)

    img = img[-100:]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)

    ret,th1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY)

    #cv2.namedWindow('th1', cv2.WINDOW_NORMAL)
    cv2.imshow("th1", th1)

#%%
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    img[dst>0.01*dst.max()]=[0,0,255]
    cv2.imshow("img", img)

   #%%import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('simple.jpg',0)

# Initiate STAR detector
star = cv2.FeatureDetector_create("STAR")

# Initiate BRIEF extractor
brief = cv2.DescriptorExtractor_create("BRIEF")

# find the keypoints with STAR
kp = star.detect(img,None)

# compute the descriptors with BRIEF
kp, des = brief.compute(img, kp)

print(brief.getInt('bytes'))
print (des.shape )

    #%%
#th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#            cv2.THRESH_BINARY,11,2)
#th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#            cv2.THRESH_BINARY,11,2)
ret3,th3 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


#cv2.namedWindow('th1', cv2.WINDOW_NORMAL)
#cv2.imshow("th1", th1)

#cv2.namedWindow('th2', cv2.WINDOW_NORMAL)
#cv2.imshow("th2", th2)

#
#cv2.namedWindow('th3', cv2.WINDOW_NORMAL)
cv2.imshow("th3", th3)

