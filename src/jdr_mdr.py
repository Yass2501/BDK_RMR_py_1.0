import datetime



f = open('../inputs/JDR_MDR/test.txt','r+')
data = f.readlines()
data = data + ['','','']
f.close()

JDR_MDR_Messages = []
k = 0
len_data = len(data)
while(k < len_data):
    if(data[k].find('Msg') == 0):
        k = k + 1
        if(data[k].find('DRU') == 0):
            #k = k + 1
            while(data[k] != ')\n' or data[k] != ')'):
                print(data[k])
                k = k + 1
    else:
        k = k + 1


