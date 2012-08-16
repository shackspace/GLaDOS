
#include <avr/io.h>
#include "../libs/kreatives-chaos/can.h"

long i=0;

int main() {
  // SETUP
  //   - initialise serial port to 9600baud
  rs232_init();  
  rs232_sendString("\r\n\r\n--- GLaDOS --- \r\n");
  rs232_sendString("GLaDOS sensor-board booting up...\r\n");

  //   - initialise the sensors.
  adc_init();
  
  //   - setup CAN-interface
  rs232_sendString("Initialising CAN-Bus interface...");
  DDRD = _BV(5);
  PORTD ^= _BV(5);
  PORTD |= _BV(5);

  // Versuche den MCP2515 zu initilaisieren
  if (!can_init(BITRATE_125_KBPS)) {
    rs232_sendString("Error (MCP2515 timeout)!\r\n");
	for (;;);
  } else {
    rs232_sendString("OK\r\n");
  }

  // initialisation complete: begin measuring.
  rs232_sendString("\r\n\r\nBeginning measurements: \r\n");

  // loop: read the sensors and broadcast results.
  while(1) {
    rs232_sendString("V0: ");
    rs232_sendInt(analogRead(0));
	rs232_sendString(", V1: ");
    rs232_sendInt(analogRead(1));
    rs232_sendString("\r\n");

	for(i=0;i<1000000;i++);
  }
}


