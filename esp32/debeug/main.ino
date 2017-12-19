#include <Arduino.h>



int pin[] = {22,5,4,27,26,14,12,13};

bool reset = false;
void setup() {
    Serial.begin(9600);

    for(int i = 0 ; i <8;i++){
        pinMode(pin[i],OUTPUT);
        digitalWrite(pin[i],HIGH);
        delay(100);

    }
    pinMode(2,OUTPUT);
    digitalWrite(2,LOW);
    pinMode(19,OUTPUT);
    digitalWrite(19,LOW);
    for(int i = 7; i >=0;i--) {
        digitalWrite(pin[i],LOW);
        delay(100);

    pinMode(23,INPUT_PULLUP);
    }
}
int i = 0;
void loop() {
    i++;
    if(i<50000) digitalWrite(2,HIGH);
    if(i>50000 && i<100000) digitalWrite(2,LOW);
    if(i>100000) i = 0;
    int length = Serial.available();
    if(length<0){
        digitalWrite(19,HIGH);
    }else{
        digitalWrite(19,LOW);
    }
    unsigned int inc = length;
	for(int k =0;k<8;k++){
		unsigned int t = 1;
		t = t<<k;
		if( inc&t){
			digitalWrite(pin[k],HIGH);
		}else{
			digitalWrite(pin[k],LOW);
		}
	}

    if (length>255){
        for(int a = 0;a<length;a++){
            Serial.read();
        }
    }

    if(length==4){
        digitalWrite(19,HIGH);
        Serial.end();
        delay(1500);
        digitalWrite(19,LOW);
        Serial.flush();
        Serial.begin(9600);
        //Serial.flush();
        }

    
}

