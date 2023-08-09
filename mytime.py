from datetime import datetime, timezone, timedelta
from dateutil import parser

# scary time formatting functions
def convert_to_est(time_str):
    dt_time = convert_to_datetime(time_str)
    correct_time = dt_time + timedelta(hours = -4)
    return correct_time.strftime('%Y-%m-%dT%H:%M:%S')

def conversion_for_gui(time_str):
    # takes a mm/dd/yyyy string and returns a datetime object with correct timezone
        # TODO: fix all the messy hardcoded timezone stuff like this line
    return parser.parse(time_str) + timedelta(hours = 4)

def convert_to_datetime(time_str):
    if isinstance(time_str, datetime):
        return time_str
    try:
        # Handle %Y-%m-%dT%H:%M:%S.%fZ format
        dt = datetime.fromisoformat(time_str)
        # Convert offset-naive datetime to offset-aware datetime
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        # If the original format parsing fails, try the new format
        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

def is_time_after(time_str1, time_str2):
    dt1 = convert_to_datetime(time_str1)
    dt2 = convert_to_datetime(time_str2)
    return dt1 > dt2

def is_time_before(time_str1, time_str2):
    dt1 = convert_to_datetime(time_str1)
    dt2 = convert_to_datetime(time_str2)
    return dt1 < dt2


def make_readable(time_str):
    if isinstance(time_str, datetime):
        return time_str.strftime('%m/%d %I:%M %p')
    dt= datetime.fromisoformat(time_str)
    dt = dt.strftime('%m/%d %I:%M %p')
    return dt

def days_between(start, end):
    # takes two datetimes and returns a list of datetimes including start, not including end
    days = []
    current_day = start
    while is_time_before(current_day, end):
        days.append(current_day)
        current_day += timedelta(days=1)
    return days