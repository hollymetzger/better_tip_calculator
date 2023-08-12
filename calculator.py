# Main file which controls the high level processes and computes tips

# import built-in modules
import csv
import datetime

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

    # get data from Square database using their API
    print('loading employee data...')

    shifts = employees.load_shifts(start, end)
    employee_list = employees.load_employees()
    employee_list = employees.divide_shifts(employee_list, shifts)


    print('loading tips data...')

    payment_list = []
    # sushi tips, not tied to specific chef since we tip them in cash
    sushi_tips = {}

    loop_start = start
    loop_end = start + datetime.timedelta(days=1)

    while True:
        if loop_end > end:
            break

        # load payments for the day
        print("loading", loop_start)
        plist = payments.load_payments(loop_start, loop_end)
        # load_payments can only load 100 at a time, loops through the rest of the day if there are > 100 payments
        if len(plist) % 100 == 0:
            last_time =  mytime.convert_to_datetime(payment_list[len(payment_list)-1].time)
            while True:
                newlist = payments.load_payments(start, last_time)
                if newlist is None:
                    break
                for p in newlist:
                    plist.append(p)
                last_time = mytime.convert_to_datetime(payment_list[len(payment_list)-1].time)

        this_day = loop_start.strftime("%m/%d/%Y")

        for p in plist:
            actives = employees.get_active_employees(employee_list, p)
            
            # add sushi tip
            if p.section == '238CS149B2003752':
                if this_day in sushi_tips:
                    sushi_tips[this_day] += p.tip * 0.5
                else:
                    sushi_tips.update({this_day:0})
                    sushi_tips[this_day] += p.tip * 0.5
                p.tip *= 0.5
            else:
                if this_day in sushi_tips:
                    sushi_tips[this_day] += p.tip * 0.12
                else:
                    sushi_tips.update({this_day:0})
                    sushi_tips[this_day] += p.tip * 0.12
                p.tip *= 0.88

            for a in actives:
                if this_day in a.tips:
                    a.tips[this_day] += (p.tip/len(actives))
                else:
                    a.tips.update({this_day:0})
                    a.tips[this_day] += (p.tip/len(actives))


        payment_list = payment_list + plist
        loop_start += datetime.timedelta(days=1)
        loop_end += datetime.timedelta(days=1)

    totaltips = 0
    for p in payment_list:
        totaltips += p.tip

    print("calculating tips...")

    print()
    print("tips per employee:")
    emptips = 0
    for e in employee_list:
        print(e.name)
        sum = 0
        for day in e.tips:
            sum += e.tips[day]
        if sum > 0:
            print(e.name)
            for day in e.tips:
                print(round(e.tips[day], 2))
            emptips += sum
    print('total loaded tips: ', totaltips)

    print('exporting csv file...')
    export(employee_list, sushi_tips, str(export_file_path), start, end)

    print('done!')
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