from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE, default=None)
    to = models.ForeignKey(User, related_name='to', on_delete=models.CASCADE, default=None)
    #sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
