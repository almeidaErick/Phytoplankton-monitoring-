DEVELOP OF UNDERWATER CAMERA FOR PHYTOPLANKTON MONITORING AND WIRELESS COMMUNICATION VIA IoT SYSTEMS


This repository has 2 main directories "OceanOptics" and "Xbee" which contain:

Xbee

* Wireless communication module implemented in python 2.7.
* Wireless protocol used is DIGIMESH.
* Library used to implement predefined functions for Xbee PRO.
* For more specific information, refer to Xbee directory.

OceanOptics

* Spectrometer module implemented in python 2.7.
* Library used to implement predfefined functions for STS miniature spectrometer from Ocean Optics.
* For more specific information, refer to OceanOptics directory.


The other directory "Monitoring" does nos contain implementation for wireless communication or the spectrometer, but instead uses both objects (Digimesh and STS spectrometer) to make:

* Gui interface for lab use.
* Deployment program (lauch module into the water to continiously collect data to send it to the server).
* For more information about how each section works, refer to the directory "Monitoring".


NOTE...!!!!

* In order to use the program, move all the files from the main repository (Phytoplanktonmonitoring) to a same location.
* This entire project is designed entirely in PYTHON for the raspberry pi, in a future if something needs to be added but is not feasible to implement it in python, feel free to change the 
  programming language (Java is the best option for more features), all the code used here were originally made in Java or C++.
* Do not use programs such as Jython (python language that uses Java classes) since it is too slow when used in raspberry pi. (I havent tried cython -> Python language that uses C functions
  and C++ methods/functions. Feel free to test it if needed).
* The predefined libraries used for this project are properly referenced in their proper directory, inside of each directory you can find the information needed to use those libraries, if 
  more informations is needed, then a link to their specific repository has been added.  
* First use gui.py (phytoplanktonmonitoring/Monitoring/labUsage) to set up the XBEE module and STS spectrometer. After that open the terminal and type (sudo nano /etc/rc.local), after that 
  uncomment the line (python /home/pi/Documents/GattonProj/optics/finalDep.py &) and save the file. Now the next time the raspberry pi turn on, the program finalDep.py 
  (phytoplanktonmonitoring/Monitoring/waterDep) will continiously be running and collecting data.

This project was entirely made at The University Of Queensland (Gatton Campus).

Contact info:
Erick Almeida (erick.almeidachavez@uqconnect.edu.au).


Winter Extension:

Lora

* Wireless communication module implemented in python 2.7.
* Wireless protocol used is LORA on the Waspmote.
* All Libraries used developed by Libelium.
* Code made to read string ending in char 'c' for concentration vlaue and send to gateway.
* Purpose of Waspmote module is to regulate Pi and read data to upload to Meshelium through IoT.
* Code in directory commented.

Contact info: Abdifatah Aden (abdifatah.aden@uqconnect.edu.au).
