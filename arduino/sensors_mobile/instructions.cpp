#include "instructions.h"
#include "../common/UltrasonicSensor.h"
#include "../common/SensorListener.h"
#include <Servo.h>
#include "PIN.h"

// Global variables
extern UltrasonicSensor SensorAr;
extern UltrasonicSensor SensorAv;
extern SensorListener   ListenerAv;
extern SensorListener   ListenerAr;
extern bool activated; 
extern Servo sensorArm1;
extern Servo sensorArm2;

void GET_NORMAL(SerialTalks& inst, Deserializer& input, Serializer& output)
{
    int delta = input.read<int>();
    output.write(ListenerAv.getStd(delta));
    output.write(ListenerAv.getVar(delta));
    output.write(ListenerAr.getStd(delta));
    output.write(ListenerAr.getVar(delta));
}


void GET_MESURE(SerialTalks& inst, Deserializer& input, Serializer& output)
{
    output.write<int>(SensorAr.getMesure());
    output.write<int>(SensorAv.getMesure());
}

void ACTIVATE_SENSORS(SerialTalks& inst, Deserializer& input, Serializer& output){
    activated = true;
	if (!sensorArm1.attached())
        {
            sensorArm1.attach(SERVO1);
        }
    sensorArm1.write(90);
	if (!sensorArm2.attached())
        {
            sensorArm2.attach(SERVO2);
        }
    sensorArm2.write(90);
}

void DESACTIVATE_SENSORS(SerialTalks& inst, Deserializer& input, Serializer& output){
    activated = false;
    sensorArm1.write(180);
    sensorArm2.write(180);
}
