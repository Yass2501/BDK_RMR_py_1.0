import multiprocessing
import decode_raw_data
import date_time_handling
import datetime
import comet_init
import time
import numpy as np
from global_variables import *


#----------------------------------------------------- Inputs ----------------------------------------------------
OBU_Directory = '../inputs/OBU_Proxy'
KM_TARGET = 1500
print_successive = 1
filter_obu_data_type = [14]
d0 = datetime.date(2020, 8, 1)
d1 = datetime.date(2020, 9, 1)
Nprocs   = 8
'''filter_obu_name = ['DSB ABs 7901', 'DSB IC3 5025', 'DSB IC3 5041', 'LT LINT41 2035', \
                   'LT LINT41 2031', 'LT LINT41 2032', 'LINT41 AR 2042', 'LINT41 AR 2040', \
                   'DSB MQ 4123', 'DSB MQ 4124']'''
filter_obu_name = ['LT LINT41 2035']
ODO_or_GPS = 'ODO'
if(Nprocs > 1):
    para = 1
else:
    para = 0
periods = date_time_handling.generate_periods(d0, d1, Nprocs)
print(periods)
################################################## Loading RMR Messages ##################################################
if __name__ == '__main__':
    periods = date_time_handling.generate_periods(d0, d1, Nprocs)
    #periods = date_time_handling.generate_periods2(d0, 7, Nprocs)
    print(periods)
    if(para == 1):
        start = time.perf_counter()
        p = multiprocessing.Pool(processes=Nprocs)
        RMR_Messages = p.starmap(decode_raw_data.extract_and_decode_rawData, [(OBU_Directory, periods[i], filter_obu_data_type, filter_obu_name) for i in range(Nprocs)])
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
        RMR_Messages_sorted = sorted(RMR_Messages_reduce, key = lambda x: (x.date_for_sort,x.time_for_sort))
        del RMR_Messages
        finish = time.perf_counter()
        print(finish - start)
        size = len(RMR_Messages)
        print('LENGTH MESSAGES : ', size)

##########################################################################################################################


    
    TrainID   = []
    f = open('../inputs/id_train_mapping.txt','r+')
    id_name_map = f.readlines()
    f.close()
    for train_name in filter_obu_name:
        TrainID.append(decode_raw_data.get_OBU_ID_from_OBU_NAME(train_name, id_name_map))

    for i in range(len(filter_obu_name)):
        comet_init.check_KM_ODO_or_KM_GPS(TrainID[i], filter_obu_name[i], RMR_Messages_sorted, KM_TARGET, ODO_or_GPS, print_successive)
    




