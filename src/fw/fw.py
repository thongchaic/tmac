import os 
import time
import random
import json 
import _thread
from lora import LoRa
from tokens import Tokens
from names import Names
from tmac import TMAC 
#from mqtt import MQTTx
class Forwarder(object):
    def __init__(self,MAC, device_config, lora_parameters, mqtt_config):
        print("init...Forwarder....")
        self.MAC=MAC 
        self.Ts = 0
        self.To = 0 
        self.isTimeout = True
        self.tries = 0
        self.latest_tries = None 

        self.TOKEN = device_config['token']
        self.tokens = Tokens()

        self.joinResponded = None 
        self.receiveSubscribe = None 
        self.ACK = None 

        self.names = Names()

        self.lora = LoRa(MAC, device_config, lora_parameters)
        self.lora.receivedJoinRequest = self.receivedJoinRequest
        self.lora.receivedJoinResponse = self.receivedJoinResponse
        self.lora.loraReceivedPublish = self.loraReceivedPublish
        self.lora.loraReceivedACK = self.loraReceivedACK
        self.lora.loraSpecial = self.loraSpecial
        self.lora.loraReceivedSubscribe = self.loraReceivedSubscribe

        #self.mqttx = MQTTx(MAC,mqtt_config)

        self.l_buffer = []#fixed: maximum recursion depth exceeded
        
        _thread.start_new_thread(self.daemon,())

 
    def loraPublish(self, payload, ACK):
        GW = self.names.gw()
        payload['MAC'] = self.MAC
        self.ACK = ACK
        self.latest_tries = None 
        self.isTimeout = True 
        #print("loraPublish:", GW, TMAC.PUBLISH, payload)
        self.l_buffer.append( (GW, TMAC.PUBLISH, json.dumps(payload).encode()) )

    def loraReceivedPublish(self,_mac, p_type, p_len, frag_count, _payload):
        #fw fw to mqtt - broker
        #print("loraReceivedPublish",_mac, p_type, _payload)
       
    
        payload = self.toJSON(_payload)
        
        if payload is None:
            return 
        #simulate broker conn.
        if 'id' not in payload:
            print("NoID")
            return 
        if 'MAC' not in payload:
            print("NoMAC")
            return 

        name = self.names.get(payload['MAC'],payload['id'])
        
        #print("MQTT.publish: topic=", name[0], ", data=",payload['values'])
        time.sleep(0.5)

        #ACK
        ack = {
            "token": random.random(),
            "received_len": p_len,
            "frag_count" : frag_count,
            "ACK"  : payload['nonce']
        }

        self.latest_tries = None
        self.isTimeout = True 
        #print("ACK:",payload['MAC'], TMAC.ACK, json.dumps(ack).encode())
        self.l_buffer.append( (payload['MAC'], TMAC.ACK, json.dumps(ack).encode()) )

    def loraReceivedSubscribe(self, _mac, _type, _payload):
        if self.receiveSubscribe:
            self.receiveSubscribe(_mac, _type, _payload)


    def loraReceivedACK(self,_mac, p_type, _payload):
        #print("ACK received:",_mac, p_type, _payload)
        if self.ACK:
            payload = self.toJSON(_payload)
            if payload is None:
                return 
            self.ACK(_mac, p_type, payload)

    def sendJoinRequest(self, _MAC, _payload, callback=None):
        #Received Request
        self.joinResponded = callback
        #print("JoinRequest:",_MAC, TMAC.JOINREQUEST, _payload)
        #print("dumps:",payload)
        self.l_buffer.append( (_MAC, TMAC.JOINREQUEST, _payload) )
        #print(self.l_buffer)
        self.Ts = time.ticks_ms()
        self.isTimeout = False 
        self.tries = 0

        #Send Response 
    def receivedJoinRequest(self, _MAC, _type, _payload):
        #print("receiveJoinRequest:",_MAC, _type, _payload)
        payload = None
        payload = self.toJSON(_payload)
        
        if payload is None:
            return 
        if payload is None:
            return 
        if 'token' not in payload:
            return
        if 'nonce' not in payload:
            return 

        #print("receiveJoinRequest:",_MAC, _type, payload)
        #Respond JoinRequest
        #print("Respond JoinRequest:",type( payload['token']), type(self.TOKEN), payload['token'],self.TOKEN)
        if self.TOKEN == payload['token']:
            token = self.tokens.add(_MAC)
            response = {
                "token" : token,
                "gw"    : self.MAC, 
                "nonce" : payload['nonce']
            }
            #print("Respond JoinRequest:",_MAC, TMAC.JOINRESPONSE, json.dumps(response).encode())
            self.l_buffer.append( (_MAC, TMAC.JOINRESPONSE, json.dumps(response).encode()) )
            #MQTT Subscribe 
            ids = payload['ids']
            for i, name in enumerate(payload['names']):
                #print("MQTT.sub:",i,_MAC,name,ids[i])
                self.names.add( _MAC, ids[i], name, 2 )
        else:
            print("Token not mached!! => do not response....")
    
    def receivedJoinResponse(self,_MAC, _type, _payload):
        #parsed = json.loads(payload)
        #print("JoinResponse:",MAC, _type, _payload)
        payload = None

        try:
            payload = self.toJSON(_payload)
        except:
            #print("json parse failed!!")
            self.loraJoinTimeout()
            return 

        if payload is None:
            return 

        if 'gw' not in payload:
            return 

        if 'token' not in payload:
            return 

        #print(payload)
        token = payload['token']
        self.tokens.add(payload['gw'],token)
        self.latest_tries = None 
        self.isTimeout = True 
        
        self.names.add(payload['gw'], "", "", 1 )

        if self.joinResponded:
            self.joinResponded(1,self.tries, payload)
        self.tries = 0
        
    def loraJoinTimeout(self):
        backoff = random.randint(2,10)
        print("\nloraJoinTimeout[backoff:",backoff,", retry:",self.tries,",",self.latest_tries)
        time.sleep(backoff)
        #print("latest:",self.latest_tries)
        if self.latest_tries is not None:
            self.isTimeout = False
            self.Ts = time.ticks_ms()
            self.l_buffer.append( self.latest_tries )
        self.tries = self.tries + 1 

    def loraSpecial(self,_mac, _type, _payload):
        #print("Trigger to simulate subscribes over lora")
        
        data = self.toJSON(_payload)
        if data is None:
            return 
        if 'letters' not in data:
            return 
        if 'count' not in data:
            return 

        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        i = int(data['count'])
        while i > 0:
            rand = ''.join(random.choice(letters) for i in range(data['letters']))
            payload = {
                "MAC": self.MAC,
                "value": rand,
            }
            #print("send Special:",json.dumps(payload).encode())
            self.l_buffer.append( (data["MAC"], TMAC.SUBSCRIBE, json.dumps(payload).encode()) )
            i = i-1
            time.sleep(5)

    def sendloraSpecial(self,letters,count):
        GW = self.names.gw()
        payload = {
           "MAC": self.MAC,
           "count": count,
           "letters": letters
        }     
        self.l_buffer.append( (GW, TMAC.SPECIAL, json.dumps(payload).encode()) )


    def toJSON(self,payload):
        try:
            return json.loads(payload)
        except:
            print("json parse failed:",payload)
            return None 
    
    def daemon(self): #fix maximum recursion depth exceeded
        interval = time.ticks_ms()
        while True:
            if self.lora:
                self.lora.receive()
            # if self.mqttx:
            #     self.mqttx.receive()

            if self.l_buffer:
                self.latest_tries = self.l_buffer.pop(0)
                self.lora.send( self.latest_tries[0], self.latest_tries[1], self.latest_tries[2] )
         
            if not self.isTimeout:
                self.To = time.ticks_ms()
                if (self.To-self.Ts) > (1000*5):
                    self.isTimeout = True 
                    self.loraJoinTimeout()

