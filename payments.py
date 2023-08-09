# Contains functions for working with payment data

from square.client import Client
import requests
import json
import os
import mytime
    
class Payment:
    def __init__(self, section, tip, time, location):
        self.section = section
        self.tip = tip
        self.time = time
        self.location = location

def load_payments(start, end):
    # Get payment data from Square database

    # Set up Square API
    headers = {
        'Authorization': 'Bearer ' + os.environ['SQUARE_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    url = 'https://connect.squareup.com/v2/payments'
    params = {
        'begin_time': start.isoformat(),
        'end_time': end.isoformat(),
        'location_id': 'LTJZEPEWD0KK8'
    }
    response = requests.get(url, headers=headers, params=params)
    
    try:
        raw_payments = json.loads(response.text)['payments']
    except KeyError:
        return
    payments = []

    for p in raw_payments:
        # subtract 4 hours from payment time to get EST timezone
        bad_timezone_time = p['created_at']
        payment_time = mytime.convert_to_est(bad_timezone_time)
        if 'device_details' in p:
            section = p['device_details']['device_id']
        else:
            section = 'error'
        if 'tip_money' in p:
            tip_money = p['tip_money']
            tip_amount = float(tip_money['amount']) / 100.0
        else:
            tip_amount = 0.0
        location = p['location_id']
        payment = Payment(section, tip_amount, payment_time, location)
        payments.append(payment)
        
    return payments

def check_total(payment_list, emp_tips, sushitips):
    totaltips = 0
    employeetips = sushitips
    for i in emp_tips:
        employeetips += i.tips
    for p in payment_list:
        totaltips += p.tip

    print("Employees tips added together = ", employeetips)
    print("Total tips collected for this period = ", totaltips)