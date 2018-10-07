#Laster ned video og ratings basert på datasett og legger alt under data-mappen

from download_utils import download_video
from misc_utils import write_ratings
from shutil import copyfile
from math import inf
import csv
import json
import ast
import os

def read_csv():
    f = open('datasets/dataset_2.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    id = 0
    for row in reader:
        if id == 0: #første rad inneholder kolonnenavn
            id += 1
            continue
        
        dwn_link = row[15]
        ratings = row[10]

        to_path = f"data/{id}"

        # to_path = "data/" + str(id)
        vid_to_path = to_path + ".mp4"
        rating_to_path = to_path + "_r" + ".txt"

        if not os.path.exists(to_path):
            os.makedirs(to_path)

        download_video(dwn_link, vid_to_path)
        write_ratings(ratings, rating_to_path)
        id += 1
    f.close()

#read_csv()