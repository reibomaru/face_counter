from django.db import models

# Create your models here.

class Count(models.Model):
    face_count = models.IntegerField(default=0)

