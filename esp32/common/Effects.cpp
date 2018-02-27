#include <Arduino.h>
#include <FastLED/FastLED.h>
#include "Effects.h"

extern CFastLED FastLED;

/* Constuctor */
Effects::Effects()
{
	/* Led matrix initialisation */
	  FastLED.addLeds<CHIPSET, ENGR_PIN, COLOR_ORDER>(leds_engr,NUM_LEDS_ENGR);

  	FastLED.addLeds<CHIPSET, LOGO_PIN, COLOR_ORDER>(leds_logo,NUM_LEDS_LOGO);

  	FastLED.addLeds<CHIPSET, BAR_PIN, COLOR_ORDER>(leds_bar,NUM_LEDS_BAR);

  	FastLED.setBrightness(BRIGHTNESS);

    FastLED.clear(true);

    FastLED.setMaxRefreshRate(50,true);
}

void Effects::select_bar_animation(int id)
{
  a_engr = (id_a_engr)id; 
}

void Effects::select_engr_animation(int id)
{ 
  a_logo = (id_a_logo)id; 
}

void Effects::select_logo_animation(int id)
{ 
  a_bar = (id_a_bar)id; 
}

/* public methodes */
void Effects::update()
{
  /* execute animation */
  static int i = 0;

  if(i == 0)  
  {
    switch(a_engr)
    {
      case ENGR_FIRE : 
              fire_effect(leds_engr, NUM_LEDS_ENGR);
              FastLED.show();
              break;
      case ENGR_CYLON : 
              cylon(leds_engr, NUM_LEDS_ENGR);
              break;
      default : 
              fire_effect(leds_engr, NUM_LEDS_ENGR);
              FastLED.show();
              break;
    }
    i++;
  }
  else if(i == 1)
  {
    switch(a_logo)
    {
      case LOGO_FIRE : 
              fire_effect(leds_logo, NUM_LEDS_LOGO);
              FastLED.show();
              break;
      case LOGO_CYLON : 
              cylon(leds_logo, NUM_LEDS_LOGO);
              break;
      default : 
              fire_effect(leds_logo, NUM_LEDS_LOGO);
              FastLED.show();
              break;
    }
    i++;
  }
  else if(i == 2)
  {
     switch(a_bar)
    {
      case BAR_FIRE : 
              fire_effect(leds_bar, NUM_LEDS_BAR);
              FastLED.show();
              break;
      case BAR_CYLON : 
              cylon(leds_bar, NUM_LEDS_BAR);
              break;
      default : 
              fire_effect(leds_bar, NUM_LEDS_BAR);
              FastLED.show();
              break;
    }
    i = 0;
  }
}

/* Private methods */

void fire_effect(CRGB * led_matrix, const int size)
{
	// Array of temperature readings at each simulation cell
   byte heat[size];

  // Step 1.  Cool down every cell a little
    for( int i = 0; i < size; i++) 
    {
      heat[i] = qsub8( heat[i],  random8(0, ((COOLING * 10) / size) + 2));
    }
  
    // Step 2.  Heat from each cell drifts 'up' and diffuses a little
    for( int k= size - 1; k >= 2; k--) {
      heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2] ) / 3;
    }
    
    // Step 3.  Randomly ignite new 'sparks' of heat near the bottom
    if( random8() < SPARKING ) 
    {
      int y = random8(7);
      heat[y] = qadd8( heat[y], random8(160,255) );
    }

    // Step 4.  Map from heat cells to LED colors
    for( int j = 0; j < size; j++) 
    {
      CRGB color = HeatColor( heat[j]);
      int pixelnumber;
      
      pixelnumber = (size-1) - j;
      
      led_matrix[pixelnumber] = color;
    }
     // display this frame
    FastLED.delay(1000 / FRAMES_PER_SECOND);
}

void fadeall(CRGB *led_matrix, const int size)
{ 
	for(int i = 0; i < size; i++) 
	{ 
		led_matrix[i].nscale8(250); 
	}
}

void cylon(CRGB * led_matrix, const int size)
{
	static uint8_t hue = 0;

  	// First slide the led in one direction
  	for(int i = 0; i < size; i++) 
  	{
    	// Set the i'th led to red 
    	led_matrix[i] = CHSV(hue++, 255, 255);
    	// Show the leds
    	FastLED.show(); 
    	// now that we've shown the leds, reset the i'th led to black
    	// leds[i] = CRGB::Black;
    	fadeall(led_matrix, size);
    	// Wait a little bit before we loop around and do it again
    	delay(10);
  	}

  	// Now go in the other direction.  
  	for(int i = (size)-1; i >= 0; i--) 
  	{
    	// Set the i'th led to red 
    	led_matrix[i] = CHSV(hue++, 255, 255);
    	// Show the leds
    	FastLED.show();
    	// now that we've shown the leds, reset the i'th led to black
    	// leds[i] = CRGB::Black;
    	fadeall(led_matrix, size);
    	// Wait a little bit before we loop around and do it again
    	delay(10);
  	}
}

// /* MATRIX METHODS */

// uint16_t Effects::XY(uint8_t x, uint8_t y)
// {
// 	uint16_t i;

// 	if( y & 0x01) 
// 	{
// 		// Odd rows run backwards
// 		uint8_t reverseX = (KMATRIXWIDTH - 1) - x;
// 		i = (y * KMATRIXWIDTH) + reverseX;
// 	} 
// 	else 
// 	{
// 		// Even rows run forwards
// 		i = (y * KMATRIXWIDTH) + x;
// 	}
		  
// 	return i;
// }