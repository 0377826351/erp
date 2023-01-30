from django.db import models
from django.contrib.auth.models import User

class Extend_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_date = models.DateTimeField()

    def __str__(self):
        return self.user_id