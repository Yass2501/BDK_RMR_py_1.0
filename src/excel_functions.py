import xlsxwriter
import datetime
import decode_raw_data
import functions
import numpy as np



def write_periods_trainNames(workbook, worksheet, period, obu_names, start):
    j = 0
    for p in period:
        worksheet.write(start[0]-2,start[1]+j,p[0].strftime('%d-%m-%y'))
        worksheet.write(start[0]-1,start[1]+j,p[1].strftime('%d-%m-%y'))
        j = j + 1
    i = 0
    for name in obu_names:
        worksheet.write(start[0]+i,start[1]-1,name)
        i = i + 1



def write_tableStats(workbook, worksheet, Title, obu_names, periods, start, data, range_color):

    merge_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#FFFFFF',
    'text_wrap':'true',
    })

    NA_format = workbook.add_format({
    'bold':     True,
    'border':   0,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#808080',
    })
    
    write_periods_trainNames(workbook, worksheet, periods, obu_names, start)
    
    worksheet.set_column(start[1]-1,start[1]-1,20)
    worksheet.merge_range(start[0]-2,start[1]-1,start[0]-1,start[1]-1, Title, merge_format)
    worksheet.set_column(start[1]-1,start[1]+len(periods)+1,15)
    worksheet.merge_range(start[0]-2,start[1]+len(periods)+1,start[0]-1,start[1]+len(periods)+1, 'Mean over periods', merge_format)
    
    i = 0
    for i in range(0,len(obu_names)):
        j = 0
        for j in range(0,len(periods)):
            if(data[i][j] == -1):
                worksheet.write(start[0]+i,start[1]+j,'',NA_format)
            else:
                worksheet.write(start[0]+i,start[1]+j,data[i][j])
            j = j + 1
        i = i + 1
    worksheet.conditional_format(start[0],start[1],i+start[0],j+start[1]+3,\
                                     {'type': '3_color_scale','min_color': '#63BE7B',\
                                      'mid_color': '#FFEB84','max_color': '#F8696B','min_value': range_color[0],\
                                      'mid_value': range_color[1],'max_value': range_color[2],'min_type': 'num','mid_type': 'num',\
                                      'max_type': 'num'})

def write_report(workbook, worksheet, Train_type, period, start, id_name_map, Occ, Occ1, Occ2, ToT, range_color):

    merge_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#FFFFFF',
    'text_wrap':'true',
    })

    report_format = workbook.add_format({
    'bold':     True,
    'border':   1,
    #'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#FFFFFF',
    'text_wrap':'true',
    })

    NA_format = workbook.add_format({
    'bold':     True,
    'border':   0,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#808080',
    })

    names = decode_raw_data.get_OBU_NAMES_from_OBU_FAMILLY(Train_type, id_name_map)
    IDs   = decode_raw_data.get_OBU_IDs_from_OBU_FAMILLY(Train_type, id_name_map)
    
    write_periods_trainNames(workbook, worksheet, period, names, start)
    worksheet.set_column(start[1]-1,start[1]-1,20)
    worksheet.merge_range(start[0]-2,start[1]-1,start[0]-1,start[1]-1,\
                          'Report Analysis'+'\r\n'+Train_type, merge_format)
    #vertical
    worksheet.write(start[0]+len(names),start[1]-1,'Mobile defect 1 / period',report_format)
    worksheet.write(start[0]+len(names)+1,start[1]-1,'Mobile defect 2 / period',report_format)
    worksheet.write(start[0]+len(names)+2,start[1]-1,'Total defect / period',report_format)
    worksheet.write(start[0]+len(names)+3,start[1]-1,'Total number of hour'+'\r\n'+'/ period',report_format)
    worksheet.write(start[0]+len(names)+4,start[1]-1,'Failure rate'+'\r\n'+'/ 24h / period',report_format)
    
    #horizontal
    worksheet.merge_range(start[0]-2,start[1]+len(period),start[0]-1,start[1]+len(period),'Total defect / train',report_format)
    worksheet.set_column(start[1]+len(period),start[1]+len(period),15)
    worksheet.merge_range(start[0]-2,start[1]+len(period)+1,start[0]-1,start[1]+len(period)+1,'Total number of hour'+'\r\n'+'/ train',report_format)
    worksheet.set_column(start[1]+len(period)+1,start[1]+len(period)+1,15)
    worksheet.merge_range(start[0]-2,start[1]+len(period)+2,start[0]-1,start[1]+len(period)+2,'Failure rate'+'\r\n'+'/ 24h / train',report_format)
    worksheet.set_column(start[1]+len(period)+2,start[1]+len(period)+2,15)

    for i in range(0,len(Occ)):
        for j in range(0,len(Occ[0])):
            if(ToT[i][j] == 0):
                worksheet.write(start[0]+i,start[1]+j,'',NA_format)
            else:
                worksheet.write(start[0]+i,start[1]+j,(Occ[i][j]/ToT[i][j])*24)
            if(i == 0):
                sumOcc = functions.sumColumn(Occ,j)
                sumToT = functions.sumColumn(ToT,j)
                worksheet.write(start[0]+len(Occ),start[1]+j,functions.sumColumn(Occ1,j))
                worksheet.write(start[0]+len(Occ)+1,start[1]+j,functions.sumColumn(Occ2,j))
                worksheet.write(start[0]+len(Occ)+2,start[1]+j,sumOcc) 
                worksheet.write(start[0]+len(Occ)+3,start[1]+j,sumToT)
                if(sumToT == 0):
                    worksheet.write(start[0]+len(Occ)+4,start[1]+j,'',NA_format)
                else:
                    worksheet.write(start[0]+len(Occ)+4,start[1]+j,(sumOcc/sumToT)*24)
        sumOcc = functions.sumLine(Occ,i)
        sumToT = functions.sumLine(ToT,i)
        worksheet.write(start[0]+i,start[1]+len(Occ[0]),sumOcc)
        worksheet.write(start[0]+i,start[1]+len(Occ[0])+1,sumToT)
        if(sumToT == 0):
            worksheet.write(start[0]+i,start[1]+len(Occ[0])+2,'',NA_format)
        else:
            worksheet.write(start[0]+i,start[1]+len(Occ[0])+2,(sumOcc/sumToT)*24)
            
    worksheet.conditional_format(start[0],start[1],start[0]+len(Occ)-1,start[1]+len(Occ[0])-1,\
                                 {'type': '3_color_scale','min_color': '#63BE7B',\
                                  'mid_color': '#FFEB84','max_color': '#F8696B','min_value': range_color[0],\
                                  'mid_value': range_color[1],'max_value': range_color[2],'min_type': 'num','mid_type': 'num',\
                                  'max_type': 'num'})
    worksheet.conditional_format(start[0]+len(Occ)+4,start[1],start[0]+len(Occ)+4,start[1]+len(Occ[0])-1,\
                                 {'type': '3_color_scale','min_color': '#63BE7B',\
                                  'mid_color': '#FFEB84','max_color': '#F8696B','min_value': range_color[0],\
                                  'mid_value': range_color[1],'max_value': range_color[2],'min_type': 'num','mid_type': 'num',\
                                  'max_type': 'num'})
    worksheet.conditional_format(start[0],start[1]+len(Occ[0])+2,start[0]+len(Occ),start[1]+len(Occ[0])+2,\
                                 {'type': '3_color_scale','min_color': '#63BE7B',\
                                  'mid_color': '#FFEB84','max_color': '#F8696B','min_value': range_color[0],\
                                  'mid_value': range_color[1],'max_value': range_color[2],'min_type': 'num','mid_type': 'num',\
                                  'max_type': 'num'})
