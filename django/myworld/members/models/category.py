from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    alias_category = models.CharField(max_length=255,primary_key=True)
    name = models.CharField( max_length=255)
    active = models.BooleanField(null=True)

    def __str__(self):
        return self.alias_category
