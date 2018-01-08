Monitoring

Monitoring directory contains 2 more directories "labUsage" and "waterDep" which contain:

labUsage:

* gui.py -> python file that create a GUI interface to modify the STS spectrometer and XBEE PRO Digimesh parameters.
* for more information on how gui.py was implemented, please refer to the directory labUsage.

waterDep:

* finalDep.py -> python file that continiously read values from spectrometer and send the desired values using Digimesh.
* for more information on how finalDep.py was implemented, please refer to the directory eaterDep.

NOTE...!!!

* Before launching the prototype to the water, first use gui.py (from labUsage directory) to configure the XBEE PRO (Adress, pan ID, channel).
* After having the last calibration algorithm from oceanOp.py (from oceanOptics/Files directory), paste the same calibration in finalDep.py.
* Feel free to modify the code from gui.py (in order to add more features) or from finalDep.py (to change what is going to be sent by XBEE PRO Digimesh).