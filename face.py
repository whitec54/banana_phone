import numpy as np
import cv2
import os
from math import sqrt
from twilio.rest import Client
import time
import speech_recognition as sr

mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()
mic_list = sr.Microphone.list_microphone_names()

phone_numbers = {
    "dante": "",
    "cam": "",
    "kyle":"",
    "ellen":""
}

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('face.xml')
banana_cascade = cv2.CascadeClassifier('banana.xml')

lower_yellow = np.array([20,100,80])
upper_yellow = np.array([100,255,255])

cap = cv2.VideoCapture(0)

face_size = bx = by = fx = fy = 0; 



# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC24c1d3865a9fdde26606a648cd4a166f"
auth_token = "783f98bc748f5490fd74879a421604d9"
client = Client(account_sid, auth_token)
called = False

def ask_for_name():
    os.system("say 'Who should banana phone call?'")
    time.sleep(1)

def urlify(in_string, in_string_length):
    return in_string[:in_string_length].replace(' ', '%20')

def listen():
    with sr.Microphone(sample_rate = sample_rate, chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        print("Say Something")
        #listens for the user's input
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print ("you said: " + text)
            return text

        #error occurs when google could not understand what was said

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def ask_for_message():
    os.system("say 'What should banana phone say?'")

def make_call(phone,message):
    call = client.calls.create(
        to=phone,
        from_="+19894484290",
        url="https://handler.twilio.com/twiml/EHfd7f8826ff4dcd5bd300601f5c85f27a?Message="+message
    )

def opperation_banana():
    cv2.circle(img, (20, 20), 20, (255,0,0), 3)

    ask_for_name()
    name = listen()
    name = name.lower()
    phone = ""

    if name in phone_numbers:
        phone = phone_numbers[name]

    ask_for_message()
    message = listen()
    message = urlify(message,len(message))
    make_call(phone,message)

currently_calling = False
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(img,img, mask= mask)
    median = cv2.medianBlur(res,13)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bananas = banana_cascade.detectMultiScale(median, 1.05, 10)

    is_banana = (len(bananas) > 0)
    is_face = (len(faces) > 0)

    if is_banana:
        (x,y,w,h) = bananas[0]
        bx = int(x + (w/2))
        by = int(y + (h/2))
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    if is_face:
        (x,y,w,h) = faces[0]
        face_size = w
        fx = int(x + (w/2))
        fy = int(y + (h/2))
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    if is_banana and is_face:
        distance = sqrt(((bx - fx)*(bx - fx)) + ((by - fy)*(by - fy)))
        cv2.line(img, (bx,by), (fx,fy), (0,0,255))

        if distance < face_size and not currently_calling:
            currently_calling = True
            opperation_banana()
        elif distance > face_size and currently_calling:
            currently_calling = False
    else:
        currently_calling = False


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break



cap.release()
cv2.destroyAllWindows()


