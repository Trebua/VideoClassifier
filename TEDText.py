from TEDGetSubs import download_subtitles
from TEDCollection import write_ratings
import csv
from TEDFolderize import get_ratings
import os
#from urllib.request import urlopen
import json
import time
import urllib.request


#categories = ["Funny","Beautiful", "Ingenious", "Courageous", "Longwinded", "Confusing", "Informative", "Fascinating", "Unconvincing", "Persuasive","Jaw-dropping","OK","Obnoxious","Inspiring"]

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
        dict_ = get_ratings(ratings)
        labels = label_string(dict_)
        download_subtitles(id, f"subtitles/{id}.txt",  additional_text=labels)
        id+=1
    f.close()

def label_string(ratings):
    categories = ["Funny","Beautiful", "Ingenious", "Courageous", "Longwinded", "Confusing", "Informative", "Fascinating", "Unconvincing", "Persuasive","Jaw-dropping","OK","Obnoxious","Inspiring"]
    rated = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for key in ratings:
        if ratings[key][1] > 0.75:
            index = categories.index(key)
            rated[index] = 1
    return rated

def write_row(id, subtitles, r,filename = "subtitles/data.csv"):
    #CSV: "id","comment_text","kat", "kat", osv. * 14
    with open(filename, "a") as f:
        writer = csv.writer(f)
        writer.writerow([id,subtitles,r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13]])

def dataset_to_csv(max_count = 200):
    f = open('datasets/dataset.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    id = 0
    with open("subtitles/data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["id","subtitles","Funny","Beautiful", "Ingenious", "Courageous", "Longwinded", "Confusing", "Informative", "Fascinating", "Unconvincing", "Persuasive","Jaw-dropping","OK","Obnoxious","Inspiring"])
    for row in reader:
        if id == 0: #første rad inneholder kolonnenavn
            id += 1
            continue
        if id > max_count:
            break
        ratings = row[10]
        dict_ = get_ratings(ratings)
        labels = label_string(dict_)
        time.sleep(1)
        subtitles = get_subtitles(id)
        if len(subtitles) > 0:
            try:
                write_row(str(id), subtitles, labels)
            except:
                continue
        id+=1
    f.close()

def get_subtitles(id, lang = "en"):
    try:
        url = f"https://www.ted.com/talks/subtitles/id/{id}/lang/{lang}"
        hdr = {'User-agent': 'your bot 0.1'} #stygg workaround for rate-limiting
        req = urllib.request.Request(url, headers=hdr)
        rsp = urllib.request.urlopen(req)
        #response.read()
        #rsp = urlopen(url)
        rsp_text = rsp.read().decode()
        d = json.loads(rsp_text)
        text = text_from_dict(d)
        return text
    except Exception as e: 
        print(e)
        return ""

def text_from_dict(dict):
    l = dict["captions"]
    illegal = ["(Laughter)","(Applause)"]
    txt = ""
    for d in l:
        if d["content"] in illegal:
            continue
        if d["content"] not in illegal:
            content = d["content"]
            content = "".join([i for i in content if i.isalpha() or i == " " or i == "\n"])
            #her kan "\n" replaces med " "
            txt += content + " "
    return txt
        
        
dataset_to_csv()