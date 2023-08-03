#include <Arduino.h>
#include "modbus.h"

void setup()
{
  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);
  digitalWrite(RE, 0);
  digitalWrite(DE, 0);
  Serial.begin(115200);
  node.begin(1, Serial);                 // Slave ID as 1
  node.preTransmission(preTransmission); // Callback for configuring RS-485 Transreceiver correctly
  node.postTransmission(postTransmission);
  randomSeed(analogRead(0));
}

void loop()
{
  node.writeSingleRegister(0x40000, 5);
  node.writeSingleRegister(0x40001, 69);
}
