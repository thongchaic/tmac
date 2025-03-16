import binascii
import time
from simple import MQTTClient
from tmac import TMAC
class MQTTx: 
    def __init__(self, MAC, mqtt_config):


        self.mqttReceiveSubscibe = None 
        self.mqttx = MQTTClient(MAC, mqtt_config['server'], mqtt_config['port'], mqtt_config['username'], mqtt_config['password'])
        self.mqttx.DEBUG = True 
        # self.mqttx.KEEP_QOS0 = False
        # self.mqttx.NO_QUEUE_DUPS = True
        # self.mqttx.MSG_QUEUE_MAX = 2
        self.mqttx.set_callback(self.subscribe)
        self.enabled = False 
        if mqtt_config['enabled']:
            self.enabled = True
        self.sub_names = {}# {'c44f336aa625': ['th/ac/srru/thongchai/office/relay']}

        if not self.mqttx.connect(clean_session=False):
           print("MQTT connected")
        
        #self.mqttx.subscribe("th/ac/srru/thongchai/office/relay")

    def add(self,_MAC, name):
        if _MAC not in self.sub_names:
            print(_MAC, " not found!")
            self.sub_names[_MAC] = [name]
            print(self.sub_names)
            return 
        if name in self.sub_names[_MAC]:
            print(name, " already subscribed!")
            return
        
        self.sub_names[_MAC].append(name)
        self.mqttx.subscribe(name)
        self.mqttx.connect(clean_session=False) #must reconnect 
        print("MQTTx: sub=>",self.sub_names)
    
    def send(self, name, payload):
        if len(payload) <= 0:
            print("No Payload")
            return
        self.mqttx.publish(name, payload)

    def subscribe(self, topic, data):
        topic = topic.decode() if isinstance(topic, (bytes)) else topic
        data = data.decode() if isinstance(data, (bytes)) else data
        print(topic, data)
        if self.mqttReceiveSubscibe:
            for m in self.sub_names:
                if topic in self.sub_names[m]:
                    self.mqttReceiveSubscibe(m, topic, data)
                    return 
       
    def receive(self):
        self.mqttx.check_msg()