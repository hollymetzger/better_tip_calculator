# Main file which controls the high level processes and computes tips

# import built-in modules
import csv
import datetime
import time

# import custom modules
import mytime
import employees
import payments
import config

# global lists
global payment_list
payment_list = []
shift_list = []
employee_list = []

# takes two datetime objects in EST from gui.py
def calculate(start, end, export_file_path):

    timing_start = time.time()

    # get data from Square database using their API

    shifts = employees.load_shifts(start, end)
    employee_list = employees.load_employees()
    employee_list = employees.divide_shifts(employee_list, shifts)

    payment_list = []

    # sushi tips, not tied to specific chef since we tip them in cash
    sushi_tips = {}

    loop_start = start
    loop_end = start + datetime.timedelta(days=1)

    while True:
        if loop_end > end:
            break

        # load payments for the day
        plist = payments.load_payments(loop_start, loop_end)

        # load_payments can only load 100 at a time, loops through the rest of the day if there are > 100 payments
        if len(plist) % 100 == 0:
            last_time =  mytime.convert_to_datetime(plist[len(plist)-1].time)
            while True:
                newlist = payments.load_payments(start, last_time)
                if newlist is None:
                    break
                for p in newlist:
                    plist.append(p)
                last_time = mytime.convert_to_datetime(plist[len(plist)-1].time)

        this_day = loop_start.strftime("%m/%d/%Y")

        for p in plist:
            config.total_tips_loaded += p.tip
            actives = employees.get_active_employees(employee_list, p)
            
            # add sushi tip
            # if the payment was from sushi bar card reader, give sushi 50%
            if p.section == '238CS149B2003752':
                # add the tip to the tip dict for the current day, if it exists
                if this_day in sushi_tips:
                    sushi_tips[this_day] += p.tip * 0.5
                # if this is the first tip added for the day, add this day to the tip dict and add tip amount as the first tip
                else:
                    sushi_tips.update({this_day:0})
                    sushi_tips[this_day] += p.tip * 0.5
                # change the tip amount to what is left after sushi tip out, to be divided amongst waiters
                p.tip *= 0.5

            # if the payment was from elsewhere, give sushi 12%
            else:
                # add the tip to the tip dict for the current day, if it exists
                if this_day in sushi_tips:
                    sushi_tips[this_day] += p.tip * 0.12
                # if this is the first tip added for the day, add this day to the tip dict and add tip amount as the first tip
                else:
                    sushi_tips.update({this_day:0})
                    sushi_tips[this_day] += p.tip * 0.12
                # change the tip amount to what is left after sushi tip out, to be divided amongst waiters
                p.tip *= 0.88

            for a in actives:
                if this_day in a.tips:
                    a.tips[this_day] += (p.tip/len(actives))
                else:
                    a.tips.update({this_day:0})
                    a.tips[this_day] += (p.tip/len(actives))

    export(employee_list, sushi_tips, str(export_file_path), start, end)


    timing_end = time.time()

    elapsed_time = timing_end - timing_start
    print(f"Elapsed time: {round(elapsed_time, 3)}")
    return

def export(emps, sushi_tips, export_file_path, start, end):
    fieldnames = ['employee']
    days = mytime.days_between(start, end)
    fieldnames += days
    with open(export_file_path, 'w', newline='') as export_file:
        writer = csv.DictWriter(export_file, fieldnames=fieldnames)
        writer.writeheader()

        for e in emps:
            emp = {'employee': e.name}
            tips = {}
            for day in e.tips:
                tips[day] = round(e.tips[day], 2)
            emp.update(tips)
            writer.writerow(emp)
        
        sushi = {'employee': 'Sushi'}
        sushi.update(sushi_tips)
        writer.writerow(sushi)

    return

# TODO: add 'type' to shift, and only divide tips among waiters