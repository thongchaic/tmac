import binascii

class TMAC:
    MAX_PKT_LENGTH=255 #defined by the sx127x.py 
    INTEREST = 4
    DATA = 5
    NACK = 6 
    JOIN_INTEREST = 7
    JOIN_DATA = 8
    JOIN_REJECTED = 9 

    def __init__(self):
        print("TMAC En/De-coder")
     
    def decode(self, raw=None):
        
        if raw is None or len(raw) <= 14:
            return None, None, None, None, None, None, None, None
     
        try:
            pkt_type = int(raw[0:2],16)
            frag = int(raw[2:4],16)
            f_count = frag & 0xF0
            f_count >>= 4 
            f_index = frag & 0x0F
            
            chksum = int(raw[4:8],16)
            n_len = int(raw[8:10],16)
            p_len = int(raw[10:12],16)

            name = binascii.unhexlify( raw[ 12:(12+(n_len*2)) ])
            payload = binascii.unhexlify( raw[(12+(n_len*2)):])
            
            name = name.decode() if isinstance(name, (bytes)) else name
            payload = payload.decode() if isinstance(payload, (bytes)) else payload
            
            return pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload
        except:
            return None, None, None, None, None, None, None, None 

    def chksum(self,data):
        #crc = binascii.crc_hqx(data,0)
        #return crc[2:]
        return 'ab'

    def encode(self,MAC,c,i,t,payload):
        #Header + Payload 
        '''
            | MAC = 48-bit MAC Address 
            | t = 8-bit Types Pub/Sub/Join
            | c = 4-bit Fragment Count 
            | i = 4-bit Fragment Index
            | l = 8-bit Payload Length     
        '''
        #no fragmentation & reassembly 

        payloaded = binascii.hexlify( payload )
        chksum = self.chksum(payloaded)
        p_type = t 
        f_count = c #Single Fragment
        f_index = i #Index of the Fragment 
        f_count = f_count << 4 
        opt = f_count | f_index 
        p_len = len(payloaded)
        
        encoded = MAC+\
                binascii.hexlify(chr(opt))+\
                binascii.hexlify(chr(p_type))+\
                binascii.hexlify(chr(p_len))+\
                payloaded+\
                chksum

        if not encoded:
            return None 
        
        print(encoded.decode())
        return encoded.decode()


