#include <Arduino.h>

#include "../common/SerialTalks.h"

    int i;
    bool t;
void setup() {
    pinMode(2,OUTPUT);
    pinMode(4,OUTPUT);
    pinMode(23,OUTPUT);
    pinMode(19,OUTPUT);
    pinMode(5,OUTPUT);
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
    digitalWrite(2,LOW);
    digitalWrite(4,LOW);
    digitalWrite(19,LOW);
    digitalWrite(5,LOW);
    digitalWrite(23,HIGH);

}
void loop() {
i++;
try{
talks.execute();
}catch(int e){
    ;
}
if(i>100000){
    if(t){
    digitalWrite(19,HIGH);
    }else{
    digitalWrite(19,LOW);
    }

    t = !t;
    i = 0;

}



}

