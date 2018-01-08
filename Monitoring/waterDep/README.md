waterDep

finalDep.py

* Import files for digimesh and STS spectrometer.
* Import GPIO ibrary in order to use the GPIO pins in the raspberry pi.
* When the program starts, it create an instance of the object for XBEE and STS.
* When the instance for XBEE is created, then load the basic configuration such as MAC addr, destination addr, channel and pan id, use the destination addr to create the specific frame to communicate with the main server.


NOTE...!!!

* If we need to put the XBEE module to sleep, then send an at command (check the list of "at" commands given in /Phytoplanktonmonitoring/Xbee/Files/README.md).
* The program won't do anything unless it detects that the push button connected to pin 23 is being pressed.
* The program will run automatically as soon as the Raspberry Pi turns on (good when using batteries as power supply for the raspberry pi).
* Add the Fluorescence calibration at line 45 of the file finalDep.py (this will be the same calibration used in in the gui.py file).