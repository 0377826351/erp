from json import JSONDecoder, JSONEncoder
from django.db import models
from django.db.models import Q
from base.helpers import uuid
from base.models import BaseModel

class Contact(BaseModel, models.Model):
    id = models.CharField(primary_key=True,editable=False,max_length=22,default=uuid)
    name = models.CharField(max_length=255,null=False,blank=False)
    phone = models.CharField(max_length=255,null=False,blank=False)
    email = models.CharField(max_length=255,null=False,blank=False)
    birthday = models.DateField(null=True, blank=False)
    address = models.CharField(max_length=1055,null=False,blank=False)
    avatar = models.CharField(max_length=255,null=False,blank=False)
    gender = models.CharField(max_length=255,null=False,blank=False)
    os = models.CharField(max_length=255,null=False,blank=False)
    problem_ids = models.JSONField(encoder=JSONEncoder, decoder=JSONDecoder, null=True, blank=False)
    is_active = models.BooleanField(default=True,blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    created_by = models.ForeignKey('user', related_name='contact_created_by', db_column='created_by', on_delete=models.CASCADE, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)
    updated_by = models.ForeignKey('user', related_name='contact_updated_by', db_column='updated_by', on_delete=models.CASCADE, null=True, blank=False)
    # Auth
    password = models.CharField(max_length=128, null=True, blank=False)
    otp = models.CharField(max_length=6, null=True, blank=False)
    token = models.CharField(max_length=255, null=True, blank=True, default="")
    token_expiresin = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'contact'
        ordering = ['-created_at']

    @classmethod
    def list_item(cls,params={},options={}):
        result = None
        if options.get('task') == 'list-item':
            args = Q()
            if params.get('keyword'):
                args.add(Q(name__icontains=params.get('keyword')) | Q(phone__icontains=params.get('keyword')) | Q(email__icontains=params.get('keyword')), Q.AND)
            if params.get('active'):
                args.add(Q(active=eval(params.get('active'))), Q.AND)
            result = cls.objects.filter(args)
        return result




