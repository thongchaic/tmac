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
#from tmac import TMAC 

class Main:
    def __init__(self):
        self.fw = Forwarder(config.MAC, config.device_config, config.lora_parameters, config.mqtt_config)

    def start(self):
        print("""
#      ^^ 
#     (oo) 
#    /(__)\\ 
#  ----------
#  <  TMAC  >    
#  ---------- 
System Init...""")


if __name__ == "__main__":
    main = Main()
    main.start()
