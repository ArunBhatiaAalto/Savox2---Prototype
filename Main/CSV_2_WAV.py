#!/bin/python

import chunk
from re import A
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import rfft, rfftfreq
import scipy.io
from time import sleep
import time

SAMPLE_RATE = 11200

def read_csv(file):
    data = []
    f = open(file, "r")

    for line in f:
        data.append([int(n) for n in line.split(",")])

    f.close()

    #transpose the data matrix
    data_t = []
    for i in range(0, len(data[0])):
        data_t.append(([c[i] for c in data]))
    return data_t


def normalize_tone(shifted_tone):
    normalized = []
    a = (sum(shifted_tone)/(len(shifted_tone)))
    #print(a)
    for p in range(len(shifted_tone)):
        normalized.append(shifted_tone[p] - a)
    return normalized


def make_csv(input_file, output_flie):
    data = read_csv(input_file)
    normalized = normalize_tone(data[0])
    array = np.array(normalized)
    scipy.io.wavfile.write(output_flie, SAMPLE_RATE, array)
