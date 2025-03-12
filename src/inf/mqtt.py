import binascii
import time
from simple import MQTTClient
from tmac import TMAC

class MQTTx: 
    def __init__(self, MAC, mqtt_config):


        self.mqttx = MQTTClient(MAC, mqtt_config['server'], mqtt_config['port'], mqtt_config['username'], mqtt_config['password'])
        self.mqttx.DEBUG = False 
        self.mqttx.KEEP_QOS0 = False
        self.mqttx.NO_QUEUE_DUPS = True
        self.mqttx.MSG_QUEUE_MAX = 2
        self.mqttx.set_callback(self.subscribe)

        if not self.mqttx.connect(clean_session=False):
           print("MQTT connected")
            
    def add(self,name):
        self.mqttx.subscribe(name)

    def send(self, _type, name, payload):
        if len(payload) <= 0:
            return
        self.mqttx.publish(name, payload)
        
    def subscribe(self, topic, data):
        topic = topic.decode() if isinstance(topic, (bytes)) else topic
        data = payload.decode() if isinstance(data, (bytes)) else data
        #print(topic, data)

                
    def receive(self):
        self.mqttx.check_msg()
        