from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from base.helpers import uuid
from base.models import BaseModel


#==============================================================================
class User(BaseModel, AbstractUser):
    first_name = None
    last_name = None
    id = models.CharField(primary_key=True, max_length=22, editable=False, default=uuid)
    name = models.CharField(max_length=255, null=False, unique=True)
    phone = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=50, null=True)
    sort_order = models.SmallIntegerField(default=255, null=False, blank=False)
    image = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        ordering = ["created_at"]

    @classmethod
    def list_item(cls, params={}, options={}):
        result = None
        if options.get('task') == 'list-item':
            args = Q(is_superuser=False)
            if params.get('keyword'):
                args.add(Q(name__icontains=params.get('keyword')) | Q(phone__icontains=params.get('keyword')) | Q(email__icontains=params.get('keyword')), Q.AND)
            if params.get('is_active'):
                args.add(Q(is_active=eval(params.get('is_active'))), Q.AND)
            result = cls.objects.filter(args)
        return result