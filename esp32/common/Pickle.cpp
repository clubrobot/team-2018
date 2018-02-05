#include <Arduino.h>
#include "Pickle.h"

Pickler::Pickler(uint8_t* frame)
{
	current_frame = frame;
	ptr = 0;
	num = 0;
}


void Pickler::start_frame()
{
 
}

void Pickler::end_frame()
{
	if(num == 1)
	{
		current_frame[ptr] = (uint8_t)TUPLE1;
		ptr++;
		current_frame[ptr] = (uint8_t)BINPUT;
		ptr++;
		current_frame[ptr] = (uint8_t)0X01;
		ptr++;
		
	}
	else if(num == 2)
	{
		current_frame[ptr] = (uint8_t)TUPLE2;
		ptr++;
		current_frame[ptr] = (uint8_t)BINPUT;
		ptr++;
		current_frame[ptr] = (uint8_t)0X01;
		ptr++;
	}
	else if(num == 3)
	{
		current_frame[ptr] = (uint8_t)TUPLE3;
		ptr++;
		current_frame[ptr] = (uint8_t)BINPUT;
		ptr++;
		current_frame[ptr] = (uint8_t)0X01;
		ptr++;
	}
	else if (num >= 4)
	{
		current_frame[ptr] = (uint8_t)TUPLE;
		ptr++;
		current_frame[ptr] = (uint8_t)BINPUT;
		ptr++;
		current_frame[ptr] = (uint8_t)0X01;
		ptr++;
	}
	current_frame[ptr] = (uint8_t)'\0';
	
}

template<>
void Pickler::dump<bool>(bool var){Pickler::dump_bool(var);}

template<>
void Pickler::dump<long>(long var){Pickler::dump_long(var);}

template<>
void Pickler::dump<float>(float var){Pickler::dump_float(var);}

template<>
void Pickler::dump<uint8_t>(uint8_t var){Pickler::dump_byte(var);}


void Pickler::dump_bool(bool var)
{
	num++;
	if(var)
		current_frame[ptr] = (uint8_t) NEWTRUE;

	else
		current_frame[ptr] = (uint8_t) NEWFALSE;
	ptr += 1;
}

void Pickler::dump_long(long var)
{
	num++;

	Serial.println(var,HEX);
	if(var <= 0xff && var >= 0)
	{
		current_frame[ptr] = (uint8_t)BININT1;
		ptr++;
		current_frame[ptr] = (uint8_t)var;
		ptr++;
		return;

	}
	else if(var <= 0xffff && var >= 0)
	{
		current_frame[ptr] = (uint8_t) BININT2; // long en uint8_t
		ptr++;
		current_frame[ptr] = (uint8_t) var;
		ptr++;
		current_frame[ptr] = (uint8_t) (var>>8);
		ptr++;
		return;
	}

	if((var >= (-0x80000000)) && (var <= 0x7fffffff))
	{
		current_frame[ptr] = (uint8_t) BININT;// long en uint8_t
		ptr++;
		current_frame[ptr] = (uint8_t) var;
		ptr++;
		current_frame[ptr] = (uint8_t) (var>>8);
		ptr++;
		current_frame[ptr] = (uint8_t) (var>>16);
		ptr++;
		current_frame[ptr] = (uint8_t) (var>>24);
		ptr++;
		return;
	}

}

void Pickler::dump_float(float var)
{
	num++;
	current_frame[ptr] = (uint8_t)BINFLOAT;
	ptr++;

	uint8_t * p = (uint8_t *)&var; 
	
	int len = sizeof(p);
	//big_endian conversion
	p[len+1] = 0X00;
	p[len+2] = 0X00;
	p[len+3] = 0X00;
	p[len+4] = 0x00;

	len +=4; 
	
	for(int i =0; i<len/2; i++)
	{
		uint8_t tmp = p[i];

        p[i] = p[len-i-1];

        p[len-i-1] = tmp;
		current_frame[ptr] = (uint8_t)BINBYTES;
	}

	ptr++;

	memcpy(current_frame+ptr,&var, len);

	ptr += len;
}

