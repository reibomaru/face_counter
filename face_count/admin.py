from django.contrib import admin
from .models import Count, UsageList, Comment

# Register your models here.
admin.site.register(Count)
admin.site.register(UsageList)
admin.site.register(Comment)
