from django import forms
from django.conf import settings
from app.modules.category.model import Category
from base.forms.base_form import BaseForm, BaseFormSearch
from base.forms.base_input import BaseHiddenInput, BaseImage, BaseSelect, BaseTextInput
from django.core import validators
from base.helpers import dict_to_list_tuple
from base.validators import base_validators

class CategoryForm(BaseForm):
    id = forms.CharField(label='ID',widget=BaseHiddenInput(),required=False)
    name = forms.CharField(label='Tên danh mục',widget = BaseTextInput(),required=True,validators=[validators.MinLengthValidator(5)])
    image = forms.CharField(label='Ảnh',widget=BaseImage(config={'box_class':'col-3'}),required=False,validators=[base_validators.UploadValidator()])
    total_item = forms.IntegerField(label='Số lượng bài viết',widget=BaseTextInput(attrs={'readonly':'readonly'}),initial=255)
    type = forms.ChoiceField(label='Loại danh mục',choices=dict_to_list_tuple(settings.TYPE_CATEGORY),widget=BaseSelect(),required=False,initial=True)
    multi_index = forms.CharField(label='Chỉ mục đa cấp',widget=BaseHiddenInput(),required=False)
    parent_id = forms.ModelChoiceField(label="Danh mục cha",widget=BaseSelect,queryset=Category.objects.all(),empty_label=settings.EMPTY_LABEL,required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        if initial:
            id= initial.get('id')
            type = initial.get('type')
            if id:
                instance = Category.objects.get(id=id)
                self.fields['parent_id'].queryset = Category.objects.exclude(id=instance.id).filter(level__lte=instance.level,type=instance.type)
            elif type:
                self.fields['type'].queryset = Category.objects.filter(type=type)

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data.get('id')
        parent = cleaned_data.get('parent_id')
        if id and parent:
            instance = Category.objects.get(id=id)
            if instance.level < parent.level:
                self.add_error('parent_id','Không thể chọn danh mục con!')
            elif instance.id == parent.id:
                self.add_error('parent_id','Không thể chọn danh mục này')

class CategorySearchForm(BaseFormSearch):
    keyword = forms.CharField(widget=BaseTextInput(attrs={'placeholder': 'Từ khoá'}))

