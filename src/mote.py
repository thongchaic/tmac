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
from tmac import TMAC 

class Main:
    def __init__(self):
        self.joined = False 
        self.fw = Forwarder(config.MAC, config.device_config, config.lora_parameters, config.mqtt_config)
        print("""
            #      ^^ 
            #     (oo) 
            #    /(__)\\ 
            #  ----------
            #  <  TMAC  >    
            #  ---------- 
            System Init...""")

    def joinGateway(self):
        self.nonce = random.random() #Generate a new nonce 
        join_payload={
            "token" : config.device_config['token'],
            "nonce" : self.nonce
        }
        self.fw.sendJoinRequest( config.MAC, json.dumps(join_payload).encode() , self.joinResponded)

        while not self.joined:
            time.sleep(1)
        print("network joined")

        data = "ON"

        payload={
            "name" : "th/ac/srru/thongchai/office/relay",
            "value"   : data #TODO - enable end-to-end encryption 
        }

        self.fw.loraPublish(TMAC.MQTT_PUBLISH, payload)
        
        #register mqtt names 

        #subscribe names  

        #publish data
    
    def joinResponded(self,status, _MAC, _type, _payload):
        print("joinResponded,=>",status, _MAC, _type, _payload)
        if status == 1:
            self.joined = True

    def publishCallback(self, _mac, p_type, payload):#=> sould(_mac, status, p_type, payload)
        print(_mac, p_type, payload)

if __name__ == "__main__":
    main = Main()
    main.joinGateway()
