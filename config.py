# Stores settings and information

from datetime import datetime, timezone, timedelta

# start and end times, enter beginning and end of pay period you wish
# to view tips for
start = datetime(2023, 7, 1, 0, 0, 0)
end = datetime(2023, 7, 2, 0, 0, 0)

# export file name/location
export_file_name = 'configtips.csv'

# Location ID. Leesburg: LTJZEPEWD0KK8, Middleburg: L6BJTA2D8EX2H
location = 'LTJZEPEWD0KK8'