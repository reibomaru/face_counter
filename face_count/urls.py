from django.urls import path
from .views import face_auth
from .views import count

urlpatterns = [
    path('', count.index, name='index'),
    path('start_count/', count.count, name='count'),
    path('terminate_count/', count.terminate, name='terminate'),
    path('face_auth/', face_auth.camera, name='camera'),
    path('send_img/', count.analize_img, name='analize_img')
]