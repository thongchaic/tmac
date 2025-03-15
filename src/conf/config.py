# ES32 TTGO v1.0 (https://github.com/Xinyuan-LilyGO/LilyGO-T-Beam/blob/master/src/board_def.h)
#define LORA_SCK        5
#define LORA_MISO       19
#define LORA_MOSI       27
#define LORA_SS         18
#define LORA_DI0        26
#define LORA_RST        23
#define LORA_DIO1       33
#define LORA_BUSY       32

# +---------+---------------------------------------------------------+
# | Value   | Description                                             |
# +---------+---------------------------------------------------------+
# | DevAddr | DevAddr (32 bits) =  device-specific network address    |
# |         | generated from the NetID                                |
# | AppEUI  | IEEE EUI64 value corresponding to the join server for   |
# |         | an application                                          |
# | NwkSKey | 128-bit network session key used with AES-CMAC          |
# | AppSKey | 128-bit application session key used with AES-CTR       |
# | AppKey  | 128-bit application session key used with AES-ECB       |
# +---------+---------------------------------------------------------+

import binascii
import machine

MAC = binascii.hexlify( machine.unique_id() )  #DevAddr
TOKEN = b'36f8f780c'
AppKey = b"1234567890ABCDEF"

device_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':23,
    'led':2,
    'token': '36f8f780c'
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
    'enabled': False,  #mote must be False 
    'server':'202.29.30.31',
    'port':1883,
    'tls_enabled': False,
    'username':'cssrru',
    'password':'good2cu*99',
    'client_id':'9ce4abc3a6c3204ef5a5d98b18a018fe'
}

wifi_config = {
    'ssid':'CSIoT',
    'password':'11235813'
}