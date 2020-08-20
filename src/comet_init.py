import decode_raw_data
import functions
import numpy as np
from global_variables import *




class COMET_INIT_Message(object):

        time_fort_sort = 0 
        date_for_sort = 0

        def __init__(self, COMET_INIT_VERSION, COMET_TRAIN_OP_TIME, COMET_DMI1_OP_TIME,\
                     COMET_DMI2_OP_TIME, COMET_DMI3_OP_TIME, COMET_DMI4_OP_TIME,\
                     COMET_TRAIN_MVNT_TIME, COMET_KM_GPS, COMET_KM_ODO, COMET_KMAC_DATE,\
                     COMET_EVC_TEST_DATE, COMET_EVC_TEST_STATUS, COMET_EVC_PRJ_VERSION_INCOHERENT,\
                     COMET_EVC_CUR_PRJ_VERSION, COMET_EVC_CUR_GATC_BASELINE, COMET_EVC_CUR_CONFIG_VERSION,\
                     COMET_EVC_MAX_TEMPERATURE_LAST_RUN, COMET_FIFO_CLEARED):

                self.COMET_INIT_VERSION = COMET_INIT_VERSION
                self.COMET_TRAIN_OP_TIME = COMET_TRAIN_OP_TIME
                self.COMET_DMI1_OP_TIME = COMET_DMI1_OP_TIME
                self.COMET_DMI2_OP_TIME = COMET_DMI2_OP_TIME
                self.COMET_DMI3_OP_TIME = COMET_DMI3_OP_TIME
                self.COMET_DMI4_OP_TIME = COMET_DMI4_OP_TIME
                self.COMET_TRAIN_MVNT_TIME = COMET_TRAIN_MVNT_TIME
                self.COMET_KM_GPS = COMET_KM_GPS
                self.COMET_KM_ODO = COMET_KM_ODO
                self.COMET_KMAC_DATE = COMET_KMAC_DATE
                self.COMET_EVC_TEST_DATE = COMET_EVC_TEST_DATE
                self.COMET_EVC_TEST_STATUS = COMET_EVC_TEST_STATUS
                self.COMET_EVC_PRJ_VERSION_INCOHERENT = COMET_EVC_PRJ_VERSION_INCOHERENT
                self.COMET_EVC_CUR_PRJ_VERSION = COMET_EVC_CUR_PRJ_VERSION
                self.COMET_EVC_CUR_GATC_BASELINE = COMET_EVC_CUR_GATC_BASELINE
                self.COMET_EVC_CUR_CONFIG_VERSION = COMET_EVC_CUR_CONFIG_VERSION
                self.COMET_EVC_MAX_TEMPERATURE_LAST_RUN = COMET_EVC_MAX_TEMPERATURE_LAST_RUN
                self.COMET_FIFO_CLEARED = COMET_FIFO_CLEARED
                
                
def extract_comet_init_messages(RMR_Messages):
        COMET_INIT_Messages = []
        for m in RMR_Messages:
                OBU_DATA = m.OBU_DATA
                if(m.OBU_DATA_TYPE == '14'):
                        index = functions.findIndexof(m.OBU_DATA, ',', 17)
                        COMET_INIT_VERSION                 = OBU_DATA[0:(index[0])]
                        COMET_TRAIN_OP_TIME                = OBU_DATA[(index[0]+1):(index[1])]
                        COMET_DMI1_OP_TIME                 = OBU_DATA[(index[1]+1):(index[2])]
                        COMET_DMI2_OP_TIME                 = OBU_DATA[(index[2]+1):(index[3])]
                        COMET_DMI3_OP_TIME                 = OBU_DATA[(index[3]+1):(index[4])]
                        COMET_DMI4_OP_TIME                 = OBU_DATA[(index[4]+1):(index[5])]
                        COMET_TRAIN_MVNT_TIME              = OBU_DATA[(index[5]+1):(index[6])]
                        COMET_KM_GPS                       = OBU_DATA[(index[6]+1):(index[7])]
                        COMET_KM_ODO                       = OBU_DATA[(index[7]+1):(index[8])]
                        COMET_KMAC_DATE                    = OBU_DATA[(index[8]+1):(index[9])]
                        COMET_EVC_TEST_DATE                = OBU_DATA[(index[9]+1):(index[10])]
                        COMET_EVC_TEST_STATUS              = OBU_DATA[(index[10]+1):(index[11])]
                        COMET_EVC_PRJ_VERSION_INCOHERENT   = OBU_DATA[(index[11]+1):(index[12])]
                        COMET_EVC_CUR_PRJ_VERSION          = OBU_DATA[(index[12]+1):(index[13])]
                        COMET_EVC_CUR_GATC_BASELINE        = OBU_DATA[(index[13]+1):(index[14])]
                        COMET_EVC_CUR_CONFIG_VERSION       = OBU_DATA[(index[14]+1):(index[15])]
                        COMET_EVC_MAX_TEMPERATURE_LAST_RUN = OBU_DATA[(index[15]+1):(index[16])]
                        COMET_FIFO_CLEARED                 = OBU_DATA[(index[16]+1):]

                        COMET_INIT_Messages.append(COMET_INIT_Message(COMET_INIT_VERSION, COMET_TRAIN_OP_TIME, COMET_DMI1_OP_TIME,\
                     COMET_DMI2_OP_TIME, COMET_DMI3_OP_TIME, COMET_DMI4_OP_TIME,\
                     COMET_TRAIN_MVNT_TIME, COMET_KM_GPS, COMET_KM_ODO, COMET_KMAC_DATE,\
                     COMET_EVC_TEST_DATE, COMET_EVC_TEST_STATUS, COMET_EVC_PRJ_VERSION_INCOHERENT,\
                     COMET_EVC_CUR_PRJ_VERSION, COMET_EVC_CUR_GATC_BASELINE, COMET_EVC_CUR_CONFIG_VERSION,\
                     COMET_EVC_MAX_TEMPERATURE_LAST_RUN, COMET_FIFO_CLEARED))

        return COMET_INIT_Messages


