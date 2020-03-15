from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from multiprocessing import Value, Process
from ctypes import c_bool
import cv2
import time
import json
import os
from mysite.settings import BASE_DIR

module_dir = os.path.dirname(__file__)
json_path = os.path.join(module_dir, 'face_count.json')
face_count = 0
eye_count = 0
isActiveGen = Value(c_bool, False)
face_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_eye.xml')
process = None


def index(request):
    return render(request, 'base.html')


def camera(request):
    return StreamingHttpResponse(
        show_result(face_cascade, eye_cascade),
        content_type="multipart/x-mixed-replace;boundary=frame"
    )


def count(request):
    global isActiveGen
    global process
    process = Process(target=gen, args=(isActiveGen,))
    process.start()
    isActiveGen.value = True
    return HttpResponse('OK')


def stop(request):
    global isActiveGen
    global process
    isActiveGen.value = False
    record_count()
    return HttpResponse('OK')


def record_count():
    count_fr = open(BASE_DIR + '/static/face_count.json', 'r')
    count_dict = json.load(count_fr)
    count_record_fr = open(
        BASE_DIR + '/face_count/face_count_records.json', 'r')
    count_record_dict = json.load(count_record_fr)
    count_record_len = len(count_record_dict["records"])
    count_record_dict["records"][str(count_record_len)] = count_dict
    fw = open(BASE_DIR + '/face_count/face_count_records.json', 'w')
    json.dump(count_record_dict, fw)


def gen(isActiveGen):
    count_dict = dict()
    cap_2 = cv2.VideoCapture(0)
    start_ut = time.time()
    count_dict['start_unix_time'] = start_ut
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
    finish_ut = time.time()
    count_dict['finish_unix_time'] = finish_ut
    fw = open(BASE_DIR + '/static/face_count.json', 'w')
    json.dump(count_dict, fw)


def count_up_face(count):
    global face_count
    face_count += count


def count_up_eye():
    global eye_count
    eye_count += 1


def show_result(face_cascade, eye_cascade):
    cap_1 = cv2.VideoCapture(0)
    while True:
        _, img = cap_1.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = img[y: y + h, x: x + w]
            face_gray = gray[y: y + h, x: x + w]
            eyes = eye_cascade.detectMultiScale(face_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face, (ex, ey),
                              (ex + ew, ey + eh), (0, 255, 0), 2)
        _, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        key = cv2.waitKey(10)
        if key == 27:  # ESCキーで終了
            break
