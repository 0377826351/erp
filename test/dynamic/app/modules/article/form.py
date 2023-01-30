from django import forms
from django.conf import settings
from app.modules.category.model import Category
from app.modules.document.model import Document
from app.modules.dynamic.model import Dynamic
from base.helpers import dict_to_list_tuple
from base.validators import base_validators
from base.forms.base_form import BaseForm, BaseFormSearch
from base.forms.base_input import BaseHiddenInput, BaseImage, BaseSelect, BaseTextInput, BaseTextarea

# =========================================================================================================
class ArticleForm(BaseForm):
    id = forms.CharField(label='ID', widget=BaseHiddenInput(), required=False)
    title = forms.CharField(label='Tiêu sờ đề', widget=BaseTextInput(config={'box_class': 'col-6'}), required=True)
    type = forms.ChoiceField(label='Loại bài viết', choices=dict_to_list_tuple(settings.TYPE_ARTICLE), widget=BaseSelect(config={'box_class': 'col-3'}), required=False, initial=True)
    image = forms.CharField(label='Ảnh', widget=BaseImage(config={'box_class': 'col-3'}), required=False, validators=[base_validators.UploadValidator()])
    code = forms.CharField(label='Mã', widget=BaseTextInput(attrs={'domain-invisible': '[["type", "!=", "page"]]'}), required=False)
    video = forms.CharField(label='Link video', widget=BaseTextInput(attrs={'domain-invisible': '[["type", "!=", "video"]]'}), required=False)
    topic_id = forms.ModelChoiceField(label='Chuyên mục', widget=BaseSelect(), queryset=Document.objects.filter(dynamic_id__in=Dynamic.objects.filter(code='problem').values_list('id')), empty_label=settings.EMPTY_LABEL, required=False)
    category_id = forms.ModelChoiceField(label='Danh mục', widget=BaseSelect(attrs={'domain-invisible': '[["type", "==", "page"]]'}), queryset=Category.objects.filter(type='video'), empty_label=settings.EMPTY_LABEL, required=False)
    is_featured = forms.ChoiceField(label='Nổi bật', choices=dict_to_list_tuple(settings.TRUE_FALSE_CHOICE), widget=BaseSelect(), required=False, initial=True)
    content = forms.CharField(label='Nội dung', widget=BaseTextarea(config={'box_class': 'col-12'}, attrs={'class': 'ckeditor', 'rows': 1}))

# =========================================================================================================
class ArticleSearchForm(BaseFormSearch):
    keyword = forms.CharField(widget=BaseTextInput(attrs={'placeholder': 'Từ khoá'}))