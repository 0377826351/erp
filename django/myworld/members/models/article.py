from django.db import models
from .category import Category
from django.conf import settings
from .choices import *

class Article(models.Model):
    title = models.CharField(max_length=255)
    alias_article = models.CharField(max_length=255) 
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    content = models.TextField()
    created = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    type = models.CharField(max_length=255,choices=form_select,default=1)
    image = models.ImageField(null=True)
    def __str__(self):
        return self.title