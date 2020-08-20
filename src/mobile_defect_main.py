import multiprocessing
import decode_raw_data 
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
filter_obu_data_type  = [2,14]      # 'all' for all messages, [2,16,14,...] for the messages type you want
filter_obu_name      = ['DSB MQ','NJ Desiro','LINT41 AR', 'NJ LINT41','DSB IC3','DSB ABs','LT LINT41']
#filter_obu_name      = ['NJ Desiro','DSB ABs']
d0 = datetime.date(2020, 6, 1)
days_per_period = 7
weeks = 8
para = 1

################################################## Loading RMR Messages ##################################################
if __name__ == '__main__':
    periods = date_time_handling.generate_periods2(d0, 7, weeks)
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

################################################## Computing stats ##################################################

    [RMR_Messages_mb1,RMR_Messages_mb2,RMR_Messages_rad,RMR_Messages_tot] = mdf.split_RMR_Messages(RMR_Messages_sorted)
    RMR_Messages_mb = sorted(RMR_Messages_mb1+RMR_Messages_mb2, key = lambda x: (x.date_for_sort,x.time_for_sort))
    mdf.double_check(RMR_Messages_mb1)
    mdf.double_check(RMR_Messages_mb2)
    print(len(RMR_Messages_mb1),len(RMR_Messages_mb2),len(RMR_Messages_rad),len(RMR_Messages_tot))
    
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
      
    occ1  = np.zeros((len(IDs),len(periods)))
    occ2  = np.zeros((len(IDs),len(periods)))
    occ   = np.zeros((len(IDs),len(periods)))
    rad   = np.zeros((len(IDs),len(periods)))
    tot   = np.zeros((len(IDs),len(periods)))
    tmvnt = np.zeros((len(IDs),len(periods)))
    occ_tot   = np.zeros((len(IDs),len(periods)))
    occ_mvnt  = np.zeros((len(IDs),len(periods)))
    
    for i in range(0,len(IDs)):
        print(decode_raw_data.get_OBU_NAME_from_OBU_ID(IDs[i], ID_NAME_MAP))
        for j in range(0,len(periods)):
            occ1[i][j]  = mdf.compute_occurence(RMR_Messages_mb1, periods[j], IDs[i])
            occ2[i][j]  = mdf.compute_occurence(RMR_Messages_mb2, periods[j], IDs[i])
            rad[i][j]   = mdf.compute_occurence(RMR_Messages_rad, periods[j], IDs[i])
            tot[i][j]   = mdf.compute_TRAIN_OP_TIME(RMR_Messages_tot, periods[j], IDs[i], 0.1)
            tmvnt[i][j] = mdf.compute_TRAIN_MVNT_TIME(RMR_Messages_tot, periods[j], IDs[i], 0.1)
            
    occ = occ1 + occ2
    for i in range(0,len(IDs)):
        for j in range(0,len(periods)):
            if(tot[i][j] == 0):
                occ_tot[i][j] = -1
            else:
                occ_tot[i][j] = occ[i][j]*24/tot[i][j]
            if(tmvnt[i][j] == 0):
                occ_mvnt[i][j] = -1
            else:
                occ_mvnt[i][j] = occ[i][j]*24/tmvnt[i][j]

