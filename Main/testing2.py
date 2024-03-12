#!/bin/python

#from ast import Return
#import time
#import joblib
#import matplotlib as matplotlib
import pandas as pd
import numpy as np
#from sklearn.tree import DecisionTreeClassifier
#from sklearn import datasets
pd.plotting.register_matplotlib_converters()
#import matplotlib.pyplot as plt
#%matplotlib inline
#import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
#from sklearn.model_selection import GridSearchCV
#from sklearn.preprocessing import MinMaxScaler
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D, Dropout
#from tensorflow.keras.utils import to_categorical
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.svm import SVC
#import os
import librosa
import librosa.display
#import glob
#import skimage
import pickle


with open('/home/pi/intelligent-audio-listener/ML/testing_16_8_claps.pkl', 'rb') as f:
    clf2 = pickle.load(f)

def tunnistus(x):

    def parser2(y):
        file_name = y
        X, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
        mels = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)
        feature.append(mels)
        label.append("classID")
        return [feature, label]

    feature = []
    label = []

    temp = parser2(x)
    temp = np.array(temp, dtype=object)
    data = temp.transpose()

    X_ = data[:, 0]
    print()
    Y = data[:, 1]
    X = np.empty([1, 128])

    for j in range(1):
       X[j] = (X_[j])

    p = clf2.predict(X)
    p2 = clf2.predict_proba(X)

    p = str(p)
    p = p.replace("[", "")
    p = p.replace("]", "")
    p = p.replace(".", "")
    p = list(p.split(" "))

    arvot = ["air_conditioner", "car_horn", "children_playing", "clapping", "drilling", "engine_idling",
                "gun_shot", "jackhammer", "siren", "street_music"]

    if "1" in p:
        p = p.index('1')
        p = (arvot[p]).upper()
        print(p)

    else:
        p = "OTHER"

    
    return p


