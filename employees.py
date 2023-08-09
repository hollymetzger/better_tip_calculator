from square.client import Client
import requests
import json
import os
import csv
from datetime import timedelta
import mytime

dine_in_tipout = {
    'Waiter I': 80,
    'Server PT': 80,
    'Waiter Assistant': 40,
    'Manager & Expediter': 20,
    'Chef': 10,
    'Dishwasher': 0,
    'Manager': 0
}
    
       
class Employee:
    def __init__(self, name, id, weight, tips, shifts):
        # employee's full name
        self.name = name
        # id used in square database to get information about employee such as shifts
        self.id = id
        # tip weight, 100 is standard, 50 means half of what they would get if tips were divided equally
        self.weight = weight
        # a dict with keys being dates and values being tips earned on those dates
        self.tips = tips
        # a list of shift objects associated with the employee
        self.shifts = shifts

class Shift:
    def __init__(self, employee, location, type, start, end):
        self.employee = employee
        self.location = location
        self.type = type # waiter, chef, expediter, etc. determines how much tip they get
        self.start = start
        self.end = end

def load_employees():
    # initializes list of tipped employees with their tip weights from csv file
    
    # Set up Square
    headers = {
        'Authorization': 'Bearer ' + os.environ['SQUARE_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    url = 'https://connect.squareup.com/v2/team-members/search'
    response = requests.post(url, headers=headers)
    raw_employees = json.loads(response.text)['team_members']
    employee_list = []

    # open csv file containing the employee tip weights
    weight_dict = {}
    with open ('employee_tip_weights.csv') as weightsfile:
        reader = csv.DictReader(weightsfile)
        for row in reader:
            name = row['Name']
            weight = int(row['Weight'])
            weight_dict[name] = weight

    # build list of employees
    for e in raw_employees:
        name = f"{e['given_name']} {e['family_name']}"
        weight = 100
        if name in weight_dict:
            weight = weight_dict[name]
        employee = Employee(name, e['id'], weight, 0, [])
        employee_list.append(employee)
    return employee_list

def get_active_employees(employee_list, payment):
    # Returns list of tipped employees clocked in at time and location of payment
    active_employees = []
    for e in employee_list:
        for s in e.shifts:
            if (s.location == payment.location) & mytime.is_time_after(payment.time, s.start) & mytime.is_time_before(payment.time, s.end):
                if s.type in ('Waiter I', 'ServerPT', 'Waiter Assistant'):
                    active_employees.append(e)
    return active_employees

def get_name(id, employee_list):
    for e in employee_list:
        if e.id == id:
            return e.name
        


###################################################################################
                            ### shift functions ###
###################################################################################

def load_shifts(start, end):
    # Returns list of all shifts with employee ID and clock in/out times
    # in pay period specified by start and end times

    # Set up Square parameters
    headers = {
        'Authorization': 'Bearer ' + os.environ['SQUARE_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    url = 'https://connect.squareup.com/v2/labor/shifts/search?'

    ###################################################################################
    # TODO: figure out how to set date filters, currently can only load
    # most recent 200 shifts from all employees/all locations combined
    params = {
        "query": {
            "filter": {
                "workday": {
                    "date_range": {
                        "start_date": "start",
                        "end_date": "end"
                    },
                    # "match_shifts_by": "START_AT",
                    # "default_timezone": "America/Los_Angeles"
                }
            }
        },
        'limit': 5
    }
    ###################################################################################

    response = requests.post(url, headers=headers, params=params)
    raw_shifts = json.loads(response.text)['shifts']
    shifts = []

    for s in raw_shifts:
        if ('end_at') in s:
            shift = Shift(s['employee_id'], s['location_id'], s['wage']['title'], s['start_at'], s['end_at'])
            shifts.append(shift)
        else:
            start_time = mytime.convert_to_datetime(s['start_at'])
            # if employee is still clocked in, assume shift will end 10 hours
            # after they clocked in
            end_time = start_time + timedelta(hours = 10)
            shift = Shift(s['employee_id'], s['location_id'], s['wage']['title'], s['start_at'], end_time.strftime('%Y-%m-%dT%H:%M:%S'))
            shifts.append(shift)
    return shifts

def divide_shifts(employees, shifts):
    # populates each employee's list of shifts
    for s in shifts:
        for employee in employees:
            if s.employee == employee.id:
                employee.shifts.append(s)
                break
    return employees


def days_between(start, end):
    # takes two datetimes and returns a list of datetimes including start, not including end
    days = []
    current_day = start
    while mytime.is_time_before(current_day, end):
        days.append(current_day)
        current_day += timedelta(days=1)