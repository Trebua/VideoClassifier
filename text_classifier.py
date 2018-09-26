# pip install seaborn og tensorflow-hub
# https://www.tensorflow.org/hub/tutorials/text_classification_with_tf_hub

import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns

# Load all files from a directory in a DataFrame.
def load_directory_data(directory):
    data = {}
    data["sentence"] = []
    data["sentiment"] = []
    for file_path in os.listdir(directory):
        with tf.gfile.GFile(os.path.join(directory, file_path), "r") as f:
            data["sentence"].append(f.read())
            sentiment = file_path.replace('_',' ').replace('.',' ').split()[1]
            data["sentiment"].append(sentiment)
    return pd.DataFrame.from_dict(data)

# Merge positive and negative examples, add a polarity column and shuffle.
def load_dataset(directory):
    '''
    ratings = ["Beautiful","Confusing", "Courageous", "Fascinating", "Funny", "Informative", "Ingenious","Inspiring","Jaw-dropping","Longwinded","Obnoxious","OK","Persuasive","Unconvincing"]
    dataframes = []
    polarity = 0 #Vet ikke hva polariteten skal være når klassifiseringen ikke er binær??
    for rating in ratings:
        df = load_directory_data(f"{directory}/{rating}/")
        df["polarity"] = polarity
        polarity += 1
        dataframes.append(df)
    return pd.concat(dataframes).sample(frac=1).reset_index(drop=True)
    pos_df = load_directory_data(os.path.join(directory, "pos"))
    neg_df = load_directory_data(os.path.join(directory, "neg"))
    pos_df["polarity"] = 1
    neg_df["polarity"] = 0
    return pd.concat([pos_df, neg_df]).sample(frac=1).reset_index(drop=True)
    '''
    funny_df = load_directory_data(os.path.join(directory, "Funny"))
    inspiring_df = load_directory_data(os.path.join(directory, "Inspiring"))
    funny_df["polarity"] = 1
    inspiring_df["polarity"] = 0

    return pd.concat([funny_df, inspiring_df]).sample(frac=1).reset_index(drop=True)

# Download and process the dataset files.
def download_and_load_datasets(force_download=False):

    #train_df = load_dataset(os.path.join(os.path.dirname(dataset),
    #                                     "aclImdb", "train"))
    #test_df = load_dataset(os.path.join(os.path.dirname(dataset),
    #                                    "aclImdb", "test"))
    train_df = load_dataset("subtitles")
    return train_df

    #return train_df, test_df


#print(load_dataset("subtitles"))
train_df = load_dataset("subtitles")

# Reduce logging output.
tf.logging.set_verbosity(tf.logging.ERROR)

#train_df, test_df = download_and_load_datasets()
train_df.head()

# Training input on the whole training set with no limit on training epochs.
train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df, train_df["polarity"], num_epochs=None, shuffle=True)

# Prediction on the whole training set.
predict_train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df, train_df["polarity"], shuffle=False)
# Prediction on the test set.
#predict_test_input_fn = tf.estimator.inputs.pandas_input_fn(
#    test_df, test_df["polarity"], shuffle=False)


embedded_text_feature_column = hub.text_embedding_column(
    key="sentence", 
    module_spec="https://tfhub.dev/google/nnlm-en-dim128/1")

labels = ["Beautiful","Confusing", "Courageous", "Fascinating", "Funny", "Informative", "Ingenious","Inspiring","Jaw-dropping","Longwinded","Obnoxious","OK","Persuasive","Unconvincing"]
estimator = tf.estimator.DNNClassifier(
    hidden_units=[500, 100],
    feature_columns=[embedded_text_feature_column],
    n_classes=2,
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.003))
    #label_vocabulary=labels)

# Training for 1,000 steps means 128,000 training examples with the default
# batch size. This is roughly equivalent to 5 epochs since the training dataset
# contains 25,000 examples.
estimator.train(input_fn=train_input_fn, steps=20)

train_eval_result = estimator.evaluate(input_fn=predict_train_input_fn)
#test_eval_result = estimator.evaluate(input_fn=predict_test_input_fn)

print("Training set accuracy: {accuracy}".format(**train_eval_result))
#print("Test set accuracy: {accuracy}".format(**test_eval_result))

