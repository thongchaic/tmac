import os 
import time
import random
import json 
import _thread
from lora import LoRa
from tokens import Tokens
from routes import Routes
from names import Names
from tmac import TMAC 
from mqtt import MQTTx

# New idea group ack 
# 
MAX_RETRY = 3

class Forwarder(object):
    
    def __init__(self,MAC, device_config, lora_parameters, mqtt_config):
        print("init...Forwarder....")
        self.MAC=MAC 
        self.Ts = 0
        self.To = 0 
        self.tries = 0
        self.checkTimeout = False
        self.latest_tries = None 

        self.TOKEN = device_config['token']
        self.tokens = Tokens()
        self.routes = Routes()
        self.loraCallback = None 
        self.receiveSubscribe = None 
        self.ACK = None 

        #self.names = Names()

        self.lora = LoRa(MAC, device_config, lora_parameters)
        
        self.lora.receivedJoinRequest = self.receivedJoinRequest
        self.lora.receivedJoinResponse = self.receivedJoinResponse
        self.lora.loraReceivedPublish = self.loraReceivedPublish
        self.lora.loraReceivedACK = self.loraReceivedACK
        #self.lora.loraSpecial = self.loraSpecial
        self.lora.loraReceivedSubscribe = self.loraReceivedSubscribe

        #mqtt_config.enable =  1 

        print("MQTT:",mqtt_config)
        self.mqttx = None 
        if mqtt_config['enabled']:
            self.mqttx = MQTTx(MAC,mqtt_config)
            self.mqttx.mqttReceiveSubscibe = self.mqttReceiveSubscibe
        
        #self.mqttx = MQTTx(MAC,mqtt_config)

        self.l_buffer = []#fixed: maximum recursion depth exceeded
        _thread.start_new_thread(self.daemon,())
 
    def loraPublish(self, _type, _payload, callback=None):
        GW = self.routes.gw()
        #payload['MAC'] = self.MAC
        #self.ACK = ACK
        # self.latest_tries = None 
        # self.isTimeout = True 
        #_payload['src_mac'] = self.MAC
        schc = {
            "rule_id": 1,
            "ack_mode": 1, #Fragmentation mode = ACK Always 
            "src_mac": self.MAC,
            "nonce": random.random(),
            "payload": _payload
        }
       
        print("\n",schc)
        self.checkTimeout = False 
        print("loraPublish:", GW, _type, _payload, ", latest try:", self.latest_tries)
        #                                             # app payload
        self.l_buffer.append( (GW, _type, json.dumps( schc ).encode()) )

    def loraReceivedPublish(self,_mac, p_type, p_len, frag_count, _payload):
        #fw fw to mqtt - broker
        print("loraReceivedPublish",_mac, p_type, p_len, frag_count, _payload)
        payload = self.toJSON(_payload)
        
        if payload is None:
            return
        if not 'payload' in payload:
            print("Payload not found!")
            return
        
        # if 'id' not in payload:
        #     print("NoID")
        #     return 
        # if 'MAC' not in payload:
        #     print("NoMAC")
        #     return 
        #xtract schc JSON
        
        if p_type == TMAC.MQTT_PUBLISH and self.mqttx:
            mqtt_pl = payload['payload']
            if mqtt_pl['with_sub']:
                self.mqttx.add(payload['src_mac'], mqtt_pl['name'])
            self.mqttx.send(mqtt_pl['name'], mqtt_pl['payload'])

        # if p_type == TMAC.MQTT_LORA_SUBSCRIBE and self.mqttx:
        #     pass 

        #elif p_type == TMAC.WS_PUBLISH:
        #    pass 
        #elif p_type == TMAC.REST_PUBLISH
        #   pass 
        # name = self.names.get(payload['MAC'],payload['id'])

        time.sleep(0.1)

        #ACK
        ack = {
            "BACK" : 1, 
            "ACK"  : payload['nonce']
        }

        #self.latest_tries = None
        #self.isTimeout = True 
        print( "ACK:", TMAC.ACK, json.dumps(ack).encode() )
        self.l_buffer.append( (payload['src_mac'], TMAC.ACK, json.dumps(ack).encode()) )

    def loraReceivedACK(self,_mac, p_type, _payload):
        print("ACK received:",_mac, p_type, _payload)
        self.latest_tries = None 
        # if self.ACK:
        #     payload = self.toJSON(_payload)
        #     if payload is None:
        #         return 
        #     self.ACK(_mac, p_type, payload)
    def mqttReceiveSubscibe(self, _MAC, name, payload):
        print("mqttReceiveSubscibe:",name, payload)
        #b'th/ac/srru/thongchai/office/relay' b'off'
        schc = {
            "rule_id": 2,
            "ack_mode": 0, #Fragmentation mode = NoACK 
            "src_mac": self.MAC,
            "nonce": random.random(),
            "payload": {
                "name": name,
                "payload": payload
            }
        }
        self.l_buffer.append( (_MAC, TMAC.MQTT_SUBSCRIBE, json.dumps( schc ).encode()) )
        #self.l_buffer.append( (_MAC, TMAC.JOINREQUEST, _payload) )

    def loraReceivedSubscribe(self, _mac, _type, _payload):
        if self.receiveSubscribe:
            self.receiveSubscribe(_mac, _type, _payload)

    def sendJoinRequest(self, _MAC, _payload, callback=None): #Sender
        self.loraCallback = callback
        print("send-JoinRequest:",_MAC, TMAC.JOINREQUEST, _payload)
        self.l_buffer.append( (_MAC, TMAC.JOINREQUEST, _payload) )
        self.Ts = time.ticks_ms()
        # self.isTimeout = False 
        self.checkTimeout = True 
        self.tries = 0
        #Send Response 

    def receivedJoinRequest(self, _MAC, _type, _payload): #Receiver
        print("receive-JoinRequest:",_MAC, _type, _payload)
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
                "gw"    : self.MAC, 
                "token"    : token, 
                "nonce" : payload['nonce']
            }

            print("response-JoinRequest:",_MAC, TMAC.JOINRESPONSE, json.dumps(response).encode())
            self.l_buffer.append( (_MAC, TMAC.JOINRESPONSE, json.dumps(response).encode()) )
            self.checkTimeout = False 
            #MQTT Subscribe 
            # ids = payload['ids']
            # for i, name in enumerate(payload['names']):
            #     #print("MQTT.sub:",i,_MAC,name,ids[i])
            #     self.names.add( _MAC, ids[i], name, 2 )
        else:
            print("Token not mached!! => do not response....")
    
    def receivedJoinResponse(self, _MAC, _type, _payload):
        #parsed = json.loads(payload)
        print("received-JoinResponse:",_MAC, _type, _payload)
        payload = None

        try:
            payload = self.toJSON(_payload)
        except:
            print("receivedJoinResponse: JSON parse failed!!")
            return 

        if payload is None:
            return 

        if 'gw' not in payload:
            return 

        if 'nonce' not in payload:
            return 

        #print(payload)

        print("self.latest_tries: ",self.latest_tries)
        if payload['nonce'] in self.latest_tries[2]:
            # nonce does not match! 
            print("nonce does not match!")
            # if self.loraCallback:
            #     self.loraCallback(-1,_MAC, _type, _payload)
            return 

        self.tokens.add(payload['gw'],payload['token'])
        self.routes.add(payload['gw'], 'gw')
        self.latest_tries = None 
        self.checkTimeout = False 
        #self.isTimeout = True 
        
        if self.loraCallback:
            self.loraCallback(1, _MAC, _type, _payload)
        
    def ALOHA(self): #ALOHA based protocol 
        backoff = random.randint(2,10)
        print("\nloraJoinTimeout[backoff:",backoff,", retry:",self.tries,",",self.latest_tries)
        time.sleep(backoff)
        #print("latest:",self.latest_tries)
        if self.latest_tries is not None:
            if self.tries < MAX_RETRY:
                #self.isTimeout = False
                self.tries = self.tries+1
                self.Ts = time.ticks_ms()
                self.checkTimeout = True 
                self.l_buffer.append( (self.latest_tries[0],self.latest_tries[1],self.latest_tries[2]) )
                self.latest_tries = None 
            else:
                self.checkTimeout = False 
                self.tries = 0
                self.latest_tries = None 
                self.joinResponded(-1, self.latest_tries[0], self.latest_tries[1], self.latest_tries[2])
]

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
            if self.mqttx:
                if self.mqttx.enabled:
                    self.mqttx.receive()

            if self.l_buffer: #and self.latest_tries is None
                self.latest_tries = self.l_buffer.pop(0)
                                #MAC                  TYPE                  PAYLOAD
                self.lora.send( self.latest_tries[0], self.latest_tries[1], self.latest_tries[2] )

            if self.checkTimeout:# not self.isTimeout:
                self.To = time.ticks_ms()
                if (self.To-self.Ts) > (1000*5): #Collision occur | Gaateway does not in ranges 
                    self.checkTimeout = False 
                    self.ALOHA() #ALOHA 