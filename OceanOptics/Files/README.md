FILES


This directory contains the file oceanOp.py, that do:

* Uses seabreeze library to use the STS Spectrometer.
* Stores the readings from the STS Spectrometer inside of python variables so we can use them later.
* Make graphs for reflection and fluorescence.

Example 

To make an instance of the object STS, we need run the python file oceanOp.py and write:

spec = STS() 

after that, we can use the function from that class like:

spec.calibrate_max() -> to store the maximum values for calibration.


NOTE....!!!!

* Calibration of reflectance (line 49 of oceanOp.py) can be compared with calibration from OceanView app in the image called reflectance.jpg (working properly).
* Calibration of fluorescence (line 73 of oceanOp.py) can be compared with calibration from OceanView app in the image called fluorescence.jpg (not working properly).
* Please check the file oceanOp.py and make a proper calibration for fluorescence (function read_samples_fluo(self)).
* After doing that, copy and paste the same function in the file phytoplanktonmonitoring/Monitoring/waterDep/finalDep.py.
