
#include <avr/io.h>
#include "../libs/kreatives-chaos/can.h"


prog_uint8_t can_filter[] =
{
    // Group 0
    MCP2515_FILTER(0),              // Filter 0
    MCP2515_FILTER(0),              // Filter 1

    // Group 1
    MCP2515_FILTER_EXTENDED(0),     // Filter 2
    MCP2515_FILTER_EXTENDED(0),     // Filter 3
    MCP2515_FILTER_EXTENDED(0),     // Filter 4
    MCP2515_FILTER_EXTENDED(0),     // Filter 5

    MCP2515_FILTER(0),              // Mask 0 (for group 0)
    MCP2515_FILTER_EXTENDED(0),     // Mask 1 (for group 1)
};


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
  DDRB |= _BV(2);

  // Versuche den MCP2515 zu initilaisieren
  if (!can_init(BITRATE_125_KBPS)) {
    rs232_sendString("Error (MCP2515 timeout)!\r\n");
	for (;;);
  } else {
    rs232_sendString("OK\r\n");
  }

  // Load filters and masks
  can_static_filter(can_filter);


  // initialisation complete: begin measuring.
  rs232_sendString("\r\n\r\nBeginning measurements: \r\n");

  // loop: read the sensors and broadcast results.
  while(1) {
    int v0 = analogRead(0);
    int v1 = analogRead(1);

    rs232_sendString("V0: ");
    rs232_sendInt(v0);
	rs232_sendString(", V1: ");
    rs232_sendInt(v1);
    rs232_sendString("\r\n");

    sendAsCAN(v0, v1);

	for(i=0;i<1000000;i++);
  }
}

void sendAsCAN(int v0, int v1) {
  can_t msg;

  msg.id = 0x0001;
  msg.flags.rtr = 0;
  msg.flags.extended = 1;

  msg.length = 4;
  msg.data[0] = (v0 & 0xff00) >> 8;
  msg.data[1] = v0 & 0xff;
  msg.data[2] = (v1 & 0xff00) >> 8;
  msg.data[3] = v0 & 0xff;

  // Send the message
  can_send_message(&msg);
}


