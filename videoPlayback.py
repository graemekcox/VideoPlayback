import cv2 #Library for the webcam 
import numpy as np #Libary for matrix in python


##
##cap =cv2.VideoCapture(0) #Sets Cap as the webcam 
##
##while True: 
##    ret,frame = cap.read() #Taking webcam object, and reading frame
##    cv2.imshow('frame',frame) #Display the video
##    #Record the video
##    
##    if cv2.waitKey(1) & 0xFF == ord('q'): #Press q to quit
##        #Save the recorded video as time closed
##        break
##
##
##cv2.destroyAllWindows() #Closes window
##cap.release() #Delets webcam object
####out.release()
##
###Open the recorded video



cap = cv2.VideoCapture('kitten.avi')
prevideo_removal_frames = 20 #This value removes the frames of video left
postvideo_removal_frames = 20 #This value removes the frames before the video 

frame_counter = prevideo_removal_frames+postvideo_removal_frames
cap.set(cv2.CAP_PROP_POS_FRAMES,prevideo_removal_frames) 
while(cap.isOpened()):
    ret, frame = cap.read()
    frame_counter += 1
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = prevideo_removal_frames+postvideo_removal_frames
        cap.set(cv2.CAP_PROP_POS_FRAMES,prevideo_removal_frames)
    if ret == True: 

        cv2.imshow('Graeme Dancing',frame)
        if cv2.waitKey(60) & 0xFF == ord('q'):
            break  
    else:
        break
    
cap.release()
cv2.destroyAllWindows()