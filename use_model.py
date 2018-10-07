import seaborn as               sns
import numpy as                 np
import matplotlib.pyplot as     plt
import pandas as                pd
import re
import matplotlib
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

stop_words = set(stopwords.words('english'))

df = pd.read_csv("subtitles/data.csv", encoding = "ISO-8859-1")
df_categories = df.drop(['id', 'subtitles'], axis=1)
counts = []
categories = list(df_categories.columns.values)
for i in categories:
    counts.append((i, df_categories[i].sum()))
df_stats = pd.DataFrame(counts, columns=['category', 'number_of_comments'])

df_stats.plot(x='category', y='number_of_comments', kind='bar', legend=False, grid=True, figsize=(8, 5))
plt.title("Number of comments per category")
plt.ylabel('# of Occurrences', fontsize=12)
plt.xlabel('category', fontsize=12)
#plt.show()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    return text

df['subtitles'] = df['subtitles'].map(lambda com : clean_text(com))

categories = ["Funny","Beautiful", "Ingenious", "Courageous", "Longwinded", "Confusing", "Informative", "Fascinating", "Unconvincing", "Persuasive","Jaw-dropping","OK","Obnoxious","Inspiring"]
train, test = train_test_split(df, random_state=42, test_size=0.2, shuffle=True)
X_train = train.subtitles
X_test = test.subtitles

#ALT OVENFOR ER HELT LIKT TEXTCLASSIFIER.PY, KUN FOR Å FÅ TAK I DATAEN PÅ SAMME FORMAT

model = joblib.load("model.joblib")

for category in categories:
    print('... Processing {}'.format(category))
    prediction = model.predict(X_test)
    print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))

