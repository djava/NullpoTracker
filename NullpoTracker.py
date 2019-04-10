import os
import re
import time
from win32 import win32gui
from win32 import win32process

def isNullpo():

    #            |------Converts a HWND to a PID------||---Gets HWND of active window---|
    currentPid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]
    
    tasklist = []
    # Gets the output of running tasklist, and splits it by line, 
    # first 3 lines are garbage, last line is blank 
    for i in os.popen('tasklist').read().split('\n')[3:-1]:
        
        # Splits each line in tasklist into just the name and PID, adds it to a list
        tasklist.append(re.split(r' {3,}| Services| Console', i)[:2])

    # Converts the name and PID into a dict to find Nullpo more easily
    tasklist = {i[0]: int(i[1]) for i in tasklist}

    # If nullpo is open,
    if 'javaw.exe' in tasklist.items():

        # If nullpo is the current window, return true
        # (sub-listed to prevent IndexErrors)
        if tasklist['javaw.exe'] == currentPid:
            return True
            
    # Return false if either one is false
    return False


print(isNullpo())