/** 
 * rs232.c 
 * 
 * GLADOS project (shackspace)
 * file by rel0c
 * 
 * No license yet.
 */

#include "../../io.h"
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/setbaud.h>

/** 
 * inits the hardware uart on the atmega to a given baudrate.
 */
void rs232_init() {
  DDRD   |= _BV(1);						// enable UART Pin on PORTD
  UBRR0   = (F_CPU / 16 / BAUD);

//#if USE_2X
//   /* U2X-Modus erforderlich */
//   UCSR0A |= (1 << U2X0);
//#else
//   /* U2X-Modus nicht erforderlich */
//   UCSR0A &= ~(1 << U2X0);
//#endif

  UCSR0A = 0x00; 
  UCSR0B = _BV(TXEN0) | _BV(RXEN0);				// enable for read & write
  UCSR0C = _BV(USBS0) | _BV(UCSZ01) |_BV(UCSZ00); 	 	// enable for async transfer 8N1
}

void rs232_sendByte(char x) {
  while (!(UCSR0A & (1<<UDRE0)));
  
  UDR0 = x;
}

void rs232_sendString(char* x) {
  while(*x) {
    rs232_sendByte(*x);
	x++;
  }
}

void rs232_sendInt(int x) {
  char output[11];
  int cur = 9;

  output[10] = '\0';
  output[9] = '0';

  while(x != 0 && cur >= 0) {
    output[cur--] = (x % 10) + '0';
    x /= 10;
  }

  rs232_sendString( &output[cur] );
}

char rs232_recvByte() {
  while(!(UCSR0A & (1<<RXC0)));

  return UDR0;
}

char rs232_rtr() {
  return (!(UCSR0A & (1<<RXC0)));
}



