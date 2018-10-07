from math import inf
import ast

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