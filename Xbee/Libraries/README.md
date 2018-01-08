Libraries

To install the library python-xbee, open the directory python-xbee and run the file setup.py. Thats all, now an example to use the library is specified below.

EXAMPLE

>>> import serial
>>> from xbee import DigiMesh

>>> serial_port = serial.Serial('/dev/ttyUSB0', 9600)
>>> xbee = DigiMesh(serial_port)

>>> while True:

>>> 	try:
>>> 		print xbee.wait_read_frame()
>>> 	except KeyboardInterrupt:
>>> 		break
		
>>> serial_port.close()

This example will perpetually read from the serial port and print out any data frames which arrive from a connected Xbee device.