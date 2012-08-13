OBJECTS=main.o arch/atmega8/rs232.o arch/atmega8/analog.o

CC=avr-gcc
CXX=avr-g++
LD=avr-ld
AR=avr-ar
AS=avr-gcc
OBJCOPY=avr-objcopy
AVRDUDE=avrdude
OUTPUT=firmware.elf

CPUSPEED=20000000
HARDWARE=__AVR_ATmega48P__
CPUTYPE=m48pa
MCPUTYPE=atmega48p
CFLAGS=-O0 -c -w -fno-exceptions -ffunction-sections -fdata-sections -Wall -D$(HARDWARE) -mmcu=$(MCPUTYPE) -DF_CPU=$(CPUSPEED)

all: $(OBJECTS) 
	$(CC) -Os -Wl,--gc-sections -mmcu=$(MCPUTYPE) -o $(OUTPUT) -mavr6 -Map=$(OUTPUT).map $(OBJECTS) ../libs/kreatives-chaos/src/libcan.a -lm
	$(OBJCOPY) -O ihex -R.eeprom $(OUTPUT) $(OUTPUT).hex
	$(AVRDUDE) -p $(CPUTYPE) -cstk500v2  -P/dev/ttyACM0 -Uflash:w:$(OUTPUT).hex:i

clean: 
	rm -f $(OBJECTS) $(OUTPUT)


