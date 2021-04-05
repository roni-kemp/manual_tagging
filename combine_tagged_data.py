import pandas as pd
import re

## load tagged data and clean up empty cot_stage
taged_df = pd.read_csv(r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\oscillation-project\adding tagged data\results_high.csv", index_col = 0)
taged_df = taged_df.drop(taged_df[taged_df["cot_stage"].isnull()].index).reset_index()
taged_df = taged_df.drop("index",axis = 1)

## load oscilation df and add empty columns
osci_df = pd.read_csv(r"C:\Users\YasmineMnb\Desktop\Roni_new\python scripts\oscillation-project\adding tagged data\osci_df.csv", index_col = 0)
columns = ["cot_stage_start","cot_stage_end","points_lst_start","points_lst_end","tube_line"]
osci_df = osci_df.join(pd.DataFrame(columns=columns))

## combine
for indx, row in osci_df.iterrows():

    ## get identifiers from osci img_file
    curr_img_file = row["img_file"].strip()
    regex = r"\\([0-9]{6})_.*([RL])*.*[A-Za-z]*_([1-5])"
    match = re.search(regex, curr_img_file)
    if not match:
        print("not found in:\n" + curr_img_file)
        continue
    date = match.group(1)
#    oriantation = match.group(2)
    tip_loc = match.group(3)
    orientation = osci_df.loc[indx]["orientation"]

    ## get data from taged files and save is as a small df
    date_df = taged_df[taged_df["directory_name"].str.contains(date)]
    date_df = date_df[date_df["directory_name"].str.contains(orientation)]
    regex_2 = r"_[{}].".format(tip_loc)
    date_df = date_df[date_df["file_name"].str.contains(tip_loc)]

    ## update osci file
    try:
        osci_df.loc[indx,"cot_stage_start"] = date_df.iloc[0]["cot_stage"]
        osci_df.loc[indx,"cot_stage_end"] = date_df.iloc[1]["cot_stage"]
        osci_df.loc[indx,"points_lst_start"] = date_df.iloc[0]["points_lst"]
        osci_df.loc[indx,"points_lst_end"] = date_df.iloc[1]["points_lst"]
        osci_df.loc[indx,"tube_line"] = date_df.iloc[0]["tube_line"]
    ## if for some resone only the first img was tagged
    except IndexError:
        print("skipped img:  ", curr_img_file)
        continue


