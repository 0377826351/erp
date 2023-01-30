from json import JSONDecoder, JSONEncoder
from django.db import models
from django.db.models import Q
from base.models import BaseModel
from base.helpers import uuid

#==============================================================================
class Dynamic(BaseModel, models.Model):
    id = models.CharField(primary_key=True, max_length=22, editable=False, default=uuid)
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=255, null=False, blank=False, unique=True)
    sort_order = models.SmallIntegerField(default=255, null=False, blank=False)
    field = models.JSONField(encoder=JSONEncoder, decoder=JSONDecoder, null=True, blank=False)
    is_dev = models.BooleanField(default=False, blank=False)
    is_active = models.BooleanField(default=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    created_by = models.ForeignKey('user', related_name='dynamic_created_by', db_column='created_by', on_delete=models.CASCADE, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)
    updated_by = models.ForeignKey('user', related_name='dynamic_updated_by', db_column='updated_by', on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        db_table = 'dynamic'
        ordering = ["name"]
    
    @classmethod
    def list_item(cls, params={}, options={}):
        result = None
        if options.get('task') == 'list-item':
            args = Q()
            if params.get('keyword'):
                args.add(Q(name__icontains=params.get('keyword')) | Q(phone__icontains=params.get('keyword')) | Q(email__icontains=params.get('keyword')), Q.AND)
            if params.get('active'):
                args.add(Q(active=eval(params.get('active'))), Q.AND)
            result = cls.objects.filter(args)
        return result