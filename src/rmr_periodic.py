import bit_bytes_manipulation 

class RMR_PERIODIC_Message(object):

    def __init__(self, RMR_PERIODIC_VERSION, TRAIN_POSITION_Q_SCALE,\
                 TRAIN_POSITION_NID_LRGB, TRAIN_POSITION_D_LRGB,\
                 TRAIN_POSITION_Q_DIRLRGB, TRAIN_POSITION_Q_DLRBG,\
                 TRAIN_POSITION_L_DOUBTOVER, TRAIN_POSITION_L_DOUBTUNDER,\
                 V_TRAIN):
        
        self.RMR_PERIODIC_VERSION        = RMR_PERIODIC_VERSION
        self.TRAIN_POSITION_Q_SCALE      = TRAIN_POSITION_Q_SCALE
        self.TRAIN_POSITION_NID_LRGB     = TRAIN_POSITION_NID_LRGB
        self.TRAIN_POSITION_D_LRGB       = TRAIN_POSITION_D_LRGB
        self.TRAIN_POSITION_Q_DIRLRGB    = TRAIN_POSITION_Q_DIRLRGB
        self.TRAIN_POSITION_Q_DLRBG      = TRAIN_POSITION_Q_DLRBG
        self.TRAIN_POSITION_L_DOUBTOVER  = TRAIN_POSITION_L_DOUBTOVER
        self.TRAIN_POSITION_L_DOUBTUNDER = TRAIN_POSITION_L_DOUBTUNDER
        self.V_TRAIN                     = V_TRAIN



def extract_rmr_periodic_message(RMR_Message):
    RMR_PERIODIC_Mess = RMR_PERIODIC_Message(None, None,\
                 None, None, None, None,None, None,None)
    
    if(RMR_Message.OBU_DATA_TYPE == '16'):
        data_hex = (RMR_Message.OBU_DATA).encode().hex()
        data_bits = ''
        for i in range(len(data_hex)):
            data_bits = data_bits + bit_bytes_manipulation.hexToBin(data_hex[i])
        RMR_PERIODIC_VERSION = data_bits[0:8]
        TRAIN_POSITION_Q_SCALE = data_bits[8:10]
        TRAIN_POSITION_NID_LRGB = data_bits[10:34]
        TRAIN_POSITION_D_LRGB = data_bits[34:49]
        TRAIN_POSITION_Q_DIRLRGB = data_bits[49:51]
        TRAIN_POSITION_Q_DLRBG = data_bits[51:53]
        TRAIN_POSITION_L_DOUBTOVER = data_bits[53:68]
        TRAIN_POSITION_L_DOUBTUNDER = data_bits[68:83]
        V_TRAIN = data_bits[83:93]

        RMR_PERIODIC_Mess = RMR_PERIODIC_Message(RMR_PERIODIC_VERSION, TRAIN_POSITION_Q_SCALE,\
                 TRAIN_POSITION_NID_LRGB, TRAIN_POSITION_D_LRGB,\
                 TRAIN_POSITION_Q_DIRLRGB, TRAIN_POSITION_Q_DLRBG,\
                 TRAIN_POSITION_L_DOUBTOVER, TRAIN_POSITION_L_DOUBTUNDER,\
                 V_TRAIN)

    return RMR_PERIODIC_Mess
    
        
        
        
    
