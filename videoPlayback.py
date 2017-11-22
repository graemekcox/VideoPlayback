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

class stream:
    def __init__(self):
        self.cap = cv2.VideoCapture('kitten.avi')
        self.cap2 = cv2.VideoCapture('kitten2.avi')
        self.root = tk.Tk() #GUI Stuff
        self.frame = None
        self.frame2 = None
        self.stopEvent = None
        self.thread = None  #Need threads for the video to work
        self.root.wm_title("Seizure Viewer") 

        ## Pre-load image
        ret, self.frame = self.cap.read()
        self.frame = imutils.resize(self.frame, width=300)
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        ret, self.frame2 = self.cap2.read()
        self.frame2 = imutils.resize(self.frame2,width=300)
        image2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)

        #Convert video frame to an image, which we will display
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        image2 = Image.fromarray(image2)
        image2 = ImageTk.PhotoImage(image2)
        #Set this image as a 'label' for tkinter
        self.panel = tk.Label(image=image)
        self.panel.image = image #Set image as frame
        self.panel.pack(side="left",padx=10,pady=10)#Image location

        self.panel2 = tk.Label(image=image2)
        self.panel2.image = image2
        self.panel2.pack(side="left", expand = "yes",padx=10,pady=10)
        

        #Threading stuff to poll videoLoop function
        #Need this so that code constantly updates frame
        self.stopEvent = threading.Event()
##        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread = threading.Timer(1/1000,self.videoLoop) #Set timer that calls function every 1/1000 secondss
        self.thread.start()

        #Create button
        # command='function you define')
        btn = tk.Button(self.root, text="Snapshot!",
                command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
                pady=10)       
        self.root.wm_title("Video Stream") #Title of gui
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        #Frame counter initialization
        self.prevideo_removal_frames = 40 #This value removes the frames of video left
        self.postvideo_removal_frames = 40 #This value removes the frames before the video 
        self.frame_counter = self.prevideo_removal_frames + self.postvideo_removal_frames
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames)
        
        self.prevideo_removal_frames2 = 0 #This value removes the frames of video left
        self.postvideo_removal_frames2 = 0 #This value removes the frames before the video 
        self.frame_counter2 = self.prevideo_removal_frames2 + self.postvideo_removal_frames2
        self.cap2.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames2)
##        self.videoLoop()
        
    def videoLoop(self):
##        while(self.cap.isOpened()):
##        while not self.stopEvent.is_set():
        ret, self.frame = self.cap.read()
        self.frame_counter +=1
        ret, self.frame2 = self.cap2.read()
        self.frame_counter2 += 1
        
        #Reset frame coutner if needed
        if self.frame_counter == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
            self.frame_counter = self.prevideo_removal_frames + self.postvideo_removal_frames
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames)
        if self.frame_counter2 == self.cap2.get(cv2.CAP_PROP_FRAME_COUNT):
            self.frame_counter2 = self.prevideo_removal_frames2 + self.postvideo_removal_frames2
            self.cap2.set(cv2.CAP_PROP_POS_FRAMES,self.prevideo_removal_frames2)    
##            time.sleep(.0333333333/2)  #Add delay equal to fps we want
        self.frame = imutils.resize(self.frame, width=300)
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.frame2 = imutils.resize(self.frame2, width=300)
        image2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
        image2 = Image.fromarray(image2)
        image2 = ImageTk.PhotoImage(image2)
        if ret == True:
            
            if self.panel is None: #If image panel doesn't exist, create it
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left",padx=10,pady=10)
            if self.panel2 is None:
                    self.panel2 = tk.Label(image=image2)
                    self.panel2.image = image2
                    self.panel2.pack(side="left", expand = "yes",padx=10,pady=10)
            else: #otherwise update 
                    self.panel.configure(image=image)
                    self.panel.image = image
                    self.panel2.configure(image=image2)
                    self.panel2.image = image2                     
        else:
            return
##            break
        self.root.after(20,self.videoLoop) #call our function after this many milliseconds
    #Sample code for function connected to button
    def takeSnapshot(self):
        ret, frame = self.cap.read()
        frame = imutils.resize(frame, width=300)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.panel.configure(image=image)
        self.panel.image = image
        ret, frame2 = self.cap2.read()
        frame2 = imutils.resize(frame2, width=300)
        image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        image2 = Image.fromarray(image2)
        image2 = ImageTk.PhotoImage(image2)
        self.panel2.configure(image=image2)
        self.panel2.image = image2
    #Function called when we close the window
    def onClose(self):
        self.stopEvent.set()
        self.root.quit()


def main():

    obj = stream()
    obj.root.mainloop()

if __name__ == '__main__':
    main()