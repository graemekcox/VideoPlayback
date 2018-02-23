from _future_ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import datetime
import imutils
import cv2
import os
import numpy as np
import time 
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation


class stream:
    def __init__(self):
        self.cap = cv2.VideoCapture('kitten.avi')
        self.root = tk.Tk() #GUI Stuff
        self.frame = None
        self.stopEvent = None
        self.thread = None  #Need threads for the video to work
        self.root.wm_title("Seizure Viewer") 

        ## Pre-load image
        ret, self.frame = self.cap.read()
        self.frame = imutils.resize(self.frame, width=300)
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        #Convert video frame to an image, which we will display
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        #Set this image as a 'label' for tkinter
        self.panel = tk.Label(image=image)
        self.panel.image = image 
        self.panel.pack(side="top",padx=10,pady=10)

        #Patient Status
        self.patient = open("patient.txt","r")
        self.text = tk.Text(self.root, height = 4, width=30)
        self.text.pack(side="top",fill="both",padx=10,pady=10)
        self.text.insert(tk.END,"Name: "+self.patient.readline()+"Birth Date: "+self.patient.readline()+"Disorder: "+self.patient.readline()+"Patient Number: "+self.patient.readline())
        #Need this so that code constantly updates frame
        self.stopEvent = threading.Event()
        self.thread = threading.Timer(1/1000,self.videoLoop) #Set timer that calls function every 1/1000 secondss
        self.thread.start()

        # command='function you define')
        btn1 = tk.Button(self.root, text="Next Siezure",command=self.nextSiezure)
        btn1.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)

        #Title of Gui
        self.root.wm_title("Video Stream") 
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        #Frame counter initialization
        self.prevideo_removal_frames = 0 #This value removes the frames of video left
        self.postvideo_removal_frames = 0 #This value removes the frames before the video 
        self.frame_counter = self.prevideo_removal_frames + self.postvideo_removal_frames
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames)

        #Graph parameters
        self.EEG = open("EEG.txt","r")
        self.EEG2 = open("EEG2.txt","r")
        self.x = [1,2,3,4,5,6,7,8,9,10]
        self.y = (self.EEG.readline().split(','))
        self.y2 = (self.EEG2.readline().split(','))
        self.fig = Figure(figsize=(2.5,2))
        self.a = self.fig.add_subplot(1,1,1)
        self.a.plot(self.x,self.y,color='red')
        self.a.plot(self.x,self.y2,color='blue')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side="top",fill="both",padx = 20, pady= 10)
        self.canvas.draw()
        
        
    def videoLoop(self):
        ret, self.frame = self.cap.read()
        self.frame_counter +=1
        time.sleep(.025)
        
        #Reset frame coutner if needed
        if self.frame_counter == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
            self.frame_counter = self.prevideo_removal_frames + self.postvideo_removal_frames
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames)

        self.frame = imutils.resize(self.frame, width=300)
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        if ret == True:
            
            if self.panel is None: #If image panel doesn't exist, create it
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="top",padx=10,pady=10)

            else: #otherwise update 
                    self.panel.configure(image=image)
                    self.panel.image = image                
        else:
            return
        self.root.after(20,self.videoLoop) #call our function after this many milliseconds


    #Buttons
    def nextSiezure(self):
        self.canvas.get_tk_widget().destroy()
        self.y =(self.EEG.readline().split(','))
        self.y2 = (self.EEG2.readline().split(','))
        self.graph()
        
    def graph(self):
        #Graph
        self.fig = Figure(figsize=(2.5,2))
        self.a = self.fig.add_subplot(1,1,1)
        self.a.plot(self.x,self.y,color='red')
        self.a.plot(self.x,self.y2,color='blue')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side="top",fill="both",padx = 20, pady= 10)
        self.canvas.draw()

    #Function called when we close the window
    def onClose(self):
        self.stopEvent.set()
        self.root.destroy()

def main():
    obj = stream()
    obj.root.mainloop()

if _name_ == '_main_':
    main()