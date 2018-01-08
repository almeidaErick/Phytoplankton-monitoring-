#!/usr/bin/python

import digimeshOp , oceanOp
import sys
import RPi.GPIO as GPIO
from time import sleep
from binascii import unhexlify, hexlify


def close(comunic):
    comunic.close()
    sys.exit()


"""Send testing message in order to check if the format chosen for the message is the correct when sending to the main server"""
def send_sensor(comunic, counter, **kwargs):
    data = "<=>"
    id_wasp = "000000001"
    data = data + unhexlify("800" + str(len(kwargs))) + "#" + id_wasp + "#" + "HSS_01" + "#" + str(counter) + "#"
    print data
    for key, value in kwargs.iteritems():
        data = data + str(key) + ":" + str(value) + "#"

    comunic.send_data(data)
    return data



def communicate(comunic, spectra, maximum):
    """initiate counter here"""
    counter = 0
    num = 0

    """HSS is the name of the sensor, 1.2 is a random value (change this when calibration was done correctly)"""
    kwargs1 = {"HSS": "1.2"}
    while True:

        if num == 256:
            num = 0
            
        
        try:
            """Here make calculations to send according with the percentage of reflection"""
            read = spectra.spec.intensities()
            #
            #here copy the calibration algorithm for fluorescence
            #we have the variable maximum (background light) and the readings (read) 
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #

            send_sensor(comunic, num, **kwargs1)

            #adding a counter for the messages sent
            num = num + 1
            
        except KeyboardInterrupt:
            print "Forced exit, bye..!!!"
            close(comunic)
            return
        
        #here put the period of time that the xbee must wait between transmissions
        sleep(5)


        

"""Start using fluorescence calibration method, is reflectance method is needed then
add another button on pin 24 for example"""
def main():
    spectra = oceanOp.STS()
    comunic = digimeshOp.XBEE_PRO()

    # set GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    #enable a pull-down resistor on pin 23
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    #wait until the button is pressed
    GPIO.wait_for_edge(23, GPIO.RISING)

    print "starting transmission"

    maximum = spectra.spec.intensities()
    
    GPIO.cleanup()
    
    communicate(comunic, spectra, maximum)



if __name__ == '__main__':
    main()
