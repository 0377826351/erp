from django import forms
from base.forms.base_form import BaseForm
from base.forms.base_input import BaseTextInput, BasePasswordInput

class AuthLoginForm(BaseForm):
    username = forms.CharField(label='Tài khoản', widget=BaseTextInput(), required=True)
    password = forms.CharField(label='Mật khẩu', widget=BasePasswordInput(), required=True)
    remember_me = forms.BooleanField(label=False, widget=forms.CheckboxInput())