#include <Arduino.h>
#include <FastLED.h>

#define ENGR_PIN 27
#define LOGO_PIN 26
#define BAR_PIN 25

#define NUM_LEDS_LOGO 19
#define NUM_LEDS_BAR 20
#define NUM_LEDS_ENGR 10

#define COLOR_ORDER BRG
#define CHIPSET     WS2811

#define BRIGHTNESS  200
#define FRAMES_PER_SECOND 30

class DomotiquePannel
{

	public:
		DomotiquePannel();
		~DomotiquePannel();

		void show(){ FastLED.show(); }

		void delay(unsigned long time_ms){ FastLED.delay(time_ms); }

		void set_bar_animation(unsigned char id);

		void set_engr_animation(unsigned char id);

		void set_logo_animation(unsigned char id);	

		void start();			

	private:

		CRGB leds_engr[NUM_LEDS_ENGR];
		CRGB leds_logo[NUM_LEDS_LOGO];
		CRGB leds_bar[NUM_LEDS_BAR];
	
};