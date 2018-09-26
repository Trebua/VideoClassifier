#Laster ned video og ratings basert på datasett og legger alt under data-mappen

from TEDGetMP4 import download_ted #tar inn dwn_link (url fra dataset) og to_path (data/videoid++)
import csv
import json
import ast
from math import inf

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

        to_path = "data/" + str(id)
        vid_to_path = to_path + ".mp4"
        rating_to_path = to_path + "_r" + ".txt"

        download_ted(dwn_link, vid_to_path)
        write_ratings(ratings, rating_to_path)
        id += 1
    f.close()

#Rydder opp ratings og skriver de til path
#Må endres: finner nå prosentandel for hver rating utifra den som har fått flest votes
def write_ratings(ratings, to_path):
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
    
    with open(to_path, 'w') as file: #Kan kanskje gjøres raskere og letter reverserbart med pickle dumps og loads
        file.write(str(dict))

#read_csv()