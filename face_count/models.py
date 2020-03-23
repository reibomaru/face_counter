from django.conf import settings
from django.db import models


class Count(models.Model):
    face_count = models.IntegerField()
    eye_count = models.IntegerField(default=0)
    start_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.face_count