void Pickler::dump_byte(uint8_t var)
{
	num++;
	int len = sizeof(var);

	if(len <= 0xff)
	{
		current_frame[ptr] = (uint8_t)SHORT_BINUNICODE;
	}
	else if(len > 0xffffffff)
	{
		current_frame[ptr] = (uint8_t)BINUNICODE8;
	}
	else
	{
		current_frame[ptr] = (uint8_t)BINUNICODE;
	}
	ptr++;

	current_frame[ptr] = (uint8_t) len;
	ptr++;
	current_frame[ptr] = (uint8_t) (len>>8);
	ptr++;
	current_frame[ptr] = (uint8_t) (len>>16);
	ptr++;
	current_frame[ptr] = (uint8_t) (len>>24);
	ptr++;
	

	memcpy(current_frame+ptr, &var, len);

	ptr += len;


	current_frame[ptr] = (uint8_t)BINPUT;
	ptr++;
	current_frame[ptr] = (uint8_t)0X00;
	ptr++;

}

UnPickler::UnPickler(uint8_t* frame)
{
	current_frame = frame;
	ptr = 0;
	remove_start_frame();
}
void UnPickler::remove_start_frame()
{
	ptr+=2;
}

void UnPickler::remove_end_frame()
{
	ptr++;
}

void UnPickler::remove_tuple_header()
{
	ptr+=1;
}

template<>
bool UnPickler::load<bool>(){return UnPickler::load_bool();}

template<>
long UnPickler::load<long>(){return UnPickler::load_long();}

template<>
float UnPickler::load<float>(){return UnPickler::load_float();}

template<>
uint8_t UnPickler::load<uint8_t>(){return UnPickler::load_byte();}

bool UnPickler::load_bool()
{

	if(current_frame[ptr] == NEWTRUE)
	{
		ptr ++;
		return true;
	}
	else
	{
		return false;
	}
	
}

long UnPickler::load_long()
{

	if(current_frame[ptr] == BININT1)
	{
		ptr++;
		long var = (long)current_frame[ptr];
		ptr ++;
		return var;
	}

	if(current_frame[ptr] == BININT2)
	{
		ptr += 2;
		long var = (long)((current_frame[ptr] << 8) | current_frame[ptr - 1] );
		ptr ++;
		return var;
	}
	if(current_frame[ptr] == BININT)
	{
		ptr += 4;
		long var = (long)((current_frame[ptr] << 24) | (current_frame[ptr-1] << 16) | (current_frame[ptr-2] << 8) | current_frame[ptr - 3] );
		ptr ++;
		return var;
	}
	if(current_frame[ptr] == LONG1)
	{
		ptr += 5;
		long var = (long)((current_frame[ptr] << 24) | (current_frame[ptr-1] << 16) | (current_frame[ptr-2] << 8) | current_frame[ptr - 3] );
		ptr +=2;
		return var;
	}
}

float UnPickler::load_float()
{
	if(current_frame[ptr] = BINFLOAT)
	{
		/* convert to little endian */
		ptr++;

		uint8_t tab[8];

		tab[7] = current_frame[ptr];
		tab[6] = current_frame[ptr+1];
		tab[5] = current_frame[ptr+2];
		tab[4] = current_frame[ptr+3];
		tab[3] = current_frame[ptr+4];
		tab[2] = current_frame[ptr+5];
		tab[1] = current_frame[ptr+6];
		tab[0] = current_frame[ptr+7];
	
	double var; 
	memcpy(&var, &tab, sizeof(tab));
		
	return (float)var;
	}
	ptr ++;

	
}

uint8_t UnPickler::load_byte()
{
	uint8_t* tab;

	if(current_frame[ptr] == BINUNICODE)
	{
		ptr+=4;
		long len = (long)((current_frame[ptr-3] << 24) | (current_frame[ptr-2] << 16) | (current_frame[ptr-1] << 8) | current_frame[ptr] );
		ptr++;
		return current_frame[ptr]; 
	}
	if(current_frame[ptr] == BINUNICODE8)
	{
		ptr+=4;
		long len = (long)((current_frame[ptr-3] << 24) | (current_frame[ptr-2] << 16) | (current_frame[ptr-1] << 8) | current_frame[ptr] );

		ptr++;
		return current_frame[ptr]; 
	}
	if(current_frame[ptr] == SHORT_BINUNICODE)
	{
		ptr+=4;
		long len = (long)((current_frame[ptr-3] << 24) | (current_frame[ptr-2] << 16) | (current_frame[ptr-1] << 8) | current_frame[ptr] );

		ptr++;
		return current_frame[ptr]; 
	}
	ptr ++;

	/* switch ending byte frame */
	ptr+= 2;


}

bool UnPickler::is_tuple()
{
	if(current_frame[ptr] == '(')
	{
		return true;
	}
	else
		return false;
}

