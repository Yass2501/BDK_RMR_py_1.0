import multiprocessing
import decode_raw_data 
import date_time_handling
import time
import datetime
import evc_tru
import rmr_periodic
from global_variables import *
import comet_init
import numpy as np


################################################## Inputs ##################################################

OBU_Directory = '../inputs/OBU_Proxy'
filter_obu_data_type  = [2]      # 'all' for all messages, [2,16,14,...] for the messages type you want
filter_onu_name      = ['DSB MQ 4123']
d0 = datetime.date(2020, 7, 31)
d1 = datetime.date(2020, 8, 7)
Nprocs = 8
para = 1

################################################## Loading RMR Messages ##################################################
if __name__ == '__main__':
    periods = date_time_handling.generate_periods(d0, d1, Nprocs)
    #periods = date_time_handling.generate_periods2(d0, 7, Nprocs)
    print(periods)
    if(para == 1):
        start = time.perf_counter()
        p = multiprocessing.Pool(processes=Nprocs)
        RMR_Messages = p.starmap(decode_raw_data.extract_and_decode_rawData, [(OBU_Directory, periods[i], filter_obu_data_type, filter_onu_name) for i in range(Nprocs)])
        p.close()
        p.join()
        RMR_Messages_reduce = []
        for i in range(0,Nprocs):
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
        RMR_Messages = decode_raw_data.extract_and_decode_rawData(OBU_Directory, periods[0], filter_obu_data_type, filter_onu_name)
        finish = time.perf_counter()
        print(finish - start)
        size = len(RMR_Messages)
        print('LENGTH MESSAGES : ', size)

##########################################################################################################################

    for m in RMR_Messages_sorted:
        data_hex = (m.OBU_DATA).encode().hex()
        TRU_NID_MESSAGE = data_hex[0:2]
        if(TRU_NID_MESSAGE == '00'):
            JRU_Mess = evc_tru.extract_jru_message(m)
            m.date_time_pretty()
            print(int(JRU_Mess.V_TRAIN,2))
            print('===================================================================')
    
    
    
    
    

        
            



    
