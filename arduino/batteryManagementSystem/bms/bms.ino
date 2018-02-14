#include <Arduino.h>

//#include "../../common/SoftI2CMaster.h"
//#include "../../common/SerialTalks.h"
//#include "../instructions.h"
#include "SBSCommands.h"

#define SDA_PORT PORTC
#define SDA_PIN 4

#define SCL_PORT PORTC
#define SCL_PIN 5

#define I2C_SLOWMODE 1

#include <SoftI2CMaster.h>

#define LED_PIN 5

#define WRITE_CONFIG 0

uint8_t sI2CDeviceAddress;

#define DATA_BUFFER_LENGTH 32
uint8_t dataBuffer[DATA_BUFFER_LENGTH];

void setup() {
    //Serial Talks Setup
	/*Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);

    talks.bind(GET_SOC_OPCODE, GET_SOC);*/

	// initialize the digital pin as an output.
	pinMode(LED_PIN, OUTPUT);

	// Shutdown SPI and TWI, timers, and ADC
	PRR = (1 << PRSPI) | (1 << PRTWI) | (1 << PRTIM1) | (1 << PRTIM2) | (1 << PRADC);
	// Disable  digital input on all unused ADC channel pins to reduce power consumption
	DIDR0 = ADC0D | ADC1D | ADC2D | ADC3D;

	Serial.begin(115200);  // start serial for output
	
	bool tI2CSucessfullyInitialized = i2c_init();
	if (tI2CSucessfullyInitialized) {
		Serial.println(F("I2C initalized sucessfully"));
	}
	else {
		Serial.println(F("I2C pullups missing"));
		BlinkLedForever(100);
	}
	Serial.flush();

	/*
	* Check for I2C device and blink until device attached
	*/
	if (!checkForAttachedI2CDevice(SBM_DEVICE_ADDRESS)) {
		int tDeviceAttached;
		do {
			tDeviceAttached = scanForAttachedI2CDevice();
			delay(500);
			TogglePin(LED_PIN);
		} while (tDeviceAttached < 0);
	}
	digitalWrite(LED_PIN,1);

#if WRITE_CONFIG
	Serial.print("Update AFE CELL MAP : ");
	Serial.println(writeDataFlashU2(AFE_CELL_MAP,(uint16_t)0x0013));
  	delay(200);
  
	Serial.print("Update MFG INIT : ");
	Serial.println(writeDataFlashU2(MANUFACTURING_STATUS_INIT,(uint16_t)0x0230));
  	delay(200);
 
	Serial.print("Update FET OPTIONS : ");
	Serial.println(writeDataFlashU2(FET_OPTIONS,(uint16_t)0x0001));
  	delay(200);
  
	Serial.print("Update DESIGN CAPACITY : ");
	Serial.println(writeDataFlashI2(DESIGN_CAPACITY_MA_CONFIG,(int16_t)1650));
	delay(200);
#endif

  	readWordFromManufacturerAccess(DEVICE_RESET);
  	delay(1000);
	Serial.print("Design Capacity mA : ");
	Serial.println((uint16_t)readWord(DESIGN_CAPACITY));
	Serial.print("Operation Status - Length :");
	uint8_t length = readBlockFromManufacturerBlockAccess((uint16_t)0, dataBuffer, DATA_BUFFER_LENGTH);
	Serial.print(length);
	Serial.print(" - 0x");
	for(uint8_t i=0; i<length; i++){
		Serial.print(dataBuffer[i],HEX);
	}
	Serial.print("Security Keys : ");
	Serial.println(readU32FromManufacturerAccess((uint16_t)0x0035), HEX);
}



void loop() {
	//Serial Talk Execution
	//talks.execute();
	Serial.print("Voltage : ");
	Serial.println((uint8_t)readWord(VOLTAGE));
	delay(1000);
	//Serial.println(readWordFromManufacturerAccess(0x002B)); //toggle LEDs
  delay(1000);
}

void BlinkLedForever(int aBinkDelay) {
	do {
		digitalWrite(LED_PIN, HIGH);
		delay(aBinkDelay);
		digitalWrite(LED_PIN, LOW);
		delay(aBinkDelay);
	} while (true);
}

void TogglePin(uint8_t aPinNr) {
	if (digitalRead(aPinNr) == HIGH) {
		digitalWrite(aPinNr, LOW);
	}
	else {
		digitalWrite(aPinNr, HIGH);
	}
}

