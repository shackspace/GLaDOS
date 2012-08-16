/** 
 * analog.c 
 * 
 * GLADOS project (shackspace)
 * file by rel0c
 * 
 * No license yet.
 */

#include "../../io.h"
#include <avr/io.h>

int analogRead(uint8_t pin) {
  uint8_t low, high;

  // currently we only read from channels 0 to 7 or 8 to 15, uCs with 
  // more ports that support ADC are not supported. Theese should be 
  // PC0 to PC5
  // ADCSRB = (ADCSRB & ~(1 << MUX5)) | (((pin >> 3) & 0x01) << MUX5);

  // set the reference to be the internal VCC (AVCC)
  ADMUX = (1 << 6) | (pin & 0x07);

  // start the conversion
  sbi(ADCSRA, ADSC);

  // ADSC is cleared when the conversion finishes
  while (bit_is_set(ADCSRA, ADSC));

  // read ADCL first; this locks ADCH until ADCH is being read.
  low  = ADCL;
  high = ADCH;

  return (high << 8) | low;
}

void adc_init() {
  // enable and init ADC for ~150kHZ
  //  -> prescaling by 128
  rs232_sendString("Initialising ADC ... ");
  ADCSRA = (1<<ADEN) | (1<<ADPS2) | (1<<ADPS1) | (1<<ADPS0);
  rs232_sendString("OK\r\n");

  // enable reading on PORT C (ADC)
  rs232_sendString("Enabling Analog Reading Ports ... ");
  PORTC = 0x00;
  rs232_sendString("OK\r\n");
}


