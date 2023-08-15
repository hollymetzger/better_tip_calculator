# Contains functions for working with time

from datetime import datetime, timezone, timedelta
from dateutil import parser

def convert_to_est(time_str):
    dt_time = convert_to_datetime(time_str)
    correct_time = dt_time + timedelta(hours = -4)
    return correct_time.strftime('%Y-%m-%dT%H:%M:%S-04:00')

def conversion_for_gui(time_str):
    # takes a mm/dd/yyyy string and returns a datetime object in UTC timezone
    return parser.parse(time_str)

def convert_to_datetime(time_str):
    if isinstance(time_str, datetime):
        return time_str
    try:
        # Handle %Y-%m-%dT%H:%M:%S.%fZ format
        return parser.parse(time_str)
    except ValueError:
        # If the original format parsing fails, try the new format
        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")

def is_time_after(time_str1, time_str2):
    dt1 = convert_to_datetime(time_str1)
    dt2 = convert_to_datetime(time_str2)
    
    # Convert dt1 to the timezone of dt2
    dt1 = dt1.replace(tzinfo=dt2.tzinfo)
    
    return dt1 > dt2

def is_time_before(time_str1, time_str2):
    dt1 = convert_to_datetime(time_str1)
    dt2 = convert_to_datetime(time_str2)
    
    # Convert dt1 to the timezone of dt2
    dt1 = dt1.replace(tzinfo=dt2.tzinfo)
    
    return dt1 < dt2


def make_readable(time_str):
    if isinstance(time_str, datetime):
        return time_str.strftime('%m/%d %I:%M %p')
    dt= datetime.fromisoformat(time_str)
    dt = dt.strftime('%m/%d %I:%M %p')
    return dt

def days_between(start, end):
    # takes two datetimes and returns a list of strings format mm/dd/yy including start, not including end
    days = []
    current_day = start
    while is_time_before(current_day, end):
        days.append(current_day.strftime('%m/%d/%Y'))
        current_day += timedelta(days=1)
    return days

# takes two strings and returns true if they are exactly 24 hours apart, indicating that the employee forgot to clock out
def forgot_to_clock_out(start, end):
    dt_start = parser.parse(start)
    dt_end = parser.parse(end)
    if dt_end == dt_start + timedelta(hours=24):
        return True
    return False