bool checkForAttachedI2CDevice(uint8_t aStandardDeviceAddress) {
	bool tOK = i2c_start(aStandardDeviceAddress << 1 | I2C_WRITE);
	i2c_stop();
	if (tOK) {
		Serial.print(F("Found attached I2C device at 0x"));
		Serial.println(aStandardDeviceAddress, HEX);
		sI2CDeviceAddress = SBM_DEVICE_ADDRESS;
		return true;
	}
	else {
		return false;
	}
}

int scanForAttachedI2CDevice(void) {
	int tFoundAdress = -1;
	for (uint8_t i = 0; i < 127; i++) {
		bool ack = i2c_start(i << 1 | I2C_WRITE);
		if (ack) {
			Serial.print(F("Found I2C device attached at address: 0x"));
			Serial.println(i, HEX);
			tFoundAdress = i;
		}
		i2c_stop();
	}
	if (tFoundAdress < 0) {
		Serial.println(F("Found no attached I2C device"));
	}
	else {
		sI2CDeviceAddress = tFoundAdress;
	}
	return tFoundAdress;
}

bool writeDataFlashU1(uint16_t address, uint8_t dataU1){
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE); //start communication with slave address and write command
	i2c_write(MANUFACTURER_BLOCK_ACCESS);			 //send command
	i2c_write((uint8_t)3);							 //send byte count

	i2c_write(address >> 8);
	i2c_write(address & 0xFF);

	bool ackData = i2c_write(dataU1);
	i2c_stop();
	return ackData;
}

bool writeDataFlashU2(uint16_t address, uint16_t dataU2){
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE); //start communication with slave address and write command
	i2c_write(MANUFACTURER_BLOCK_ACCESS);			 //send command
	i2c_write((uint8_t)4);							 //send byte count

	i2c_write(address >> 8);
	i2c_write(address & 0xFF);

	i2c_write(dataU2 >> 8);
	bool ackData = i2c_write(dataU2 & 0xFF);
	i2c_stop();
	return ackData;
}

bool writeDataFlashU4(uint16_t address, uint32_t dataU4){
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE); //start communication with slave address and write command
	i2c_write(MANUFACTURER_BLOCK_ACCESS);			 //send command
	i2c_write((uint8_t)6);							 //send byte count

	i2c_write(address >> 8);
	i2c_write(address & 0xFF);

	i2c_write(dataU4 >> 24);
	i2c_write(dataU4 >> 16);
	i2c_write(dataU4 >> 8);
	bool ackData = i2c_write(dataU4 & 0xFF);
	i2c_stop();
	return ackData;
}

bool writeDataFlashI1(uint16_t address, int8_t dataI1){
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE); //start communication with slave address and write command
	i2c_write(MANUFACTURER_BLOCK_ACCESS);			 //send command
	i2c_write((uint8_t)3);							 //send byte count

	i2c_write(address >> 8);
	i2c_write(address & 0xFF);

	bool ackData = i2c_write(dataI1);
	i2c_stop();
	return ackData;
}

bool writeDataFlashI2(uint16_t address, int16_t dataI2){
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE); //start communication with slave address and write command
	i2c_write(MANUFACTURER_BLOCK_ACCESS);			 //send command
	i2c_write((uint8_t)4);							 //send byte count

	i2c_write(address >> 8);
	i2c_write(address & 0xFF);

	i2c_write(dataI2 >> 8);
	bool ackData = i2c_write(dataI2 & 0xFF);
	i2c_stop();
	return ackData;
}

bool writeDataFlashI4(uint16_t address, int32_t dataI4){
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE); //start communication with slave address and write command
	i2c_write(MANUFACTURER_BLOCK_ACCESS);			 //send command
	i2c_write((uint8_t)6);							 //send byte count

	i2c_write(address >> 8);
	i2c_write(address & 0xFF);

	i2c_write(dataI4 >> 24);
	i2c_write(dataI4 >> 16);
	i2c_write(dataI4 >> 8);
	bool ackData = i2c_write(dataI4 & 0xFF);
	i2c_stop();
	return ackData;
}

uint16_t readWordFromManufacturerAccess(uint16_t aCommand) {
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(MANUFACTURER_ACCESS);
	// Write manufacturer command word
	i2c_rep_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(aCommand);
	i2c_write(aCommand >> 8);
	i2c_stop();
	// Read manufacturer result word
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(MANUFACTURER_ACCESS);
	i2c_rep_start((sI2CDeviceAddress << 1) | I2C_READ);
	uint8_t tLSB = i2c_read(false);
	uint8_t tMSB = i2c_read(true);
	i2c_stop();
	return (uint16_t) tLSB | (((uint16_t) tMSB) << 8);
}

