#include <Arduino.h>
#include "tcptalks.h"
#include "Pickle.h"
#include "EEPROM.h"
#include <WiFi/src/WiFi.h>

TCPTalks tcpt;

void SWITCH_LED(TCPTalks &inst, UnPickler& input, Pickler& output)
{
    bool var;

    pinMode(2, OUTPUT);

    var = input.load<bool>();
   
    if(var)
    {
        Serial.println("ON");
        digitalWrite(2, HIGH);

    }
    else 
    {
        Serial.println("false");
        digitalWrite(2, LOW);
    }

    // output.dump<bool>(var);
     output.dump<long>(10);
    // output.dump<double>(1.1);
    
    //output.dump<char>(0X02);
    output.dump<long>(11);

    //output.dump<char*>("hello world");
}

void TCPTalks::PING(TCPTalks& inst, UnPickler& input, Pickler& output)
{
    output.dump<bool>(true);
}

void TCPTalks::GETUUID(TCPTalks& inst, UnPickler& input, Pickler& output)
{
    char uuid[TCPTALKS_UUID_LENGTH];
    tcpt.getUUID(uuid);
    output.dump<char*>(uuid);
}

void TCPTalks::SETUUID(TCPTalks& inst, UnPickler& input, Pickler& output)
{   
    char* uuid;//[TCPTALKS_UUID_LENGTH];
    uuid = input.load<char*>();
    tcpt.setUUID(uuid);
}

void TCPTalks::GETEEPROM(TCPTalks& inst, UnPickler& input, Pickler& output)
{
    int addr = input.load<long>();
    output.dump<char>(EEPROM.read(addr));
}

void TCPTalks::SETEEPROM(TCPTalks& inst, UnPickler& input, Pickler& output)
{
    int addr = input.load<long>();
    byte value = input.load<char>();
    EEPROM.write(addr,value);
    EEPROM.commit();
}

TCPTalks::TCPTalks()
{	
    //ip = "192.168.0.12";
    ip = "192.168.1.13";
    
	port =  25565;

	password = "\n";

	is_connected = false;
	is_authentificated = false;

	// ssid = "NUMERICABLE-9251_2GEXT";
	// pass = "26338b5a57";

    ssid = "CLUB_ROBOT";
    pass = "zigouigoui";

    //m_state = TCPTALKS_WAITING_STATE;

    //Initialize EEPROM
 //   EEPROM.begin(EEPROM_SIZE);

        // Initialize UUID stuff
// #ifdef BOARD_UUID
//     setUUID(BOARD_UUID);
//     EEPROM.commit();
// #else
//     char uuid[SERIALTALKS_UUID_LENGTH];
//     if (!getUUID(uuid) || uuid[0] == '\0')
//     {
//         generateRandomUUID(uuid, SERIALTALKS_DEFAULT_UUID_LENGTH);
//         setUUID(uuid);
//     }
// #endif // BOARD_UUID

    bind(TCPTALKS_PING_OPCODE,      TCPTalks::PING);
    bind(TCPTALKS_GETUUID_OPCODE,   TCPTalks::GETUUID);
    bind(TCPTALKS_SETUUID_OPCODE,   TCPTalks::SETUUID);
    bind(TCPTALKS_DISCONNECT_OPCODE,TCPTalks::DISCONNECT);
    bind(TCPTALKS_GETEEPROM_OPCODE, TCPTalks::GETEEPROM);
    bind(TCPTALKS_SETEEPROM_OPCODE, TCPTalks::SETEEPROM);

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
    sendback(AUTHENTIFICATION_OPCODE,NOT_RETCODE,(byte*)password);

    // last_time = millis();
    // Serial.print("wait for authentification...");

    // while(!client.connect(ip, port))
    // {
    //     Serial.print(".");
    //     delay(5);
    //     long current_time = millis();
    //     if(current_time - last_time > timeout )
    //     {
    //         Serial.println("authentification Failed");
    //         return;
    //     }
       
    // }
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

    long opcode = input.load<long>();

    Serial.print("opcode : ");
    Serial.println(opcode, HEX);

    long retcode = input.load<long>();

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

    //Serial.println(currentTime);
    if (m_state != TCPTALKS_WAITING_STATE && (currentTime - m_lastTime > 100)) // 0.1s timeout // 100  m_state != TCPTALKS_WAITING_STATE && 
    {
        // Abort previous communication
        Serial.println("abort");
        m_state = TCPTALKS_WAITING_STATE;
    }

    for (int i = 0; i < length ; i++)
    {
        // Read the incoming byte
        byte inc;

        //Serial.println("in");
        client.read(&inc , 1);
        //Serial.println("out");

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
                    is_connected = true;
                    ret |= execinstruction(m_inputBuffer);
                    m_state = TCPTALKS_WAITING_STATE;
                    client.flush();
                }
                break;
        }
    }
    return ret;
}

