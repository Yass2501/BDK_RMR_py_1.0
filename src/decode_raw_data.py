import os
import functions
import datetime
from global_variables import *



############################ Classes ############################



class RMR_Message(object):
    
    time_for_sort = 0
    date_for_sort = 0
    double_check  = 0
    
    def __init__(self, OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE, \
                OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA):

        self.OBU_LEN = OBU_LEN
        self.OBU_VER = OBU_VER
        self.OBU_ID = OBU_ID
        self.OBU_ACK = OBU_ACK
        self.OBU_GPS = OBU_GPS
        self.OBU_DATA_TYPE = OBU_DATA_TYPE
        self.OBU_CUSTOM = OBU_CUSTOM
        self.OBU_DATA_LEN = OBU_DATA_LEN
        self.OBU_DATA = OBU_DATA

    def date_time_pretty(self):
        gps_field = self.decode_GPS()
        TIME = gps_field[GPS_TIME]
        DATE = gps_field[GPS_DATE]
        date_time = datetime.datetime(2000+int(DATE[4:6]),int(DATE[2:4]),int(DATE[0:2]),int(TIME[0:2]),int(TIME[2:4]),int(TIME[4:6]))
        print(date_time.strftime('%d-%m-%Y  %H:%M:%S'))

    def decode_GPS(self):
        
        Index = functions.findIndexof(self.OBU_GPS,',', 9)
        gps_field = functions.arrayAllocate('',10)
        
        gps_field[GPS_VALIDITY] = self.OBU_GPS[0:Index[0]]
        gps_field[GPS_TIME] = self.OBU_GPS[Index[0]+1:Index[1]]
        gps_field[GPS_DATE] = self.OBU_GPS[Index[1]+1:Index[2]]
        gps_field[GPS_LATITUDE] = self.OBU_GPS[Index[2]+1:Index[3]]
        gps_field[GPS_LONGITUDE] = self.OBU_GPS[Index[3]+1:Index[4]]
        gps_field[GPS_ALTITUDE] = self.OBU_GPS[Index[4]+1:Index[5]]
        gps_field[GPS_HDOP_STATUS] = self.OBU_GPS[Index[5]+1:Index[6]]
        gps_field[GPS_SPEED] = self.OBU_GPS[Index[6]+1:Index[7]]
        gps_field[GPS_DIRECTION] = self.OBU_GPS[Index[7]+1:Index[8]]
        gps_field[GPS_SATELLITE_NB] = self.OBU_GPS[Index[8]+1:(len(self.OBU_GPS)-1)]
        
        return gps_field
        
    def print(self):

        print('=================================================')
        print('OBU Length : ',self.OBU_LEN)
        print('OBU Version : '+self.OBU_VER)
        print('OBU ID : '+self.OBU_ID)
        print('OBU Ack : '+self.OBU_ACK)
        print('OBU GPS : '+self.OBU_GPS)
        print('OBU Data type : '+self.OBU_DATA_TYPE)
        print('OBU Cust : '+self.OBU_CUSTOM)
        print('OBU data length : ',self.OBU_DATA_LEN)
        print('OBU data : ',self.OBU_DATA)
        print('=================================================')

    def name_frome_ID(self,Id_name_strings):
        i = 0
        Name = ''
        for line in Id_name_strings:
            Id = line[0:line.find('\t')]
            Name = line[line.find('\t')+1:len(line)-1]
            if(Id==self.OBU_ID):
                break
        return Name


