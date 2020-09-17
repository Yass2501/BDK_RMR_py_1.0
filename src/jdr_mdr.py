import datetime



f = open('../inputs/JDR_MDR/test.txt','r+')
data = f.readlines()
f.close()

k = 0
count = 0
l_mess = len(data)
print(l_mess)
while(k < l_mess):
    if(data[k].find('Msg') == 0):
        index = k
        if(data[index+1].find('JRU') == 0):
            stri = data[index+2].split(' ')
            k = k + 27
    else:
        k = k + 1
        
            
        


