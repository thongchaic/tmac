#import _thread
import time 
from machine import Pin, SoftSPI
from sx127x import SX127x
import math
from tmac import TMAC
#ESP32 TTGOv1 

class LoRa(object):
    def __init__(self, MAC, device_config, lora_parameters):
        print("init...LoRa...")
        self.tmac = TMAC()
        self.onPublish = None
        self.onSubscribe = None
        self.onJoin = None 

        self.buffer = {}

        device_spi = SoftSPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SoftSPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

        i=5
        while i > 0:
            print(i,'.',end=' ')
            time.sleep(1)
            i = i-1
        
        self.lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
        self.MAC = MAC
        self.on_send = False
        
    def send(self,MAC,_type, payload):
       
        if len(payload)<=0:
            return
        self.on_send = True

        #prefix = name[len(name)-10:]

        pkt_len = 14+(len(name)*2)+(len(payload)*2)
        if pkt_len>TMAC.MAX_PKT_LENGTH: #Do fragmentation 
            c = int(math.ceil(pkt_len/TMAC.MAX_PKT_LENGTH))
            size = int(len(payload)/c)+1
            for i in range( c ):
                frag = payload[i*size:(i+1)*size]
                
                hexlify = self.tmac.encode(MAC,c,i,_type,frag)
                self.lora.println(hexlify, implicit_header=False)
                time.sleep(0.10)
        else:
            #encode( MAC,c,i,t,payload )
            hexlify = self.tmac.encode(MAC,1,0,_type,payload)

            self.lora.println(hexlify, implicit_header=False)
        self.on_send = False
        
    def receive(self):
        if self.on_send:
            return

        if not self.lora.received_packet():
            return 

        payload = self.lora.read_payload()
        if payload is None or len(payload) < 14:
            return

        pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(payload)
        
        if pkt_type is None:
            return 

        #suffix = name
        #for sfx in self.buffer.keys():
        #   if sfx in name:
        #       name = sfx 
        #       break 

        if (f_count-1) != f_index: #more frag
            if name in self.buffer:
                self.buffer[name].append([f_index,payload])# = self.buffer[name] + payload
            else:
                self.buffer[name] = [f_index,payload]
            return
        
        if (f_count-1) == f_index: #last frag or no frag 
            if name in self.buffer:
                #payload = self.buffer[name] + payload
                if len(self.buffer[name]) != f_count: #missed some fragments 
                    self.buffer.pop(name)
                    return
                self.buffer[name].sort()
                _payload = ''
                for p in enumerate(self.buffer[name]):
                    _payload += p
                payload = _payload+payload
                self.buffer.pop(name)
