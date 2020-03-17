from django.http import StreamingHttpResponse
import cv2
import json
import os
from mysite.settings import BASE_DIR

face_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    BASE_DIR + '/face_count/src/haarcascade_eye.xml')


def camera(request):
    return StreamingHttpResponse(
        show_result(face_cascade, eye_cascade),
        content_type="multipart/x-mixed-replace;boundary=frame"
    )


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
