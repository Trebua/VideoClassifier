#Laster ned videoer fra datasett og putter filmer i mapper om de har mer enn 0.75 ratings for kategori
from TEDGet import download_ted #tar inn dwn_link (url fra dataset) og to_path (data/videoid++)
import csv
import json
import ast
from math import inf
from shutil import copyfile
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
                    download_ted(dwn_link, path)
                    created = path
                else:
                    copyfile(created, path)
        id += 1
    f.close()

#Rydder opp i ratings og returnerer dictionary
def get_ratings(ratings):
    lst = ast.literal_eval(ratings) #Evaluerer streng til liste og dictionary på en trygg måte
    dict = {} #dict vil være på formen: kategori : [antall stemmer, prosentandel av antall stemmer]
    max = -inf

    for row in lst:
        votes = row["count"]
        category = row["name"]
        max = votes if votes > max else max #Tar utgangspunkt i max og ikke total antall votes for å regne ut prosent
        dict[category] = [votes,0]
    
    for key in dict:
        dict[key][1] = dict[key][0]/max #finner prosentandel som har stemt på kategorien
    
    return dict

read_csv()