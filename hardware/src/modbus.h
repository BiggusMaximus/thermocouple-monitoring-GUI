#include <ModbusMaster.h>
#define DE 3
#define RE 2

ModbusMaster node;

void preTransmission()
{
    digitalWrite(RE, 1);
    digitalWrite(DE, 1);
}
void postTransmission()
{
    digitalWrite(RE, 0);
    digitalWrite(DE, 0);
}