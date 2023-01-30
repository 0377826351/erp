from django.db import models
from django.db.models import Q
from base.models import BaseModel
from base.helpers import uuid

class Question(BaseModel,models.Model):
    id = models.CharField(primary_key=True, max_length=22, editable=False, default=uuid)
    question = models.CharField(max_length=1055, null=False, blank=False)
    answer = models.CharField(max_length=1055, null=False, blank=False)
    is_active = models.BooleanField(default=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    created_by = models.ForeignKey('user', related_name='question_created_by', db_column='created_by', on_delete=models.CASCADE, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)
    updated_by = models.ForeignKey('user', related_name='question_updated_by', db_column='updated_by', on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        db_table = 'question'
        ordering = ['-created_at']

    @classmethod
    def list_item(cls, params={}, options={}):
        result = None
        if options.get('task') == 'list-item':
            args = Q()
            if params.get('keyword'):
                args.add(Q(question__icontains=params.get('keyword')) | Q(answer__icontains=params.get('keyword')), Q.AND)
            if params.get('active'):
                args.add(Q(active=eval(params.get('active'))), Q.AND)
            result = cls.objects.filter(args)
        return result