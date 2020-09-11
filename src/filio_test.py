import multiprocessing
import decode_raw_data
import evc_tru
import date_time_handling
import time
import datetime
from global_variables import *
import numpy as np
import xlsxwriter
import excel_functions
import mobile_defect_functions as mdf

################################################## Inputs ##################################################

OBU_Directory = '../inputs/OBU_Proxy'
filter_obu_data_type  = [2]      # 'all' for all messages, [2,16,14,...] for the messages type you want
filter_obu_name      = ['DSB MQ','NJ Desiro','LINT41 AR', 'NJ LINT41','DSB IC3','DSB ABs','LT LINT41']
#filter_obu_name      = ['LINT41 AR']
d0 = datetime.date(2020, 5, 1)
d1 = datetime.date(2020, 8, 1)
DEFECTS = [462,463,464,'CHANNEL']
#DEFECTS = [370,371,372,'PSU']
days_per_period = 7
weeks = 2
para = 1
Nproc = 8

################################################## Loading RMR Messages ##################################################
if __name__ == '__main__':
    periods = date_time_handling.generate_periods2(d0, days_per_period, weeks)
    #periods = date_time_handling.generate_periods(d0, d1, Nproc)
    #print([periods[0][0],periods[len(periods)-1][1]])
    print(periods)
    if(para == 1):
        start = time.perf_counter()
        p = multiprocessing.Pool(processes=weeks)
        RMR_Messages = p.starmap(decode_raw_data.extract_and_decode_rawData, [(OBU_Directory, periods[i], filter_obu_data_type, filter_obu_name) for i in range(weeks)])
        p.close()
        p.join()
        RMR_Messages_reduce = []
        for i in range(0,weeks):
            for m in RMR_Messages[i]:
                RMR_Messages_reduce.append(m)
        RMR_Messages_sorted = sorted(RMR_Messages_reduce, key = lambda x: (x.date_for_sort,x.time_for_sort))
        del RMR_Messages_reduce
        del RMR_Messages
        finish = time.perf_counter()
        print(finish - start)
        print('LENGTH MESSAGES : ', len(RMR_Messages_sorted))
    else:
        start = time.perf_counter()
        RMR_Messages = decode_raw_data.extract_and_decode_rawData(OBU_Directory, [periods[0][0],periods[len(periods)-1][1]], filter_obu_data_type, filter_obu_name)
        RMR_Messages_sorted = sorted(RMR_Messages, key = lambda x: (x.date_for_sort,x.time_for_sort))
        del RMR_Messages
        finish = time.perf_counter()
        print(finish - start)
        size = len(RMR_Messages)
        print('LENGTH MESSAGES : ', size)



################################################## DRU Filter ##################################################

    print('Start filtering DRU...')
    
    for m in RMR_Messages_sorted:
        if(m.OBU_DATA_TYPE == '2'):
            data_hex        = (m.OBU_DATA).encode().hex()
            TRU_NID_MESSAGE = data_hex[0:2]
            if(TRU_NID_MESSAGE == '09'):
                DRU_NID_PACKET = data_hex[16:18]
                if(DRU_NID_PACKET == '01'):
                    DRU_NID_SOURCE = data_hex[22:24]
                    if(DRU_NID_SOURCE == '06'):
                        DRU_M_DIAG = data_hex[24:27]
                        DRU_X_TEXT = data_hex[30:]
                        if(DRU_M_DIAG == hex(513)[2:]):
                            dru_x_text = bytes.fromhex(DRU_X_TEXT)
                            dru_x_text_ascii = dru_x_text.decode("ascii")
                            FILIO1 = dru_x_text_ascii[19:39]
                            FILIO2 = dru_x_text_ascii[63:]
                            print(FILIO2[14])
                        

        
            



    
