from tkinter import *
import tkinter as tk
import stepper

#root window
root = Tk()
#root.geometry("1920x1080")

duration_var = tk.IntVar()
def durationSubmit():
    duration = duration_var.get()
    #print(duration)
    duration_var.set("")
    duration_time_label = Label(motorFrame, text = duration)
    duration_time_label.grid(row=1, column=1)
    stepper.countdown()

motorFrame = Frame(root)
motorFrame.pack()

duration_label = Label(motorFrame, text = "Timer duration: ")
duration_label.grid(row=0, column=0)
duration_entry = Entry(motorFrame, textvariable=duration_var)
duration_entry.grid(row=0, column=1)

startMotor = Button(motorFrame, text="Start Motor!", command=durationSubmit)
startMotor.grid(row=1, column=0)



root.mainloop()