def extract_comet_init_message(RMR_Message):
        COMET_INIT_Mess = COMET_INIT_Message(None, None, None,\
                                             None, None, None,\
                                             None, None, None,\
                                             None, None, None,\
                                             None, None, None,\
                                             None, None, None)
        OBU_DATA = RMR_Message.OBU_DATA
        if(RMR_Message.OBU_DATA_TYPE == '14'):
                index = functions.findIndexof(OBU_DATA, ',', 17)
                COMET_INIT_VERSION                 = OBU_DATA[0:(index[0])]
                COMET_TRAIN_OP_TIME                = OBU_DATA[(index[0]+1):(index[1])]
                COMET_DMI1_OP_TIME                 = OBU_DATA[(index[1]+1):(index[2])]
                COMET_DMI2_OP_TIME                 = OBU_DATA[(index[2]+1):(index[3])]
                COMET_DMI3_OP_TIME                 = OBU_DATA[(index[3]+1):(index[4])]
                COMET_DMI4_OP_TIME                 = OBU_DATA[(index[4]+1):(index[5])]
                COMET_TRAIN_MVNT_TIME              = OBU_DATA[(index[5]+1):(index[6])]
                COMET_KM_GPS                       = OBU_DATA[(index[6]+1):(index[7])]
                COMET_KM_ODO                       = OBU_DATA[(index[7]+1):(index[8])]
                COMET_KMAC_DATE                    = OBU_DATA[(index[8]+1):(index[9])]
                COMET_EVC_TEST_DATE                = OBU_DATA[(index[9]+1):(index[10])]
                COMET_EVC_TEST_STATUS              = OBU_DATA[(index[10]+1):(index[11])]
                COMET_EVC_PRJ_VERSION_INCOHERENT   = OBU_DATA[(index[11]+1):(index[12])]
                COMET_EVC_CUR_PRJ_VERSION          = OBU_DATA[(index[12]+1):(index[13])]
                COMET_EVC_CUR_GATC_BASELINE        = OBU_DATA[(index[13]+1):(index[14])]
                COMET_EVC_CUR_CONFIG_VERSION       = OBU_DATA[(index[14]+1):(index[15])]
                COMET_EVC_MAX_TEMPERATURE_LAST_RUN = OBU_DATA[(index[15]+1):(index[16])]
                COMET_FIFO_CLEARED                 = OBU_DATA[(index[16]+1):]

                COMET_INIT_Mess = COMET_INIT_Message(COMET_INIT_VERSION, COMET_TRAIN_OP_TIME, COMET_DMI1_OP_TIME,\
                     COMET_DMI2_OP_TIME, COMET_DMI3_OP_TIME, COMET_DMI4_OP_TIME,\
                     COMET_TRAIN_MVNT_TIME, COMET_KM_GPS, COMET_KM_ODO, COMET_KMAC_DATE,\
                     COMET_EVC_TEST_DATE, COMET_EVC_TEST_STATUS, COMET_EVC_PRJ_VERSION_INCOHERENT,\
                     COMET_EVC_CUR_PRJ_VERSION, COMET_EVC_CUR_GATC_BASELINE, COMET_EVC_CUR_CONFIG_VERSION,\
                     COMET_EVC_MAX_TEMPERATURE_LAST_RUN, COMET_FIFO_CLEARED)

        return COMET_INIT_Mess

                        

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
                                COMET_INIT_Mess = extract_comet_init_message(m)
                                train_op_time_tuple.append((int(COMET_INIT_Mess.COMET_TRAIN_OP_TIME),m.date_for_sort,m.time_for_sort))
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

