import os
import decode_raw_data
import multiprocessing
import datetime
import date_time_handling
import time
import bit_bytes_manipulation
from global_variables import *

################################################## Classes ##################################################

class DRU_Message(object):
    
    def __init__(self,L_MESSAGE, DATE, TIME_PADDING,\
                 DRU_NID_PACKET, DRU_NID_SOURCE, \
                 DRU_M_DIAG, DRU_NID_CHANNEL,\
                 DRU_L_TEXT, DRU_X_TEXT, DRU_N_ITER,\
                 DRU_NID_DATA, DRU_L_DATA, DRU_Q_TEXTCLASS,\
                 DRU_Q_TEXTCONFIRM, DRU_Q_TEXT
                 ):
        self.L_MESSAGE = L_MESSAGE
        self.DATE = DATE
        self.TIME_PADDING = TIME_PADDING
        self.DRU_NID_PACKET = DRU_NID_PACKET
        self.DRU_NID_SOURCE = DRU_NID_SOURCE
        self.DRU_M_DIAG = DRU_M_DIAG
        self.DRU_L_TEXT = DRU_L_TEXT
        self.DRU_X_TEXT = DRU_X_TEXT
        self.DRU_N_ITER = DRU_N_ITER
        self.DRU_NID_DATA = DRU_NID_DATA
        self.DRU_L_DATA = DRU_L_DATA
        self.DRU_Q_TEXTCLASS = DRU_Q_TEXTCLASS
        self.DRU_Q_TEXTCONFIRM = DRU_Q_TEXTCONFIRM
        self.DRU_Q_TEXT = DRU_Q_TEXT

    def dru_x_text_ascii(self):
        if(isinstance(self.DRU_X_TEXT, list)):
            dru_x_text_ascii = []
            for d in self.DRU_X_TEXT:
                dru_x_text = bytes.fromhex(d)
                dru_x_text_ascii.append(dru_x_text.decode("ascii"))
            return dru_x_text_ascii
        else:
            dru_x_text = bytes.fromhex(self.DRU_X_TEXT)
            dru_x_text_ascii = dru_x_text.decode("ascii")
            return dru_x_text_ascii
    
        


class JRU_Message(object):

    def __init__(self, NID_MESSAGE, L_MESSAGE, DATE, TIME, Q_SCALE, NID_LRBG,\
                 D_LRBG, Q_DIRLRBG, Q_DLRBG, L_DOUBTOVER,\
                 L_DOUBTUNDER, V_TRAIN, DRIVER_ID, NID_ENGINE,\
                 SYSTEM_VERSION, LEVEL, MODE, PACKET_VARIABLES):
        
        self.NID_MESSAGE = NID_MESSAGE
        self.L_MESSAGE = L_MESSAGE
        self.DATE = DATE
        self.TIME = TIME
        self.Q_SCALE = Q_SCALE
        self.NID_LRBG = NID_LRBG
        self.D_LRBG = D_LRBG
        self.Q_DIRLRBG = Q_DIRLRBG
        self.Q_DLRBG = Q_DLRBG
        self.L_DOUBTOVER = L_DOUBTOVER
        self.L_DOUBTUNDER = L_DOUBTUNDER
        self.V_TRAIN = V_TRAIN
        self.DRIVER_ID = DRIVER_ID
        self.NID_ENGINE = NID_ENGINE
        self.SYSTEM_VERSION = SYSTEM_VERSION
        self.LEVEL = LEVEL
        self.MODE = MODE
        self.PACKET_VARIABLES = PACKET_VARIABLES
        

################################################## Functions ##################################################


