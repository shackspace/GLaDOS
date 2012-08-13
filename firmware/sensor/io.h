
#define BAUD 9600
#define sbi(sfr, bit) (_SFR_BYTE((sfr)) |= _BV((bit)))
#define cbi(sfr, bit) (_SFR_BYTE((sfr)) &= ~(_BV((bit))))


