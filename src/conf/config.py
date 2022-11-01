# ES32 TTGO v1.0 (https://github.com/Xinyuan-LilyGO/LilyGO-T-Beam/blob/master/src/board_def.h)
#define LORA_SCK        5
#define LORA_MISO       19
#define LORA_MOSI       27
#define LORA_SS         18
#define LORA_DI0        26
#define LORA_RST        23
#define LORA_DIO1       33
#define LORA_BUSY       32

import binascii
import machine

MAC = binascii.hexlify( machine.unique_id() )

device_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':23,
    'led':2,
    'mode':0
}

lora_parameters = {
    'frequency': 9232E6, 
    'tx_power_level': 14, 
    'signal_bandwidth': 125E3,    
    'spreading_factor': 7, 
    'coding_rate': 4, 
    'preamble_length': 8,
    'implicit_header': False, 
    'sync_word': 0x12, 
    'enable_CRC': False,
    'invert_IQ': False
}

mqtt_config = {
    'server':'192.168.1.111',
    'port':1883,
    'tls_enabled': False,
    'username':'miot',
    'password':'mqtt',
    'client_id':'good2cu*99'
}

wifi_config = {
    'ssid':'PNHome2',
    'password':'st11ae58*'
}
