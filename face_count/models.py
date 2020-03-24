from django.conf import settings
from django.db import models


class Count(models.Model):
    data_title = models.CharField(max_length=50, default='カウント')
    face_count = models.IntegerField()
    eye_count = models.IntegerField(default=0)
    start_unix_datetime = models.FloatField(blank=True, null=True)
    finish_unix_datetime = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.data_title