// //This example code is in the Public Domain (or CC0 licensed, at your option.)
// //By Evandro Copercini - 2018
// //
// //This example creates a bridge between Serial and Classical Bluetooth (SPP)
// //and also demonstrate that SerialBT have the same functionalities of a normal Serial

// #include "BluetoothSerial.h"

// #if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
// #error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
// #endif

// BluetoothSerial SerialBT;

// void setup() {
//   Serial.begin(115200);
//   SerialBT.begin("ESP32test"); //Bluetooth device name
//   Serial.println("The device started, now you can pair it with bluetooth!");
// }

// void loop() {
//   if (Serial.available()) {
//     SerialBT.write(Serial.read());
//   }
//   if (SerialBT.available()) {
//     Serial.write(SerialBT.read());
//   }
//   delay(20);
// }
#include "btstack.h"
 
static void packet_handler (uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size);
 
static btstack_packet_callback_registration_t hci_event_callback_registration;
 
static void packet_handler (uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size){
 
   uint16_t rfcomm_channel_id;
 
   if (packet_type == HCI_EVENT_PACKET
       && hci_event_packet_get_type(packet) == RFCOMM_EVENT_INCOMING_CONNECTION){
 
       rfcomm_channel_id = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);
       rfcomm_accept_connection(rfcomm_channel_id);
 
     }else if (packet_type == RFCOMM_DATA_PACKET){
 
        printf("Received data: '");
 
        for (int i=0;i<size;i++){
             putchar(packet[i]);
         }
 
          printf("\n----------------\n");
    }
}
 
int btstack_main(int argc, const char * argv[]){
 
    hci_event_callback_registration.callback = &packet_handler;
    hci_add_event_handler(&hci_event_callback_registration);
 
    l2cap_init();
 
    rfcomm_init();
 
    rfcomm_register_service(packet_handler, 1, 0xffff); 
 
    sdp_init();
 
    gap_discoverable_control(1);
 
    hci_power_control(HCI_POWER_ON);
 
    return 0;
}