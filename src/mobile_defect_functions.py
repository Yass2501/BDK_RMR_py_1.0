import decode_raw_data
import functions
import numpy as np
from global_variables import *



################################################## Functions ##################################################
            

def compute_TRAIN_OP_TIME(RMR_Messages, period, OBU_ID, comet_init_coeff):
        date1_int = int(period[0].strftime('%y%m%d'))
        date2_int = int(period[1].strftime('%y%m%d'))
        train_op_time = 0
        train_op_time_list = []
        train_op_time_tuple = []
        for m in RMR_Messages:
                gps_field = m.decode_GPS()
                tmp = gps_field[GPS_DATE]
                date_mess = int(tmp[4:6] + tmp[2:4] + tmp[0:2])
                if((m.OBU_ID == OBU_ID) and (date1_int <= date_mess < date2_int)):
                        if(m.OBU_DATA_TYPE == '14'):
                                index = functions.findIndexof(m.OBU_DATA, ',', 17)
                                OBU_DATA = m.OBU_DATA
                                TRAIN_OP_TIME = int(OBU_DATA[(index[0]+1):(index[1])])
                                train_op_time_tuple.append((int(TRAIN_OP_TIME),m.date_for_sort,m.time_for_sort))
        train_op_time_tuple_sorted = sorted(train_op_time_tuple, key = lambda x: (x[1],x[2]))
        i = 0 
        for t in train_op_time_tuple_sorted:
                #print(t[0],t[1],t[2])
                train_op_time_list.append(t[0])
                i = i + 1
        offset = 0
        for i in range(0,len(train_op_time_list)-1):
                if((train_op_time_list[i+1]<train_op_time_list[i]) and ((train_op_time_list[i]-train_op_time_list[i+1])/train_op_time_list[i]) > comet_init_coeff):
                        offset = train_op_time_list[i]
                        index = i
                        break
        if(offset > 0):
                for i in range(index+1,len(train_op_time_list)):
                        train_op_time_list[i] = train_op_time_list[i] + offset
        
        if(len(train_op_time_list) == 0):
                return 0
        else:
                return (max(train_op_time_list) - min(train_op_time_list))


def compute_TRAIN_MVNT_TIME(RMR_Messages, period, OBU_ID, comet_init_coeff):
        date1_int = int(period[0].strftime('%y%m%d'))
        date2_int = int(period[1].strftime('%y%m%d'))
        train_mvnt_time = 0
        train_mvnt_time_list = []
        train_mvnt_time_tuple = []
        for m in RMR_Messages:
                gps_field = m.decode_GPS()
                tmp = gps_field[GPS_DATE]
                date_mess = int(tmp[4:6] + tmp[2:4] + tmp[0:2])
                if((m.OBU_ID == OBU_ID) and (date1_int <= date_mess < date2_int)):
                        if(m.OBU_DATA_TYPE == '14'):
                                index = functions.findIndexof(m.OBU_DATA, ',', 17)
                                OBU_DATA = m.OBU_DATA
                                TRAIN_MVNT_TIME = int(OBU_DATA[(index[5]+1):(index[6])])
                                train_mvnt_time_tuple.append((int(TRAIN_MVNT_TIME),m.date_for_sort,m.time_for_sort))
        train_mvnt_time_tuple_sorted = sorted(train_mvnt_time_tuple, key = lambda x: (x[1],x[2]))
        i = 0 
        for t in train_mvnt_time_tuple_sorted:
                #print(t[0],t[1],t[2])
                train_mvnt_time_list.append(t[0])
                i = i + 1
        offset = 0
        for i in range(0,len(train_mvnt_time_list)-1):
                if((train_mvnt_time_list[i+1]<train_mvnt_time_list[i]) and ((train_mvnt_time_list[i]-train_mvnt_time_list[i+1])/train_mvnt_time_list[i]) > comet_init_coeff):
                        offset = train_mvnt_time_list[i]
                        index = i
                        break
        if(offset > 0):
                for i in range(index+1,len(train_mvnt_time_list)):
                        train_mvnt_time_list[i] = train_mvnt_time_list[i] + offset
        
        if(len(train_mvnt_time_list) == 0):
                return 0
        else:
                return (max(train_mvnt_time_list) - min(train_mvnt_time_list))


def compute_occurence(RMR_Messages, period, OBU_ID):
    date1_int = int(period[0].strftime('%y%m%d'))
    date2_int = int(period[1].strftime('%y%m%d'))
    occ = 0
    for m in RMR_Messages:
        gps_field = m.decode_GPS()
        tmp = gps_field[GPS_DATE]
        date_mess = int(tmp[4:6] + tmp[2:4] + tmp[0:2])
        data_hex        = (m.OBU_DATA).encode().hex()
        TRU_NID_MESSAGE = data_hex[0:2]
        if((m.OBU_ID == OBU_ID) and (date1_int <= date_mess < date2_int) and (m.double_check == 0)):
            occ = occ + 1
    return occ



def double_check(RMR_Messages):
    for i in range(0,len(RMR_Messages)-1):
        gps_field_curr = RMR_Messages[i].decode_GPS()
        gps_field_next = RMR_Messages[i+1].decode_GPS()
        if((gps_field_curr[GPS_DATE] == gps_field_next[GPS_DATE]) and (gps_field_curr[GPS_TIME] == gps_field_next[GPS_TIME]) \
           and (RMR_Messages[i].OBU_ID == RMR_Messages[i+1].OBU_ID)):
            RMR_Messages[i+1].double_check = 1


def split_RMR_Messages(RMR_Messages):
    RMR_Messages_mb1 = []
    RMR_Messages_mb2 = []
    RMR_Messages_rad = []
    RMR_Messages_tot = []
    M_DIAG_MB1 = hex(421)[2:]
    M_DIAG_MB2 = hex(422)[2:]
    Q_TEXT_RAD = hex(57)[2:]
    for m in RMR_Messages:
        if(m.OBU_DATA_TYPE == '2'):
            data_hex = (m.OBU_DATA).encode().hex()
            TRU_NID_MESSAGE = data_hex[0:2]
            if(TRU_NID_MESSAGE == '09'):
                DRU_NID_PACKET   = data_hex[16:18]
                if(DRU_NID_PACKET == '01'):
                    DRU_NID_SOURCE    = data_hex[22:24]
                    DRU_M_DIAG        = data_hex[24:27]
                    if(DRU_NID_SOURCE == '07'):
                        if(DRU_M_DIAG == M_DIAG_MB1):
                            RMR_Messages_mb1.append(m)
                        elif(DRU_M_DIAG == M_DIAG_MB2):
                            RMR_Messages_mb2.append(m)
                elif(DRU_NID_PACKET == '05'):
                    DRU_NID_SOURCE    = data_hex[22:24]
                    DRU_N_ITER        = data_hex[24:26]
                    DRU_Q_TEXT        = ['0' for i in range(int(DRU_N_ITER,16))]
                    L_reste = int(len(data_hex[26:]) / int(DRU_N_ITER,16))
                    for i in range(0,int(DRU_N_ITER,16)):  # Loop on N_ITER
                        index = 26 + L_reste*i
                        DRU_Q_TEXT[i]        = data_hex[index+8:index+10]
                        if(DRU_Q_TEXT[i] == Q_TEXT_RAD):
                            RMR_Messages_rad.append(m)
                            break
        elif(m.OBU_DATA_TYPE == '14'):
            RMR_Messages_tot.append(m)

    return [RMR_Messages_mb1,RMR_Messages_mb2,RMR_Messages_rad,RMR_Messages_tot]
                    
                        
                    



                        




