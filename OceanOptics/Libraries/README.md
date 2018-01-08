Libraries

To install the library python-seabreeze, open the directory python-seabreeze and run the file setup.py. The library will now be installed properly and can be used in a python program

EXAMPLE

>>> import seabreeze.spectrometers as sb

>>> devices = sb.list_devices()

>>> print devices

[<SeaBreezeDevice STS: S05753>]

>>> spec = sb.Spectrometer(devices[0])

>>> spec.integration_time_micros(12000)

>>> spec.wavelengths()

array([  633.60461426,   634.06913177,   634.53368059, ...,  1124.18028027,
        1124.67676501,  1125.17328106])

>>> spec.intensities()

array([ 1572.,  1555.,  1560., ...,  1535.,  1531.,  1521.])

For a more detailed use of this library, please refer to the file oceanOp.py.
