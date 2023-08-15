# Stores settings and information

from datetime import datetime, timezone, timedelta

# start and end times, enter beginning and end of pay period you wish
# to view tips for
start = datetime(2023, 7, 1, 0, 0, 0)
end = datetime(2023, 7, 2, 0, 0, 0)

# export file name/location
export_file_name = 'configtips.csv'

# Location ID. Leesburg: LTJZEPEWD0KK8, Middleburg: L6BJTA2D8EX2H
location = 'L6BJTA2D8EX2H'


# choose whether to fill in days when an employee earned no tips with zero (True) or leave it blank (False)
zero_fill_export = False

# choose what happens to unassigned tips
    # ignore: don't assign them to anyone, put them in a seperate row
    # divide_equally: divide them equally among everyone clocked in at the time, if anyone
    # give_to_next_server: give them all to the next server to clock in. ie. an online order comes in at 10am, first server to clock in gets tip
unassigned_tips = 'ignore'

# validation information

total_tips_loaded = 0
total_tips_assigned = 0