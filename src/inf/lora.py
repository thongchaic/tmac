#import _thread
import time 
from machine import Pin, SoftSPI, reset 
from sx127x import SX127x
import math
import binascii
from tmac import TMAC
import gc 
#ESP32 TTGOv1 

class LoRa(object):
    def __init__(self, MAC, device_config, lora_parameters):
        print("init...LoRa...")
        self.MAC = MAC.decode() if isinstance(MAC, (bytes)) else MAC
        self.tmac = TMAC()
        self.loraSubscribe = None
        self.receivedJoinRequest = None
        self.receivedJoinResponse = None  
        self.loraReceivedPublish = None
        self.loraReceivedACK = None 
        self.loraSpecial = None 
        self.loraReceivedSubscribe = None 
        self.buffer = {}
        gc.enable()
        device_spi = SoftSPI(baudrate = 10000000, 
            polarity = 0, phase = 0, bits = 8, firstbit = SoftSPI.MSB,
            sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
            mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
            miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

        i=5
        while i > 0:
            print(i,'.',end=' ')
            time.sleep(0.5)
            i = i-1
        try:
            self.lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
        except:
            print("\nInit lora failed, system rebooting...")
            time.sleep(1)
            reset()

        self.on_send = False
    
    def send(self,MAC,_type, _payload):
       
        if len(_payload)<=0:
            return
        self.on_send = True
        pkt_len = len(binascii.hexlify(_payload))
        c = int(math.ceil(pkt_len/(TMAC.MAX_PKT_LENGTH-TMAC.HEADER_LEN)))
        if c > 1: 
            size = int(len(_payload)/c)+1
            for i in range( c ):
                frag = _payload[i*size:(i+1)*size]
                hexlify = self.tmac.encode(MAC,c,i,_type,frag)
                time.sleep(0.1)
                self.lora.println(hexlify, implicit_header=False)
        else:
           
            hexlify = self.tmac.encode(MAC,1,0,_type,_payload)
            if hexlify is not None:
                self.lora.println(hexlify, implicit_header=False)
    
        self.on_send = False
        gc.collect()
        
    def receive(self):
        if self.on_send:
            return

        if not self.lora.received_packet():
            return 

        payload = self.lora.read_payload()

        if payload is None or len(payload) < 20:
            return
        
        _mac, f_count, f_index, p_type, p_len, _payload = self.tmac.decode(payload)
        # if p_type == TMAC.PUBLISH:
        #     print("y:",_mac, f_count, f_index, p_type, p_len, _payload)
        if _mac is None or f_count is None or f_index is None or p_type is None or p_len is None or _payload is None:
            return 

        o_payload = ''
        o_plen = 0
        frag_count = 0

        if f_index == 0:
            if _mac in self.buffer:
                self.buffer.pop(_mac)

        if (f_count-1) != f_index: #more frag
            if _mac in self.buffer:
                self.buffer[_mac].append( (f_index,_payload,p_len) )# = self.buffer[name] + payload
            else:
                self.buffer[_mac] = [ (f_index,_payload,p_len) ]
            return
        if (f_count-1) == f_index: #last frag or no frag 
            if _mac in self.buffer:
                self.buffer[_mac].append( (f_index,_payload,p_len) )
                self.buffer[_mac].sort()
                frag_count = len(self.buffer[_mac])
                for i, frag in enumerate(self.buffer[_mac]):
                    #print("R:",_mac,i, frag)
                    o_payload = o_payload + frag[1]
                    o_plen = o_plen+frag[2]
                self.buffer.pop(_mac)
            else:
                frag_count = 1 
                o_payload = _payload #Single fragment
                o_plen = p_len
            
        
        #print(o_payload)
        if p_type == TMAC.JOINREQUEST:
            if self.receivedJoinRequest:
                self.receivedJoinRequest(_mac, p_type, o_payload)
        if p_type == TMAC.JOINRESPONSE:
            if self.receivedJoinResponse:
                self.receivedJoinResponse(_mac, p_type, o_payload)
        
        if p_type == TMAC.PUBLISH and _mac == self.MAC:
            if self.loraReceivedPublish:
                self.loraReceivedPublish(_mac, p_type,o_plen,frag_count, o_payload)
        if p_type == TMAC.SUBSCRIBE and _mac == self.MAC:
            if self.loraReceivedSubscribe:
                self.loraReceivedSubscribe(_mac, p_type, o_payload)

        if p_type == TMAC.ACK and _mac == self.MAC:
            #print("ACK received..")
            if self.loraReceivedACK:
                self.loraReceivedACK(_mac, p_type, o_payload)

        if p_type == TMAC.SPECIAL and _mac == self.MAC:
            if self.loraSpecial:
                self.loraSpecial(_mac, p_type, o_payload)
        gc.collect()
