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

# takes two datetime objects from gui.py
def calculate(start, end, export_file_path):

    # get data from Square database using their API
    print('loading payment data...')

    payment_list = []
    # sushi tips, not tied to specific chef since we tip them in cash
    sushi_tips = 0.0

    loop_start = start
    loop_end = start + datetime.timedelta(days=1)

    while True:
        if loop_end > end:
            break
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

        payment_list = payment_list + plist
        loop_start += datetime.timedelta(days=1)
        loop_end += datetime.timedelta(days=1)

    print("Verify payments:")
    for p in payment_list:
        print(p.time, p.tip)

    totaltips = 0
    for p in payment_list:
        totaltips += p.tip

    print('loading employee data...')
    shifts = employees.load_shifts(start, end)
    for s in shifts:
        print(s.type)
    employee_list = employees.load_employees()
    employee_list = employees.divide_shifts(employee_list, shifts)

    print("Verify employee shifts:")
    for e in employee_list:
        print(e.name)
        for s in e.shifts:
            print(s.start, s.end)

    print("calculating tips...")
    for p in payment_list:
        actives = employees.get_active_employees(employee_list, p)
        

        # subtract sushi tip
        if p.section == '238CS149B2003752':
            sushi_tips += p.tip * 0.5
            p.tip *= 0.5
        else:
            sushi_tips += p.tip * 0.12
            p.tip *= 0.88

        for a in actives:
            
            print("adding", p.tip/len(actives), "to", a.name)
            a.tips += p.tip/len(actives)

    print()
    print("total tips")
    emptips = 0
    for e in employee_list:
        if (e.tips > 0):
            print(e.name, round(e.tips, 2))
            emptips += e.tips
    print("Sushi: ", round(sushi_tips, 2))
    print("everyone's assigned tips: ", round(sushi_tips+emptips, 2))
    # print('total loaded tips: ', totaltips)

    print('exporting csv file...')
    export(employee_list, sushi_tips, export_file_path)

    print('done!')
    return

def export(emps, sushi_tips, export_file_path):
    with open(export_file_path, 'w', newline='') as export_file:
        writer = csv.DictWriter(export_file, fieldnames=['employee','tips'])
        writer.writeheader()
        for e in emps:
            writer.writerow({'employee': e.name, 'tips': e.tips})
        writer.writerow({'employee': 'Sushi Chefs', 'tips': sushi_tips})

    return


# TODO: add 'type' to shift, and only divide tips among waiters
# TODO: change tips format to be dict of days and tips per day
# TODO: change exported csv to contain columns of each day, and a total column
# TODO: implement export location functionality using the tkinter filedialog.askopenfilename
