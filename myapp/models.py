from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
import datetime as dt

class CustomUser(AbstractUser):
    user_icon_image = models.ImageField("画像")

    def __str__(self) -> str:
        return self.username
    

class Talk(models.Model):
    sender = models.ForeignKey(CustomUser, verbose_name=("送信者"), on_delete=models.CASCADE, related_name="talk_sent")
    receiver = models.ForeignKey(CustomUser, verbose_name=("受信者"), on_delete=models.CASCADE, related_name="talk_received")
    content = models.TextField(verbose_name=("内容"))
    send_datetime = models.DateTimeField(verbose_name=("送信日時"), auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.content