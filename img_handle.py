import os
import cv2
import numpy as np
#%

def mous_interactions(event,x,y,flags,param):
    global img, origin_cache, points_lst
    global tube_line

    if event == cv2.EVENT_LBUTTONDOWN:
        if flags == 17: ## if hold down shift key - line
            tube_line[0] = (x,y)
        else:
            points_lst.append((x,y))

    elif event == cv2.EVENT_LBUTTONUP and flags == 16: ## if hold down shift key - finish line
        tube_line[1] = (x,y)
        cv2.line(img,tube_line[0],tube_line[1],(0,255,0),2)

    ## double right click to delete
    elif event == cv2.EVENT_RBUTTONDBLCLK:

        ## if hold down shift key - remove line
        if flags == 18:
            img = origin_cache.copy()
            tube_line = [(-1,-1),(-1,-1)]

        ## if not shift key - remove points
        else:
            try:
                closest_point = find_closest_point((x,y),points_lst)
                del points_lst[closest_point]
                ## reconstruct img
                img = origin_cache.copy()
                cv2.line(img,tube_line[0],tube_line[1],(0,255,0),2)
            except ValueError:
                print("no points in list!")

def find_closest_point(mous_point, points_lst):
    points_lst_array = np.array(points_lst)
    dists=np.sqrt(np.sum((mous_point-points_lst_array)**2,axis=1))
    return dists.argmin()

def draw_points(img, points_lst):
    for point in points_lst:
        cv2.circle(img, point, 1, (0, 5, 250), -1)

def check_result(text1 = "is this ok? (Enter / Esc)", text2 = "make your changes now pleas..."):
    global img, origin_cache
    print(text1)

    while True:
        k=cv2.waitKey(1) & 0xFF
        if k==27: # Escape Key
            img = origin_cache.copy()
            cv2.line(img,tube_line[0],tube_line[1],(0,255,0),2)
            print(text2)
            return False
        elif k==13: # Enter Key
            return True

def choose_dev_stage():
    global img
    print("choose Cotyledon developmental stage: \n(1-Closed / 2-Open / 3-Hook)")
    while True:
        k=cv2.waitKey(1) & 0xFF
#        if k!= 255:
#            print(k)
        if k==13: # Enter Key
            print("sorry, need to choos: (1-Closed / 2-Open / 3-Hook)\nEsc for abort")
        if k==49: # 1 Key
            cot_stage = "Closed"
            break
        if k==50: # 2 Key
            cot_stage = "Open"
            break
        if k==51: # 3 Key
            cot_stage = "Hook"
            break
        elif k==27: # Escape Key
            print("Exiting! missing data!")
            return None
    pos = (20,20)
    font = 1
    font_size = 1
    font_thickness = 1
    cv2.putText(img, cot_stage, pos, font, font_size,(90,255,30),font_thickness)
    cv2.imshow('image', img)


def work_on_img(full_img_path):

    global img, origin_cache
    img = cv2.imread(full_img_path)
    origin_cache = img.copy()

    global tube_line
    tube_line = [(-1,-1),(-1,-1)]

    global points_lst
    points_lst = []

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    while(1):
        cv2.setMouseCallback('image', mous_interactions)


        draw_points(img, points_lst)
        cv2.imshow('image', img)

        k=cv2.waitKey(1) & 0xFF
        if k==27: # Esc KEY
            print("Exiting! you stoped...")
            cv2.destroyAllWindows()
            return "Break", k

        elif k==13: #Enter key
            for indx in range(1,len(points_lst)):
                cv2.line(img, points_lst[indx], points_lst[indx-1], (0, 5, 250), 2)
            cv2.imshow('image', img)
            ok = check_result()
            if not ok:
                continue
            cot_stage = choose_dev_stage()
            ok = check_result()
            if not ok:
                continue
            elif ok:
                print("ok!")
                ok = check_result(text1 = "any comments?", text2 = "you chose to add a comment.. if it was a mistake just click the comand window and press enter")
                if not ok:
                    comments = input("write comment now: ")
                else: comments = ""
                break
    cv2.destroyAllWindows()
    img_data = {"full_img_path":full_img_path,"tube_line":tube_line,"points_lst":points_lst,"cot_stage":cot_stage,"comments":comments}
    return img_data, k
#%%
full_img_path = r"C:\Users\YasmineMnb\Desktop\SynologyDrive\proper_experiments\200831_contin_low\1_R\Croped_2\8053_CROPED.jpg"
data_lst = work_on_img(full_img_path)
#%% def loop_through_all_folders(start_indx):

def loop_through_single_exp(curr_exp_folder_path):
    img_lst = os.listdir(curr_exp_folder_path)
    for img in img_lst:
        full_img_path = os.path.join(curr_exp_folder_path, img)
        print(img)
        img_data, k = work_on_img(full_img_path)
        if not k == 27: ## didn't press esc:
            with open("TEST.txt", "a") as out_file:
                out_file.write(str(img_data))
                out_file.write("\n")
            print("saved! :) moving on")
        else:
            return False
    return True

from pathlib import Path
repo_dir = Path(".").absolute()
imgs_dir = repo_dir/"first_last_imgs"

exp_lst = os.listdir(imgs_dir)
#indx_lst = len(exp_lst)

start_indx = 49

for indx in range(start_indx-1, len(exp_lst)):
    curr_folder = exp_lst[indx]
    curr_exp_folder_path = os.path.join(imgs_dir, exp_lst[indx])
    print(curr_folder)
    stat = loop_through_single_exp(curr_exp_folder_path)
    if not stat:
        break


#%%

with open("test_file.txt", "a") as out_file:
    out_file.write(str(data_lst))
    out_file.write("\n")

#%%
with open("test_file.txt", "r") as in_file:
    for line in in_file:
        q = eval(line)
        print(q)



