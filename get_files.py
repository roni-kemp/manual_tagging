## get the full paths of the files
## create new folders with first and last img per location per experiment (collect that)
## combined with img handling this should give a folder containing ONE text file with the dictionary data
## and a folder per experiment containing firt and last img clean and marked for every location

import os
import re
#%%

#%%
prop_exp_folder =  r"C:\Users\YasmineMnb\Desktop\SynologyDrive\proper_experiments"

exp_folder_lst = str(os.listdir(prop_exp_folder))

regex = r"[0-9]{6}_contin[_]*[low]*"
matches = re.finditer(regex, exp_folder_lst, re.MULTILINE)


for match in matches:
    per_exp_path = prop_exp_folder+"\\"+match.group()

    for dirname, dirnames, filenames in os.walk(full_path):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            if subdirname.upper()[:6] == "CROPED":
                per_location_path = os.path.join(dirname, subdirname)

                for dirname, dirnames, filenames in os.walk(per_location_path):
                    print(filenames[0])
                    print(filenames[-1])


#%% usfull

pic_lst = [os.path.join(in_path, f_name) for f_name in os.listdir(in_path)]

os.mkdir(out_path)