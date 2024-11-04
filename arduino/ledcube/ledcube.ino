#include <SPI.h>

#define SS    10
#define MOSI  11
#define MISO  12
#define SCLK  13

int rcvIdx = 0;
uint8_t rcvData[64];

uint8_t spiBuff[128][8];

uint8_t getLayerBitDensity(uint8_t data[64], uint8_t index, uint8_t density){
  switch(index){
    case 0:
      return ((data[63]>density)<<7 | (data[62]>density)<<6 | (data[59]>density)<<5 | (data[58]>density)<<4 | (data[55]>density)<<3 | (data[54]>density)<<2 | (data[50]>density)<<1 | (data[51]>density));
    case 1:
      return ((data[47]>density)<<7 | (data[46]>density)<<6 | (data[43]>density)<<5 | (data[42]>density)<<4 | (data[39]>density)<<3 | (data[38]>density)<<2 | (data[34]>density)<<1 | (data[35]>density));
    case 2:
      return ((data[31]>density)<<7 | (data[30]>density)<<6 | (data[27]>density)<<5 | (data[26]>density)<<4 | (data[23]>density)<<3 | (data[22]>density)<<2 | (data[18]>density)<<1 | (data[19]>density));
    case 3:
      return ((data[15]>density)<<7 | (data[14]>density)<<6 | (data[11]>density)<<5 | (data[10]>density)<<4 | (data[7]>density)<<3 | (data[6]>density)<<2 | (data[2]>density)<<1 | (data[3]>density));
    
    case 4:
      return ((data[60]>density)<<7 | (data[61]>density)<<6 | (data[56]>density)<<5 | (data[57]>density)<<4 | (data[52]>density)<<3 | (data[53]>density)<<2 | (data[49]>density)<<1 | (data[48]>density));
    case 5:
      return ((data[44]>density)<<7 | (data[45]>density)<<6 | (data[40]>density)<<5 | (data[41]>density)<<4 | (data[36]>density)<<3 | (data[37]>density)<<2 | (data[33]>density)<<1 | (data[32]>density));
    case 6:
      return ((data[28]>density)<<7 | (data[29]>density)<<6 | (data[24]>density)<<5 | (data[25]>density)<<4 | (data[20]>density)<<3 | (data[21]>density)<<2 | (data[17]>density)<<1 | (data[16]>density));
    case 7:
      return ((data[12]>density)<<7 | (data[13]>density)<<6 | (data[8]>density)<<5 | (data[9]>density)<<4 | (data[4]>density)<<3 | (data[5]>density)<<2 | (data[1]>density)<<1 | (data[0]>density));
  }
}

void setup() {
  Serial.begin(115200);

  SPI.begin();
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV2);
  SPI.setDataMode(SPI_MODE0);
}

void loop() {
  while (Serial.available()) {
    uint8_t tmp = Serial.read();

    if (rcvIdx >= 63) {
      // full
      rcvData[63] = tmp;
      rcvIdx = 0;

      for(uint8_t density=0; density < 128; density++){
        for (uint8_t i = 0; i < 8; i++) {
          spiBuff[density][i] = getLayerBitDensity(rcvData, i, density);
        }
      }

    } else if (tmp == 255){
      // reset
      rcvIdx = 0;
    } else {
      //tmpは0-127
      rcvData[rcvIdx] = tmp;
      rcvIdx++;
    }
  }

  for(uint8_t density=0; density < 128; density++){
    for (uint8_t i = 0; i < 8; i++) {
      SPI.transfer(~(1 << i));
      SPI.transfer( spiBuff[density][i] );

      PORTB &= ~(_BV(PB2));
      PORTB |= _BV(PB2);
    }
  }
}
