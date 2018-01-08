# Purpose of file is to regulate measurements with pi
# When run will take a reading and send across serial to Waspmote
# Change mode at set controls section - bg means recording bg, samp means recording samp (only 1 should be true at a time)


# Includes
from numpy import *
import seabreeze.spectrometers as sb
import serial
import time
import matplotlib.pyplot as plt

# Initialize devices
spec = sb.Spectrometer(sb.list_devices()[0])
#sPort = serial.Serial("/dev/ttyUSB0", 115200, timeout = 1)

#load values
bgra = loadtxt("bgra.txt"); # background with light off without filter
bgrf = loadtxt("bgrf.txt"); # background with light on with filter 
# Read values
w = spec.wavelengths()
spec.integration_time_micros(12000000)

# set controls
bg = 0
samp = 1

# create background variable
bgr = array(w)*0

if bg:
    print("Recording Background")
    # Set background
    intS = array(spec.intensities())
    bgr = intS
    savetxt("bgr.txt", bgr)
    print("Background Recorded")
    time.sleep(2)
    
if (bg == 0):
    bgr = loadtxt("bgr.txt")

if samp:
    print("Recording Sample")
    spec.integration_time_micros(12000000)
    intS = array(spec.intensities())
    intS = intS - bgr
    print("Sample Recorded")

# Average values
fluo = (intS[104]+intS[105]+intS[106]+intS[107])/4.0
print fluo

# Calculate concentration
m = 3758011
c = 0
conc = (fluo - c)/m # mol/L
vol = 1000
molmca = 0.89351 # molar mass of chlorophyll a
mconc = conc*molmca # kg/L

mconc470 = long(mconc*1000000) # ug/L
print mconc470

plt.figure()
plt.plot(w, bgr)
plt.figure()
plt.plot(w, intS)
plt.show()

# Send concentration
#readMessage = sPort.readline()
#mString = readMessage.decode().strip()

# wait 1 second
#time.sleep(1)

if 0: #(mString == "E#")
        while(1):
            
            # write to waspmote
            print mconc470
            sPort.write("%dc" % mconc470)
            
            # wait 1 second
            time.sleep(7)
            
            # read from waspmote
            readMessage = sPort.readline()
            mString = readMessage.decode().strip()
            
            # if transmission sucess leave while loop
            if (mString == "ACK"):
                print("Sent!")
                break
            
            # let error be known and try again
            elif (mString == "NACK"):
                print("Not sent.. >:[")