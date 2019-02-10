/**
   NOTE: You must not use delay() or I2C communications will fail, use tws_delay() instead (or preferably some smarter timing system)

   You need to have at least 8MHz clock on the ATTiny for this to work (and in fact I have so far tested it only on ATTiny85 @8MHz using internal oscillator)
   Remember to "Burn bootloader" to make sure your chip is in correct mode
*/


#define I2C_SLAVE_ADDRESS 0x4 // the 7-bit address (remember to change this when adapting this example)

#include <TinyWireS.h>

#ifndef TWI_RX_BUFFER_SIZE
#define TWI_RX_BUFFER_SIZE ( 16 )
#endif

void requestEvent()
{
  int val = analogRead(1);
  if (digitalRead(2) == LOW)
    val /= 2;

  uint8_t v = val / 4;
  v = 42;
  TinyWireS.send(v);
}


/**
   The I2C data received -handler

   This needs to complete before the next incoming transaction (start, data, restart/stop) on the bus does
   so be quick, set flags for long running tasks to be called from the mainloop instead of running them directly,
*/
void receiveEvent(uint8_t howMany)
{
  if (howMany < 1 || howMany > TWI_RX_BUFFER_SIZE)
    return;

  uint8_t data;
  while (howMany--)
    data = TinyWireS.receive();

  PORTB = data & 0b00000111;
}


void setup()
{
  pinMode(2, INPUT_PULLUP);

  //RGB LED
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(7, OUTPUT);

  //MODE LEDs
  DDRB = 0b00000111;
  

  TinyWireS.begin(I2C_SLAVE_ADDRESS);
  TinyWireS.onReceive(receiveEvent);
  TinyWireS.onRequest(requestEvent);
}

void loop()
{
  /**
     This is the only way we can detect stop condition (http://www.avrfreaks.net/index.php?name=PNphpBB2&file=viewtopic&p=984716&sid=82e9dc7299a8243b86cf7969dd41b5b5#984716)
     it needs to be called in a very tight loop in order not to miss any (REMINDER: Do *not* use delay() anywhere, use tws_delay() instead).
     It will call the function registered via TinyWireS.onReceive(); if there is data in the buffer on stop.
  */
  TinyWireS_stop_check();
}