def extract_dru_message(RMR_Message):
    DRU_Mess = DRU_Message(None, None, None,\
                             None, None,\
                             None, None,\
                             None, None, None,\
                             None, None, None,\
                             None, None)
    data_hex = (RMR_Message.OBU_DATA).encode().hex()
    TRU_NID_MESSAGE = data_hex[0:2]
    if(RMR_Message.OBU_DATA_TYPE == '2' and TRU_NID_MESSAGE == '09'):
        L_MESSAGE        = data_hex[2:6]
        DATE             = data_hex[6:10]
        TIME_PADDING     = data_hex[10:16]
        DRU_NID_PACKET   = data_hex[16:18]
        DRU_L_PACKET     = data_hex[18:22]
        if(DRU_NID_PACKET == '01'):
            DRU_NID_SOURCE    = data_hex[22:24]
            DRU_M_DIAG        = data_hex[24:27]
            DRU_NID_CHANNEL   = data_hex[27:28]
            DRU_L_TEXT        = data_hex[28:30]
            DRU_X_TEXT        = data_hex[30:]
            DRU_L_DATA        = None
            DRU_Q_TEXTCLASS   = None
            DRU_Q_TEXTCONFIRM = None
            DRU_Q_TEXT        = None
            DRU_N_ITER        = None
            DRU_NID_DATA      = None
            DRU_Mess = DRU_Message(L_MESSAGE, DATE, TIME_PADDING,\
                                 DRU_NID_PACKET, DRU_NID_SOURCE,\
                                 DRU_M_DIAG, DRU_NID_CHANNEL,\
                                 DRU_L_TEXT, DRU_X_TEXT, DRU_N_ITER,\
                                 DRU_NID_DATA, DRU_L_DATA, DRU_Q_TEXTCLASS,\
                                 DRU_Q_TEXTCONFIRM, DRU_Q_TEXT)
        elif(DRU_NID_PACKET == '05'):
            DRU_NID_SOURCE    = data_hex[22:24]
            DRU_N_ITER        = data_hex[24:26]
            DRU_M_DIAG        = None
            DRU_NID_CHANNEL   = None
            # Allocation
            DRU_NID_DATA      = ['0' for i in range(int(DRU_N_ITER,16))]
            DRU_L_DATA        = ['0' for i in range(int(DRU_N_ITER,16))]
            DRU_Q_TEXTCLASS   = ['0' for i in range(int(DRU_N_ITER,16))]
            DRU_Q_TEXTCONFIRM = ['0' for i in range(int(DRU_N_ITER,16))]
            DRU_Q_TEXT        = ['0' for i in range(int(DRU_N_ITER,16))]
            DRU_L_TEXT        = ['0' for i in range(int(DRU_N_ITER,16))]
            DRU_X_TEXT        = ['0' for i in range(int(DRU_N_ITER,16))]                
            L_reste = int(len(data_hex[26:]) / int(DRU_N_ITER,16))
            for i in range(0,int(DRU_N_ITER,16)):  # Loop on N_ITER
                index = 26 + L_reste*i
                DRU_NID_DATA[i]      = data_hex[index:index+2]
                DRU_L_DATA[i]        = data_hex[index+2:index+4]
                DRU_Q_TEXTCLASS[i]   = data_hex[index+4:index+6]
                DRU_Q_TEXTCONFIRM[i] = data_hex[index+6:index+8]
                DRU_Q_TEXT[i]        = data_hex[index+8:index+10]
                DRU_L_TEXT[i]        = data_hex[index+10:index+12]
                DRU_X_TEXT[i]        = data_hex[index+12:((index+12)+int(DRU_L_TEXT[i],16)*2)]
            DRU_Mess = DRU_Message(L_MESSAGE, DATE, TIME_PADDING,\
                                 DRU_NID_PACKET, DRU_NID_SOURCE,\
                                 DRU_M_DIAG, DRU_NID_CHANNEL,\
                                 DRU_L_TEXT, DRU_X_TEXT, DRU_N_ITER,\
                                 DRU_NID_DATA, DRU_L_DATA, DRU_Q_TEXTCLASS,\
                                 DRU_Q_TEXTCONFIRM, DRU_Q_TEXT)
        else:
            DRU_Mess = DRU_Message(None, None, None,\
                             None, None,\
                             None, None,\
                             None, None, None,\
                             None, None, None,\
                             None, None)
    return DRU_Mess



