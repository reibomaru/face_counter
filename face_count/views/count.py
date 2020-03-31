from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Value, Process
from ctypes import c_bool
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
    'eye_count':0
}
module_dir = os.path.dirname(__file__)
json_path = os.path.join(module_dir, 'face_count.json')
face_count = 0
eye_count = 0
# isActiveGen = Value(c_bool, False)
face_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_eye.xml')
# cv2.imread()


def index(request):
    return render(request, 'base.html')


def count(request):
    global count_dict
    count_dict['start_unix_time'] = time.time()
    # global isActiveGen
    # process = Process(target=gen, args=(isActiveGen,))
    # process.start()
    # isActiveGen.value = True
    # analize_img()
    return HttpResponse('OK')


def stop(request):
    global count_dict
    count_dict['finish_unix_time'] = time.time()
    record_count(count_dict)
    # global isActiveGen
    # isActiveGen.value = False
    return HttpResponse('OK')

# @csrf_exempt
def analize_img(request):
    global count_dict
    # f = cv2.imdecode(request.body, 0)
    # print('POST:', request.POST)
    print('content_type:', request.content_type)
    # print('body:', request.body)
    # print('FILES:', request.FILES)
    # print(request.POST)
    # request_str = str(request.body)
    # request_dict = json.loads(request.body)
    # print(request.POST['img'][:20])
    request_dict = request.POST
    img_base64 = request_dict['img']
    # img_base64 = bytes(img_str)
    # cap_2 = cv2.VideoCapture(0)
    # _, img = cap_2.read()
    # print('ideal:', img.shape)
    # print('bytes:', img.tobytes())
    # img_base64 = request.body
    # print(img_base64)
    # print(img_base64[:20])
    r = base64.b64decode(img_base64.replace('data:image/png;base64,', ''))
                                                       
    # print(np.frombuffer(img_base))
    pil_img = Image.open(io.BytesIO(r))
    img_np = np.asarray(pil_img)
    # img_np = np.frombuffer(r, dtype=np.uint8)
    # img_np.reshape([59, 100, 3])
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    # img_np = img_np[:, :, ::-1]
    cv2.imwrite('python.png', img_np)
    faces = face_cascade.detectMultiScale(img_np, 1.3, 5)
    if type(faces) != tuple:
        count_up_face(len(faces))
        for x, y, w, h in faces:
            face_gray = img_np[y: y + h, x: x + w]
            eyes = eye_cascade.detectMultiScale(face_gray)
            if type(eyes) != tuple:
                count_up_eye()
    # r = base64.decodebytes(img_base64)
    # q = np.frombuffer(r, dtype=np.float64)
    # print()
    # print(img_np.shape)
    # print(request_dict['width'])
    # print(request_dict['height'])

    # print(np.frombuffer(img_byte_ideal)

    return JsonResponse(count_dict)

# def gen(isActiveGen):
#     count_dict = dict()
#     cap_2 = cv2.VideoCapture(0)
#     count_dict['start_unix_time'] = time.time()
#     while isActiveGen.value:
#         _, img = cap_2.read()
#         if None:
#             print('画像がありません')
#             break
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#         if type(faces) != tuple:
#             count_up_face(len(faces))
#             for x, y, w, h in faces:
#                 face_gray = gray[y: y + h, x: x + w]
#                 eyes = eye_cascade.detectMultiScale(face_gray)
#                 if type(eyes) != tuple:
#                     count_up_eye()
#         count_dict['face_count'] = face_count
#         count_dict['eye_count'] = eye_count
#         fw = open(BASE_DIR + '/static/face_count.json', 'w')
#         json.dump(count_dict, fw)
#         time.sleep(3)


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
