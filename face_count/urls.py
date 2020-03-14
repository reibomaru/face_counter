from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stop_count/', views.stop, name='stop'),
    path('start_count/', views.count, name='count'),
    path('face_auth/', views.camera, name='camera')
]