def extract_jru_message(RMR_Message):
    JRU_Mess = JRU_Message(None, None, None,\
                             None, None,\
                             None, None,\
                             None, None, None,\
                             None, None, None,\
                             None, None, None,\
                             None, None)
    data_hex = (RMR_Message.OBU_DATA).encode().hex()
    TRU_NID_MESSAGE = data_hex[0:2]
    if(RMR_Message.OBU_DATA_TYPE == '2' and TRU_NID_MESSAGE == '00'):
        data_bin = bit_bytes_manipulation.hexToBin_loop(data_hex)
        NID_MESSAGE = data_bin[8:16]
        L_MESSAGE = data_bin[16:27]
        DATE      = data_bin[27:43]
        TIME      = data_bin[43:65]
        Q_SCALE   = data_bin[65:67]
        NID_LRBG  = data_bin[67:91]
        D_LRBG    = data_bin[91:106]
        Q_DIRLRBG = data_bin[106:108]
        Q_DLRBG   = data_bin[108:110]
        L_DOUBTOVER = data_bin[110:125]
        L_DOUBTUNDER = data_bin[125:140]
        V_TRAIN = data_bin[140:150]
        DRIVER_ID = data_bin[150:278]
        NID_ENGINE = data_bin[278:302]
        SYSTEM_VERSION = data_bin[302:309]
        LEVEL = data_bin[309:312]
        MODE = data_bin[312:316]
        PACKET_VARIABLES = data_bin[316:]
        JRU_Mess = JRU_Message(NID_MESSAGE, L_MESSAGE, DATE, TIME, Q_SCALE, NID_LRBG,\
                 D_LRBG, Q_DIRLRBG, Q_DLRBG, L_DOUBTOVER,\
                 L_DOUBTUNDER, V_TRAIN, DRIVER_ID, NID_ENGINE,\
                 SYSTEM_VERSION, LEVEL, MODE, PACKET_VARIABLES)
        
    return JRU_Mess


def MM_compute_occurence(RMR_Messages, period, OBU_ID, M_DIAG):
    date1_int = int(period[0].strftime('%y%m%d'))
    date2_int = int(period[1].strftime('%y%m%d'))
    occ = 0
    for m in RMR_Messages:
        gps_field = m.decode_GPS()
        tmp = gps_field[GPS_DATE]
        date_mess = int(tmp[4:6] + tmp[2:4] + tmp[0:2])
        data_hex        = (m.OBU_DATA).encode().hex()
        TRU_NID_MESSAGE = data_hex[0:2]
        if((m.OBU_ID == OBU_ID) and (date1_int <= date_mess < date2_int)):
            if(m.OBU_DATA_TYPE == '2' and TRU_NID_MESSAGE == '09'):
                DRU_Mess = extract_dru_message(m)
                if(DRU_Mess.DRU_NID_PACKET == '01'):
                    if(DRU_Mess.DRU_NID_SOURCE == '07'):
                        if(DRU_Mess.DRU_M_DIAG == M_DIAG):
                            occ = occ + 1
    return occ

def TEXT_MESSAGE_compute_occurence(RMR_Messages, period, OBU_ID, Q_TEXT):
    date1_int = int(period[0].strftime('%y%m%d'))
    date2_int = int(period[1].strftime('%y%m%d'))
    occ = 0
    for m in RMR_Messages:
        gps_field = m.decode_GPS()
        tmp = gps_field[GPS_DATE]
        date_mess = int(tmp[4:6] + tmp[2:4] + tmp[0:2])
        data_hex        = (m.OBU_DATA).encode().hex()
        TRU_NID_MESSAGE = data_hex[0:2]
        if((m.OBU_ID == OBU_ID) and (date1_int <= date_mess < date2_int)):
            if(m.OBU_DATA_TYPE == '2' and TRU_NID_MESSAGE == '09'):
                DRU_Mess = extract_dru_message(m)
                if(DRU_Mess.DRU_NID_PACKET == '05'):
                    if(DRU_Mess.DRU_NID_SOURCE == '01'):
                        if(isinstance(DRU_Mess.DRU_Q_TEXT, list)):
                            sum = 0
                            for q in DRU_Mess.DRU_Q_TEXT:
                                if(q == Q_TEXT):
                                    sum = sum + 1
                            occ = occ + sum
                        else:
                            if(DRU_Mess.DRU_Q_TEXT == Q_TEXT):
                                occ = occ + 1
    return occ
                        




