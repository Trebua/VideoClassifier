from TEDGetSubs import download_subtitles
from TEDCollection import write_ratings
import csv
from TEDFolderize import get_ratings
import os

def dataset_to_text(max_count = 10):
    f = open('datasets/dataset_10.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    id = 0
    for row in reader:
        if id == 0: #første rad inneholder kolonnenavn
            id += 1
            continue
        if id > max_count:
            break
        ratings = row[10]
        dict = get_ratings(ratings)
        for key in dict:
            subpath = f"subtitles/{key}/"
            path = f"{subpath}{id}_{key}.txt"
            if not os.path.exists(subpath):
                    os.makedirs(subpath)
            if dict[key][1] > 0.75:
                download_subtitles(id, path)
        id+=1
    f.close()
        
        
dataset_to_text()