#     0                   1                   2                   3
#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                                                               |
#    ~                          Base Header                          ~
#    |                                                               |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                                                               |
#    ~                     Peer Header (variable)                    ~
#    |                                                               |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                 Payload Info Header (optional)                |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                      Payload Data (variable)                  |
#    ~                                                               ~
#    |               +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |               |          Padding (0-255 bytes)                |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                                                               |
#    ~              Integrity Check Value-ICV (variable)             ~
#    |                                                               |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

class EESP: 

    def __init__(self, raw):
        # self.base_header = None  #middleboxes such as routers or firewalls
        # self.peer_header = None  #The 'Peer Header' is used to support replay protection and to store cryptographic synchronization data
        # self.payload_header = 0x00000000 
        # self.payload_data = None #+padding 
        # self.icv = None 

    def init_base_header(self):
        first_bit = 0x1 #1b-it 
        version = 0xa  #4-bit
        opt_len = 0xb  #5-bit
        flags = 0x00    #6-bit
        sess_id = 0x0000#16-bit 

        base_header = (first_bit << 31) | (version << 28) | (opt_len << 23) | (flags << 16) | (sess_id)
        return base_header

    def init_peer_header(self):
        pass 
        
    def print()
    