from django.shortcuts import render
from django.http import HttpResponse
from multiprocessing import Value, Process
from ctypes import c_bool
import cv2
import time
import json
import os
from mysite.settings import BASE_DIR
from face_count.models import Count

module_dir = os.path.dirname(__file__)
json_path = os.path.join(module_dir, 'face_count.json')
face_count = 0
eye_count = 0
isActiveGen = Value(c_bool, False)
face_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_eye.xml')


def index(request):
    return render(request, 'base.html')


def count(request):
    global isActiveGen
    process = Process(target=gen, args=(isActiveGen,))
    process.start()
    isActiveGen.value = True
    return HttpResponse('OK')


def stop(request):
    global isActiveGen
    isActiveGen.value = False
    return HttpResponse('OK')


def gen(isActiveGen):
    count_dict = dict()
    cap_2 = cv2.VideoCapture(0)
    count_dict['start_unix_time'] = time.time()
    while isActiveGen.value:
        _, img = cap_2.read()
        if None:
            print('画像がありません')
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if type(faces) != tuple:
            count_up_face(len(faces))
            for x, y, w, h in faces:
                face_gray = gray[y: y + h, x: x + w]
                eyes = eye_cascade.detectMultiScale(face_gray)
                if type(eyes) != tuple:
                    count_up_eye()
        count_dict['face_count'] = face_count
        count_dict['eye_count'] = eye_count
        fw = open(BASE_DIR + '/static/face_count.json', 'w')
        json.dump(count_dict, fw)
        time.sleep(3)
    count_dict['finish_unix_time'] = time.time()
    record_count(count_dict)


def record_count(count):
    print(count)
    Count.objects.create(
        face_count=count['face_count'],
        eye_count=count['eye_count'],
        start_unix_datetime=count['start_unix_time'],
        finish_unix_datetime=count['finish_unix_time'],
    )


def count_up_face(count):
    global face_count
    face_count += count


def count_up_eye():
    global eye_count
    eye_count += 1
