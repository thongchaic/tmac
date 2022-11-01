import network
import time 

import config  
from lora import LoRa
#from fw import Forwarder 
class Main:
    def __init__(self):
        #self.fw = Forwarder(mqtt_config, device_config, lora_parameters)
        self.lora = LoRa(config.MAC, config.device_config, config.lora_parameters)
        
    def wifi_con(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(wifi_config['ssid'], wifi_config['password'])
            while not wlan.isconnected():
                pass

        print(wlan.ifconfig())
    def start(self):
        print("Test LoRa class")

        while True:
            #readsensors
            d = 12.1234
            payload='{id:1,distance:'+str(d)+'}'
            self.lora.send(config.MAC,1, payload.encode() )
            time.sleep(60)
            
        
if __name__ == "__main__":
    main = Main()
    #main.wifi_con() #smart_bin 
    main.start()
