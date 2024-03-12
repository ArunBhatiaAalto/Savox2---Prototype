import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
pd.plotting.register_matplotlib_converters()
from tensorflow.keras.utils import to_categorical
import librosa
import librosa.display

df = pd.read_csv("/Users/arunbhatia/Desktop/UrbanSound8K/metadata/UrbanSound8K2.csv")
print(df.head())

feature = []
label = []
n = 7824
c = 0

def parser(row):
    for i in range(n):
        file_name = '/Users/arunbhatia/Desktop/UrbanSound8K/audio/fold' + str(int(df["fold"][i])) + '/' + df["slice_file_name"][i]
        if df["classID"][i] == 1 or df["classID"][i] == 3 or df["classID"][i] == 4 or df["classID"][i] == 5 or df["classID"][i] == 6 or df["classID"][i] == 7 or df["classID"][i] == 8:
            X, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
            mels = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)

            feature.append(mels)
            label.append(df["classID"][i])
            globals()['c'] += 1
            print(df["class"][i], i)
    return [feature, label]


temp = parser(df)
temp = np.array(temp)
data = temp.transpose()

X_ = data[:, 0]
Y = data[:, 1]
X = np.empty([c, 128])
print(c)

for i in range(c):
    X[i] = (X_[i])

Y = to_categorical(Y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, shuffle=True, stratify=Y, random_state=0)

clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train, y_train)
acc_train = clf.score(X_train, y_train)
acc_test = clf.score(X_test, y_test)
print(f"Training error: {acc_train}")
print(f"Test error: {acc_test}")

import pickle

with open('testing_16_8_claps.pkl', 'wb') as f:
    pickle.dump(clf, f)