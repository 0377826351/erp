import uuid
from django.db import models
from base.models import BaseModel
from django.db.models import Q
from base.helpers import HanlderFile, uuid
from slugify import slugify
import logging; logger = logging.getLogger(__name__)

class Article(BaseModel,models.Model):
    id = models.CharField(primary_key=True, max_length=22, editable=False, default=uuid)
    title = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=True, blank=True)
    image = models.CharField(max_length=255, null=True)
    video = models.CharField(max_length=255, null=True)
    category_id = models.ForeignKey('category',db_column='category_id',on_delete=models.DO_NOTHING,null=True,blank=False)
    topic_id = models.ForeignKey('document',db_column='topic_id',on_delete=models.DO_NOTHING,null=True,blank=False)
    is_featured = models.BooleanField(default=True)
    content = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    created_by = models.ForeignKey('user', related_name='article_created_by', db_column='created_by', on_delete=models.DO_NOTHING, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)
    updated_by = models.ForeignKey('user', related_name='article_updated_by', db_column='updated_by', on_delete=models.DO_NOTHING, null=True, blank=False)

    class Meta:
        db_table = 'article'
        ordering = ['created_at']

    def __str__(self):
        return self.title

    @classmethod 
    def list_item(cls,params={},options={}):
        result = None
        if options.get('task') == 'list-item':
            args = Q()
            if params.get('keyword'):
                args.add(Q(title__icontains=params.get('keyword')),Q.AND)
            type = params.get('type')
            if type == 'all':
                return cls.objects.filter(args)
            else:
                args.add(Q(type=type),Q.AND)
            result = cls.objects.filter(args)
        return result

    def delete(self,*args,**kwargs):
        if self.image:
            HanlderFile.delete_image(self.image)
        self.category_id.update_total_item()
        return super().delete(*args,**kwargs)
    
    def save(self,*args,**kwargs):
        if not self.code:
            self.code = slugify(self.title)
        self.category_id.update_total_item()
        return super().save(*args,**kwargs)