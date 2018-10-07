#Laster ned videoer fra datasett og putter filmer i mapper om de har mer enn 0.75 ratings for kategori
from download_utils import download_video #tar inn dwn_link (url fra dataset) og to_path (data/videoid++)
from misc_utils import get_ratings
from shutil import copyfile
import csv
import json
import os

def read_csv():
    #ratings er index 10
    #url er nest siste index (15)

    f = open('datasets/dataset_2.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    id = 0
    for row in reader:
        if id == 0: #første rad inneholder kolonnenavn
            id += 1
            continue
        
        dwn_link = row[15]
        ratings = row[10]

        dict = get_ratings(ratings)
        created = ""

        for key in dict:
            if dict[key][1] > 0.75:
                subpath = f"training/{key}"
                path = f"{subpath}/{id}.mp4"
                if not os.path.exists(subpath):
                    os.makedirs(subpath)
                if len(created) == 0:
                    download_video(dwn_link, path)
                    created = path
                else:
                    copyfile(created, path)
        id += 1
    f.close()

#read_csv()