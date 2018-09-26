from TEDGetSubs import download_subtitles
from TEDCollection import write_ratings
import csv

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
        download_subtitles(id,f"subtitles/{id}_text.txt")
        ratings = row[10]
        write_ratings(ratings, f"subtitles/{id}_ratings.txt")
        id+=1
    f.close()
        
        
dataset_to_text()