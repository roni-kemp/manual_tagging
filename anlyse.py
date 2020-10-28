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
import re
#from tqdm import tqdm as tq


def load_data(file_path):
    data_lst = []
    with open(file_path, "r") as in_file:
        for line in in_file:
            q = eval(line)
            data_lst.append(q)
    return data_lst

def dist(st_point,end_point):
    """ converts 2 points into numpy array and calculates the distance """
    st = np.array(st_point)
    end = np.array(end_point)
    return np.linalg.norm(st - end)

def get_size(img_data):
    """
    get a general idea of the size of the shoot.
    assuming:
      - the tube_line = 2cm
    """
    tube_line = img_data["tube_line"]
    st = tube_line[0]
    end = tube_line[1]

    tube_size_in_pixls = round(dist(st,end)) # (size of the base in number of pixls)
    if tube_size_in_pixls == 0:
        print(img_data)
        return -1
    conv_ratio = 2/tube_size_in_pixls             # (the size of a single pixl)

    length_in_pixl = sum_points(img_data)
    length = length_in_pixl * conv_ratio
    return length

def sum_points(img_data):
    """
    should be replaced with get_s_lst[-1]   !!!
    """
    sum_of_points_dst = 0
    points_lst = img_data["points_lst"]
    for i, point in enumerate(points_lst[:-1]):
        sum_of_points_dst += dist(point,points_lst[i+1])
    return sum_of_points_dst

def get_s_lst(img_data):
    ds_lst = []
    points_lst = img_data["points_lst"]
    for i, point in enumerate(points_lst[:-1]):
        ds_lst.append(dist(point,points_lst[i+1]))
    s_lst = np.cumsum(ds_lst)
    return s_lst

def get_theta_lst(img_data):
    img_data = categorize(img_data)
    points_lst = img_data["points_lst"]
    theta_lst = []
    for i, point in enumerate(points_lst[:-1]):
        rel_x = points_lst[i+1][0] - point[0]
        rel_y = points_lst[i+1][1] - point[1]
        theta = np.arccos(rel_x/np.sqrt(rel_y**2+rel_x**2))*180/np.pi
        if img_data["oriantation"] == "R":
            theta = 90-theta
        else:
            theta = -(90-theta)
        theta = round(theta,1)
        theta_lst.append(theta)
    theta_array = np.array(theta_lst)

    return theta_array

def get_size_distribution(data_lst):
    sizes = []
    for img_data in data_lst:
        size = get_size(img_data)
        if img_data["comments"] != "":
            print(img_data["comments"] )
        if size == -1:
            continue
        sizes.append(size)
#        if size<0.5:
#            img_show(img_data)
    return sizes

def categorize(img_data):
    path = img_data["full_img_path"]
    exp = path.split("\\")[-2]
    file_name = path.split("\\")[-1]
    location = int(re.findall(r"_([1-5])\.", file_name)[0])
    img_data["location"] = location
    oriantation = re.findall(r"_([LR])\\", path)[0]
    img_data["oriantation"] = oriantation
    ## for the first/last tag i need to get the folder content and compare
    ## the 2 file numbers
    parent_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\first_last_imgs"
    img_lst = os.listdir(parent_path + "\\" + exp)
    first = ""
    last = ""
    for img in img_lst:
        num = img.split("_")[0]
        if first == "":
            first = num
        elif last == "" and num != first:
            last = num
            break

    ## add the tag
    if first in file_name:
        img_data["f_l_tag"] = "F"
    if last in file_name:
        img_data["f_l_tag"] = "L"
    return img_data


def img_show(img_data):
    res_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\progression\result_imgs"
    o_img_path=img_data["full_img_path"]
    new_img_path = res_path +"\\20"+ o_img_path.split("\\20")[-1]
    img = cv2.imread(new_img_path)

    ## add points
    for point in img_data["points_lst"]:
        cv2.circle(img, point,1,(255,0,0), -1)

    while True:
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.imshow('image', img)
        k=cv2.waitKey(1) & 0xFF
        if k==27: # Esc KEY
            print("Exiting! you stoped...")
            cv2.destroyAllWindows()
            break
    cv2.destroyAllWindows()


#%%
file_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\snflwrs zip to Roni\first try - 1-11.txt"
file_path = r"C:\Users\YasmineMnb\Downloads\progression\1-27 next time start at 28.txt"
data_lst = load_data(file_path)


#%%
first_lst = []
last_lst = []
ugly_lst = []
for img_data in data_lst:
    if img_data["tube_line"][0] == (-1,-1) \
    or img_data["comments"] == "weird"\
    or "tube" in img_data["comments"]:

        ugly_lst.append(img_data)
        continue

    img_data = categorize(img_data)
    if img_data["f_l_tag"] == "L":
        last_lst.append(img_data)
    else:
        first_lst.append(img_data)
#%%
sizes_first = get_size_distribution(first_lst)
sizes_first = np.array(sizes_first)
sizes_last = get_size_distribution(last_lst)
sizes_last = np.array(sizes_last)

#%%  boxplot
fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True)

box = ax1.boxplot([sizes_first,sizes_last], labels = ["size first","size last"], widths = 0.6)

plt.title("size distribution")
#%%  histogram
fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True)

plt.hist(sizes_first,15,)# alpha = 0.5)
plt.hist(sizes_last,15, alpha = 0.5)
plt.grid(True)
plt.title("size distribution")

#%% fitting


fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True)
for img_data in last_lst:
    #%%
    theta_lst = get_theta_lst(img_data)
#    if max(theta_lst) < 0:
#        img_show(img_data)
#        print(img_data["full_img_path"])
    s_lst = get_s_lst(img_data)

    plt.plot(s_lst,theta_lst)

#%%
from scipy.optimize import curve_fit

def func(s, a, L, c):
    return a * np.exp(-s/L) + c


#%%

a_guess = 1
L_guess = 250
c_guess = 0


xdata = np.linspace(0, 300, 10)

y_guess = func(xdata, a_guess, L_guess, c_guess)
print(y_guess[:5])
#np.random.seed(1729)
#y_noise = 0.2 * np.random.normal(size=xdata.size)
#ydata = y + y_noise


popt, pcov = curve_fit(func, s_lst, theta_lst, p0=[a_guess,b_guess,c_guess])



#%%


fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True)
plt.plot(xdata, func(xdata, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
plt.plot(xdata, y_guess, label='init_guess a=%5.3f, b=%5.3f, c=%5.3f' % tuple([a_guess,b_guess,c_guess]))
plt.plot(s_lst, theta_lst, label='data')

plt.legend()







