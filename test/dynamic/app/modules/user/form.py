from pickle import FALSE
from django import forms
from base.forms.base_form import BaseForm, BaseFormSearch
from base.forms.base_input import *

class UserForm(BaseForm):
    id = forms.CharField(label='ID', widget=BaseHiddenInput(), required=False)
    name = forms.CharField(label='Tên', widget=BaseTextInput())
    username = forms.CharField(label='Tên đăng nhập', widget=BaseTextInput(), required=True)
    password = forms.CharField(label='Mật khẩu', widget=BasePasswordInput(), required=True)
    is_active = forms.ChoiceField(label='Hiển thị', choices=((True, 'Hoạt động'), (False, 'Không hoạt động')), widget=BaseSelect(), required=False, initial=True)
    phone = forms.CharField(label='Số điện thoại', widget=BaseTextInput(), required=False)
    email = forms.CharField(label='Địa chỉ email', widget=BaseTextInput(), required=False)

class UserFormSearch(BaseFormSearch):
    keyword = forms.CharField(widget=BaseTextInput(attrs={'placeholder': 'Từ khoá'}))
    is_active = forms.ChoiceField(choices=((None, '- Hiển thị -'), (False, 'Không hoạt động'), (True, 'Hoạt động')), widget=BaseSelect())