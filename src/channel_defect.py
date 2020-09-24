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
import functions

################################################## Inputs ##################################################

OBU_Directory = '../inputs/OBU_Proxy'
filter_obu_data_type  = [2,14]      # 'all' for all messages, [2,16,14,...] for the messages type you want
#filter_obu_name      = ['DSB MQ','NJ Desiro','LINT41 AR', 'NJ LINT41','DSB IC3','DSB ABs','LT LINT41']
#filter_obu_name      = ['DSB IR4']
g = open('../inputs/JDR_MDR/List_Train.csv','r+')
filter_obu_name = g.readlines()
g.close()
d0 = datetime.date(2019, 8, 1)
DEFECTS = [462,463,464,'CHANNEL']
#DEFECTS = [370,371,372,'PSU']
days_per_period = 7
weeks = 59
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
    
    RMR_Messages_sorted_dru_filtered = []
    RMR_Messages_sorted_tot = []
    for m in RMR_Messages_sorted:
        if(m.OBU_DATA_TYPE == '2'):
            data_hex        = (m.OBU_DATA).encode().hex()
            TRU_NID_MESSAGE = data_hex[0:2]
            if(TRU_NID_MESSAGE == '09'):
                DRU_NID_PACKET = data_hex[16:18]
                if(DRU_NID_PACKET == '01'):
                    DRU_NID_SOURCE = data_hex[22:24]
                    '''if(DRU_NID_SOURCE == '06'):
                        DRU_M_DIAG = data_hex[24:27]
                        if(DRU_M_DIAG == hex(513)[2:]):
                            RMR_Messages_sorted_dru_filtered.append(m)'''
                    if(DRU_NID_SOURCE == '07'):
                        DRU_M_DIAG = data_hex[24:27]
                        if(DRU_M_DIAG == str(hex(DEFECTS[0])[2:]) or DRU_M_DIAG == str(hex(DEFECTS[1])[2:]) or DRU_M_DIAG == str(hex(DEFECTS[2])[2:])):
                            RMR_Messages_sorted_dru_filtered.append(m)
        elif(m.OBU_DATA_TYPE == '14'):
            RMR_Messages_sorted_tot.append(m)
        
                        
    print('End filtering DRU...')
    print('LENGTH MESSAGES DRU : ', len(RMR_Messages_sorted_dru_filtered))
    print('LENGTH MESSAGES COMET INIT : ', len(RMR_Messages_sorted_tot))

################################################## Computing stats ##################################################

    IDs = []
    Names = []
    indexTrains = []
    cnt = 0
    cnt_prev = 0
    for name in filter_obu_name:
        IDs =  IDs + decode_raw_data.get_OBU_IDs_from_OBU_FAMILLY(name, ID_NAME_MAP)
    for id in IDs:
        Names.append(decode_raw_data.get_OBU_NAME_from_OBU_ID(id, ID_NAME_MAP))
    for familly_name in filter_obu_name:
        name = decode_raw_data.get_OBU_NAMES_from_OBU_FAMILLY(familly_name, ID_NAME_MAP)
        cnt  = cnt + len(name)
        indexTrains.append([[cnt_prev,cnt-1],familly_name])
        cnt_prev = cnt

    sum_0 = 0
    sum_1 = 0
    sum_2 = 0
    sum_fan = 0
    channel_X_defect  = np.zeros((len(IDs),len(periods)))
    channel_1_defect  = np.zeros((len(IDs),len(periods)))
    channel_2_defect  = np.zeros((len(IDs),len(periods)))
    channel_3_defect  = np.zeros((len(IDs),len(periods)))
    channel_3_defect_ov_tot = np.zeros((len(IDs),len(periods)))
    #no_ala_fan  = np.zeros((len(IDs),len(periods)))
    tot = np.zeros((len(IDs),len(periods)))
    
    for i in range(0,len(IDs)):
        print('Train op Time computing... '+decode_raw_data.get_OBU_NAME_from_OBU_ID(IDs[i], ID_NAME_MAP))
        for j in range(0,len(periods)):
            tot[i][j]   = mdf.compute_TRAIN_OP_TIME(RMR_Messages_sorted_tot, periods[j], IDs[i], 0.1)
            
    for i in range(0,len(IDs)):
        print(decode_raw_data.get_OBU_NAME_from_OBU_ID(IDs[i], ID_NAME_MAP))
        for j in range(0,len(periods)):
            print('\t',periods[j])
            p = periods[j]
            date1_int = int(p[0].strftime('%y%m%d'))
            date2_int = int(p[1].strftime('%y%m%d'))
            sum_0 = 0
            sum_1 = 0
            sum_2 = 0
            sum_fan = 0
            for m in RMR_Messages_sorted_dru_filtered:
                data_hex        = (m.OBU_DATA).encode().hex()
                gps_field = m.decode_GPS()
                tmp = gps_field[GPS_DATE]
                date_mess = int(tmp[4:6] + tmp[2:4] + tmp[0:2])
                if((m.OBU_ID == IDs[i]) and (date1_int <= date_mess < date2_int)):
                    TRU_NID_MESSAGE = data_hex[0:2]
                    if(TRU_NID_MESSAGE == '09'):
                        DRU_NID_PACKET = data_hex[16:18]
                        if(DRU_NID_PACKET == '01'):
                            DRU_NID_SOURCE = data_hex[22:24]
                            '''if(DRU_NID_SOURCE == '06'):
                                DRU_M_DIAG = data_hex[24:27]
                                if(DRU_M_DIAG == str(hex(513)[2:])):
                                    DRU_X_TEXT = data_hex[30:]
                                    dru_x_text = bytes.fromhex(DRU_X_TEXT)
                                    dru_x_text_ascii = dru_x_text.decode("ascii")
                                    FILIO1 = dru_x_text_ascii[19:39]
                                    FILIO2 = dru_x_text_ascii[63:]
                                    if(FILIO2[14] == '0'):
                                        sum_fan = sum_fan + 1'''
                            if(DRU_NID_SOURCE == '07'):
                                DRU_M_DIAG = data_hex[24:27]
                                if(DRU_M_DIAG == str(hex(DEFECTS[0])[2:])):
                                    sum_0 = sum_0 + 1
                                elif(DRU_M_DIAG == str(hex(DEFECTS[1])[2:])):
                                    sum_1 = sum_1 +1
                                elif(DRU_M_DIAG == str(hex(DEFECTS[2])[2:])):
                                    sum_2 = sum_2 +1
            channel_1_defect[i][j] = sum_0
            channel_2_defect[i][j] = sum_1
            channel_3_defect[i][j] = sum_2
            if(tot[i][j] == 0):
                channel_3_defect_ov_tot[i][j] = -1
            else:
                channel_3_defect_ov_tot[i][j] = channel_3_defect[i][j]*24/tot[i][j]
            #no_ala_fan[i][j] = sum_fan     
            

