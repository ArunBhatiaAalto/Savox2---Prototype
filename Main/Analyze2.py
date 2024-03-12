
import matplotlib.pyplot as plt
import numpy as np
from numpy import append, array, concatenate, argmax
from scipy.fft import rfft, rfftfreq
from scipy.signal import fftconvolve
from scipy.signal import correlate
import scipy.io
import collections
from time import sleep

SAMPLE_RATE = 20000
MIC_DISTANCE = 0.20

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


def write(data):
    f = open("./out2.txt", "w")
    for i in data:
        f.write(str(i) + "\n")
    f.close()


#create a time vector
def create_x(data, rate, offset):
    x = []
    for i in range(0, len(data)):
        x.append(i/rate + offset)
    return x


def draw_fft(data, rate):
    ff = np.abs(np.fft.rfft(data))
    x = np.fft.fftfreq(len(ff), 1/rate)
    plt.plot(x,ff)
    plt.show()


def draw_func(data, rate, offset):
    x = create_x(data, rate, offset)
    plt.plot(x,data)
    plt.show()


def recording_length(data):
    length = len(data)/SAMPLE_RATE
    return length


def phase_offset(data, shift = -1):
    x  = collections.deque(data)
    x.rotate(shift)
    return x


def normalize_tone(shifted_tone):
    normalized = []
    a = (sum(shifted_tone)/(len(shifted_tone)))
   
    for p in range(len(shifted_tone)):
        normalized.append(shifted_tone[p] - a)
    return normalized


def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = np.sin((2 * np.pi) * frequencies)
    return x, y


def fourier_transform_dt(tone, dt = 30):                           
    fourier_time = []
    chunks = [tone[x:x+dt] for x in range(0, len(tone), dt)]
    x = []
    k = 1
    for n in range(len(chunks)):
        yf = rfft(chunks[n])   
        xf = rfftfreq(dt, 1 / SAMPLE_RATE)
        fourier = peaks(xf, yf)
        if len(fourier) > 0:
            fourier_time.append(fourier)             
            x.append(n * dt / SAMPLE_RATE)
            k += 1

    #Piirrä fourier ajan funktiona
    for xe, ye in zip(x, fourier_time):
        plt.scatter([xe] * len(ye), ye , c = "red")                      
    plt.show()
    return x, fourier_time
      

def peaks(x, y):
    dt = 30
    peak_list = []
    frequency_list = []
    chunk_size = int(dt / 10)
    absolute_value = np.abs(y)
    chunks = [absolute_value[x:x+chunk_size] for x in range(0, len(absolute_value), chunk_size)] 
    n = 0
    for i in range(len(chunks)):
        index = np.where(chunks[i] == np.amax(chunks[i]))
        if np.amax(chunks[i]) > 0:                                                  #Raja-arvo
            real_index = int(index[0]) + n * chunk_size
            peak_list.append(real_index)
            frequency_list.append(int(x[real_index]))
            n += 1
    print("Detected:{} (Hz)".format(frequency_list))
    return frequency_list   


def cross_correlate(left, right):
    difference = correlate(left, right)
    return difference


def direction(data, mic_distance, dt = 400):
    chunk_duration = dt/SAMPLE_RATE
    print(chunk_duration)
    delay = []
    time_axis = []   
    #Normalize data form both channels
    normalized_data_ch1 = normalize_tone(data[1])          
    normalized_data_ch2 = normalize_tone(data[3])
    #Split data to chunks wiht size dt.
    chunks_ch1 = [normalized_data_ch1[x:x+dt] for x in range(0, len(normalized_data_ch1), dt)]
    chunks_ch2 = [normalized_data_ch2[x:x+dt] for x in range(0, len(normalized_data_ch2), dt)]

    for i in range(len(chunks_ch1)):
        left = array (list (chunks_ch1[i]))      
        right = array (list (chunks_ch2[i]))
        #Phase shift for testing purpouses
        left_s = phase_offset(left)
        right_s =phase_offset(right)
        chunk_dt = (right, right_s)
        #filter out measurement errors
        if abs(max(left)) < 50:
            a = 0.0
        #Calculate angle
        else:                                             
            cor = (argmax(cross_correlate(chunk_dt[0], chunk_dt[1]))) - dt + 1  
            t = cor/SAMPLE_RATE
            sina = t*340/mic_distance
            a = np.sin(sina) * 180/(np.pi)
        time_axis.append(i * (dt/SAMPLE_RATE))
        delay.append(a)
        plt.plot(time_axis, delay)
    plt.show()
              

def fourier_trasnsform_sound():
    data = read_csv(r"C:\Users\marku\OneDrive\Desktop\intelligent-audio-listener-main\test_data\out6.csv")
    normalized = normalize_tone(data[1])          #datalistan indeksi: joko 0, 1 tai 3. Riippuen tiedostosta

    draw_func(normalized, SAMPLE_RATE, 0)
    fourier_transform_dt(normalized)

    array = np.array(normalized)
    scipy.io.wavfile.write("data.wav", SAMPLE_RATE, array)



def calculate_sound_direction():
    data = read_csv(r"C:\Users\marku\OneDrive\Desktop\intelligent-audio-listener-main\test_data\out6.csv")
    normalized = normalize_tone(data[1])
    draw_func(normalized, SAMPLE_RATE, 0)
    direction(data, MIC_DISTANCE)                  #Sound source angle as a function of time

if __name__ == "__main__":
    calculate_sound_direction()
    fourier_trasnsform_sound()

