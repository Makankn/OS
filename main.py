from tkinter import *
from customtkinter import *
import random
import math

# Setup main application window
root = CTk()
root.geometry("600x200")
root.title("MMU simulator")
set_appearance_mode("dark")
set_default_color_theme("green")

# Initialize global variables for simulation state
counter = 0
storageCapacity = 0
pageSize = 0
processList = []
processListSegment = []
MMUtype = ''
totalProccess = 0
doneProccess = 0
activeProccess = 0
inMemoryList = []
doneProcessList = []
waitingProccess = 0
remainingPagesInMemory = 0
memoryLeft = 0

# Process class to handle individual process attributes
class Process:
    def __init__(self, ID, time, memory, segmentNumber):
        self.ID = ID
        self.time = time
        self.memory = memory
        self.inMemory = False
        self.done = False
        self.waiting = False
        self.endTime = 0
        self.pageNumbers = 0
        self.segmentNumber = segmentNumber

# Initialize simulation by setting storage and page size from user input
def getValue():
    global storageCapacity, pageSize, MMUtype, processList, processListSegment, remainingPagesInMemory, memoryLeft
    try:
        storageCapacity = int(entryStorage.get())
        pageSize = int(entrypageSize.get())
    except ValueError:
        print("Please enter valid integers for storage capacity and page size.")
        return

    entrypageSize.configure(state='disabled')
    entryStorage.configure(state='disabled')
    MMUlist.configure(state='disabled')
    submitButton.configure(state='disabled')

    MMUtype = optionmenu_var.get()
    processList = processGenerator()  # Correct typo in function name
    mButton1.configure(state=NORMAL)

    if MMUtype == 'paging':
        memoryPageNumbers = storageCapacity // pageSize  # Use integer division for clarity
        remainingPagesInMemory = memoryPageNumbers
    else:
        processListSegment = sorted(processList, key=lambda x: x.segmentNumber, reverse=True)
        memoryLeft = storageCapacity

# Generate a list of random processes
def processGenrator():
    proccesTimelist = [x for x in range(1, 10)]
    processMemoryList = [x*2 for x in range(1, 10)]
    segmnetNumberList = [x*2 for x in range(1, 10)]
    for i in range(10000):
        obj = Process(i + 1, random.choice(proccesTimelist), random.choice(processMemoryList), random.choice(segmnetNumberList))
        processList.append(obj)
    waitingProccess = len(processList)
    return processList

# Handle paging simulation logic
def paging(processList):
    for index, obj in enumerate(processList):
        obj.pageNumbers = math.ceil(obj.memory / int(pageSize))
        if obj.pageNumbers <= remainingPagesInMemory and not obj.inMemory:
            obj.inMemory = True
            obj.endTime = counter + obj.time
            inMemoryList.append(obj)
            activeProccess += 1
            waitingProccess -= 1
            remainingPagesInMemory -= obj.pageNumbers

# Update process status at each tick
def checkEnding(activeProcessList):
    for obj in activeProcessList:
        if obj.endTime == counter and not obj.done:
            obj.done = True
            if MMUtype == 'paging':
                remainingPagesInMemory += obj.pageNumbers
            else:
                memoryLeft += obj.memory
            doneProcessList.append(obj)
            doneProccess += 1
            activeProccess -= 1

# Handle segmentation simulation logic
def segmentation(processList):
    for obj in processList:
        if obj.memory <= memoryLeft and not obj.inMemory:
            obj.inMemory = True
            obj.endTime = counter + obj.time
            inMemoryList.append(obj)
            activeProccess += 1
            waitingProccess -= 1
            memoryLeft -= obj.memory

# Process time increment and trigger simulation step
def nClick():
    global counter
    counter += 1
    mButton1.configure(text=f'add 1 sec \n your timer is: {counter}')
    if MMUtype == 'paging':
        paging(processList)
        checkEnding(inMemoryList)
    else:
        segmentation(processListSegment)
        checkEnding(inMemoryList)

# UI setup for simulation control
optionmenu_var = StringVar(value="paging")
algorithmLable = CTkLabel(root, text='Choose an algorithm:', text_color='#42569e')
algorithmLable.grid(row=0, column=0, pady=5, padx=10)
MMUlist = CTkOptionMenu(root, variable=optionmenu_var, values=['paging', 'segmentation'], text_color='#d0cbd8', button_hover_color='#42569e', dropdown_hover_color='#42569e', hover=True)
MMUlist.grid(row=0, column=1, pady=5, sticky=E)

entryStorage = CTkEntry(root, width=140)
entryStorage.grid(row=1, column=1, pady=5)
entrypageSize = CTkEntry(root, width=140)
entrypageSize.grid(row=2, column=1, pady=5)

submitButton = CTkButton(root, text="Submit", command=getValue, state='normal', text_color='#d0cbd8', hover_color='#42569e')
submitButton.grid(row=3, column=1, pady=5)

doneCounter = CTkLabel(root, text=doneProccess, text_color='#42569e')
doneCounter.grid(row=0, column=4, pady=5)

waitCounter = CTkLabel(root, text=waitingProccess, text_color='#42569e')
waitCounter.grid(row=1, column=4, pady=5)

activeCounter = CTkLabel(root, text=activeProccess, text_color='#42569e')
activeCounter.grid(row=2, column=4, pady=5)

root.mainloop()
