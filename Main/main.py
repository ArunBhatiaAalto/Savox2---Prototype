#!/bin/python

from display_driver import update_screen, update_text

update_text(["", "Loading"])

from inspect import getfile
import os
from sound_direction import direction
from CSV_2_WAV import make_csv
from testing2 import tunnistus
import time

#Data directory.
def get_files(dir):
    result = []
    for file in os.listdir(dir):
        result.append(file)
    
    return result


def main():
    tiedostot = get_files("/home/pi/intelligent-audio-listener/test_data")
    if len(tiedostot) > 0:
        time.sleep(0.2)
        input_file = "/home/pi/intelligent-audio-listener/test_data/" + str(tiedostot[0])
        output_file = input_file.replace(".csv", ".wav")
        output_file = output_file.replace("test_data", "test_data_wav")
        make_csv(input_file, output_file)
        sound = tunnistus(output_file)
    
        print(sound)
        suunta = direction(input_file)
        print(suunta)
        
        if suunta != None:
            update_screen(suunta, [str(sound),"","Suunta:", '{} astetta'.format(suunta)])
        else:
    	    update_text(["", sound])

        os.remove(input_file)
        os.remove(output_file)


if __name__ == "__main__":
    update_text(["", "Ready"])
    while True:
        main()
