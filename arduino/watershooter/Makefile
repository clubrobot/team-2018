#Board properties
BOARD_UUID = watershooter
BOARD_TAG = nano
BOARD_SUB = atmega328


#Sketch sources
COMMON = ../common
LOCAL_INO_SRCS = watershooter.ino 
LOCAL_CPP_SRCS = \
    instructions.cpp \
    $(COMMON)/SerialTalks.cpp \
    $(COMMON)/BrushlessMotor.cpp \
	$(COMMON)/Adafruit_TCS34725.cpp \
	$(COMMON)/Wire.cpp \
	$(COMMON)/PeriodicProcess.cpp


LOCAL_C_SRCS = \
	$(COMMON)/twi.c


#sketch libraries
ARDUINO_LIBS = Servo EEPROM

CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x20

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk
