from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import base64
import io
import numpy as np
import cv2
from PIL import Image
import time
import json
import os
from mysite.settings import BASE_DIR
from face_count.models import Count

count_dict = {
    'face_count': 0,
    'eye_count': 0,
    'start_unix_time':time.time(),
    'finish_unix_time': None,
}
face_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_eye.xml')


def index(request):
    return render(request, 'base.html')


def count(request):
    global count_dict
    count_dict['face_count'] = 0
    count_dict['eye_count'] = 0
    count_dict['start_unix_time'] = time.time()
    return HttpResponse('OK')


def terminate(request):
    global count_dict
    count_dict['finish_unix_time'] = time.time()
    record_count(count_dict)
    return HttpResponse('OK')

def analize_img(request):
    global count_dict
    request_dict = request.POST
    img_base64 = request_dict.get('img')
    r = base64.b64decode(img_base64.replace('data:image/png;base64,', ''))
    pil_img = Image.open(io.BytesIO(r))
    img_np = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_BGR2RGB)
    img_gray_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('python.png', img_np)
    faces = face_cascade.detectMultiScale(img_gray_np, 1.3, 5)
    if type(faces) != tuple:
        count_up_face(len(faces))
        for x, y, w, h in faces:
            cv2.rectangle(img_np, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = img_np[y: y + h, x: x + w]
            face_gray = img_gray_np[y: y + h, x: x + w]
            eyes = eye_cascade.detectMultiScale(face_gray)
            if type(eyes) != tuple:
                count_up_eye()
    cv2.imwrite('python1.png', img_np)
    _, img_png = cv2.imencode('.png', img_np)
    # print(type(img_np))
    # img_bytes = img_np.tobytes()
    # count_dict['img_base64'] = base64.b64encode(img_jpg)
    print(base64.b64encode(img_png)[:20])
    print(base64.b64encode(img_png).decode("utf-8")[:100])
    # print(type(img_base64))
    count_dict['img_base64'] = "data:image/png;base64," + base64.b64encode(img_png).decode("utf-8")
    return JsonResponse(count_dict, safe=False)

def record_count(count):
    data_title = 'データ：' + str(timezone.now())
    Count.objects.create(
        data_title=data_title,
        face_count=count['face_count'],
        eye_count=count['eye_count'],
        start_unix_datetime=count['start_unix_time'],
        finish_unix_datetime=count['finish_unix_time'],
    )


def count_up_face(count):
    global count_dict
    count_dict['face_count'] += count


def count_up_eye():
    global count_dict
    count_dict['eye_count'] += 1
