
#define TIMEOUT 1500
#define PIN_OFFSET 2

#include <Wire.h>
#include <SoftPWM.h>
SOFTPWM_DEFINE_CHANNEL(2, DDRD, PORTD, PORTD2);  //Arduino pin 2
SOFTPWM_DEFINE_CHANNEL(3, DDRD, PORTD, PORTD3);  //Arduino pin 3
SOFTPWM_DEFINE_CHANNEL(4, DDRD, PORTD, PORTD4);  //Arduino pin 4
SOFTPWM_DEFINE_CHANNEL(5, DDRD, PORTD, PORTD5);  //Arduino pin 5
SOFTPWM_DEFINE_CHANNEL(6, DDRD, PORTD, PORTD6);  //Arduino pin 6
SOFTPWM_DEFINE_CHANNEL(7, DDRD, PORTD, PORTD7);  //Arduino pin 7
SOFTPWM_DEFINE_CHANNEL(8, DDRB, PORTB, PORTB0);  //Arduino pin 8
SOFTPWM_DEFINE_CHANNEL(9, DDRB, PORTB, PORTB1);  //Arduino pin 9


int towBarTargetPosition;


void setup() {
  lastUpdate = millis();

  Wire.begin(0x30);
  Wire.onReceive(receiveEvent);

  for (size_t i = 0; i < 10; i++) { // MotorDriver outputs
    pinMode(i + PIN_OFFSET, OUTPUT);
  }
}

void loop() {
  //TIMEOUT -> Alles geht aus
  if (millis() > lastUpdate + TIMEOUT) {
    for (size_t i = 0; i < 10; i++) {
      digitalWrite(i + PIN_OFFSET, LOW);
    }
  }

  //TowBar: soll mit Poti vergleichen und bewegen
  int v = analogRead(A0);
}


void receiveEvent(int howMany) {
  lastUpdate = millis();
  if (howMany == 2) {
    int ident = Wire.read();
    int value = Wire.read() - 128;

    if ((ident & 0b00111100) == 96) { // TowBar
      towBarTargetPosition = value;
    }

    if ((ident & 0b00111100) == 112) { // Throttle
        size_t pin = PIN_OFFSET + ((ident & 0b00000011) * 2);
        if (value > 0) {
          digitalWrite(pin + 1, LOW);
          //PWM
        } else if (value < 0) {
          digitalWrite(pin, LOW);
          //PWM
        } else {
          digitalWrite(pin, LOW);
          digitalWrite(pin + 1, LOW);
        }
    }
    
  }
}