################################################## Writing on excel sheets ##################################################
    current_time = datetime.datetime.now()
    current_time_string = current_time.strftime("%y%m%d %H%M%S")
    workbook = xlsxwriter.Workbook('../outputs/reports/mobile_defect_'+current_time_string[0:6]+'_'+current_time_string[7:]+'.xlsx')
    
    worksheet_dt_mb = workbook.add_worksheet('Data treated Mobile Defects')
    worksheet_dt_rd = workbook.add_worksheet('Data treated Radio Failure')
    worksheet_mb1   = workbook.add_worksheet('Mobile defect 1')
    worksheet_mb2   = workbook.add_worksheet('Mobile defect 2')
    worksheet_mb    = workbook.add_worksheet('Mobile defect')
    worksheet_mb_tot = workbook.add_worksheet('Mobile defect ov Tain Op Time')
    worksheet_mb_mvnt = workbook.add_worksheet('Mobile defect ov Tain Mvnt Time')
    worksheet_rd    = workbook.add_worksheet('Radio Failure')
    worksheet_tot   = workbook.add_worksheet('Train Op Time')
    worksheet_mvnt  = workbook.add_worksheet('Train Mvnt Time')
    worksheet_mb_report = workbook.add_worksheet('Report')

        # Data treated sheet filling
    Inputs_fieds  = ['Train name','OBU date','OBU time','Latitude','Longitude','Full coordinates','Mobile defect','Full date']
    true_format   = workbook.add_format({'bold': False, 'fg_color': 'red','align': 'center'})
    false_format  = workbook.add_format({'bold': False, 'fg_color': 'yellow','align': 'center'})
    titles_format = workbook.add_format({'bold': True,'align': 'center'})
    coord_format  = workbook.add_format({'bold': False,'align': 'left'})
    mobile_defect_format = workbook.add_format({'bold': False,'align': 'center'})
    for j in range(0,len(Inputs_fieds)):
        worksheet_dt_mb.set_column(0,j,25)
        worksheet_dt_mb.write(0,j,Inputs_fieds[j],titles_format)
    i = 1
    for mess in RMR_Messages_mb:
        if(mess.double_check == 0):
            if(m.OBU_DATA_TYPE == '2'):
                data_hex = (mess.OBU_DATA).encode().hex()
                TRU_NID_MESSAGE = data_hex[0:2]
                if(TRU_NID_MESSAGE == '09'):
                    DRU_NID_PACKET   = data_hex[16:18]
                    if(DRU_NID_PACKET == '01'):
                        DRU_NID_SOURCE    = data_hex[22:24]
                        DRU_M_DIAG        = data_hex[24:27]
                        if(DRU_NID_SOURCE == '07'):
                            if(DRU_M_DIAG == hex(421)[2:]):
                                mobile = 1
                            elif(DRU_M_DIAG == hex(422)[2:]):
                                mobile = 2
            name  = mess.name_frome_ID(ID_NAME_MAP)
            gps   = mess.decode_GPS()
            date  = gps[GPS_DATE]
            date2 = date[0]+date[1]+'-'+date[2]+date[3]+'-'+date[4]+date[5]
            Time  = gps[GPS_TIME]
            Time  = Time[0]+Time[1]+':'+Time[2]+Time[3]+':'+Time[4]+Time[5]
            lat   = gps[GPS_LATITUDE]
            long  = gps[GPS_LONGITUDE]
            if(len(lat)>0):
                lat_maps  = float(lat[0]+lat[1])+float(lat[2:len(lat)-1])/60
                lat = lat[0:2]+u'\N{DEGREE SIGN}'+lat[2:len(lat)-1]+' '+lat[len(lat)-1]
            else:
                lat_maps  = ''
                lat = u'\N{DEGREE SIGN}'+' N'
            if(len(long)>0):
                long_maps = float(long[0]+long[1]+long[2])+float(long[3:len(long)-1])/60
                long = long[0:3]+u'\N{DEGREE SIGN}'+long[3:len(long)-1]+' '+long[len(long)-1]
            else:
                long_maps = ''
                long = u'\N{DEGREE SIGN}'+' E'
            worksheet_dt_mb.write(i,0,name)
            worksheet_dt_mb.write(i,1,date2)
            worksheet_dt_mb.write(i,2,Time)
            worksheet_dt_mb.write(i,3,lat_maps,coord_format)
            worksheet_dt_mb.write(i,4,long_maps,coord_format)
            worksheet_dt_mb.write(i,5,lat+' '+long)
            worksheet_dt_mb.write(i,6,mobile,mobile_defect_format)
            worksheet_dt_mb.write(i,7,'20'+date[4]+date[5]+'-'+date[2]+date[3]+'-'+date[0]+date[1]+'  '+Time)
            i = i + 1


    # Data treated sheet filling
    Inputs_fieds  = ['Train name','OBU date','OBU time','Latitude','Longitude','Full coordinates','Full date']
    true_format   = workbook.add_format({'bold': False, 'fg_color': 'red','align': 'center'})
    false_format  = workbook.add_format({'bold': False, 'fg_color': 'yellow','align': 'center'})
    titles_format = workbook.add_format({'bold': True,'align': 'center'})
    coord_format  = workbook.add_format({'bold': False,'align': 'left'})
    mobile_defect_format = workbook.add_format({'bold': False,'align': 'center'})
    for j in range(0,len(Inputs_fieds)):
        worksheet_dt_rd.set_column(0,j,25)
        worksheet_dt_rd.write(0,j,Inputs_fieds[j],titles_format)
    i = 1
    for mess in RMR_Messages_rad:
        if(mess.double_check == 0):
            name  = mess.name_frome_ID(ID_NAME_MAP)
            gps   = mess.decode_GPS()
            date  = gps[GPS_DATE]
            date2 = date[0]+date[1]+'-'+date[2]+date[3]+'-'+date[4]+date[5]
            Time  = gps[GPS_TIME]
            Time  = Time[0]+Time[1]+':'+Time[2]+Time[3]+':'+Time[4]+Time[5]
            lat   = gps[GPS_LATITUDE]
            long  = gps[GPS_LONGITUDE]
            if(len(lat)>0):
                lat_maps  = float(lat[0]+lat[1])+float(lat[2:len(lat)-1])/60
                lat = lat[0:2]+u'\N{DEGREE SIGN}'+lat[2:len(lat)-1]+' '+lat[len(lat)-1]
            else:
                lat_maps  = ''
                lat = u'\N{DEGREE SIGN}'+' N'
            if(len(long)>0):
                long_maps = float(long[0]+long[1]+long[2])+float(long[3:len(long)-1])/60
                long = long[0:3]+u'\N{DEGREE SIGN}'+long[3:len(long)-1]+' '+long[len(long)-1]
            else:
                long_maps = ''
                long = u'\N{DEGREE SIGN}'+' E'
            worksheet_dt_rd.write(i,0,name)
            worksheet_dt_rd.write(i,1,date2)
            worksheet_dt_rd.write(i,2,Time)
            worksheet_dt_rd.write(i,3,lat_maps,coord_format)
            worksheet_dt_rd.write(i,4,long_maps,coord_format)
            worksheet_dt_rd.write(i,5,lat+' '+long)
            worksheet_dt_rd.write(i,6,'20'+date[4]+date[5]+'-'+date[2]+date[3]+'-'+date[0]+date[1]+'  '+Time)
            i = i + 1
        
    
    excel_functions.write_tableStats(workbook, worksheet_mb1, 'Mobile 1 Defects', Names, periods, [2,1], occ1, [0,5,10])
    excel_functions.write_tableStats(workbook, worksheet_mb2, 'Mobile 2 Defects', Names, periods, [2,1], occ2, [0,5,10])
    excel_functions.write_tableStats(workbook, worksheet_mb, 'Total Mobile Defects', Names, periods, [2,1], occ, [0,5,10])
    excel_functions.write_tableStats(workbook, worksheet_mb_tot, 'Total Mobile Defects / ToT', Names, periods, [2,1], occ_mvnt, [0,1,2])
    excel_functions.write_tableStats(workbook, worksheet_mb_mvnt, 'Total Mobile Defects / TmvntT', Names, periods, [2,1], occ_tot, [0,1,2])
    excel_functions.write_tableStats(workbook, worksheet_rd, 'Radio Total Failure', Names, periods, [2,1], rad, [0,5,10])
    excel_functions.write_tableStats(workbook, worksheet_tot, 'Train Op Time', Names, periods, [2,1], tot, [0,90,180])
    excel_functions.write_tableStats(workbook, worksheet_mvnt, 'Train Mvnt Time', Names, periods, [2,1], tmvnt, [0,90,180])

    
    start = [2,1]
    for it in indexTrains:
        index = it[0]
        Train_type = it[1]
        Occ_trunc  = occ[index[0]:index[1]+1][:]
        Occ1_trunc = occ1[index[0]:index[1]+1][:]
        Occ2_trunc = occ2[index[0]:index[1]+1][:]
        Rad_trunc  = rad[index[0]:index[1]+1][:]
        ToT_trunc  = tot[index[0]:index[1]+1][:]
        excel_functions.write_report(workbook, worksheet_mb_report, Train_type, periods, start, ID_NAME_MAP, Occ_trunc, Occ1_trunc, Occ2_trunc, ToT_trunc, [0,1,2])
        offset = len(decode_raw_data.get_OBU_NAMES_from_OBU_FAMILLY(Train_type, ID_NAME_MAP)) + 9
        start[0] = start[0] + offset 
    
    workbook.close()

        
            



    
