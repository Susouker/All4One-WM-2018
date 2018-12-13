
#define TIMEOUT 1500
#define PIN_OFFSET 2

#include <Servo.h>
#include <Wire.h>

Servo steering[4];
int targetPosition[4];

long lastUpdate;


void setup() {
  lastUpdate = millis();

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

  //VGC: soll mit Poti vergleichen und bewegen
  for (size_t i = 0; i < 4; i++) {
    int v = analogRead(i);
  }
}

void receiveEvent(int howMany) {
  lastUpdate = millis();
  if (howMany == 2) {
    int ident = Wire.read();
    int value = Wire.read() - 128;

    if ((ident & 0b00111100) == 32) { // Lenkung
      steering[ident & 0b00000011].write((value * 0.4476f) + 90);
    }

    if ((ident & 0b00111100) == 48) { // VGC
      targetPosition[(ident & 0b00000011)] = value;
    }

  }
}
