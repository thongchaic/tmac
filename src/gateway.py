import network
import time 
import random 
import config  
import json 
import gc 
import os 
import binascii
import esp32 
from fw import Forwarder 

class Main:
    def __init__(self):
        self.fw = Forwarder(config.MAC, config.device_config, config.lora_parameters, config.mqtt_config)

    def start(self):
        print("""
            #      ^^ 
            #     (oo) 
            #    /(__)\ 
            #   ----------
            #  < TMAC(GW) >    
            #  ---------- 
            System Init...""")        
    # def wifi_con(self):
    #     wlan = network.WLAN(network.STA_IF)
    #     wlan.active(True)
    #     if not wlan.isconnected():
    #         wlan.connect(config.wifi_config['ssid'], config.wifi_config['password'])
    #         while not wlan.isconnected():
    #             pass
    #     print(wlan.ifconfig())
    
if __name__ == "__main__":
    main = Main()
    main.start()
    #main.wifi_con()
