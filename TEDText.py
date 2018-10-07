from download_utils import download_subtitles
from misc_utils import write_ratings, get_ratings
import urllib.request
import csv
import os
import json
import time

#Leser inn ratings og lager labels utifra det.
def get_labels(ratings):
    categories = ["Funny","Beautiful", "Ingenious", "Courageous", "Longwinded", "Confusing", "Informative", "Fascinating", "Unconvincing", "Persuasive","Jaw-dropping","OK","Obnoxious","Inspiring"]
    rated = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for key in ratings:
        if ratings[key][1] > 0.75:
            index = categories.index(key)
            rated[index] = 1
    return rated

#Skriver en rad til CSV på formen: "id","comment_text","kat", "kat", osv.
def write_row(id, subtitles, r,filename = "subtitles/data.csv"):
    with open(filename, "a") as f:
        writer = csv.writer(f)
        writer.writerow([id,subtitles,r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13]])

#Lager treningsdata som csv-fil
def dataset_to_csv(max_count = 2200):
    bad_ids = [0,33,686,1155,1236, 1513,1532,1637]
    f = open('datasets/dataset.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    id = 0
    #with open("subtitles/data.csv", "w") as f:
    #    writer = csv.writer(f)
    #    writer.writerow(["id","subtitles","Funny","Beautiful", "Ingenious", "Courageous", "Longwinded", "Confusing", "Informative", "Fascinating", "Unconvincing", "Persuasive","Jaw-dropping","OK","Obnoxious","Inspiring"])
    for row in reader:
        if id < 1638:#første rad inneholder kolonnenavn
            id += 1
            continue
        if id > max_count:
            break
        ratings = row[10]
        ratings = get_ratings(ratings)
        labels = get_labels(ratings)
        #time.sleep(1) #For å ikke få rate-limiting, kan kanskje fjernes?
        subtitles = download_subtitles(id)
        if len(subtitles) > 0:
            try:
                write_row(str(id), subtitles, labels)
            except:
                continue
        id+=1
    f.close()
        
dataset_to_csv()