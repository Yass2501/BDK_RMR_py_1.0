import datetime
import jdr_mdr_classes as jdr_mdr


f = open('../inputs/JDR_MDR/test2.txt','r+')
data = f.readlines()
data = data
f.close()

JDR_MDR_Messages = []
k = 0
i = 0
len_data = len(data)
while(k < len_data):
    if(data[k].find('Msg') == 0):
        tmp = data[k].split(' ')
        Msg_ID = int(tmp[1])
        if(data[k+1].find('JRU') == 0):
            Msg_Type = 'JRU'
            tmp = data[k+3].split(':')              # L_MESSAGE
            L_MESSAGE = int(tmp[1])
            tmp = data[k+4].split(':')              # DATE_YEAR
            DATE_YEAR = int(tmp[1])
            tmp = data[k+5].split(':')              # DATE_MOUNTH
            DATE_MOUNTH = int(tmp[1])
            tmp = data[k+6].split(':')              # DATE_DAY
            DATE_DAY = int(tmp[1])
            tmp = data[k+7].split(':')              # TIME_HOURS
            TIME_HOURS = int(tmp[1])
            tmp = data[k+8].split(':')              # TIME_MINUTES
            TIME_MINUTES = int(tmp[1])
            tmp = data[k+9].split(':')              # TIME_SECONDS
            TIME_SECONDS = int(tmp[1])
            tmp = data[k+10].split()                # TIME_MILLISECONDS
            TIME_MILLISECONDS = int(tmp[2][0:tmp[2].find('m')])
            tmp = data[k+11].split(':')                # TRAIN_POS_Q_SCALE
            Q_SCALE = tmp[1]
            tmp = data[k+12].split(':')                # TRAIN_POS_NID_C
            NID_C = tmp[1]
            tmp = data[k+13].split(':')                # TRAIN_POS_NID_BG
            NID_BG = tmp[1]
            tmp = data[k+14].split(':')                # TRAIN_POS_D_LRBG
            D_LRBG = tmp[1]
            tmp = data[k+15].split(':')                # TRAIN_POS_Q_DIRLRBG
            Q_DIRLRBG = tmp[1]
            tmp = data[k+16].split(':')                # TRAIN_POS_Q_DLRBG
            Q_DLRBG = tmp[1]
            tmp = data[k+17].split(':')                # TRAIN_POS_L_DOUBTOVER
            L_DOUBTOVER = tmp[1]
            tmp = data[k+18].split(':')                # TRAIN_POS_L_DOUBTUNDER
            L_DOUBTUNDER = tmp[1]
            tmp = data[k+19].split(':')                # V_TRAIN
            V_TRAIN = tmp[1]
            tmp = data[k+23].split(':')                # LEVEL
            LEVEL = tmp[1]
            tmp = data[k+24].split(':')                # MODE
            MODE = tmp[1]
            DATE = datetime.date(DATE_YEAR,DATE_MOUNTH,DATE_DAY)
            TIME = datetime.time(TIME_HOURS,TIME_MINUTES,TIME_SECONDS,1000*TIME_MILLISECONDS)
            JDR_MDR_JRU_MESS = jdr_mdr.JRU_Message(L_MESSAGE, DATE, TIME, Q_SCALE, NID_C, D_LRBG, Q_DIRLRBG,\
                 Q_DLRBG, L_DOUBTOVER, L_DOUBTUNDER, V_TRAIN, LEVEL, MODE)
            JDR_MDR_Messages.append(jdr_mdr.Message(Msg_ID, Msg_Type, JDR_MDR_JRU_MESS))
            print(JDR_MDR_Messages[i].Data.MODE)
            i = i + 1
    k=k+1

print(len(JDR_MDR_Messages))
            


