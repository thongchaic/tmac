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
        #self.wifi_con()

        self.filename = None 
        self.app_lv_tries = 0
        self.t_start = time.ticks_ms()
        self.letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.fw = Forwarder(config.MAC, config.device_config, config.lora_parameters, config.mqtt_config)
        
    def wifi_con(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(config.wifi_config['ssid'], config.wifi_config['password'])
            while not wlan.isconnected():
                pass

        print(wlan.ifconfig())

    def start(self):
        print("""
#      ^^ 
#     (oo) 
#    /(__)\\ 
#  ----------
#  <  TMAC  >    
#  ---------- 
System Init...""")
        self.TOKEN = None 
        self.next = False 
        if config.device_config['mode'] == 0:
            self.IoTEndDevice()
        elif config.device_config['mode'] == 1:
            self.Gateway()

    def IoTEndDevice(self):
        #file exists 
        counter = self.counter()
            
        auth_payload={
            "token" : config.device_config['token'],
            "names" : ["/tmac/p","/tmac/n"],
            "ids"   : [1, 2],
            "nonce" : random.random()
        }
        print("counter: ",counter)
# 
#####  Experiment 1 :  Join Gateway 
#
        i=40
        self.filename="joinrequest-"+str(counter)+".json"
        print("\n#Experiment 1: Joinrequest",self.filename)
        while i > 0:
            print("#### ",i," ####")
            self.t_start = time.ticks_ms()
            print(">>>>JoinRequest",config.MAC,json.dumps(auth_payload).encode())
            self.fw.sendJoinRequest( config.MAC,json.dumps(auth_payload).encode(), self.joinResponded)
            self.next = False 
            while not self.next:
                #print(".",end="")
                time.sleep(0.5)
            i = i-1
            time.sleep(2)




#         
#####  Experiment 2 : Publish with 250 bytes of payload over LoRa ##############################################################
#        
        self.filename="publish-250-"+str(counter)+".json"
        self.next = False 
        self.fw.sendJoinRequest( config.MAC,json.dumps(auth_payload).encode(), self.joinResponded)
        while not self.next:
            print(".",end="")
            time.sleep(0.5)
        print("\n#Experiment 2: 250 bytes",self.filename)
        
        i=40
        payload={
            "token" : self.TOKEN,
            "id"   : 1,
            "values": {"hall":esp32.hall_sensor(),"temp":esp32.raw_temperature()},
            "nonce" : random.random()
        }
        tries = 0 #application level retransmission 
        self.app_lv_tries = 0
        while i > 0:
            print("####",i,"####")
            self.t_start = time.ticks_ms()
            self.next = False
            #print(">>>>loraPublish:",json.dumps(payload))
            self.fw.loraPublish(payload, self.ACK)
            timeout = True  
            while time.ticks_diff(time.ticks_ms(),self.t_start) < 10000:
                if not self.next:
                    timeout = False 
                    #print(".",end="")
                    time.sleep(0.5)
                    print("")
                    break  
            if not timeout:
                i = i-1
                time.sleep(1)
            else:
                print("timeout=>retry:",self.app_lv_tries)
                self.app_lv_tries = self.app_lv_tries+1  
                time.sleep(2)
            
#        
#####  Experiment 3 : Publish with 500 bytes of payload over LoRa  ########################################################
   
        i=40
        self.filename="publish-500-"+str(counter)+".json"
        print("""\n#Experiment 3 : 500bytes """+self.filename)
        self.next = False 
        self.fw.sendJoinRequest( config.MAC,json.dumps(auth_payload).encode(), self.joinResponded)
        while not self.next:
            print(".",end="")
            time.sleep(0.5)
        
        payload={
            "token" : self.TOKEN,
            "id"   : 1,
            "values": {"hall":esp32.hall_sensor(),"temp":esp32.raw_temperature()},
            "nonce" : random.random()
        }
        pad = 295-len(binascii.hexlify( json.dumps(payload).encode() ))
        padding = ''.join(random.choice(self.letters) for i in range(pad))
        payload['padding'] = padding
        tries = 0 #application level retransmission 
        time.sleep(2)

        #self.fw.loraPublish(payload, self.ACK)
        
        self.app_lv_tries = 0
        while i > 0:
            print("####",i,"####")
            self.t_start = time.ticks_ms()
            self.next = False
            self.fw.loraPublish(payload, self.ACK)
            timeout = True  
            while time.ticks_diff(time.ticks_ms(),self.t_start) < 10000:
                #print(".")
                time.sleep(0.5)
                if self.next:
                    timeout = False 
                    break  
            if not timeout:
                i = i-1
                time.sleep(1)
            else:
                self.app_lv_tries = self.app_lv_tries+1  
                print("Timeout retry:",self.app_lv_tries)
                time.sleep(2)
            
#        
#####  Experiment 4 : Publish with 750 bytes of payload over LoRa  ########################################################
#    
        i=40
        self.filename="publish-750-"+str(counter)+".json"
        print("""\n\n\n#Experiment 4 : 750bytes """+self.filename)
        self.next = False 
        self.fw.sendJoinRequest( config.MAC,json.dumps(auth_payload).encode(), self.joinResponded)
        while not self.next:
            print(".",end="")
            time.sleep(0.5)
        

        payload={
            "token" : self.TOKEN,
            "id"   : 1,
            "values": {"hall":esp32.hall_sensor(),"temp":esp32.raw_temperature()},
            "nonce" : random.random()
        }
        pad = 400-len(binascii.hexlify( json.dumps(payload).encode() ))
        padding = ''.join(random.choice(self.letters) for i in range(pad))
        payload['padding'] = padding
        tries = 0 #application level retransmission 
        time.sleep(2)

        #self.fw.loraPublish(payload, self.ACK)
        
        self.app_lv_tries = 0
        while i > 0:
            print("####",i,"####")
            self.t_start = time.ticks_ms()
            self.next = False
            self.fw.loraPublish(payload, self.ACK)
            timeout = True  
            while time.ticks_diff(time.ticks_ms(),self.t_start) < 10000:
                time.sleep(0.5)
                if self.next:
                    timeout = False 
                    break  
            if not timeout:
                i = i-1
                time.sleep(1)
            else:
                self.app_lv_tries = self.app_lv_tries+1  
                print("Timeout => tries:",self.app_lv_tries)
                time.sleep(2)


#        
#####  Experiment 5 : Subscribe  ########################################################
#    
        i=40
        self.filename="subscribe-"+str(counter)+".json"
        print("""\n\n\n#Experiment 5 :  Subscribe"""+self.filename)
        self.next = False 
        self.fw.sendJoinRequest( config.MAC,json.dumps(auth_payload).encode(), self.joinResponded)
        while not self.next:
            print(".",end="")
            time.sleep(0.5)
        
        payload={
            "token" : random.random(),
            "id"   : 1,
            "values": {"hall":esp32.hall_sensor(),"temp":esp32.raw_temperature()},
            "nonce" : random.random()
        }
        tries = 0 #application level retransmission 
        time.sleep(2)        
        self.app_lv_tries = 0
        while i > 0:
            print("####",i,"####")
            #print(">>>loraPublish:",json.dumps(payload))
            self.next = False     
            self.t_start = time.ticks_ms()
            self.fw.loraPublish(payload, self.ACK)
            timeout = True  
            while time.ticks_diff(time.ticks_ms(),self.t_start) < 10000:
                time.sleep(0.5)
                if self.next:
                    timeout = False 
                    break  
            if not timeout:
                i = i-1
                time.sleep(1)
            else:
                self.app_lv_tries = self.app_lv_tries+1  
                print("Timeout => tries:",self.app_lv_tries)
                time.sleep(2)


    def receiveSubscribe(self,_mac, _type, _payload):
        print("receiveSubscribe:",_mac, _type, _payload)
    
    
    def joinResponded(self,_status,tries, payload):
        #print("joinResponded(Ready to send DATA)",_status,tries,payload)
        #print("Ready to send DATAs")
        delay = time.ticks_diff(time.ticks_ms(), self.t_start)
        payload['tries'] = tries
        payload['status'] = _status
        payload['memfree'] = gc.mem_free()
        payload['delay'] = delay
        payload['t_start'] = self.t_start
        payload['t_stop'] = time.ticks_ms()
        self.TOKEN = payload['token']
        print("<<<<Response & write:",self.filename,json.dumps(payload))
        self.writeNclose(self.filename,json.dumps(payload))
        self.next = True 

    def ACK(self,_mac, p_type,  payload):        
        payload['tries'] = self.app_lv_tries
        self.app_lv_tries = 0
        payload['memfree'] = gc.mem_free()
        payload['t_start'] = self.t_start
        payload['t_stop'] = time.ticks_ms()
        payload['delay'] = time.ticks_diff(time.ticks_ms(), self.t_start)
        payload['hall'] = esp32.hall_sensor()
        payload['temp'] = esp32.raw_temperature()
        print("<<<<ACK & write:",self.filename,json.dumps(payload))
        self.writeNclose(self.filename,json.dumps(payload))
        self.next = True

    def Gateway(self):
        #self.wifi_con()
        print("Gateway")

    def onSubscribe(self, _type, topic, payload):
        print("type:",_type)
        print("topic:",topic)
        print("payload:",payload) 
    
    def counter(self):
        if 'counter' not in os.listdir():
            f = open("counter","w")
            f.write(1)
            f.close()
            return 1 
        
        g = open("counter","r")
        i = int(g.read())
        g.close()

        j = i+1
        h = open("counter","w")
        h.write(str(j))
        h.close()

        return j

    def writeNclose(self,filename,data):
        f = open(filename,"a")
        print(filename,":",data)
        f.write(data+"\n")
        f.close()

if __name__ == "__main__":
    main = Main()
    main.start()
