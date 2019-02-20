// nano 0
// Lenkung und VGC

#define TIMEOUT 1500
#define PIN_OFFSET 2
#define THRESHOLD 6

#include <Servo.h>
#include <Wire.h>

long lastUpdate;

Servo steering[4];

int VGCtargetPosition[4] = {256,256,256,256};
int VGCmin[4] = {0,0,0,0};
int VGCmax[4] = {0,0,0,0};
float VGCfactor[4] = {0, 0, 0, 0};

void setup() {
  lastUpdate = millis();

  //Serial.begin(9600);

  readEEPROM();

  Wire.begin(0x30);
  Wire.onReceive(receiveEvent);

  for (size_t i = 0; i < 4; i++) { // Lenkung
    steering[i].attach(i + PIN_OFFSET);
  }
  for (size_t i = 0; i < 8; i++) { // VGC motor driver
    pinMode(i + 4 + PIN_OFFSET, OUTPUT);
  }
}

void loop() {
  //TIMEOUT -> Alles geht aus
  if (millis() > lastUpdate + TIMEOUT) {
    for (size_t i = 0; i < 4; i++) {
      steering[i].write(90);
    }
    for (size_t i = 0; i < 8; i++) {
      digitalWrite(i + 4 + PIN_OFFSET, LOW);
    }
  }
  moveVGC();
}

void moveVGC() {
  //VGC: Soll mit Poti vergleichen und bewegen
  //Strom auf den geraden Pins führt dazu, dass sich der VGC Arm hoch bewegt und der Poti-Wert kleiner wird
  for (size_t i = 0; i < 4; i++) {
    size_t pin = PIN_OFFSET + 4 + i * 2;

    int currentPos = (analogRead(i) - VGCmin[i]) * VGCfactor[i];
    int difference = currentPos - VGCtargetPosition[i];

    if (difference > THRESHOLD) {
      digitalWrite(pin, HIGH);
      digitalWrite(pin + 1, LOW);
    } else if (difference < -THRESHOLD) {
      digitalWrite(pin + 1, HIGH);
      digitalWrite(pin, LOW);
    } else {
      digitalWrite(pin, LOW);
      digitalWrite(pin + 1, LOW);
    }
  }
  delay(10);
}

void readEEPROM(){
  int value;
  uint8_t address;
  for (size_t m = 0; m < 2; m++) {
    for (size_t i = 0; i < 4; i++) {
      address = ((m<<3) + (i<<1));
      value = (EEPROM.read(address) << 8); // HIGH BYTE
      value += EEPROM.read(address + 1); // LOW BYTE

      if(m==0)
        VGCmin[i] = value;
      else
        VGCmax[i] = value;
    }
  }
  calcVGCfactors();
}

void writeEEPROM(){
  int value;
  uint8_t address;
  for (size_t m = 0; m < 2; m++) {
    for (size_t i = 0; i < 4; i++) {
      address = ((m<<3) + (i<<1));
      if(m==0)
        value = VGCmin[i];
      else
        value = VGCmax[i];

      EEPROM.write(address, (value >> 8) & 0xFF); // HIGH BYTE
      EEPROM.write(address + 1, value & 0xFF); //LOW BYTE
    }
  }
}

void calcVGCfactors(){
  for (size_t i = 0; i < 4; i++) {
    VGCfactor[i] = (float)256 / (VGCmax[i] - VGCmin[i]);
  }
}

void receiveEvent(int howMany) {
  lastUpdate = millis();
  if (howMany == 2) {
    uint8_t ident = Wire.read();
    int value = Wire.read() - 128;

    if ((ident & 0b00111100) == 32) { // Lenkung
      steering[ident & 0b00000011].write((value * 0.4476f) + 90);
      Serial.println(value);
    }

    if ((ident & 0b00111100) == 48) { // VGC
      VGCtargetPosition[(ident & 0b00000011)] = value;
    }

    if ((ident & 0b00111000) == 56) { // VGC min/max adj
      if(min(ident & 0b00000100))
        VGCmin[(ident & 0b00000011)] += value;
      else
        VGCmax[(ident & 0b00000011)] += value;

      calcVGCfactors();
    }

    if ((ident & 0b00111000) == 40) { // VGC min/max adj
      writeEEPROM();
    }

  }
}
