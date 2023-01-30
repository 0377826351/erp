from django import forms
from base.forms.base_form import BaseForm, BaseFormSearch
from base.forms.base_input import *
from app.modules.dynamic.model import Dynamic
from .model import Document
from base.validators import base_validators


class DocumentForm(BaseForm):
    id = forms.CharField(label='ID', widget=BaseHiddenInput(), required=False)
    name = forms.CharField(label='Tên', widget=BaseTextInput(), required=True)
    code = forms.CharField(label='Mã', widget=BaseTextInput(), required=True)
    dynamic_id = forms.ModelChoiceField(label='Chuyên mục', queryset=Dynamic.objects.all(), widget=BaseSelect(), required=True, empty_label='-- Chọn --')
    parent = forms.ModelChoiceField(label='Bản ghi cha', queryset=Document.objects.filter(parent_id=None), widget=BaseSelect(), required=False, empty_label='-- Chọn --')
    image = forms.CharField(label='Ảnh', widget=BaseImage(config={'box_class': 'col-3'}), required=False, validators=[base_validators.UploadValidator()])
    sort_order = forms.CharField(label='Thứ tự', widget=BaseNumberInput(attrs={'value': 255}), required=False)
    is_dev = forms.ChoiceField(label='Dùng cho Dev', choices=((True, 'Có'), (False, 'Không')), widget=BaseSelect(), required=True, initial=False)
    is_active = forms.ChoiceField(label='Hiển thị', choices=((True, 'Hoạt động'), (False, 'Không hoạt động')), widget=BaseSelect(), required=False, initial=True)
    
class DocumentFormSearch(BaseFormSearch):
    keyword = forms.CharField(widget=BaseTextInput(attrs={'placeholder': 'Từ khoá'}))
    dynamic_id = forms.ModelChoiceField(queryset=Dynamic.objects.all(), widget=BaseSelect(), required=True, empty_label='-- Chọn chuyên mục --')
    is_active = forms.ChoiceField(choices=((None, '- Hiển thị -'), (False, 'Không hoạt động'), (True, 'Hoạt động')), widget=BaseSelect())