############################ Functions ############################

	
def extract_and_decode_rawData(OBU_Proxy_dir, period, filter_obu_data_type, filter_obu_name):
    
    date1_int = int(period[0].strftime('%y%m%d'))
    date2_int = int(period[1].strftime('%y%m%d'))
    
    if(filter_obu_name != 'all'):
        g = open('../inputs/id_train_mapping.txt','r+')
        id_name_map = g.readlines()
        g.close()
        obu_name_split = filter_obu_name[0].split(' ')
        test_familly_train = 1
        for s in obu_name_split:
            if(s.isdigit()):
                test_familly_train = 0
        filter_obu_id = []
        if(test_familly_train):
            for obu_name in filter_obu_name:
                filter_obu_id = filter_obu_id + get_OBU_IDs_from_OBU_FAMILLY(obu_name, id_name_map)
        else:
            for obu_name in filter_obu_name:
                filter_obu_id.append(get_OBU_ID_from_OBU_NAME(obu_name, id_name_map))
 
    ListDir   = os.listdir('./'+OBU_Proxy_dir)  # List all directories present in OBU_proxy
    Raw_data_decoded = []
    i_rmr_mess = 0
    index_G1 = 0
    index_G1_end = 0
    dir_flag = 0
    for directory in ListDir:
        #print('Directory : '+directory)
        ListFiles = os.listdir('./'+OBU_Proxy_dir+'/'+directory)
        dir_flag = 1
        for filename in ListFiles:
            filename_date = filename[2:4]+filename[5:7]+filename[8:10]
            filename_date_int = int(filename_date)
            if(date1_int <= filename_date_int < date2_int):
                if(dir_flag == 1):
                    print('Directory : '+directory)
                    dir_flag = 0
                print('File name : '+filename)
                f = open('./'+OBU_Proxy_dir+'/'+directory+'/'+filename,'r+')
                lines = f.readlines()
                for i in range(0,len(lines)):
                    if((lines[i].find('<G1>') != -1)):
                        k = i
                        data_str = lines[i]
                        while((lines[k].find('</G1>') == -1)):
                            k = k + 1
                            data_str = data_str + lines[k]
                        index_G1     = data_str.find('<G1>')
                        index_G1_end = data_str.find('</G1>')+5
                        Index        = functions.findIndexof(data_str, ';', 8)
                        
                        OBU_LEN       = str(int((data_str[(index_G1+4):(Index[0])]).encode().hex(),16))
                        OBU_VER       = data_str[(Index[0]+1):Index[1]]
                        OBU_ID        = data_str[(Index[1]+1):Index[2]]
                        OBU_ACK       = data_str[(Index[2]+1):Index[3]]
                        OBU_GPS       = data_str[(Index[3]+1):Index[4]]
                        OBU_DATA_TYPE = data_str[(Index[4]+1):Index[5]]
                        OBU_CUSTOM    = data_str[(Index[5]+1):Index[6]]
                        OBU_DATA_LEN  = data_str[(Index[6]+1):Index[7]]
                        OBU_DATA      = data_str[(Index[7]+1):index_G1_end-5]

                        if(filter_obu_data_type == 'all'):
                            Raw_data_decoded.append(RMR_Message(OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE,OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA))
                            gps_field = Raw_data_decoded[i_rmr_mess].decode_GPS()
                            Raw_data_decoded[i_rmr_mess].date_for_sort = functions.dateStringToIntConvert(gps_field[GPS_DATE])
                            obu_time = gps_field[GPS_TIME]
                            Raw_data_decoded[i_rmr_mess].time_for_sort = int(obu_time[0:6])
                            i_rmr_mess = i_rmr_mess + 1
                        else:
                            filter_sum = 0
                            for filter in filter_obu_data_type:
                                if(filter == int(OBU_DATA_TYPE)):
                                    filter_sum = 1
                                    break
                            if(filter_sum == 1):
                                if(filter_obu_name == 'all'):    
                                    Raw_data_decoded.append(RMR_Message(OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE,OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA))
                                    gps_field = Raw_data_decoded[i_rmr_mess].decode_GPS()
                                    Raw_data_decoded[i_rmr_mess].date_for_sort = functions.dateStringToIntConvert(gps_field[GPS_DATE])
                                    obu_time = gps_field[GPS_TIME]
                                    Raw_data_decoded[i_rmr_mess].time_for_sort = int(obu_time[0:6])
                                    i_rmr_mess = i_rmr_mess + 1
                                else:
                                    filter_sum2 = 0
                                    for filter_id in filter_obu_id:
                                        if(filter_id == OBU_ID):
                                            filter_sum2 = 1
                                            break
                                    if(filter_sum2 == 1):
                                        Raw_data_decoded.append(RMR_Message(OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE,OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA))
                                        gps_field = Raw_data_decoded[i_rmr_mess].decode_GPS()
                                        Raw_data_decoded[i_rmr_mess].date_for_sort = functions.dateStringToIntConvert(gps_field[GPS_DATE])
                                        obu_time = gps_field[GPS_TIME]
                                        Raw_data_decoded[i_rmr_mess].time_for_sort = int(obu_time[0:6])
                                        i_rmr_mess = i_rmr_mess + 1
                                        
                f.close()
            
    len_raw_data = i_rmr_mess
    print('The number of messages to be treated : ',len_raw_data)
    return Raw_data_decoded



def get_OBU_ID_from_OBU_NAME(obu_name, id_name_map):
    id = '' 
    for line in id_name_map:
        if(line.find(obu_name) != -1):
            id = line[0:6]
            break
    return id

def get_OBU_IDs_from_OBU_FAMILLY(familly_name, id_name_map):
    ids = []
    for line in id_name_map:
        if(line.find(familly_name) != -1):
            ids.append(line[0:6])
    return ids
	
def get_OBU_NAMES_from_OBU_FAMILLY(familly_name, id_name_map):
    names = []
    for line in id_name_map:
        if(line.find(familly_name) != -1):
            names.append(line[7:(len(line)-1)])
    return names

def get_OBU_NAME_from_OBU_ID(obu_id, id_name_map):
    name = '' 
    for line in id_name_map:
        if(line.find(obu_id) != -1):
            name = line[7:(len(line)-1)]
            break
    return name


