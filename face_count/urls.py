from django.urls import path
from .views import count
from .views import usage
from .views import base
from django.conf import settings  # 追加
from django.conf.urls.static import static

urlpatterns = [
    path('', count.index, name='index'),
    path('start_count/', count.count, name='count'),
    path('terminate_count/', count.terminate, name='terminate'),
    path('usage/', usage.index, name='usage'),
    path('send_img/', count.analize_img, name='analize_img'),
    path('post_comment/', base.post_comment, name='post_comment'),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
