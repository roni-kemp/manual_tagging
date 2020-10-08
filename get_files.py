## get the full paths of the files
## create new folders with first and last img per location per experiment (collect that)
## combined with img handling this should give a folder containing ONE text file with the dictionary data
## and a folder per experiment containing firt and last img clean and marked for every location

import os
import re
from tqdm import tqdm as tq
#%%

#%%
prop_exp_folder =  r"D:\my original pictures\prop_exp_more_1"

exp_folder_lst = str(os.listdir(prop_exp_folder))

regex = r"[0-9]{6}_contin[_]*[low]*"
matches = re.finditer(regex, exp_folder_lst, re.MULTILINE)

lst = []
for match in tq(matches):
    per_exp_path = prop_exp_folder+"\\"+match.group()
    exp_date = match.group()
    lst.append(exp_date)
    for dirname, dirnames, _ in os.walk(per_exp_path):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            if subdirname.upper()[:6] == "CROPED":
                per_location_path = os.path.join(dirname, subdirname)

                O_L_regex = r"(_[L,R])\\Croped(_[1-5])"
                O_L_match = re.search(O_L_regex, per_location_path)
                if O_L_match:
                    orient = O_L_match.group(1)
                    loc = O_L_match.group(2)

                    new_folder = exp_date + orient
                    rel_path = r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\manual_tagging\first_last_imgs"
                    new_folder =  os.path.join(rel_path, new_folder)
                    if not os.path.isdir(new_folder):
                        os.mkdir(new_folder)

                    filenames = os.listdir(per_location_path)
                    firs_img_path = os.path.join(per_location_path, filenames[0])
                    last_img_path = os.path.join(per_location_path, filenames[-1])
#                    print(firs_img_path, last_img_path)

                    first_new_name = filenames[0].strip(".jpg") + loc + ".jpg"
                    first_new_path = os.path.join(new_folder, first_new_name)
                    last_new_name = filenames[-1].strip(".jpg") + loc + ".jpg"
                    last_new_path = os.path.join(new_folder, last_new_name)

                    os.system(r'copy "{in_path}" "{out_path}"'.format(in_path = firs_img_path, out_path = first_new_path))
                    os.system(r'copy "{in_path}" "{out_path}"'.format(in_path = last_img_path, out_path = last_new_path))


#%% usfull

pic_lst = [os.path.join(in_path, f_name) for f_name in os.listdir(in_path)]

os.mkdir(out_path)