import serial
from xbee import DigiMesh
from binascii import unhexlify, hexlify
from time import sleep

"""
    This class create an instance for DigiMesh communication:
    Thursday, 12 January : function to set channel, pan ID, destination address, and also to send frames to the specified
                           address channel and panID. Also additiona functions to parse responses have been created, more
                           information for each function are specified below. (Example to create an instance of DigiMesh)
                           instance = XbeePro(). NOTE: all functions are AT command, the exception is for the function
                           send_data that is a TX command.
"""

class XBEE_PRO:

    """
        Initialize XbeePro instance, it check to which of the USB port it is connected (ttyUSB0 or ttyUSB1), also it sets
        the baudrate to 9600 (works better with this value you are free to try another baudrates: 2400, 4800, 9600, 19200,
        38400, 57600, 115200, 230400, 460800, 921600).
    """
    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyUSB1', 9600, 5)
        except serial.SerialException:
            print "Wrong port, trying with a different one"
            self.ser = serial.Serial('/dev/ttyUSB0', 9600, 5)
            
        self.xbee = DigiMesh(self.ser)
        self.dest_addr = '\x00\x13\xA2\x00\x40\xC1\x65\xCE'

        self.addr_init_low = '\x00\x00\x00\x00'
        self.addr_init_high = '\x00\x00\x00\x00'
        self.chan_init = '\x00'
        self.pan_init = '\x00\x00'

        sleep(5)

        self.load_init()

    def load_init(self):

        self.xbee.send("at", frame_id='A', command='AP', parameter="\x01")
        response = self.xbee.wait_read_frame()

        self.xbee.send("at", frame_id='F', command='WR')
        response = self.xbee.wait_read_frame()
        
        
        self.xbee.send("at", frame_id='A', command='CH')
        response = self.xbee.wait_read_frame()
        self.chan_init = response['parameter']

        self.xbee.send("at", frame_id='B', command='ID')
        response = self.xbee.wait_read_frame()
        self.pan_init = response['parameter']

        self.xbee.send("at", frame_id='C', command='DL')
        response = self.xbee.wait_read_frame()
        self.addr_init_low = response['parameter']

        self.xbee.send("at", frame_id='D', command='DH')
        response = self.xbee.wait_read_frame()
        self.addr_init_high = response['parameter']


        self.xbee.send("at", frame_id='A', command='AP', parameter="\x02")
        response = self.xbee.wait_read_frame()

        self.xbee.send("at", frame_id='F', command='WR')
        response = self.xbee.wait_read_frame()

        self.dest_addr = self.addr_init_high + self.addr_init_low



        """enable encryption"""
        self.xbee.send("at", frame_id='A', command='EE', parameter="\x01")
        response = self.xbee.wait_read_frame()
        

        """This encryption key represents "UQnetkeYUQnetkeY", if you want to change they key simply
        go to an online converter string->hex and the copy below in parameter, example:
        * if result string->hex = "58551556", then add the scape character before a byte,
        58551556 -> \x58\x55\x15\x56"""
        
        self.xbee.send("at", frame_id='A', command='KY', parameter="\x55\x51\x6e\x65\x74\x6b\x65\x59\x55\x51\x6e\x65\x74\x6b\x65\x59")
        response = self.xbee.wait_read_frame()


        self.xbee.send("at", frame_id='F', command='WR')
        response = self.xbee.wait_read_frame()
        

    """
        Set the channel to the DigiMesh antenna to communicate, you will be expecting 2 'OK' responses when you set this,
        one OK for setting the channel, and another one when writing to volatile memory in the device, if not then try
        again.
    """
    def set_chan(self):
        new_chan = raw_input("Enter new channel (from (0C to 17)): ")
        new_chan_hex = unhexlify(new_chan)

        #write the channel
        self.xbee.send("at", frame_id='A', command='CH', parameter=new_chan_hex)
        response = self.xbee.wait_read_frame()
        self.resp_at_parsing(response)

        #write to volatile memory
        self.xbee.send("at", frame_id='F', command='WR')
        response = self.xbee.wait_read_frame()
        self.resp_at_parsing(response)


    """
        Set the panID to the DigiMesh antenna to communicate, you will be expecting 2 'OK' responses when you set this,
        one OK for setting the panID, and another one when writing to volatile memory in the device, if not then try
        again.
    """
    def set_pan_id(self):
        new_pan = raw_input("Enter new PAN ID (from (0000 to FFFF)): ")
        new_pan_hex = unhexlify(new_pan)

        #write the pandID
        self.xbee.send("at", frame_id='B', command='ID', parameter=new_pan_hex)
        response = self.xbee.wait_read_frame()
        self.resp_at_parsing(response)

        #write to volatile memory
        self.xbee.send("at", frame_id='F', command='WR')
        response = self.xbee.wait_read_frame()
        self.resp_at_parsing(response)


    """
        Set the destination address of the DigiMesh antenna, the default value for this variable is 0013A20040C165CE,
        if you are working with a different address then use this function and the variable will change. The variable of the
        address will be used to create the frame that will be sent to the base. You will be expecting three 'OK's responses
        one for setting the LSB of the address, another one when setting the MSB of the address and the last one when
        writting to volatile memory of the device.
    """
    def set_dest_addr(self):
        lower = raw_input("Enter LSBytes (from (00000000 to FFFFFFFF)): ")
        lower_hex = unhexlify(lower)

        #write LSB of the destination address
        self.xbee.send("at", frame_id='C', command='DL', parameter=lower_hex)
        response = self.xbee.wait_read_frame()
        self.resp_at_parsing(response)

        #write MSB of the destination address
        upper = raw_input("Enter MSBytes (from (00000000 to FFFFFFFF)): ")
        upper_hex = unhexlify(upper)
        self.xbee.send("at", frame_id='D', command='DH', parameter=upper_hex)
        response = self.xbee.wait_read_frame()
        self.resp_at_parsing(response)

        #write to volatile memory
        self.dest_addr = upper_hex+lower_hex
        self.xbee.send("at", frame_id='F', command='WR')
        response = self.xbee.wait_read_frame()
        self.resp_at_parsing(response)


    """
        Send the frame to the base, we create a frame because the device is working in API2 mode, it does not matter
        if the receiver (base) is in transparent mode or API2, the message will be receive accordingly to what it is
        needed. Example is the base is set to API2 mode, then we receive the entire frame, if the base is set to
        transparent mode then it will receive only the data needed. 
    """
    def send_data(self, message):
        self.xbee.send("tx", frame_id='G', dest_addr=self.dest_addr, data=message)
        response = self.xbee.wait_read_frame()
        self.resp_tx_parsing(response)
        

    """
        Check status of the AT commands, if you want to be more specific on the responses you could add more of this
        options in the if statements, ['frame_id'] , ['command'] , ['status'] , ['parameter'].
    """
    def resp_at_parsing(self, response):
        if response['status'] == '\x00':
            print "OK"

        elif response['status'] == '\x01':
            print "ERROR"

        elif response['status'] == '\x02':
            print "Invalid Command"

        elif response['status'] == '\x03':
            print "Invalid Parameter"

        else:
            print "No Response"

            
    """
        Check status of the TX command, if you want to be more specific on the responses you could add more of this
        options in the if statements, ['frame_id'] , ['reserved'] , ['retries'] , ['deliver_status'] , ['discover_status']
    """
    def resp_tx_parsing(self, response):
        if response['deliver_status'] == '\x00':
            print "Success"

        elif response['deliver_status'] == '\x02':
            print "CCA Failure"

        elif response['deliver_status'] == '\x15':
            print "Invalid Destination Endpoint"

        elif response['deliver_status'] == '\x21':
            print "Network ACK Failure"

        elif response['deliver_status'] == '\x22':
            print "Not Joined to Network"

        elif response['deliver_status'] == '\x23':
            print "Self-addressed"

        elif response['deliver_status'] == '\x24':
            print "Address not found"

        elif response['deliver_status'] == '\x25':
            print "Route not found"

        else:
            print "No Response"

    def gui_save(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.xbee.send("at", frame_id='K', command=key, parameter=unhexlify(value))
            response = self.xbee.wait_read_frame()

            self.xbee.send("at", frame_id='F', command='WR')
            response = self.xbee.wait_read_frame()
            
            print response
        self.dest_addr = unhexlify(kwargs["DH"])+unhexlify(kwargs["DL"])
    

    """
        Close the serial communication of the DigiMesh antenna.
    """
    def close(self):
        self.xbee.halt()
        self.ser.close()

    
