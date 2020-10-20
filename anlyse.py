# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:18:00 2020

@author: YasmineMnb
"""
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import time
from scipy import signal
import cv2
#from tqdm import tqdm as tq
#%%

def load_data():
    data_lst = []
    with open(r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\snflwrs zip to Roni\first try - 1-11.txt", "r") as in_file:
        for line in in_file:
            q = eval(line)
            data_lst.append(q)
    return data_lst
            #%%
data_lst = load_data()
def dist(st_point,end_point):
    st = np.array(st_point)
    end = np.array(end_point)
    return np.linalg.norm(st - end)

#def dist(x1,y1,x2,y2):
#    return ((x2-x1)**2 + (y2-y1)**2)**0.5

#%%
def get_size(img_data):
    """
    get a general idea of the size of the shoot.
    assuming:
      - the tube_line = 2cm
    """
    #%%
    tube_line = img_data["tube_line"]
    st = tube_line[0]
    end = tube_line[1]

    tube_size_in_pixls = round(dist(st,end)) # (size of the base in number of pixls)
    if tube_size_in_pixls == 0:
        print(img_data)
        return -1
    conv_ratio = 2/tube_size_in_pixls             # (the size of a single pixl)

    length_in_pixl = sum_points(img_data)
    length= length_in_pixl*conv_ratio
    return length

def sum_points(img_data):
    sum_of_points_dst = 0
    points_lst = img_data["points_lst"]
    for i, point in enumerate(points_lst[:-1]):
        sum_of_points_dst += dist(point,points_lst[i+1])
    return sum_of_points_dst
            #%%
def get_size_distribution(data_lst):
    sizes = []
    for img_data in data_lst:
        size = get_size(img_data)
        if img_data["comments"] != "":
            print(img_data["comments"] )
        if size == -1:
            continue
        sizes.append(size)
#        if size>2:
#            img_show(img_data)
    return sizes

#%% boxplot


sizes = get_size_distribution(data_lst)

fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True)

box = ax1.boxplot(sizes, labels = ["size of plants"])
plt.title("size distribution")



#%%
def img_show(img_data):
    res_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\snflwrs zip to Roni\result_imgs"
    o_img_path=img_data["full_img_path"]
    new_img_path = res_path +"\\20"+ o_img_path.split("\\20")[-1]

    img = cv2.imread(new_img_path)
    while True:
        cv2.imshow('image', img)
        k=cv2.waitKey(1) & 0xFF
        if k==27: # Esc KEY
            print("Exiting! you stoped...")
            cv2.destroyAllWindows()
            break
    cv2.destroyAllWindows()

    #%% fitting

from scipy.optimize import curve_fit

def func(x, a, b, c):
    return -a * np.exp(-b * x) + c




a_guess = 34
b_guess = 0.006
c_guess = -22


xdata = np.linspace(-50, -400, 10)

y_guess = func(xdata, a_guess, b_guess, c_guess)
#np.random.seed(1729)
#y_noise = 0.2 * np.random.normal(size=xdata.size)
#ydata = y + y_noise




arr = np.array(img_data["points_lst"])
x = -arr[:,0]
y = -arr[:,1]


popt, pcov = curve_fit(func, x, y, p0=[a_guess,b_guess,c_guess])






fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True)
plt.plot(xdata, func(xdata, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
plt.plot(xdata, y_guess, label='init_guess a=%5.3f, b=%5.3f, c=%5.3f' % tuple([a_guess,b_guess,c_guess]))
plt.plot(x,y, label='data')

plt.legend()