int TCPTalks::sendback(uint8_t opcode, long retcode, byte * args)
{
    int ptr = 0;
    size_t size;

    byte frame[TCPTALKS_OUTPUT_BUFFER_SIZE];

    /*start header frame*/
    frame[ptr] = PROTO; 
    ptr++;
    frame[ptr] = DEFAULT_PROTOCOL;
    ptr++;
    frame[ptr] = SHORT_BINBYTES;
    ptr++;
    frame[ptr] = 0X01;
    ptr++;
    frame[ptr] = TCPTALKS_SLAVE_BYTE;
    ptr++;
    frame[ptr] = BINPUT;
    ptr++;
    frame[ptr] = 0X00;
    ptr++;
    /* end header frame */

    /* ADD opcode if it defined */
    if(opcode != NOT_OPCODE)
    {
        frame[ptr] = BININT1;
        ptr++;
        frame[ptr] = opcode;
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
        memcpy(tab,(byte*)&retcode, sizeof(retcode));

        frame[ptr] = tab[0];
        ptr++;
        frame[ptr] = tab[1];
        ptr++;
        frame[ptr] = tab[2];
        ptr++;
        frame[ptr] = tab[3];
        ptr++;
        frame[ptr] = 0X00;
        ptr++;

    }


    if(strlen((char*)args) <= 3)
    {
        frame[ptr] = NONE;
        ptr++;
        frame[ptr] = TUPLE1; 
        ptr++;
        frame[ptr] = BINPUT;
        ptr++;
        frame[ptr] = 0X01;
        ptr++;
    }
    else
    {
        /* get argument size */
        size = strlen((char*)args);
        Serial.println(size);

        if(args[size - 3] == TUPLE)
        {
            Serial.println("big tuple");

            uint8_t tmp[MAX_BUFFER_SIZE];
            
            tmp[0] = (uint8_t)MARK;
            memcpy(tmp+1, args, size);

            memcpy(args, tmp, (size+1));

            size = strlen((char*)args);
        }

        memcpy(frame+ptr, args, size);

        ptr += size;
    }


    /*ending frame*/
    frame[ptr] = TUPLE3;
    ptr++;
    frame[ptr] = BINPUT;
    ptr++;
    frame[ptr] = 0X02;
    ptr++;
    frame[ptr] = STOP;
    ptr++;

    client.write(frame, ptr);

    for(int i = 0; i<=ptr;i++)
    {
        Serial.print(frame[i],HEX);
        Serial.print(" ");
    }

    Serial.println("");
    
}

bool TCPTalks::getUUID(char* uuid)
{

    for (int i = 0; i < EEPROM_SIZE; i++)
    {
        uuid[i] = EEPROM.read(TCPTALKS_UUID_ADDRESS + i);
        switch(byte(uuid[i]))
        {
        case '\0': return true;
        case 0xFF: return false;
        default  : continue;
        }
    }
    return false;
}

void TCPTalks::setUUID(const char* uuid)
{
    int i = 0;
    do
        EEPROM.write(TCPTALKS_UUID_ADDRESS + i, uuid[i]);
    while(uuid[i++] != '\0');
    EEPROM.commit();
}




void TCPTalks::generateRandomUUID(char* uuid, int length)
{
    // Initialize the random number generator
    randomSeed(analogRead(0));

    // Generate the UUID from a list of random hexadecimal numbers
    for (int i = 0; i < length; i++)
    {
        if (i % 5 == 4)
            uuid[i] = '-';
        else
        {
            long digit = random(16);
            if (digit < 10)
                uuid[i] = char('0' + digit);
            else
                uuid[i] = char('a' + digit - 10);
        }
    }
    uuid[length] = '\0';
}
