from TEDGet import download_ted #tar inn dwn_link (url fra dataset) og to_path (data/videoid++)
import csv
import json
import ast
#import cPickle as pickle

def read_csv():
    #ratings er index 10
    #url er nest siste index (15)
    f = open('dataset_2.csv', 'r')
    reader = csv.reader(f)
    id = 0
    for row in reader:
        if id == 0: #første rad inneholder kolonnenavn
            id += 1
            continue
        
        dwn_link = row[15]
        ratings = row[10]

        to_path = "data/" + str(id)
        vid_to_path = to_path + ".mp4"
        rating_to_path = to_path + "_r" + ".txt"

        download_ted(dwn_link, vid_to_path)
        write_ratings(ratings, rating_to_path)
        id += 1
    f.close()

#Rydder opp ratings og skriver de til path
def write_ratings(ratings, to_path):
    lst = ast.literal_eval(ratings) #Evaluerer streng til liste og dictionary på en trygg måte

    #Dictionary med alle mulige ratings fra datasettet (TED har endret til andre ratings nå)
    dict = {"Funny": 0, "Beautiful":0, "Ingenious":0, "Courageous":0, "Longwinded":0, "Confusing":0, "Informative":0, "Fascinating":0, "Unconvincing":0,"Persuasive":0,"Jaw-dropping":0,"OK":0,"Obnoxious":0,"Inspiring":0}
    for row in lst:
        dict[row["name"]] = row["count"]
    with open(to_path, 'w') as file: #Kan kanskje gjøres raskere og letter reverserbart med pickle dumps og loads
        file.write(str(dict))

read_csv()