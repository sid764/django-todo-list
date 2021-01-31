from django.db import models

# Create your models here.

class Reminder(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    deadline = models.DateTimeField()
