##
import joblib
import matplotlib as matplotlib
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pickle
from sklearn import datasets
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import os
import librosa
import librosa.display
import glob
import skimage

df = pd.read_csv("/Users/arunbhatia/Desktop/UrbanSound8K/metadata/UrbanSound8K.csv")
print(df.head())

feature = []
label = []
n = 8732

def parser(row):
    for i in range(n):
        file_name = '/Users/arunbhatia/Desktop/UrbanSound8K/audio/fold' + str(df["fold"][i]) + '/' + df["slice_file_name"][i]
        X, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
        mels = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)
        feature.append(mels)
        label.append(df["classID"][i])
        print(df["classID"][i], i)
    return [feature, label]


temp = parser(df)
temp = np.array(temp)
data = temp.transpose()

X_ = data[:, 0]
Y = data[:, 1]
X = np.empty([n, 128])

for i in range(n):
    X[i] = (X_[i])

Y = to_categorical(Y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, shuffle=True, stratify=Y, random_state=0)

clf = DecisionTreeClassifier(criterion='entropy')
clf.fit(X_train, y_train)
acc_train = clf.score(X_train, y_train)
acc_test = clf.score(X_test, y_test)
print(f"Training error: {acc_train}")
print(f"Test error: {acc_test}")

import pickle

with open('testing_27_7.pkl', 'wb') as f:
    pickle.dump(clf, f)
