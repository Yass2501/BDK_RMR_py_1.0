# GPS field names
GPS_VALIDITY     = 0
GPS_TIME         = 1
GPS_DATE         = 2
GPS_LATITUDE     = 3
GPS_LONGITUDE    = 4
GPS_ALTITUDE     = 5
GPS_HDOP_STATUS  = 6
GPS_SPEED        = 7
GPS_DIRECTION    = 8
GPS_SATELLITE_NB = 9

# Maintenance Manager states
OK = 0
WARNING = 1
DEFECT = 2
BLOCKING_DEFECT = 3

# Train <--> IDs mapping
f = open('../inputs/id_train_mapping.txt')
ID_NAME_MAP = f.readlines()
f.close()