uint32_t readU32FromManufacturerAccess(uint16_t aCommand) {
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(MANUFACTURER_ACCESS);
	// Write manufacturer command word
	i2c_rep_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(aCommand);
	i2c_write(aCommand >> 8);
	i2c_stop();
	// Read manufacturer result word
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(MANUFACTURER_ACCESS);
	i2c_rep_start((sI2CDeviceAddress << 1) | I2C_READ);
	uint8_t u1LSB = i2c_read(false);
	uint8_t u1MSB = i2c_read(false);
	uint8_t u2LSB = i2c_read(false);
	uint8_t u2MSB = i2c_read(true);
	i2c_stop();
	return ((uint32_t) u1LSB << 16) | ((uint32_t) u1MSB << 24) | (uint32_t) u2LSB | ((uint32_t) u2MSB << 8);
}

uint16_t readWord(uint8_t aFunction) {
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(aFunction);
	i2c_rep_start((sI2CDeviceAddress << 1) | I2C_READ);
	uint8_t tLSB = i2c_read(false);
	uint8_t tMSB = i2c_read(true);
	i2c_stop();
	return (uint16_t) tLSB | (((uint16_t) tMSB) << 8);
}

uint8_t readBlockFromManufacturerBlockAccess(uint16_t aCommand, uint8_t* aDataBufferPtr, uint8_t aDataBufferLength) {
	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(MANUFACTURER_BLOCK_ACCESS);
	i2c_write((uint8_t)2);
	// Write manufacturer command word
	i2c_write(aCommand & 0xFF);
	i2c_write(aCommand >> 8);
	i2c_stop();

	i2c_start((sI2CDeviceAddress << 1) | I2C_WRITE);
	i2c_write(MANUFACTURER_BLOCK_ACCESS);
	i2c_rep_start((sI2CDeviceAddress << 1) + I2C_READ);

	// First read length of data
	uint8_t tLengthOfData = i2c_read(false);
	if (tLengthOfData > aDataBufferLength) {
		tLengthOfData = aDataBufferLength;
	}

	// then read data
	uint8_t tIndex;
	for (tIndex = 0; tIndex < tLengthOfData - 1; tIndex++) {
		aDataBufferPtr[tIndex] = i2c_read(false);
	}
	// Read last byte with "true"
	aDataBufferPtr[tIndex++] = i2c_read(true);

	i2c_stop();
	return tLengthOfData;
}

uint8_t readBlock(uint8_t aCommand, uint8_t* aDataBufferPtr, uint8_t aDataBufferLength) {
	i2c_start((sI2CDeviceAddress << 1) + I2C_WRITE);
	i2c_write(aCommand);
	i2c_rep_start((sI2CDeviceAddress << 1) + I2C_READ);

	// First read length of data
	uint8_t tLengthOfData = i2c_read(false);
	if (tLengthOfData > aDataBufferLength) {
		tLengthOfData = aDataBufferLength;
	}

	// then read data
	uint8_t tIndex;
	for (tIndex = 0; tIndex < tLengthOfData - 1; tIndex++) {
		aDataBufferPtr[tIndex] = i2c_read(false);
	}
	// Read last byte with "true"
	aDataBufferPtr[tIndex++] = i2c_read(true);

	i2c_stop();
	return tLengthOfData;
}

uint8_t readBlockDataFlash(uint8_t aCommand, uint8_t* aDataBufferPtr, uint8_t aDataBufferLength) {
	i2c_start((sI2CDeviceAddress << 1) + I2C_WRITE);
	i2c_write(aCommand & 0xFF);
	i2c_write(aCommand >> 8);
	i2c_rep_start((sI2CDeviceAddress << 1) + I2C_READ);

	// First read length of data
	uint8_t tLengthOfData = i2c_read(false);
	if (tLengthOfData > aDataBufferLength) {
		tLengthOfData = aDataBufferLength;
	}

	// then read data
	uint8_t tIndex;
	for (tIndex = 0; tIndex < tLengthOfData - 1; tIndex++) {
		aDataBufferPtr[tIndex] = i2c_read(false);
	}
	// Read last byte with "true"
	aDataBufferPtr[tIndex++] = i2c_read(true);

	i2c_stop();
	return tLengthOfData;
}
