
#define TIMEOUT 1500

#define PIN_SREVO_STEERING_FR 0
#define PIN_SREVO_STEERING_FL 0
#define PIN_SREVO_STEERING_BR 0
#define PIN_SREVO_STEERING_BL 0

#define PIN_MOTOR_FR_0 0
#define PIN_MOTOR_FR_1 0
#define PIN_MOTOR_FL_0 0
#define PIN_MOTOR_FL_1 0
#define PIN_MOTOR_BR_0 0
#define PIN_MOTOR_BR_1 0
#define PIN_MOTOR_BL_0 0
#define PIN_MOTOR_BL_1 0


#include <Servo.h>

Servo steeringFR;
Servo steeringFL;
Servo steeringBR;
Servo steeringBL;

long lastUpdate;


void setup() {
  lastUpdate = millis();

}

void loop() {
  
  if (millis() > lastUpdate + TIMEOUT) {
    //Alles stoppen und so was
    
  }

}
