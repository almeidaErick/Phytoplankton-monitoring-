/*  
 *  ----- [SX_06c] - TX to Meshlium (with ACKs) ----- 
 *
 *  Read Value from Serial and Send to Meshelium over Lora
 */

// Include this library to transmit with sx1272
#include <WaspSX1272.h>
#include <WaspFrame.h>

// define the Waspmote ID 
//////////////////////////////////////////
char nodeID[] = "SP_01";
//////////////////////////////////////////

// Define the Meshlium address to send packets
// The default Meshlium address is '1'
uint8_t meshlium_address = 1;

// USB reads 1 byte at a time so add to an array 20 characters long
char rChar;
char rMessage[21];
// Value being sent should be a float
int value;

// status variable
int e;
uint8_t cnt = 0;
uint8_t send_message_flag = 0;

void setup()
{
  // Init USB port
  USB.ON();
  //USB.println(F("SX_06c example"));
  //USB.println(F("Semtech SX1272 module. TX in LoRa to MESHLIUM (with ACKs)"));

  // Switch ON RTC
  RTC.ON();

  // Switch ON ACC
  ACC.ON();

  // set the Waspmote ID
  frame.setID(nodeID);  

  //USB.println(F("----------------------------------------"));
  //USB.println(F("Setting configuration:")); 
  //USB.println(F("----------------------------------------"));
  
  // Init sx1272 module
  sx1272.ON();

  // Select frequency channel
  e = sx1272.setChannel(CH_12_900);
  //USB.print(F("Setting Channel CH_12_900.\t state ")); 
  //USB.println(e);

  // Select implicit (off) or explicit (on) header mode
  e = sx1272.setHeaderON();
  //USB.print(F("Setting Header ON.\t\t state "));  
  //USB.println(e); 

  // Select mode (mode 1)
  e = sx1272.setMode(1);  
  //USB.print(F("Setting Mode '1'.\t\t state "));
  //USB.println(e);  

  // Select CRC on or off
  e = sx1272.setCRC_ON();
  //USB.print(F("Setting CRC ON.\t\t\t state "));
  //USB.println(e); 

  // Select output power (Max, High or Low)
  e = sx1272.setPower('H');
  //USB.print(F("Setting Power to 'H'.\t\t state ")); 
  //USB.println(e); 

  // Select the node address value: from 2 to 255
  e = sx1272.setNodeAddress(25);
  //USB.print(F("Setting Node Address to '25'.\t state "));
  //USB.println(e);
  //USB.println();

  delay(1000);

  //USB.println(F("----------------------------------------"));
  //USB.println(F("Sending:")); 
  //USB.println(F("----------------------------------------"));
}


void loop()
{

  // get Time from RTC
  RTC.getTime();
  
  // get Value from serial
  if(USB.available() > 0) {
    
    
    // convert from char represenation to equivalent int
    rChar = USB.read();
    if(rChar == 'c') {
      rChar = '\0';
    }
    
    // if buffer overflow
    if(cnt > 20){
      Utils.blinkRedLED(200, 5);
      if(((rChar == '\n') || (rChar == '\0'))){
        // Reset counter
        cnt = 0;
      }
      // Always do nothing in the overflow case
      return;
    }
    
    // if buffer didn't overflow add char to buffer
    rMessage[cnt++] = rChar;
    
    // if newline char or string terminator before end of buffer
    if(((rChar == '\n') || (rChar == '\0')) && cnt <= 20){
      // Reset counter and run
      cnt = 0;
      send_message_flag = 1;
      
      // Convert string to float
      value = atoi(rMessage);
      memset(rMessage, 0 , sizeof(rMessage));
    }
    
    // Allowed to send message
    if (send_message_flag) {
      ////////////////////////////////////////////
      // 1. Create ASCII frame
      ///////////////////////////////////////////  
    
      //USB.println(F("Create a new Frame:"));
      
      // create new frame
      frame.createFrame(ASCII);  
    
      // add frame fields - remove every unnecessary one
  //    frame.addSensor(SENSOR_DATE, RTC.date, RTC.month, RTC.year);
  //    frame.addSensor(SENSOR_TIME, RTC.hour, RTC.minute, RTC.second);
      frame.addSensor(SENSOR_BAT, PWR.getBatteryLevel()); 

      frame.addSensor(SENSOR_PP, value);

      // Prints frame
      //frame.showFrame();
    
      ///////////////////////////////////////////
      // 2. Send packet
      ///////////////////////////////////////////  
    
      // Sending packet before ending a timeout
      e = sx1272.sendPacketTimeoutACK( meshlium_address, frame.buffer, frame.length );
      
      // if ACK was received check signal strength
      if( e == 0 )
      { 
        // Will replace serial sending with LED flickers
        Utils.blinkGreenLED(200, 5);
        USB.println(F("ACK"));       
        
  //      USB.println(F("Packet sent OK"));  
  
  //      e = sx1272.getSNR();
  //      USB.print(F("-> SNR: "));
  //      USB.println(sx1272._SNR); 
        
  //      e = sx1272.getRSSI();
  //      USB.print(F("-> RSSI: "));
  //      USB.println(sx1272._RSSI);   
        
  //      e = sx1272.getRSSIpacket();
  //      USB.print(F("-> Last packet RSSI value is: "));    
  //      USB.println(sx1272._RSSIpacket); 
      }
      else 
      { 
        // Will replace serial sending with LED flickers
        Utils.blinkRedLED(200, 5);
        USB.println(F("NACK")); 
  
  //      USB.println(F("Error sending the packet"));  
  //      USB.print(F("state: "));
  //      USB.println(e, DEC);
      }
      
  //    USB.println();
      send_message_flag = 0;
      delay(5000);
    }
    
  }
}