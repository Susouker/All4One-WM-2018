
#define TIMEOUT 1500
#define PIN_OFFSET 2
#define THRESHOLD 4

#include <Servo.h>
#include <Wire.h>

long lastUpdate;

Servo steering[4];

int VGCtargetPosition[4] = {100,100,100,100};
int VGCmin[4] = {310,555,480,510};
int VGCmax[4] = {460,777,630,660};

void setup() {
  lastUpdate = millis();

  Serial.begin(9600);

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

  //VGC: Soll mit Poti vergleichen und bewegen
  //Strom auf den geraden Pins führt dazu, dass sich der VGC Arm hoch bewegt und der Poti-Wert kleiner wird
  for (size_t i = 0; i < 4; i++) {
    int currentPos = analogRead(i) * (VGCmax[i] - VGCmin[i]) / 1024 + VGCmin[i];
    int difference = currentPos - VGCtargetPosition[i];
    size_t pin = PIN_OFFSET + 4 + i * 2;
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

void receiveEvent(int howMany) {
  lastUpdate = millis();
  if (howMany == 2) {
    int ident = Wire.read();
    int value = Wire.read() - 128;

    if ((ident & 0b00111100) == 32) { // Lenkung
      steering[ident & 0b00000011].write((value * 0.4476f) + 90);
      Serial.println(value);
    }

    if ((ident & 0b00111100) == 48) { // VGC
      VGCtargetPosition[(ident & 0b00000011)] = value;
    }

  }
}
