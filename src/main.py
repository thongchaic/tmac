import network
import time 
import config  
#from fw import Forwarder 
class Main:
    def __init__(self):
        #self.fw = Forwarder(mqtt_config, device_config, lora_parameters)
        pass 
    def wifi_con(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(wifi_config['ssid'], wifi_config['password'])
            while not wlan.isconnected():
                pass

        print(wlan.ifconfig())
    def start(self):
        pass 
        
if __name__ == "__main__":
    main = Main()
    main.wifi_con()
    main.start()
