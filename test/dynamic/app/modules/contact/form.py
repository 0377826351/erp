from django import forms
from django.conf import settings
from app.modules.document.model import Document
from base.helpers import dict_to_list_tuple
from base.forms.base_form import BaseForm, BaseFormSearch
from base.forms.base_input import *


class ContactForm(BaseForm):
    id = forms.CharField(label='ID', widget=BaseHiddenInput(), required=False)
    name = forms.CharField(label='Tên', widget=BaseTextInput(), required=True)
    phone = forms.CharField(label='Số điện thoại', widget=BaseTextInput(), required=True)
    email = forms.CharField(label='Email', widget=BaseTextInput(), required=False)
    gender = forms.ChoiceField(label='Giới tính', choices=dict_to_list_tuple(settings.GENDER), widget=BaseSelect(), required=False)
    password = forms.CharField(label='Mật khẩu', widget=BasePasswordInput(), required=False)
    problem_ids = forms.ModelMultipleChoiceField(label='Vấn đề gặp phải', queryset=Document.objects.filter(dynamic_id__code='problem'), widget=BaseSelectMultiple(), required=False)
    is_active = forms.ChoiceField(label='Hiển thị', choices=dict_to_list_tuple(settings.ACTIVE_STATE), widget=BaseSelect(), required=False, initial=True)
    avatar = forms.CharField(label='Avatar', widget=BaseImage(), required=False)

class ContactFormSearch(BaseFormSearch):
    keyword = forms.CharField(widget=BaseTextInput(attrs={'placeholder': 'Từ khoá'}))
    is_active = forms.ChoiceField(choices=((None, '- Hiển thị -'), (False, 'Không hoạt động'), (True, 'Hoạt động')), widget=BaseSelect())