import binascii

class TMAC:
    MAX_PKT_LENGTH=255 #defined by the sx127x.py 
    HEADER_LEN=22

    MQTT_PUBLISH = 1
    MQTT_SUBSCRIBE = 2
    MQTT_LORA_SUBSCRIBE = 7

    ACK = 5
    JOINREQUEST = 3
    JOINRESPONSE = 4
    SPECIAL = 6
    
    def __init__(self):
        print("Init...TMAC En/De-coder")
     
    def decode(self, raw=None ):
        if raw is None or len(raw) <= 22:
            return None, None, None, None, None, None
        try:
            _mac = raw[0:12]
            frag = int(raw[12:14],16)
            f_count = frag & 0xF0
            f_count >>= 4 
            f_index = frag & 0x0F
            p_type = int(raw[14:16],16)
            p_len = len(raw) #int(raw[16:18],16)
            payload = binascii.unhexlify( raw[18:-2])
            _mac = _mac.decode() if isinstance(_mac, (bytes)) else _mac
            payload = payload.decode() if isinstance(payload, (bytes)) else payload
            return _mac, f_count, f_index, p_type, p_len, payload
        except:
            return None, None, None, None, None, None

    def chksum(self,data,poly=0x1021, init_val=0xFFFF):
        #TODO - validate checksum calc
        # crc = init_val
        # for byte in data:
        #     crc ^= (byte << 8) 
        #     for _ in range(8): 
        #         if crc & 0x8000: 
        #             crc = (crc << 1) ^ poly 
        #         else:
        #             crc <<= 1 
        #         crc &= 0xFFFF 
        # return crc
        return 'ab'

    def encode(self,MAC,c,i,t,payload):

        MAC = MAC.encode() if isinstance(MAC, (str)) else MAC

        '''
            | MAC = 48-bit MAC Address
            | t = 8-bit Types Pub/Sub/Join/etc...
            | c = 4-bit Fragment Count 
            | i = 4-bit Fragment Index
            | l = 8-bit Payload Length     
        '''

        chksum = self.chksum(payload)                       #
        f_count = c                                         #
        f_index = i                                         #
        f_count = f_count << 4                              #
        opt = f_count | f_index                             #Fragment Count & Fragment Index 
        opt = ('{:0>2}').format(hex(opt)[2:]).encode()      #
        p_type = ('{:0>2}').format(hex(t)[2:]).encode()     #Packet Types
        p_len = len(payload)                                #plen 
        p_len = ('{:0>2}').format(hex(p_len)[2:]).encode()  #

        encoded = MAC+\
                opt+\
                p_type+\
                p_len+\
                binascii.hexlify(payload)+\
                chksum

        if not encoded:
            return None 
        return encoded.decode()
