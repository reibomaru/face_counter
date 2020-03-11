from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import numpy as np
import cv2
import threading
from multiprocessing import Process
import time
from time import sleep
import json
import os
from mysite.settings import BASE_DIR


module_dir = os.path.dirname(__file__)
json_path = os.path.join(module_dir, 'count.json')
face_count = 0
eye_count = 0
count_dict = dict()

face_cascade = cv2.CascadeClassifier(BASE_DIR + '/face_count/src/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(BASE_DIR + '/face_count/src/haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

def index(request):
    return render(request, 'base.html', count_dict)

def camera(request):
    return StreamingHttpResponse(show_result(cap, face_cascade, eye_cascade),content_type="multipart/x-mixed-replace;boundary=frame")

def count(request):
    return StreamingHttpResponse(gen()) 

def gen():
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # print(type(faces))
        if type(faces) != tuple :
            count_up_face()
        count_dict['face_count'] = face_count
        fw = open(BASE_DIR + '/static/count.json', 'w')
        json.dump(count_dict, fw)       
        sleep(3)
        yield '...'
        key = cv2.waitKey(10)
        if key == 27:  # ESCキーで終了
            break
        
def count_up_face():
    global face_count
    face_count += 1
    print('顔の検出した回数は{}回です'.format(face_count))

def show_result(cap, face_cascade, eye_cascade):
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = img[y: y + h, x: x + w]
            face_gray = gray[y: y + h, x: x + w]
            eyes = eye_cascade.detectMultiScale(face_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)       
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        key = cv2.waitKey(10)
        if key == 27:  # ESCキーで終了
            break
