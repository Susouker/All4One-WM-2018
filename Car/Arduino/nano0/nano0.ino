
#define TIMEOUT 1500

#include <Servo.h>
#include <Wire.h>

Servo steering[4];

long lastUpdate;


void setup() {
  lastUpdate = millis();

  Wire.begin(0x30);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);           // start serial for output

  for (size_t i = 0; i < 4; i++) {
    steering[i].attach(i);
  }
  for (size_t i = 0; i < 8; i++) {
    pinMode(i + 4, OUTPUT);
  }
}

void loop() {

  if (millis() > lastUpdate + TIMEOUT) {
      for (size_t i = 0; i < 4; i++) {
        steering[i].write(90);
      }
      for (size_t i = 0; i < 8; i++) {
        digitalWrite(i + 4, LOW);
      }
  }

}

void receiveEvent(int howMany) {
  lastUpdate = millis();
  while (1 < Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
  }
  int x = Wire.read();    // receive byte as an integer
  Serial.println(x);         // print the integer
}
