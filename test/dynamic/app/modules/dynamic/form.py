from pickle import FALSE
from django import forms
from app.modules.user.model import User
from base.forms.base_form import BaseForm, BaseFormSearch
from base.forms.base_input import *


class DynamicForm(BaseForm):
    id = forms.CharField(label='ID', widget=BaseHiddenInput(), required=False)
    name = forms.CharField(label='Tên', widget=BaseTextInput(), required=True)
    code = forms.CharField(label='Mã', widget=BaseTextInput(), required=True)
    sort_order = forms.CharField(label='Thứ tự', widget=BaseNumberInput(attrs={'value': 255}), required=False)
    is_dev = forms.ChoiceField(label='Dùng cho Dev', choices=((True, 'Có'), (False, 'Không')), widget=BaseSelect(), required=True, initial=False)
    is_active = forms.ChoiceField(label='Hiển thị', choices=((True, 'Hoạt động'), (False, 'Không hoạt động')), widget=BaseSelect(), required=False, initial=True)
    
class DynamicFormSearch(BaseFormSearch):
    keyword = forms.CharField(widget=BaseTextInput(attrs={'placeholder': 'Từ khoá'}))
    is_active = forms.ChoiceField(choices=((None, '- Hiển thị -'), (False, 'Không hoạt động'), (True, 'Hoạt động')), widget=BaseSelect())