import os
import re
import time
from win32 import win32gui
from win32 import win32process


currentPid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]

taskDict = {(re.split(r' {3,}| Services| Console', i)[:2])[0]:
            int((re.split(r' {3,}| Services| Console', i)[:2])[1])
            for i in os.popen('tasklist').read().split('\n')[3:-1]}

if taskDict['javaw.exe'] == currentPid:
    print("It's nullpo!")
