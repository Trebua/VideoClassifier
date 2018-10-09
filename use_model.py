import pandas as pd
from sklearn.externals import joblib

def classify_text(text):
    pipe = joblib.load("model.joblib")          #Laster trent modell

    #Lager dataframe for teksten som skal klassifiseres
    df = pd.DataFrame()
    df["id"] = 1
    df["subtitles"] = text                      #Kanskje kjøre clean_text her
    categories = ["Funny","Beautiful", "Ingenious", "Courageous", "Longwinded", "Confusing", "Informative", "Fascinating", "Unconvincing", "Persuasive","Jaw-dropping","OK","Obnoxious","Inspiring"]
    for cat in categories:
        df[cat] = 0

    #Lager predictions
    predictions = pd.Series(pipe.predict(df[categories]))
    results = []
    counter = 0
    for pred in predictions:
        if pred == 1:
            results.append(categories[counter])
        counter += 1
    print(results)

classify_text("hei hei")