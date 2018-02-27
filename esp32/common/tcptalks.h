#ifndef __TCPTALKS_H__
#define __TCPTALKS_H__

#include <Arduino.h>
#include "Pickle.h"
#include <WiFi/src/WiFi.h>

#ifndef EEPROM_SIZE
#define EEPROM_SIZE 1024
#endif

#ifndef TCPTALKS_INPUT_BUFFER_SIZE
#define TCPTALKS_INPUT_BUFFER_SIZE 64
#endif

#ifndef TCPTALKS_OUTPUT_BUFFER_SIZE
#define TCPTALKS_OUTPUT_BUFFER_SIZE 64
#endif

#ifndef TCPTALKS_MAX_OPCODE
#define TCPTALKS_MAX_OPCODE 0x20
#endif

#ifndef TCPTALKS_UUID_ADDRESS
#define TCPTALKS_UUID_ADDRESS 0x0000000000
#endif

#ifndef TCPTALKS_UUID_LENGTH
#define TCPTALKS_UUID_LENGTH	32
#endif

#define TCPTALKS_MASTER_BYTE (uint8_t)'R'
#define TCPTALKS_SLAVE_BYTE  (uint8_t)'A'

#define TCPTALKS_PING_OPCODE       0x0
#define TCPTALKS_GETUUID_OPCODE    0x1
#define TCPTALKS_SETUUID_OPCODE    0x2
#define TCPTALKS_DISCONNECT_OPCODE 0x3
#define TCPTALKS_GETEEPROM_OPCODE  0x4
#define TCPTALKS_SETEEPROM_OPCODE  0x5

#define AUTHENTIFICATION_OPCODE 0xAA

#define NOT_OPCODE  0XFF
#define NOT_RETCODE 0XFE

#define TCPTALKS_BAUDRATE 115200

typedef uint8_t byte;



class TCPTalks
{
	public: // Public API

	TCPTalks();

	typedef void (*Instruction)(TCPTalks& inst, UnPickler& input, Pickler& output);

	void connect(int timeout);

	bool authentificate(int timeout);
		
	void disconnect();
		
	void bind(uint8_t opcode, Instruction instruction);

	//void rawsend(uint8_t* rawbytes);
		
	void send(uint8_t opcode, uint8_t* args);

	void sendback(int retcode, uint8_t* args);

	void process(uint8_t* message);
		
	bool execinstruction(uint8_t* args);
		
	bool execute();
	
	void sleep_until_disconnected();

	int sendback(uint8_t opcode, long retcode, byte * args);

	bool getUUID(char* uuid);
	void setUUID(const char* uuid);

	static void generateRandomUUID(char* uuid, int length);

		
	protected: // Protected methods

	char* ip;

	int port;

	char* password = "";

	bool is_connected;
	bool is_authentificated;

	char* ssid     = "";
	char* pass = "";

	WiFiClient client;

	Instruction	m_instructions[TCPTALKS_MAX_OPCODE];

	enum //     m_state
	{
		TCPTALKS_WAITING_STATE,
		TCPTALKS_INSTRUCTION_STARTING_STATE,
		TCPTALKS_INSTRUCTION_RECEIVING_STATE,
	}m_state;


	byte        m_bytesNumber;
	byte        m_bytesCounter;
	long        m_lastTime;

	byte  m_inputBuffer [TCPTALKS_INPUT_BUFFER_SIZE];
	byte  m_outputBuffer[TCPTALKS_OUTPUT_BUFFER_SIZE];

	private:

	static void PING   (TCPTalks& inst, UnPickler& input, Pickler& output);
	static void GETUUID(TCPTalks& inst, UnPickler& input, Pickler& output);
	static void SETUUID(TCPTalks& inst, UnPickler& input, Pickler& output);
	static void DISCONNECT(TCPTalks& inst, UnPickler& input, Pickler& output){ESP.restart();}
	static void GETEEPROM(TCPTalks& inst, UnPickler& input, Pickler& output);
	static void SETEEPROM(TCPTalks& inst, UnPickler& input, Pickler& output);
};


void SWITCH_LED(TCPTalks& inst, UnPickler& input, Pickler& output);
#endif // __TCPTALKS_H__
