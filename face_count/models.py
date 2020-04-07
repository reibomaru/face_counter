from django.conf import settings
from django.db import models


class Count(models.Model):
    data_title = models.CharField(max_length=50, default='カウント')
    face_count = models.IntegerField(default=0)
    eye_count = models.IntegerField(default=0)
    start_unix_datetime = models.FloatField(blank=True, null=True)
    finish_unix_datetime = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.data_title

class UsageList(models.Model):
    list_title = models.CharField(max_length=15, default='タイトル')
    list_id = models.IntegerField(default=1)
    list_img = models.ImageField(upload_to='images/')
    list_content = models.TextField()
    list_link = models.CharField(max_length=100)
    list_link_title = models.CharField(max_length=15, default='タイトル')
    def __str__(self):
        return self.list_title

class Comment(models.Model):
    name = models.CharField(max_length=30)
    mail = models.CharField(max_length=30)
    comment = models.TextField()
    created_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.name
