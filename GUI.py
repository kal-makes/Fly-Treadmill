
from datetime import datetime
from tkinter import *
import tkinter as tk
import stepper
import numpy as np 
import cv2
from PIL import Image, ImageTk
import threading
from random import randint
import time
import datetime as dt

GPIO_pins = (14, 15, 18)  
direction= 20       # Direction -> GPIO Pin
step = 21 
reset = 23     # Step -> GPIO Pin
testMotor = stepper.stepperMotor(GPIO_pins, direction, step, reset)
testMotor.resolution_set("1/16")

#root window
root = tk.Tk()
root.title('FlyGUI')
root.geometry('{}x{}'.format(1100, 550))
#create containers
top_frame=Frame(root, bg="purple", width=1100, height=50, pady=2)
center_frame=Frame(root, bg="white",width=50, height=40)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center_frame.grid(row=1, sticky="nsew")

top_frame.grid_rowconfigure(0, weight=1)
top_frame.grid_columnconfigure(4, weight=1)

date=dt.datetime.now()
dateLabel = Label(top_frame, bg="purple", text=f"{date:%A, %B %d, %Y}", font="Calibri, 10", fg="gold", padx=10)
dateLabel.grid(row=1)
#create widgets 
imageFrame = tk.LabelFrame(center_frame, width=600, height=550, text="Camera")
motorFrame = tk.LabelFrame(center_frame, width=500, height = 550, text="Stepper Motor")

center_frame.grid_rowconfigure(8, weight=1)
center_frame.grid_columnconfigure(3, weight=1)

imageFrame.grid(column=0, row=0, sticky="w")
imageFrame.grid_rowconfigure(2, weight=1)
imageFrame.grid_columnconfigure(0, weight=1)
imageFrame.grid_propagate(False)

motorFrame.grid(column=1, row=0, sticky="w")
motorFrame.grid_rowconfigure(5, weight=1)
motorFrame.grid_columnconfigure(4, weight=1)
motorFrame.grid_propagate(False)
#camera button
startCamera = Button(imageFrame, text="Start Camera!", command=lambda:threading.Thread(target=show_frame).start())
startCamera.grid_propagate(False)
startCamera.grid(row=1, pady=10)

# #Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0)
cap = cv2.VideoCapture(0)

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    # print("TRUE")
def eStop():
    testMotor.stopMotor()
def motorStatus():
    while 1:
        if testMotor.status == True:
            print("true")
        else:
            print("false")

duration_var = tk.IntVar()
specific_time = IntVar()
speed_var = IntVar()

speed_label = Label(motorFrame, text="Speed (RPM): ")
speed_entry = Entry(motorFrame, textvariable=speed_var)
speed_label.grid(row=2, column=0, pady=10)
speed_entry.grid(row=2, column=1, pady=10)

hourCB=Checkbutton(motorFrame, text="Hours", variable = specific_time, onvalue=1)
minuteCB=Checkbutton(motorFrame, text="Minutes", variable = specific_time, onvalue=2)
secondsCB=Checkbutton(motorFrame, text="Seconds", variable = specific_time, onvalue=3)
hourCB.grid(row=1, column=0)
minuteCB.grid(row=1, column=1)
secondsCB.grid(row=1, column=2)

estop=Button(motorFrame,text="STOP MOTOR", fg="white", bg="red", font="bold",command=lambda:threading.Thread(target=eStop).start()  )
estop.grid(row=3, column=1, pady=10, sticky="ns")


img=Image.open("/home/pi/Documents/GUI ICONS/ONUtiger.png")
img_resize=img.resize((100,100))
final_image=ImageTk.PhotoImage(img_resize)
logo = Label(motorFrame, image=final_image)
logo.grid(row=4, column=1)
status_var = tk.StringVar()
status_label = Label(motorFrame, textvariable=status_var, )
status_label.grid(row=2, column=2)
def durationSubmit():
    duration = duration_var.get()
    specific=specific_time.get()
    speed = speed_var.get()
    testMotor.stepper_speed(speed)
    print("Duration"+str(duration))
    print("Specific"+str(specific))
    print("Speed"+str(speed))
    duration_var.set("")
    duration_time_label = Label(root, text = duration)
    duration_time_label.grid(row=5, column=5)
    status_var.set("MOTOR RUNNING!")
    threading.Thread(target=testMotor.run_timed(specific,duration)).start()
    status_var.set("MOTOR STOPPED!")
    

duration_label = Label(motorFrame, text = "Timer duration: ")
duration_label.grid(row=0, column=0)
duration_entry = Entry(motorFrame, textvariable=duration_var)
duration_entry.grid(row=0, column=1)

startMotor = Button(motorFrame, text="Start Motor!", command=lambda:threading.Thread(target=durationSubmit).start(), padx = 10)
startMotor.grid(row=0, column=2, padx=10)

root.mainloop()




