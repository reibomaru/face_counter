from django.shortcuts import render
from face_count.models import UsageList


def index(request):
    usage_list = UsageList.objects.all()
    return render(request, 'face_count/usage.html', {'usage_list': usage_list})
