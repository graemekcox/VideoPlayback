from __future__ import print_function
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
import csv



class stream:
    def __init__(self):
        self.titles = ['seizure_1.csv','seizure_2.csv','seizure_3.csv','seizure_4.csv','seizure_5.csv','normal.csv]
        self.cap = cv2.VideoCapture('kitten.avi')
        self.root = tk.Tk() #GUI Stuff
        self.frame = None
        self.stopEvent = None
        self.thread = None  #Need threads for the video to work
        self.root.configure(background='black')
        self.count = 0

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
        self.panel.place(x=200,y=0)
        
        #Need this so that code constantly updates frame
        self.stopEvent = threading.Event()
        self.thread = threading.Timer(1/1000,self.videoLoop) #Set timer that calls function every 1/1000 secondss
        self.thread.start()

        # command='function you define')
        self.btn1 = tk.Button(self.root, text="Change Seizure",command=self.ChangeSeizure)
        self.btn1.place(x=950,y=120)
        self.btn1.config(height = 1,width=12)
        

        #List Box
        self.list = tk.Listbox(self.root)
        self.list.insert(1,'Seizure_1.csv')
        self.list.insert(2,'Seizure_2.csv')
        self.list.insert(3,'Seizure_3.csv')
        self.list.insert(4,'Seizure_4.csv')
        self.list.insert(5,'Seizure_5.csv')
        self.list.insert(5,'Normal.csv')
        self.list.place(x=950, y=20)
        self.list.config(height = 5, width = 60)
        
        
        #Title of Gui
        self.root.wm_title("Seizure Viewer") 
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        #Frame counter initialization
        self.prevideo_removal_frames = 0 #This value removes the frames of video left
        self.postvideo_removal_frames = 0 #This value removes the frames before the video 
        self.frame_counter = self.prevideo_removal_frames + self.postvideo_removal_frames
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames)

        #Patient Status
        self.Id = tk.Label(self.root,text='Patient Id')
        self.Id.place(x=550,y=20)
        self.Id_text = tk.Text(self.root, height = 1, width = 24)
        self.Id_text.place(x=700,y=20)
        self.Age = tk.Label(self.root,text='Patient Age')
        self.Age.place(x=550,y=60)
        self.Age_text = tk.Text(self.root, height = 1, width = 24)
        self.Age_text.place(x=700,y=60)
        self.Symptom = tk.Label(self.root,text='Patient Symptom')
        self.Symptom.place(x=550,y=100)
        self.Symptom_text = tk.Text(self.root, height = 1, width = 24)
        self.Symptom_text.place(x=700,y=100)
        self.Weight = tk.Label(self.root,text='Patient Weight')
        self.Weight.place(x=550,y=140)
        self.Weight_text = tk.Text(self.root, height = 1, width = 24)
        self.Weight_text.place(x=700,y=140)
        self.Height = tk.Label(self.root,text='Patient Height')
        self.Height.place(x=550,y=180)
        self.Height_text = tk.Text(self.root, height = 1, width = 24)
        self.Height_text.place(x=700,y=180)
        self.counter = 1
        with open(self.titles[self.count],'r') as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file)
            for line in self.csv_reader:
                self.patient_info = line
                self.counter+=1
                if self.counter == 2:
                    break
        self.Id_text.insert(tk.END,self.patient_info[0])
        self.Age_text.insert(tk.END,self.patient_info[1])
        self.Symptom_text.insert(tk.END,self.patient_info[2])
        self.Weight_text.insert(tk.END,self.patient_info[3])
        self.Height_text.insert(tk.END,self.patient_info[4])
                       

        #Displaying Graphs
        data = np.genfromtxt(self.titles[self.count],delimiter=',')
        self.x = range(data.shape[1])
        self.fig = Figure(figsize=(2.5,6))
        for i in range(data.shape[0]): # For number of electrodes
            self.a = self.fig.add_subplot(data.shape[0]/2,2,i+1)
            self.a.plot(self.x, data[i][:],color='red')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=0,y=250)
        self.canvas.get_tk_widget().config(height = 700, width = 2000)
        self.a.set_yticklabels([])        
        self.canvas.draw()
        
        
    def videoLoop(self):
        ret, self.frame = self.cap.read()
        self.frame_counter +=1
        time.sleep(.025)
        
        #Reset frame coutner if needed
        if self.frame_counter == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
            self.frame_counter = self.prevideo_removal_frames + self.postvideo_removal_frames
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames)

        self.frame = imutils.resize(self.frame,width=300)
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        if ret == True:        
            if self.panel is None: #If image panel doesn't exist, create it
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.place(x=700,y=0)

            else: #otherwise update 
                    self.panel.configure(image=image)
                    self.panel.image = image                
        else:
            return
        self.root.after(20,self.videoLoop) #call our function after this many milliseconds


   #Buttons
    def ChangeSeizure(self):
        self.filename = self.list.get('active')
        self.graph()
        self.patient()
        
        
    def graph(self):
        #Graph
        data = np.genfromtxt(self.filename,delimiter=',')
        self.x = range(data.shape[1])
        self.fig = Figure(figsize=(2.5,6))
        for i in range(data.shape[0]): # For number of electrodes
            self.a = self.fig.add_subplot(data.shape[0]/2,2,i+1)
            self.a.plot(self.x, data[i][:],color='red')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=0,y=250)
        self.canvas.get_tk_widget().config(height = 700, width = 2000)
        self.a.set_yticklabels([])        
        self.canvas.draw()

        
    def patient(self):
        self.Id_text = tk.Text(self.root, height = 1, width = 24)
        self.Id_text.place(x=700,y=20)
        self.Age_text = tk.Text(self.root, height = 1, width = 24)
        self.Age_text.place(x=700,y=60)
        self.Symptom_text = tk.Text(self.root, height = 1, width = 24)
        self.Symptom_text.place(x=700,y=100)
        self.Weight_text = tk.Text(self.root, height = 1, width = 24)
        self.Weight_text.place(x=700,y=140)
        self.Height_text = tk.Text(self.root, height = 1, width = 24)
        self.Height_text.place(x=700,y=180)
        self.counter = 1
        with open(self.filename,'r') as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file)
            for line in self.csv_reader:
                self.patient_info = line
                self.counter+=1
                if self.counter == 2:
                    break
        self.Id_text.insert(tk.END,self.patient_info[0])
        self.Age_text.insert(tk.END,self.patient_info[1])
        self.Symptom_text.insert(tk.END,self.patient_info[2])
        self.Weight_text.insert(tk.END,self.patient_info[3])
        self.Height_text.insert(tk.END,self.patient_info[4])

    #Function called when we close the window
    def onClose(self):
        self.stopEvent.set()
        self.root.destroy()

def main():
    obj = stream()
    obj.root.mainloop()

if __name__ == '__main__':
    main()
