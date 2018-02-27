#ifndef __PANNELEFFECTS_H__
#define __PANNELEFFECTS_H__

#include <Arduino.h>
#include <FastLED/FastLED.h>

/* MATRIX PINS*/
#define ENGR_PIN 27
#define LOGO_PIN 26
#define BAR_PIN 25

/* MATRIX SIZE*/
#define KMATRIXWIDTH 	5
#define KMATRIXHEIGHT 	4

/* MATRIX SIZE TWO*/
#define NUM_LEDS_LOGO 19
#define NUM_LEDS_BAR 20
#define NUM_LEDS_ENGR (int)(5*4)

#define COLOR_ORDER BRG
#define CHIPSET     WS2811

#define BRIGHTNESS  200
#define FRAMES_PER_SECOND 30

#define DEFAULT_ANIMATION 0X01
#define FIRE 			  0X01
#define CYLON 			  0X02

#define MAX_EFFECT		  0X20
/* **************************FIRE PARAMETERS *********************************
* COOLING: How much does the air cool as it rises?
* Less cooling = taller flames.  More cooling = shorter flames.
* Default 50, suggested range 20-100 
*/
#define COOLING  80
/*
* SPARKING: What chance (out of 255) is there that a new spark will be lit?
* Higher chance = more roaring fire.  Lower chance = more flickery fire.
* Default 120, suggested range 50-200.
*/
#define SPARKING 50
/*****************************************************************************/

class PannelEffects
{
	public:

	PannelEffects();

	typedef void (*Effect)(CRGB * led_matrix, const int size);

	//void show(){ FastLED.show(); }

	//void delay(unsigned long time_ms){ FastLED.delay(time_ms); }

	void select_bar_animation(uint8_t id){ id_a_engr = id; }

	void select_engr_animation(uint8_t id){ id_a_logo = id; };

	void select_logo_animation(uint8_t id){ id_a_bar = id; };	

	void execute_animation();



	protected:

	uint8_t id_a_engr = DEFAULT_ANIMATION;
	uint8_t id_a_logo = DEFAULT_ANIMATION;
	uint8_t id_a_bar  = DEFAULT_ANIMATION; 

	CRGB leds_engr[NUM_LEDS_ENGR];
	CRGB leds_logo[NUM_LEDS_LOGO];
	CRGB leds_bar[NUM_LEDS_BAR];

	Effect animation[MAX_EFFECT];

	bool gReverseDirection = true; /* used in fire_effect()*/

	void fire_effect(CRGB * led_matrix, const int size);
	void fadeall(CRGB *led_matrix, const int size);
	void cylon(CRGB * led_matrix, const int size);

	/* MATRIX METHODS */

	/* return index in led array */
	uint16_t XY(uint8_t x, uint8_t y); 
};

#endif // __PANNELEFFECTS_H__