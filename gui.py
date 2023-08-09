from tkinter import *
from tkinter import ttk
import calculator as calc
import employees
import payments
import mytime

root = Tk()
root.title("Tip Calculator")

emps = employees.load_employees()
user_start = StringVar()
user_end = StringVar()

def ClickMe():
    return

def Run_Report():
    # get start and end
    start = mytime.conversion_for_gui(user_start.get())
    end = mytime.conversion_for_gui(user_end.get())
    print("start: ", start, 'end:', end)
    calc.calculate(start, end, 'csvfile.csv')
    return

mainframe = ttk.Frame(
    root,
    padding="13 13 22 22"
)

mainframe.grid(column=0, row=0, sticky=(N, W, E, S), padx=30, pady=20)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

calender = ttk.Frame(
    mainframe,
    padding=15,
    borderwidth=10,
    relief='sunken'
)
calender.grid(row=1)
    
cal_label = Label(
    calender,
    text="Select timeframe",
    font=("Arial", 14),
)
cal_label.grid()
    
startlabel = ttk.Label(
    calender,
    text="Start date: MM/DD/YY"
)
startlabel.grid()

startentry = ttk.Entry(
    calender,
    textvariable = user_start
)
startentry.insert(0, '08/01/23')
startentry.grid()
    
endlabel = ttk.Label(
    calender,
    text="End date: MM/DD/YY"
)
endlabel.grid()

endentry = ttk.Entry(
    calender,
    textvariable = user_end
)
endentry.insert(0, '08/02/23')
endentry.grid()

saveas = Button(
    mainframe,
    text="Save as...",
    font=("Arial", 14),
    command=ClickMe
)
saveas.grid(row=2)

export_location = StringVar()
exportloc = Label(
    mainframe,
    textvariable = export_location,
    font=("Arial", 14)
)
exportloc.grid(row=3)

runreport = ttk.Button(
    text="Run Report",
    command=Run_Report
)
runreport.grid()

root.mainloop()