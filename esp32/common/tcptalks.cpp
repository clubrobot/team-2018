#include <Arduino.h>
#include "tcptalks.h"
#include "Pickle.h"
#include <WiFi/src/WiFi.h>


void SWITCH_LED(TCPTalks &inst, UnPickler& input, Pickler& output)
{
    bool var;
    long val;
    float val1;

    pinMode(2, OUTPUT);

    var = input.load_bool();
    val = input.load_long();
    val1 = input.load_float();

    if(var)
    {
        Serial.println("ON");
        Serial.println(val);
        Serial.println(val1);
        digitalWrite(2, HIGH);

    }
    else 
    {
        Serial.println("false");
        digitalWrite(2, LOW);
    }

    //output.dump_long(1000);
}

TCPTalks::TCPTalks()
{
	
    ip = "192.168.0.16";
    
	port =  25565;

	password = "";

	is_connected = false;
	is_authentificated = false;

	ssid = "NUMERICABLE-9251_2GEXT";
	pass = "26338b5a57";
}

void TCPTalks::connect(int timeout)
{
    Serial.print("Connecting to ");
    Serial.println(ssid);
    /* connect to your WiFi */
    WiFi.begin(ssid, pass);
    /* wait until ESP32 connect to WiFi*/

    long last_time = millis();
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(5);
        Serial.print(".");
        long current_time = millis();
        if(current_time - last_time > timeout )
        {
            Serial.println("Connexion Failed");
            return;
        }
    }

    Serial.println("");
    Serial.println("WiFi connected with IP address: ");
    Serial.println(WiFi.localIP());
    Serial.println("");

    last_time = millis();
    Serial.print("wait for server...");

    while(!client.connect(ip, port))
    {
        Serial.print(".");
        delay(5);
        long current_time = millis();
        if(current_time - last_time > timeout )
        {
            Serial.println("Connexion Failed");
            return;
        }
       
    }

    is_connected = true;
    Serial.println("connected");


    authentificate(5);

    /* add authentification steps */

}

bool TCPTalks::authentificate(int timeout)
{
	byte authentification_frame[17] = {PROTO, DEFAULT_PROTOCOL, SHORT_BINBYTES, 0X01, TCPTALKS_SLAVE_BYTE, BINPUT, 0X00, BININT1, AUTHENTIFICATION_OPCODE,NONE, TUPLE1, BINPUT, 0X01, TUPLE3, BINPUT, 0X02, STOP };
    client.write(authentification_frame, sizeof(authentification_frame));

    //sendback(AUTHENTIFICATION_OPCODE,NOT_RETCODE,(byte*)password);

    is_authentificated = true;
	return is_authentificated;
}

void TCPTalks::disconnect()
{	
	client.stop();
    
	is_connected = false;
}

void TCPTalks::bind(uint8_t opcode, Instruction instruction)
{
	// Add a command to execute when receiving the specified opcode
	if (opcode < TCPTALKS_MAX_OPCODE)
		m_instructions[opcode] = instruction;
}

void TCPTalks::send(uint8_t opcode, uint8_t* args)
{
    long retcode = random(0, 0xFFFFFFFF);
}

bool TCPTalks::execinstruction(uint8_t* inputBuffer)
{
    UnPickler input(inputBuffer);
    Pickler   output(m_outputBuffer);

    long opcode = input.load_long();

    Serial.print("opcode : ");
    Serial.println(opcode, HEX);

    long retcode = input.load_long();

    Serial.print("retcode : ");
    Serial.println(retcode);

    if(input.is_tuple())
        input.remove_tuple_header();

    if (m_instructions[opcode] != 0)
    {
        m_instructions[opcode](*this, input, output);

        output.end_frame();

        sendback(NOT_OPCODE, retcode, m_outputBuffer);

        return true;
    }
    return false;
}

bool TCPTalks::execute()
{
    bool ret = false;

    int length = client.available();

    long currentTime = millis();
    if (m_state != TCPTALKS_WAITING_STATE && currentTime - m_lastTime > 100) // 0.1s timeout
    {
        // Abort previous communication
        m_state = TCPTALKS_WAITING_STATE;
    }


    for (int i = 0; i < length; i++)
    {
        // Read the incoming byte
        byte inc;

        client.read(&inc , 1);

        Serial.println(inc,HEX);
        m_lastTime = currentTime;
        // Use a state machine to process the above byte
        switch (m_state)
        {
        // An instruction always begin with the Master byte
        case TCPTALKS_WAITING_STATE:
            if (inc == TCPTALKS_MASTER_BYTE)
            {
                m_state = TCPTALKS_INSTRUCTION_RECEIVING_STATE;
                m_bytesCounter = 0;
            }
           
            Serial.println("wait...");
            continue;

        case TCPTALKS_INSTRUCTION_RECEIVING_STATE:
            m_inputBuffer[m_bytesCounter] = inc;
            m_bytesCounter++;

            Serial.println("exec");
            if(inc == '.')
            {
                Serial.println();
                is_connected = true;
                ret |= execinstruction(m_inputBuffer);
                m_state = TCPTALKS_WAITING_STATE;
            }
        }
    }
    return ret;
}

int TCPTalks::sendback(uint8_t opcode, long retcode, byte * args)
{
    int ptr = 0;

    byte frame[TCPTALKS_OUTPUT_BUFFER_SIZE];

    /*start header frame*/
    frame[ptr] = (byte)PROTO; 
    ptr++;
    frame[ptr] = (byte)DEFAULT_PROTOCOL;
    ptr++;
    frame[ptr] = (byte)SHORT_BINBYTES;
    ptr++;
    frame[ptr] = (byte)0X01;
    ptr++;
    frame[ptr] = (byte)TCPTALKS_SLAVE_BYTE;
    ptr++;
    frame[ptr] = (byte)BINPUT;
    ptr++;
    frame[ptr] = (byte)0X00;
    ptr++;
    /* end header frame */

    /* ADD opcode if it defined */
    if(opcode != NOT_OPCODE)
    {
        frame[ptr] = (byte)BININT1;
        ptr++;
        frame[ptr] = (byte)opcode;
        ptr++;
    }
    else if(retcode != NOT_RETCODE)
    {
        frame[ptr] = (byte)LONG1;
        ptr++;
        frame[ptr] = (byte)0X05;
        ptr++;

        byte tab[4] = {0};
        /* add retcode */
        memcpy((byte*)tab, &retcode, sizeof(retcode));

        frame[ptr] = (byte)tab[0];
        ptr++;
        frame[ptr] = (byte)tab[1];
        ptr++;
        frame[ptr] = (byte)tab[2];
        ptr++;
        frame[ptr] = (byte)tab[3];
        ptr++;
        frame[ptr] = (byte)0X00;
        ptr++;

    }
    if(sizeof(args) <= 4)
    {
        frame[ptr] = NONE;
        ptr++;
        frame[ptr] = (byte)TUPLE1; 
        ptr++;
        frame[ptr] = (byte)BINPUT;
        ptr++;
        frame[ptr] = (byte)0X01;
        ptr++;
    }
    else
    {
        memcpy(frame+ptr,args, sizeof(args));
        ptr += sizeof(args);
    }


    /*ending frame*/
    frame[ptr] = (byte)TUPLE3;
    ptr++;
    frame[ptr] = (byte)BINPUT;
    ptr++;
    frame[ptr] = (byte)0X02;
    ptr++;
    frame[ptr] = (byte)STOP;
    ptr++;

    client.write(frame, ptr);

    for(int i = 0; i<=ptr;i++)
    {
        Serial.print(frame[i],HEX);
        Serial.print(" ");
    }

    Serial.println("");
    
}