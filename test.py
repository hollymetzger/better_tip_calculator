from datetime import datetime, timezone, timedelta
from dateutil import parser

iso_utc_string = "2023-08-01T00:05:32.307Z"
print(parser.parse(iso_utc_string))

iso_offset_string = "2023-07-07T11:15:00-04:00"
print(parser.parse(iso_offset_string))
