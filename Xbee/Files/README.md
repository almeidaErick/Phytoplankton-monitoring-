FILES 

digimeshOp.py

* Information on how functions work are found inside of the file digimeshOp.py.
* The way to communicate to the XBEE PRO from the raspberry pi is through serial interface, and writing to that serial the specific frames (described below).
* No need to create functions to create more frames, those functions are defined for private used only, that public functions use to modified them internally, so no need to worry 
  about that.
  
EXAMPLE:

Run the program, and then write into idle:

  xbee_test = XBEE_PRO() 

Now xbee_test refers to an instance of XBEE_PRO(), now the functions from inside of the file digimeshOp.py can be used like:

  xbee_test.set_chan()

This function will ask the user to give a channel to set the XBEE module in order to communicate with the server. Thats all that needs to be known in order to use the functions from 
digimeshOp.py.
Now if more functions are needed to create in order to modify the XBEE PRO module, firts we need to know that the frame looks like this: 



  "at":             
  
                        [{'name':'id',        'len':1,      'default':'\x08'},
  
                         {'name':'frame_id',  'len':1,      'default':'\x00'},
                         
                         {'name':'command',   'len':2,      'default':None},
                         
                         {'name':'parameter', 'len':None,   'default':None}]


that frame is used in order to set different parameter values to the XBEE PRO, or simply by reading them ("at" -> use to modify and read). For a list of at commands refer to this link
(bibing.us.es/proyectos/abreproy/12027/fichero/Volumen4%252FCapitulo14.pdf). 

Inside of the frame:

* id -> \x08 specific for "at" command, if "tx" command is needed there is also a frame for that with id \x10.
* frame_id -> one byte long, could be any value it only helps to read responses with the same frame_id, example, you send an "at" command with frame_id "A", the response will have the same
  frame_id "A" (not neccesary to specify).
* command -> at command specified in the link from above.
* parameter -> value specified in order to modify that specific "at" command, if no parameter value is specified, then the response will be the reading of the current command inside of 
  the XBEE PRO module.

example to read the channel

  1.- xbee_test.xbee.send("at", frame_id='A', command='CH')
  
  2.- response = self.xbee.wait_read_frame()
  
  3.- chan_init = response['parameter'] 

chan_init will have the value for the channel read from XBEE PRO module.


example to write the channel

  1.- xbee_test.xbee.send("at", frame_id='A', command='CH', parameter="\x13")
  
  2.- response = self.xbee.wait_read_frame()

Thats all that needs to be known in order to use the XBEE PRO module.


NOTE...!!!

* "tx" frame not explained since the function from digimeshOp.py (xbee_test.send_data("hello world")) will do all the work. Instead of "Hello World" can go any string value.
* variable "response" will contain the entire response from a command, to see it just type (print response).
  

