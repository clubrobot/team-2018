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
    $(COMMON)/BrushlessMotor.cpp



#sketch libraries
ARDUINO_LIBS = Servo EEPROM

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk
