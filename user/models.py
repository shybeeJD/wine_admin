from django.db import models

# Create your models here.
from django.contrib import admin

class User(models.Model):
    '''用户表'''

    username = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)
    superUser=models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'



admin.site.register(User)