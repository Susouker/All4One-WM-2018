// nano 1
// TowBar und Throttle

#define TIMEOUT 1500
#define PIN_OFFSET 2
#define THRESHOLD 4

#include <Wire.h>
#include <SoftPWM.h>

long lastUpdate;

SOFTPWM_DEFINE_CHANNEL(0, DDRD, PORTD, PORTD2);  //Arduino pin 2
SOFTPWM_DEFINE_CHANNEL(1, DDRD, PORTD, PORTD3);  //Arduino pin 3
SOFTPWM_DEFINE_CHANNEL(2, DDRD, PORTD, PORTD4);  //Arduino pin 4
SOFTPWM_DEFINE_CHANNEL(3, DDRD, PORTD, PORTD5);  //Arduino pin 5
SOFTPWM_DEFINE_CHANNEL(4, DDRD, PORTD, PORTD6);  //Arduino pin 6
SOFTPWM_DEFINE_CHANNEL(5, DDRD, PORTD, PORTD7);  //Arduino pin 7
SOFTPWM_DEFINE_CHANNEL(6, DDRB, PORTB, PORTB0);  //Arduino pin 8
SOFTPWM_DEFINE_CHANNEL(7, DDRB, PORTB, PORTB1);  //Arduino pin 9
SOFTPWM_DEFINE_CHANNEL(8, DDRB, PORTB, PORTB2);  //Arduino pin 10
SOFTPWM_DEFINE_CHANNEL(9, DDRB, PORTB, PORTB3);  //Arduino pin 11

SOFTPWM_DEFINE_OBJECT_WITH_PWM_LEVELS(10, 128);

int towBarTargetPosition = 128;
int towBarMin = 270;
int towBarMax = 740;
float towBarFactor = 0;

void setup() {
  lastUpdate = millis();

  Wire.begin(0x31);
  Wire.onReceive(receiveEvent);

  Palatis::SoftPWM.begin(60);

  for (size_t i = 0; i < 10; i++) { // MotorDriver outputs
    pinMode(i + PIN_OFFSET, OUTPUT);
  }

  towBarFactor = (float)256 / (towBarMax - towBarMin);
}

void loop() {
  //TIMEOUT -> Alles geht aus
  if (millis() > lastUpdate + TIMEOUT) {
    for (size_t i = 0; i < 10; i++) {
      Palatis::SoftPWM.set(i + PIN_OFFSET, 0);
    }
  }

  //TowBar: soll mit Poti vergleichen und bewegen
  int currentPos = (analogRead(0) - towBarMin) * towBarFactor;
  int difference = currentPos - towBarTargetPosition;

  if (difference > THRESHOLD) {
    Palatis::SoftPWM.set(8, 10 + difference * 0.7);
    Palatis::SoftPWM.set(9, 0);
  } else if (difference < -THRESHOLD) {
    Palatis::SoftPWM.set(9, 10 - difference * 0.7);
    Palatis::SoftPWM.set(8, 0);
  } else {
    Palatis::SoftPWM.set(8, 0);
    Palatis::SoftPWM.set(9, 0);
  }
}


void receiveEvent(int howMany) {
  lastUpdate = millis();
  if (howMany == 2) {
    int ident = Wire.read();
    int value = Wire.read();

    if ((ident & 0b00111100) == 32) { // TowBar
      towBarTargetPosition = value;
    }

    value -= 128;

    if ((ident & 0b00111100) == 48) { // Throttle
      size_t pin = ((ident & 0b00000011) * 2);
      if (value > 0) {
        Palatis::SoftPWM.set(pin, value);
        Palatis::SoftPWM.set(pin + 1, 0);
      } else if (value < 0) {
        Palatis::SoftPWM.set(pin + 1, -value);
        Palatis::SoftPWM.set(pin, 0);
      } else {
        Palatis::SoftPWM.set(pin, 0);
        Palatis::SoftPWM.set(pin + 1, 0);
      }
    }

  } else { // iwas falsch also lesen und ignorieren
    while (Wire.available())
      Wire.read();
  }
}
