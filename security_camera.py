import cv2
import time
import datetime
#import os

cap = cv2.VideoCapture(1)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

framesize = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

#start recording:
#out = cv2.VideoWriter("video.mp4", fourcc, 20.0, framesize)
#stop recording:
#out.release

#prepare camera logic
timer = 5
recording = False
recording_stopped_time = None
timer_started = False

while True:
    _, frame = cap.read()

    #Gesicht(er) erkennen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 3)#Y
   

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x+width, y + height), (255, 0, 0), 3)

    if len(faces) >0:
        if recording:
            timer_started = False

        else:
            date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            out = cv2.VideoWriter((date + ".mp4"), fourcc, 10.0, framesize)
            recording = True
            print ("Recording started!")

    elif recording:
        if timer_started:
            if time.time() - recording_stopped_time >= timer:
                    recording = False
                    timer_started = False
                    out.release()
                    print("Stopped recording!")
        else:
            timer_started = True
            recording_stopped_time = time.time()

    if recording:
        out.write(frame)

    cv2.imshow("Securitycamera", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
out.release()