############################################ Excel ##################################################

    current_time = datetime.datetime.now()
    current_time_string = current_time.strftime("%y%m%d %H%M%S")
    workbook  = xlsxwriter.Workbook('../outputs/reports/'+DEFECTS[3]+'_X_defect_'+current_time_string[0:6]+'_'+current_time_string[7:]+'.xlsx')
    worksheet_1 = workbook.add_worksheet(DEFECTS[3]+' 1')
    worksheet_2 = workbook.add_worksheet(DEFECTS[3]+' 2')
    worksheet_3 = workbook.add_worksheet(DEFECTS[3]+' 3')
    #worksheet_fan = workbook.add_worksheet('FAN MODULE')
    worksheet_tot = workbook.add_worksheet('Train Op Time')
    worksheet_ch3_tot = workbook.add_worksheet('CHANNEL 3 normalized')
    
    excel_functions.write_tableStats(workbook, worksheet_1, DEFECTS[3]+' 1', Names, periods, [2,1], channel_1_defect, [0,5,10])
    excel_functions.write_tableStats(workbook, worksheet_2, DEFECTS[3]+' 2', Names, periods, [2,1], channel_2_defect, [0,5,10])
    excel_functions.write_tableStats(workbook, worksheet_3, DEFECTS[3]+' 3', Names, periods, [2,1], channel_3_defect, [0,5,10])
    excel_functions.write_tableStats(workbook, worksheet_tot,'Train Op Time', Names, periods, [2,1], tot, [0,90,180])
    excel_functions.write_tableStats(workbook, worksheet_ch3_tot, 'CHANNEL 3 normalized', Names, periods, [2,1], channel_3_defect_ov_tot, [0,1,2])
    #excel_functions.write_tableStats(workbook, worksheet_fan,'FAN MODULE', Names, periods, [2,1], no_ala_fan, [0,5,10])
    start = [2,1]
    for i in range(0,len(IDs)):
        worksheet_1.write(start[0]+i,start[1]+len(periods)+1,functions.meanColMatrix(channel_1_defect,i))
        worksheet_2.write(start[0]+i,start[1]+len(periods)+1,functions.meanColMatrix(channel_2_defect,i))
        worksheet_3.write(start[0]+i,start[1]+len(periods)+1,functions.meanColMatrix(channel_3_defect,i))
        worksheet_ch3_tot.write(start[0]+i,start[1]+len(periods)+1,functions.meanColMatrix(channel_3_defect_ov_tot,i))
    workbook.close()


            



    
