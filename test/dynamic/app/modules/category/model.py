from django.db import models
from slugify import slugify
from app.modules.article.model import Article
from base.models import BaseModel
from django.db.models import Q
from base.helpers import uuid
import logging; logger = logging.getLogger(__name__)

def auto_integer():
    obj = Category.objects.order_by('-id_int').first()
    return 1 if not obj else obj.id_int + 1

class Category(BaseModel,models.Model):
    id = models.CharField(primary_key=True,max_length=22,editable=False,default=uuid)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=255,null=True,blank=True)
    id_int = models.IntegerField(default=auto_integer)
    multi_index = models.CharField(max_length=255)
    parent_id = models.ForeignKey('Category',related_name='category_parent_id',db_column='parent_id',on_delete=models.CASCADE,null=True,blank=False)
    level = models.IntegerField(default=0)
    total_item = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=False)
    created_by = models.ForeignKey('user',related_name='category_created_by',db_column='created_by',on_delete=models.CASCADE,null=True,blank=False)
    update_at = models.DateTimeField(auto_now_add=True,null=True,blank=False)
    update_by = models.ForeignKey('user',related_name='category_update_by',db_column='update_by',on_delete=models.CASCADE,null=True,blank=False)

    class Meta:
        db_table = 'category'
        ordering = ['-id_int']

    def __str__ (self):
        return self.name

    def update_total_item(self):
        self.total_item = Article.objects.filter(category_id=self.id).count()
        return self.save()

    @property
    def multi_name(self):
        if not self.parent_id:
            return self.name
        multi_name = ''
        list_index = self.multi_index.split('/')
        for index in list_index:
            if index:
                multi_name += '/' + Category.objects.get(id_int=index).name
        return multi_name[1:]

    @property
    def list_childs(self):
        return Category.objects.exclude(multi_index=self.multi_index).filter(multi_index__contains=self.multi_index).order_by('id_int')

    @property
    def list_parent(self):
        if self.parent_id:
            root_multi_index = '/{}/'.format(self.multi_index.split('/')[1])
            return Category.objects.exclude(multi_index=self.multi_index).filter(multi_index__endswith=root_multi_index).order_by('id_int')
        else:
            return None

    @property
    def is_have_childs(self):
        return bool(len(self.list_childs))

    def update_infomation(self):
        if not self.parent_id:
            self.multi_index = '/{}/'.format(self.id_int)
        else:
            self.multi_index = '{}{}/'.format(self.parent_id.multi_index,self.id_int)
            self.level = self.multi_index.count('/') - 2
        self.save(update_infomation=True)

    @classmethod
    def list_item(cls, params={}, options={}):
        result = None
        if options.get('task') == 'list-item':
            args = Q()
            if params.get('keyword'):
                args.add(Q(name__icontains=params.get('keyword')) | Q(multi_index__icontains=params.get('keyword')), Q.AND)
            if params.get('type'):
                args.add(Q(type=params.get('type')), Q.AND)
            result = cls.objects.filter(args)
        return result

    def save(self,*args, **kwargs):
        if kwargs.get('update_infomation'):
            del kwargs['update_infomation']
            return super().save(*args, **kwargs)
        list_childs = self.list_childs
        self.update_infomation()
        if list_childs:
            for child in list_childs:
                child.update_infomation()
        return super().save(*args, **kwargs)

    def delete(self,*args, **kwargs):
        list_childs = self.list_childs
        ret = super().delete(*args, **kwargs)
        if list_childs:
            for child in list_childs:
                if child:
                    child.update_infomation()
        return ret