def compute_TRAIN_OP_TIME_para(RMR_Messages, periods, OBU_IDs, comet_init_coeff):
        train_op_time = np.zeros((len(OBU_IDs),len(periods)))
        i = 0
        for id in OBU_IDs:
                print(decode_raw_data.get_OBU_NAME_from_OBU_ID(id, ID_NAME_MAP))
                j = 0
                for period in periods:
                        date1_int = int(period[0].strftime('%y%m%d'))
                        date2_int = int(period[1].strftime('%y%m%d'))
                        train_op_time_list = []
                        train_op_time_tuple = []
                        for m in RMR_Messages:
                                gps_field = m.decode_GPS()
                                tmp = gps_field[GPS_DATE]
                                date_mess = int(tmp[4:6] + tmp[2:4] + tmp[0:2])
                                if((m.OBU_ID == id) and (date1_int <= date_mess < date2_int)):
                                        if(m.OBU_DATA_TYPE == '14'):
                                                COMET_INIT_Mess = extract_comet_init_message(m)
                                                train_op_time_tuple.append((int(COMET_INIT_Mess.COMET_TRAIN_OP_TIME),m.date_for_sort,m.time_for_sort))
                        train_op_time_tuple_sorted = sorted(train_op_time_tuple, key = lambda x: (x[1],x[2]))
                        ii = 0 
                        for t in train_op_time_tuple_sorted:
                                train_op_time_list.append(t[0])
                                ii = ii + 1
                        offset = 0
                        for ii in range(0,len(train_op_time_list)-1):
                                if((train_op_time_list[ii+1]<train_op_time_list[ii]) and ((train_op_time_list[ii]-train_op_time_list[ii+1])/train_op_time_list[ii]) > comet_init_coeff):
                                        offset = train_op_time_list[ii]
                                        index = ii
                                        break
                        if(offset > 0):
                                for ii in range(index+1,len(train_op_time_list)):
                                        train_op_time_list[ii] = train_op_time_list[ii] + offset
                        
                        if(len(train_op_time_list) == 0):
                                train_op_time[i][j] = 0
                        else:
                                train_op_time[i][j] = (max(train_op_time_list) - min(train_op_time_list))
                        j = j + 1
                i = i + 1
        return train_op_time
                
