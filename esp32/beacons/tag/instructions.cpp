#include "instructions.h"

extern float p[2]; // Target point

void GET_POSITION(SerialTalks &talks, Deserializer &input, Serializer &output)
{
    output.write<float>(p[0]);
    output.write<float>(p[1]);

}
