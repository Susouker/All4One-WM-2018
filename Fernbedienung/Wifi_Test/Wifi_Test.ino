#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Wire.h>

#define SLAVE_ADR 0x04

const char* ssid = "ADHV4K";
const char* password = "MollisWinter2019";
const char* host = "192.168.178.40";
const int   port = 14044;

const int led = 13;

WiFiClient client;

long nextUpdate = 0;
int refreshRate = 20;

uint8_t butNum[7] = {16, 0, 2, 14, 12, 13, 15};
bool butPressed[7] = {0, 0, 0, 0, 0, 0, 0};

uint8_t steeringMode = 0;

uint8_t receivedData[32];

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  for (int i = 0; i < sizeof(butNum); i++) {
    pinMode(butNum[i], INPUT_PULLUP);
    butPressed[i] = digitalRead(butNum[i]) == LOW;
  }

  Wire.begin();

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  nextUpdate = millis();
}

void connectToServer() {
  while (!client.connect(host, port)) {
    Serial.println("connection failed");
    delay(1000);
  }
  Serial.println("connected");
}

void loop() {
  if (millis() > nextUpdate) {

    //if disconnected: Auto reconnect
    if (!client.connected()) {
      Serial.println("disconnected");
      connectToServer();
    }

    //receive Data
    uint8_t lenght = 0;
    while (client.available()) {
      receivedData[lenght] = client.read();
      lenght++;
    }

    //interpret Data
    uint8_t index = 0;
    while (lenght > index) {
      char identifier = receivedData[index];
      Serial.println(identifier);
      switch (identifier) {
        case 'M':
          setModeLights(receivedData[index + 1]);
          index += 2;
          break;
        default:
          Serial.println("ERR:Ident");
          index++;
          break;
      }
    }

    //send Data
    sendSteeringData(false);
    refreshButtons();


    //
    if (millis() > nextUpdate + refreshRate)
      nextUpdate = millis();
    nextUpdate += refreshRate;
  }
}

void setModeLights(uint8_t newMode) {
  uint8_t toWrite = 0;
  if ((newMode & 0b11111100) == 4) {
    toWrite = 0b00000001;
  } else if (newMode == 20) {
    toWrite = 0b00000010;
  } else if (newMode == 28) {
    toWrite = 0b00000100;
  }
  Wire.beginTransmission(SLAVE_ADR);
  Serial.print("writing to i2c: ");
  Serial.println(toWrite);
  Wire.write(toWrite);
  Wire.endTransmission();
}

uint8_t lastSteering = 0;
uint8_t lastThrottle = 0;

void sendSteeringData(bool force) {
  Wire.requestFrom(SLAVE_ADR, 1);

  uint8_t throttle;
  if (Wire.available()) {
    throttle = Wire.read();
  } else {
    throttle = 128;
    Serial.println("no Throttle input");
  }

  uint8_t steering = (analogRead(0) >> 2) & 0xFF;
  if (butPressed[6])
    steering = (steering >> 1) + 64;
  /*
    Serial.print(throttle);
    Serial.print(",");
    Serial.println(steering);
  */

  if (force || abs(steering - lastSteering) > 1 || abs(throttle - lastThrottle) > 1) {
    const uint8_t toSend[] = {'s', steering, throttle};
    client.write(toSend, sizeof(toSend));

    lastSteering = steering;
    lastThrottle = throttle;
  }
}

void refreshButtons() {
  bool tmp = false;
  for (int i = 0; i < sizeof(butNum); i++) {
    tmp = digitalRead(butNum[i]) == LOW;
    if (butPressed[i] != tmp) {
      butPressed[i] = tmp;
      if (i < 5) {
        if (i < 3 && tmp)
          steeringMode = i;
        sendModeData();
      } else if (i == 5) {
        const uint8_t toSend[] = {'Q', tmp};
        client.write(toSend, sizeof(toSend));
      }
    }
  }
}

void sendModeData() {
  uint8_t m = 4;

  switch (steeringMode) {
    case 0:
      if (butPressed[3])
        m = 6;
      if (butPressed[4])
        m = 7;
      break;
    case 1:
      m = 20;
      break;
    case 2:
      m = 28;
      break;
  }

  const uint8_t toSend[] = {'M', m};
  client.write(toSend, sizeof(toSend));
  sendSteeringData(true);
}
