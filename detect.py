import cv2
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from pygame import mixer
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymongo
from pymongo import MongoClient

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017')  #mongodb connection
db = client['mydb']  # database name
collection = db['test']  # collection name

def insert():

    try:
        # Capture and store a frame
        ret, frame = cap.read()
        # Convert frame to binary format for storing in MongoDB
        frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
        # Create a document to insert into MongoDB
        document = {
            'Image': frame_data
        }
        # Insert the document into MongoDB
        collection.insert_one(document)

        #client.close()

        return "Image Inserted in DB"
    except Exception as e:
        print(e)
        return "Error occured while inserting data"

def sendemail():
    try:
        sender = 'preetam119@gmail.com'
        receiver = 'preetam6468@gmail.com'

        message = MIMEMultipart()
        message["To"] = receiver
        message["From"] = sender
        message["Subject"] = 'Alert!!!!!'

        title = '<b> This is an alert from DDDS </b>'
        messageText = MIMEText('''Your relative is feeling drowsy while driving!!!''', 'html')
        message.attach(messageText)

        email = sender
        # app password
        password = 'nrcyohnahepnievx'

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email, password)
        fromaddr = sender
        toaddrs = receiver
        server.sendmail(fromaddr, toaddrs, message.as_string())

        server.quit()

        return "Email sent"
    except Exception as e:
        print(e)
        return "Error occured while sending the email"

mixer.init()
sound = mixer.Sound('alarm.wav')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
model = load_model(os.path.join("models", "model.h5")) #loading the pre trained model

lbl = ['Close', 'Open']

path = os.getcwd()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
score = 0
thicc = 2

while (True):
    ret, frame = cap.read()
    height, width = frame.shape[:2] #height, width

    # Preprocessing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converting to gray scale

    faces = face_cascade.detectMultiScale(gray, minNeighbors=3, scaleFactor=1.1, minSize=(25, 25))
    eyes = eye_cascade.detectMultiScale(gray, minNeighbors=1, scaleFactor=1.1)

    cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

    #face detection
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

    #Eye detection
    for (x, y, w, h) in eyes:

        eye = frame[y:y + h, x:x + w]   #Region of interest in frame
        eye = cv2.resize(eye, (80, 80))
        eye = eye / 255
        eye = eye.reshape(80, 80, 3)
        eye = np.expand_dims(eye, axis=0)
        prediction = model.predict(eye)

        # Condition for Close Eyes
        if prediction[0][0] > 0.30:
            cv2.putText(frame, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            score = score + 1
            if (score > 10):
                try:

                    sound.play()
                    cv2.putText(frame, "Danger! Danger! Danger!", (180, height - 50), font, 1, (0, 0, 255), 1,cv2.LINE_AA)

                    # To insert image in db
                    resdb = insert()
                    print(resdb)

                    #to trigger email
                    resemail = sendemail()
                    print(resemail)


                except:
                    pass
                if (thicc < 16):
                    thicc = thicc + 2
                else:
                    thicc = thicc - 2
                    if (thicc < 2):
                        thicc = 2
                cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)

        # Condition for Open
        elif prediction[0][1] > 0.90:
            score = score - 1
            if score < 0:
                score = 0
            cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)



    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
