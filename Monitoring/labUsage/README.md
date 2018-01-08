labUsabe

gui.py

* Create program to configure XBEE module and STS parameters.

* Send testing message to XCTU app (module connected to a computer) and testing message (HS: 1.2) to the main server.

* To see more information on how each function works, refer to the document gui.py.


NOTE...!!!

* In order to send a message to the main server, the message must have a specific payload:

<=> FrameType NumFields # SerialID # WaspmoteID # Sequence # Sensor_1 # Sensor_2 # ... Sensor_n #

Now lets remember what the tx frame looks like:


"tx":

                        [{'name':'id',              'len':1,        'default':'\x10'},

                         {'name':'frame_id',        'len':1,        'default':'\x00'},

                         {'name':'dest_addr',       'len':8,        'default':None},

                         {'name':'reserved',        'len':2,         'default':'\xFF\xFE'},

                         {'name':'broadcast_radius', 'len':1,         'default':'\x00'},

                         {'name':'options',         'len':1,        'default':'\x00'},

                         {'name':'data',            'len':None,     'default':None}]

data parameter will contain the entire payload specified above.

* The entire payload is a STRING (is good to know when trying to concatenate any other value).

* This GUI uses the calibration for Fluorescence (which does not work properly), for instance the graph will look ugly.

* The buttons and entry boxes works perfect, then if another parameter is added and the program wont respond, then maybe do further test in the new features before adding them to the entire GUI.

* If any line of code is "weird", then maybe check tkInter documentation for python 2.7.

* The save parameter, reads the entry boxes and send those values as "at" commands..!!, so if any other parameter of the XBEE module needs to be configured, then use the "at" frame.

* HS is the name of the sensor in the main server, for instance, if another value for the sensor needs to be sent, then ask the tutor for help to create another sensors.

* Lets say TM (temperature) sensor is needed, then make a frame "tx" with the specific payload (<=> ..... #) with the new sensor, check check line 228 of the gui.py file to see how the function works.

* Any more relevant information will be continiously added here :)

