# Intelligent audio listener

This is the software repository for the prototype project Intelligent audio listener. The aim of the project was to build a device which could classify sound sources and calculate their direction relative to the user.

This software was written for the Raspberry pi 4, but other pi models should be compatible with minor adjustments. The repository includes a pre-trained machine learning algorithm for sound classification.

### Building

Install the necessary Python dependencies:
```
dep1
dep2...
```

Enable SPI through the Raspberry's configuration interface accessed with:
```
raspi-config
```

Clone this repository and navigate to the chwspi directory in order to compile the SPI communicator:
```
git clone https://version.aalto.fi/gitlab/protopaja-savox-2/intelligent-audio-listener.git
cd intelligent-audio-listener/chwspi
make
```
Edit the source code in chwspi.c to suit the hardware configuratrion before compiling.

### Usage

Launch `chwspi/chwspi` and `Main/main.py` to start the program manually.
Optionally launch `app.sh` which enables operation with switches connected to gpio pins 17, 22 and 27. These have to be configured as inputs for this to work.

For example, pin 17 can be configured as an input with:
```
echo "17" > /sys/class/gpio/export
```
