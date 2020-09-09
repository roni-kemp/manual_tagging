import os
import cv2
import numpy as np
#%%

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

def check_result():
    global img, origin_cache
    print("is this ok? (Enter / Esc)")

    while True:
        k=cv2.waitKey(1) & 0xFF
        if k==27: # Escape Key
            img = origin_cache.copy()
            cv2.line(img,tube_line[0],tube_line[1],(0,255,0),2)
            print("ok, make your changes")
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
            print("Exiting")
            break
        elif k==13: #Enter key
            for indx in range(1,len(points_lst)):
                cv2.line(img, points_lst[indx], points_lst[indx-1], (0, 5, 250), 2)
            cv2.imshow('image', img)
            ok = check_result()
            cot_stage = choose_dev_stage()
            ok = check_result()
            if ok:
                print("ok!")
                comments = input("any comments?")
                break
            else:
                comments = "missing data"
                break

    cv2.destroyAllWindows()
    data_lst = {"full_img_path":full_img_path,"tube_line":tube_line,"points_lst":points_lst,"cot_stage":cot_stage,"comments":comments}
    return data_lst

full_img_path = r"C:\Users\YasmineMnb\Desktop\SynologyDrive\proper_experiments\200831_contin_low\1_R\Croped_2\8053_CROPED.jpg"
data_lst = work_on_img(full_img_path)
#%%



with open("test_file.txt", "a") as out_file:
    out_file.write(str(data_lst))
    out_file.write("\n")

#%%
with open("test_file.txt", "r") as in_file:
    for line in in_file:
        q = eval(line)
        print(q)