'''                        
def check_reset_COMET(TrainID, TrainName, RMR_Messages, ODO_or_GPS, print_successive):
        COMET_TRAIN_OP_TIME_prev = 0
        COMET_KM_ODO_prev   = np.inf
        COMET_KM_GPS_prev   = np.inf
        COMET_TRAIN_OP_TIME_prev = 0
        COMET_KM_prev = np.inf
        IsReset = False
        for m in RMR_Messages:
            if(m.OBU_ID == TrainID):
                index = findIndexof(m.OBU_DATA, ',', 17)
                gps_field      = m.decode_GPS()
                OBU_DATE       = gps_field[GPS_DATE]
                OBU_TIME       = gps_field[GPS_TIME]
                OBU_DATA       = m.OBU_DATA
                COMET_KM_ODO   = int(OBU_DATA[(index[7]+1):(index[8])])
                COMET_KM_GPS   = int(OBU_DATA[(index[6]+1):(index[7])])
                COMET_TRAIN_OP_TIME = int(OBU_DATA[(index[0]+1):(index[1])])
                if(print_successive):
                    print(COMET_TRAIN_OP_TIME)
                if(ODO_or_GPS == 'ODO'):
                    COMET_KM = COMET_KM_ODO
                if(ODO_or_GPS == 'GPS'):
                    COMET_KM = COMET_KM_GPS
                if(COMET_TRAIN_OP_TIME < COMET_TRAIN_OP_TIME_prev):
                    IsReset = True
                    break
                if(ODO_or_GPS == 'ODO'):
                    COMET_KM_prev = COMET_KM_ODO
                if(ODO_or_GPS == 'GPS'):
                    COMET_KM_prev = COMET_KM_GPS
                OBU_DATE_prev       = OBU_DATE
                OBU_TIME_prev       = OBU_TIME
                COMET_TRAIN_OP_TIME_prev = COMET_TRAIN_OP_TIME
                COMET_KM_ODO_prev = COMET_KM_ODO
                COMET_KM_GPS_prev = COMET_KM_GPS
        if(IsReset):
            hour = str(OBU_TIME)
            hour = hour[0]+hour[1]+':'+hour[2]+hour[3]+':'+hour[4]+hour[5]
            hour_prev = str(OBU_TIME_prev)
            hour_prev = hour_prev[0]+hour_prev[1]+':'+hour_prev[2]+hour_prev[3]+':'+hour_prev[4]+hour_prev[5]
            print('===============================================================================================================================')
            print('[20'+OBU_DATE_prev[4]+OBU_DATE_prev[5]+'-'+OBU_DATE_prev[2]+OBU_DATE_prev[3]+'-'+OBU_DATE_prev[0]+OBU_DATE_prev[1]+'  '+hour+']',end=' ')
            print('TRAIN_OP_TIME of train '+TrainName+': '+' with value ['+str(COMET_TRAIN_OP_TIME_prev)+']; ',end=' ')
            print('KM_GPS is : '+str(COMET_KM_GPS_prev)+'; ', end=' ')
            print('KM_ODO is : '+str(COMET_KM_ODO_prev))
            print('[20'+OBU_DATE[4]+OBU_DATE[5]+'-'+OBU_DATE[2]+OBU_DATE[3]+'-'+OBU_DATE[0]+OBU_DATE[1]+'  '+hour+']',end=' ')
            print('TRAIN_OP_TIME of train '+TrainName+': '+' with value ['+str(COMET_TRAIN_OP_TIME)+']; ',end=' ')
            print('KM_GPS is : '+str(COMET_KM_GPS)+'; ', end=' ')
            print('KM_ODO is : '+str(COMET_KM_ODO))
            print('===============================================================================================================================')
        else:
            print('No reset comet has been detected in this period')

#############################################################

def check_KM_ODO_or_KM_GPS(TrainID, TrainName, RMR_Messages, KM_TARGET, ODO_or_GPS, print_successive):
        COMET_KM_ODO_prev   = np.inf
        COMET_KM_GPS_prev   = np.inf
        COMET_KM_prev = np.inf
        IsFound = False
        for m in RMR_Messages:
            if(m.OBU_ID == TrainID):
                index = findIndexof(m.OBU_DATA, ',', 17)
                gps_field      = m.decode_GPS()
                OBU_DATE       = gps_field[GPS_DATE]
                OBU_TIME       = gps_field[GPS_TIME]
                OBU_DATA       = m.OBU_DATA
                COMET_KM_ODO   = int(OBU_DATA[(index[7]+1):(index[8])])
                COMET_KM_GPS   = int(OBU_DATA[(index[6]+1):(index[7])])
                if(ODO_or_GPS == 'ODO'):
                    COMET_KM = COMET_KM_ODO
                if(ODO_or_GPS == 'GPS'):
                    COMET_KM = COMET_KM_GPS
                if(COMET_KM >= KM_TARGET and COMET_KM_prev <= KM_TARGET):
                    IsFound = True
                    break
                if(print_successive):
                    print(COMET_KM)
                if(ODO_or_GPS == 'ODO'):
                    COMET_KM_prev = COMET_KM_ODO
                if(ODO_or_GPS == 'GPS'):
                    COMET_KM_prev = COMET_KM_GPS
                OBU_DATE_prev       = OBU_DATE
                OBU_TIME_prev       = OBU_TIME
        if(IsFound):
            hour = str(OBU_TIME)
            hour = hour[0]+hour[1]+':'+hour[2]+hour[3]+':'+hour[4]+hour[5]
            hour_prev = str(OBU_TIME_prev)
            hour_prev = hour_prev[0]+hour_prev[1]+':'+hour_prev[2]+hour_prev[3]+':'+hour_prev[4]+hour_prev[5]
            print('===============================================================================')
            print('[20'+OBU_DATE_prev[4]+OBU_DATE_prev[5]+'-'+OBU_DATE_prev[2]+OBU_DATE_prev[3]+'-'+OBU_DATE_prev[0]+OBU_DATE_prev[1]+'  '+hour_prev+']',end=' ')
            print('KM_'+ODO_or_GPS+' of train '+TrainName+': '+' with value ['+str(COMET_KM_prev)+']')
            print('[20'+OBU_DATE[4]+OBU_DATE[5]+'-'+OBU_DATE[2]+OBU_DATE[3]+'-'+OBU_DATE[0]+OBU_DATE[1]+'  '+hour+']',end=' ')
            print('KM_'+ODO_or_GPS+' of train '+TrainName+': '+' with value ['+str(COMET_KM)+']')
            print('===============================================================================')
        else:
            print('The value of '+str(KM_TARGET)+' km has not been find in this period')'''
