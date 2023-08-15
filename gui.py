# Contains GUI

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import calculator as calc
import employees
import payments
import mytime

root = Tk()
root.title("Tip Calculator")

user_start = StringVar()
user_end = StringVar()
export_location = StringVar()
export_location.set('File Path')

def get_export_path():
    print("calling get export path")
    global export_location
    export_location.set(filedialog.asksaveasfilename(defaultextension=".csv"))
    return

def Run_Report():
    # get start and end times in user's time zone and convert them to UTC for calculating
    start = mytime.conversion_for_gui(user_start.get())
    end = mytime.conversion_for_gui(user_end.get())
    export_location_string = export_location.get()
    print("exporting to ", export_location_string)
    calc.calculate(start, end, export_location_string)
    return

def donothing():
    return

mainframe = ttk.Frame(
    root,
    padding="13 13 22 22"
)

mainframe.grid(column=0, row=0, sticky=(N, W, E, S), padx=30, pady=20)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

menu_bar = Menu(root)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

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
startentry.insert(0, '08/14/23')
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
endentry.insert(0, '08/15/23')
endentry.grid()

saveas = Button(
    mainframe,
    text="Save as...",
    font=("Arial", 14),
    command=get_export_path
)
saveas.grid(row=2)

export_location_label = Label(
    mainframe,
    textvariable = export_location,
    font=("Arial", 14)
)
export_location_label.grid()

runreport = ttk.Button(
    text="Run Report",
    command=Run_Report
)
runreport.grid()

root.mainloop()