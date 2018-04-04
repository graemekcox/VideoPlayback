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

import sys
sys.path.insert(0, '/Users/graemecox/Documents/Capstone/Code/eegSvm/PreprocessingFunctions/')

from eeg import *

# patient = Patient(1317205,10,'/Users/graemecox/Documents/Capstone/Data/EEG_Data/Dog_1/')


class stream:
    def __init__(self):

        ## Define some example patients for us to use
        # temp_pat= Patient(1317205,23,175,180,'Tonic/Clonic Seizure','/Users/graemecox/Documents/Capstone/Data/EEG_Data/Dog_1/')
        # self.patient_list = []
        # self.patient_list.append(temp_pat)
        # temp_pat = Patient(1314569,22,200,140,'Infantile','/Users/graemecox/Documents/Capstone/Data/EEG_Data/Dog_2/')
        # self.patient_list.append(temp_pat)
        # temp_pat = Patient(1315405,22, 180,182,'Grand Mal','/Users/graemecox/Documents/Capstone/Data/EEG_Data/Dog_3/')
        # self.patient_list.append(temp_pat)

        self.patient_list = np.load('patient_list.npy')
        self.patient_index = 0
        self.current_patient = self.patient_list[self.patient_index]

        self.titles = ['P1_seizure_1.csv','P1_seizure_2.csv','P1_seizure_3.csv','P1_seizure_4.csv','P1_seizure_5.csv','P1_normal.csv']
        self.cap = cv2.VideoCapture('/Users/graemecox/Documents/Capstone/Code/VideoStream/kitten.avi')
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
        self.panel.place(x=200,y=20)
        
        #Need this so that code constantly updates frame
        self.stopEvent = threading.Event()
        self.thread = threading.Timer(1/1000,self.videoLoop) #Set timer that calls function every 1/1000 secondss
        self.thread.start()

        # command='function you define')
        self.btn1 = tk.Button(self.root, text="Change Dataset",command=self.ChangeSeizure)
        self.btn1.place(x=950,y=120)
        self.btn1.config(height = 1,width=12)

        self.btn2 = tk.Button(self.root, text = "Change Patient",command = self.ChangePatient)
        self.btn2.place(x=1150,y=120)
        self.btn2.config(height = 1, width = 12)
        

        #List Box                       
        self.list = tk.Listbox(self.root)
        for i in range(len(self.titles)):
            self.list.insert(i+1,self.titles[i])
        self.list.place(x=950, y=20)
        self.list.config(height = 5, width = 30)

        self.list2 = tk.Listbox(self.root)
        #List all 
        for i in range(len(self.patient_list)):
            self.list2.insert(i+1, str(self.patient_list[i].id))
        # self.list2.insert(1,'Patient_1')
        # self.list2.insert(2,'Patient_2')
        # self.list2.insert(3,'Patient_3')
        self.list2.place(x=1150, y=20)
        self.list2.config(height=5, width = 30)
        
        
        #Title of Gui
        self.root.wm_title("Seizure Viewer") 
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        #Frame counter initialization
        self.prevideo_removal_frames = 0 #This value removes the frames of video left
        self.postvideo_removal_frames = 0 #This value removes the frames before the video 
        self.frame_counter = self.prevideo_removal_frames + self.postvideo_removal_frames
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames)

        #Patient Status
        self.Id = tk.Label(self.root,text='Patient ID',background='black',foreground='white',font='16')
        self.Id.place(x=550,y=20)
        self.Id_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Id_text.place(x=700,y=20)
        self.Age = tk.Label(self.root,text='Patient Age',background='black',foreground='white',font='16')
        self.Age.place(x=550,y=70)
        self.Age_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Age_text.place(x=700,y=70)
        self.Symptom = tk.Label(self.root,text='Patient Seizure',background='black',foreground='white',font='16')
        self.Symptom.place(x=550,y=120)
        self.Symptom_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Symptom_text.place(x=700,y=120)
        self.Weight = tk.Label(self.root,text='Patient Weight',background='black',foreground='white',font='16')
        self.Weight.place(x=550,y=170)
        self.Weight_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Weight_text.place(x=700,y=170)
        self.Height = tk.Label(self.root,text='Patient Height',background='black',foreground='white',font='16')
        self.Height.place(x=550,y=220)
        self.Height_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Height_text.place(x=700,y=220)
        self.counter = 1
        with open(self.titles[self.count],'r') as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file)
            for line in self.csv_reader:
                self.patient_info = line
                self.counter+=1
                if self.counter == 2:
                    break


        self.Id_text.insert(tk.END,str(self.current_patient.id))
        self.Age_text.insert(tk.END,str(self.current_patient.age))
        self.Symptom_text.insert(tk.END,str(self.current_patient.symptom))
        self.Weight_text.insert(tk.END,str(self.current_patient.weight))
        self.Height_text.insert(tk.END,str(self.current_patient.height))

        # self.Id_text.insert(tk.END,self.patient_info[0])
        # self.Age_text.insert(tk.END,self.patient_info[1])
        # self.Symptom_text.insert(tk.END,self.patient_info[2])
        # self.Weight_text.insert(tk.END,self.patient_info[3])
        # self.Height_text.insert(tk.END,self.patient_info[4])
                       

        #Displaying Graphs
        
        data = np.genfromtxt(self.titles[self.count],delimiter=',')
        self.x = range(data.shape[1])
        self.fig = Figure(figsize=(2.5,6))
        self.fig.patch.set_facecolor("black")
        for i in range(data.shape[0]): # For number of electrodes
            self.a = self.fig.add_subplot(data.shape[0]/2,2,i+1)
            self.a.plot(self.x, data[i][:],color='red')
            self.a.tick_params(axis='x', colors='white')
            self.a.tick_params(axis='y', colors='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)       
        self.canvas.get_tk_widget().place(x=0,y=250)
        self.canvas.get_tk_widget().config(height = 700, width = 2000)
        self.canvas.draw()
        self.Title = tk.Label(self.root,text='Patient '+str(self.current_patient.id)+'\n Seizure #'+str(self.current_patient.ictalIndex),background='black',foreground='white',font=("Courier",'24'))


        # self.Title = tk.Label(self.root,text='Patient '+self.patient_info[0]+'\n Seizure #'+self.patient_info[2],background='black',foreground='white',font=("Courier",'24'))
        self.Title.place(x=850,y=250)
        
        
    def videoLoop(self):
        ret, self.frame = self.cap.read()
        self.frame_counter +=1
        time.sleep(.025)
        
        #Reset frame counter if needed
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
        self.patient()
        self.graph()


    def ChangePatient(self):
        temp_id = self.list2.get('active')

        for i in range(len(self.patient_list)):
            if str(self.patient_list[i].id) == str(temp_id):
                temp_index = i

        self.current_patient = self.patient_list[temp_index]
        self.patient_index = temp_index
        self.filename = self.list.get('active') #Get current selected seizure (CHANGE LATER)
        self.patient()
        self.graph()
        # temp_index = 
        # print(self.title)
      #  self.titles = self.list.get('active')
    #   self.patient()
    #   self.graph()
        
        
        
    def graph(self):
        #Graph
        data = np.genfromtxt(self.filename,delimiter=',')
        self.x = range(data.shape[1])
        self.fig = Figure(figsize=(2.5,6))
        self.fig.patch.set_facecolor("black")
        for i in range(data.shape[0]): # For number of electrodes
            self.a = self.fig.add_subplot(data.shape[0]/2,2,i+1)
            self.a.plot(self.x, data[i][:],color='red')
            self.a.tick_params(axis='x', colors='white')
            self.a.tick_params(axis='y', colors='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root) 
        self.canvas.get_tk_widget().place(x=0,y=250)
        self.canvas.get_tk_widget().config(height = 700, width = 2000)
        self.canvas.draw()
        self.Title = tk.Label(self.root,text='Patient '+str(self.current_patient.id)+'\n Seizure #'+str(self.current_patient.ictalIndex),background='black',foreground='white',font=("Courier",'24'))
        self.Title.place(x=850,y=250)

        
    def patient(self):
        self.Id_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Id_text.place(x=700,y=20)
        self.Age_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Age_text.place(x=700,y=70)
        self.Symptom_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Symptom_text.place(x=700,y=120)
        self.Weight_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Weight_text.place(x=700,y=170)
        self.Height_text = tk.Text(self.root, height = 1, width = 24,font='14')
        self.Height_text.place(x=700,y=220)
        self.counter = 1
        with open(self.filename,'r') as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file)
            for line in self.csv_reader:
                self.patient_info = line
                self.counter+=1
                if self.counter == 2:
                    break


        # # self.Id_text.insert(tk.END, str(self.pat.id))
        # print(self.patient_info[0])
        # print(self.patient_info[1])

        self.Id_text.insert(tk.END,str(self.current_patient.id))
        self.Age_text.insert(tk.END,str(self.current_patient.age))
        self.Symptom_text.insert(tk.END,str(self.current_patient.symptom))
        self.Weight_text.insert(tk.END,str(self.current_patient.weight))
        self.Height_text.insert(tk.END,str(self.current_patient.height))

        # self.Id_text.insert(tk.END,self.patient_info[0])
        # self.Age_text.insert(tk.END,self.patient_info[1])
        # self.Symptom_text.insert(tk.END,self.patient_info[2])
        # self.Weight_text.insert(tk.END,self.patient_info[3])
        # self.Height_text.insert(tk.END,self.patient_info[4])

    #Function called when we close the window
    def onClose(self):
        self.stopEvent.set()
        self.root.destroy()

def main():
    obj = stream()
    obj.root.mainloop()

if __name__ == '__main__':
    main()
