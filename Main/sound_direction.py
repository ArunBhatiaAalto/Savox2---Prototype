#!/bin/python

import numpy as np
from scipy.signal import correlate
from scipy.signal import correlate

#Data
SAMPLE_RATE = 10000
MIC_DISTANCE = 0.19
RESOLUTION = 1024

#angle ofset for each mic pair
MIC1_MIC2 = 0                                 #1     2
MIC1_MIC3 = 45
MIC3_MIC1 = 90                                #3     4
MIC3_MIC4 = 135
MIC4_MIC3 = 180
MIC4_MIC2 = 225
MIC2_MIC4 = 270
MIC2_MIC1 = 315


AMPLITUDE_THRESHOLD = 0.85

#MIC_ORDER = [0, 2, 1, 3]
#MIC_ORDER = [1,3,0,2]
MIC_ORDER = [2,0,3,1]

#read a csv file into a 2d-array
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


def shift_to_angle(shift):
        t = shift/SAMPLE_RATE
        sina = t*340/MIC_DISTANCE
        a = np.sin(sina) * 180/(np.pi)
        return a


#constatant sound
########################

def angle_const(ch1, ch2):
    assert len(ch1) == len(ch2), "ch1 and ch2 must have the same shape"
    ch1 = np.array(list(ch1))     
    ch2 = np.array(list(ch2))
    #filter out measurement errors
                              
    cor = np.argmax(cross_correlate(ch1, ch2)) - len(ch1) + 1   #argmax
    a = shift_to_angle(cor)
    return a

#########################

def normalize_shift(shifted_tone):
    #Creates generator for normalized tone
    avg = (sum(shifted_tone)/(len(shifted_tone)))
    for p in range(len(shifted_tone)):
        yield ((shifted_tone[p] - avg) / (RESOLUTION / 4))


def cross_correlate(ch1, ch2):
    difference = correlate(ch1, ch2)
    return difference

#sharp sound
########################

def find_peak(data):
    max_value = abs(max(data))
    
    for i in range(len(data)):

        point = data[i]

        if abs(point) > abs(AMPLITUDE_THRESHOLD * max_value):
        
            return i


def angle_sharp(ch1, ch2):

    start_ch1 = find_peak(ch1)
    start_ch2 = find_peak(ch2)

    cor = start_ch1 - start_ch2
    a = shift_to_angle(cor)

    return a

##########################################################

def sort_channels(ch1, ch2, ch3, ch4):
    #Starting point of sound in each channel
    start_ch1 = find_peak(ch1)
    start_ch2 = find_peak(ch2)
    start_ch3 = find_peak(ch3)
    start_ch4 = find_peak(ch4)


    #Sort channels by when sound hit the mic
    channels = {'ch1' : start_ch1, 'ch2' : start_ch2, 'ch3' : start_ch3, 'ch4' : start_ch4}
    channels = {k: v for k, v in sorted(channels.items(), key=lambda item: item[1])}
    print(channels.keys())
    #Get firs 2 entries and store key and value in alist
    first_2 = [list(channels.items())[0], list(channels.items())[1]]
    return first_2


#return only one real direction of sound
def direction(path):

    data = read_csv(path)

    mic1 = list(normalize_shift(data[MIC_ORDER[0]]))           #   mic1        mic2
    mic2 = list(normalize_shift(data[MIC_ORDER[1]]))                   
    mic3 = list(normalize_shift(data[MIC_ORDER[2]]))
    mic4 = list(normalize_shift(data[MIC_ORDER[3]]))           #   mic3        mic4

   

    #Find max and avarage in mic 1 data.
    data_max = abs(max(mic1, key=abs))
    data_avg = sum(abs(number) for number in mic1)/len(mic1)

    #Get firs 2 channels hit by sound
    order = sort_channels(mic1, mic2, mic3, mic4)

    first_name = order[0][0]
    first_index = int(order[0][1])

    second_name = order[1][0]
    second_index = int(order[1][1])

    print('Channels hit first: {} and {}'.format(first_name, second_name))

    

    #Front
    if first_name == 'ch1' and second_name == 'ch2':
        cor = second_index - first_index
        offset = MIC1_MIC2
    elif first_name == 'ch2' and second_name == 'ch1':
        cor = first_index - second_index
        offset = MIC2_MIC1

    #Left:
    elif first_name == 'ch1'and second_name == 'ch3':
        cor = second_index - first_index
        offset = MIC1_MIC3
    elif first_name == 'ch3' and second_name == 'ch1':
        cor = first_index - second_index
        offset = MIC3_MIC1
    
    #right
    elif first_name == 'ch2'and second_name == 'ch4':
        cor = second_index - first_index
        offset = MIC2_MIC4
    elif first_name == 'ch4' and second_name == 'ch2':
        cor = first_index - second_index
        offset = MIC4_MIC2
    
    #back
    elif first_name == 'ch3' and second_name == 'ch4':
        cor = second_index - first_index
        offset = MIC3_MIC4
    elif first_name == 'ch4' and second_name == 'ch3':
        cor = first_index - second_index
        offset = MIC4_MIC3
    
    #exception: Sound should always hit 2 mics on the same side first.
    else:
        cor = None

    #calculate angle form cor
    print(cor)
    if cor != None:
        angle = shift_to_angle(cor) + offset
        print('Angle: {:.0f}'.format(angle))

        return angle





if __name__ == '__main__':
    direction('/Users/markuslang/Desktop/Python/intelligent-audio-listener/test_data/12_08_2022_16_14_16.csv')
    

