from pickle import FALSE
from django import forms
from app.modules.user.model import User
from base.forms.base_form import BaseForm, BaseFormSearch
from base.forms.base_input import *


class QuestionForm(BaseForm):
    id = forms.CharField(label='ID', widget=BaseHiddenInput(), required=False)
    question = forms.CharField(label='Câu hỏi', widget=BaseTextInput(), required=True)
    answer = forms.CharField(label='Câu trả lời', widget=BaseTextarea(), required=True)
    sort_order = forms.CharField(label='Thứ tự', widget=BaseNumberInput(attrs={'value': 255}), required=False)
    is_active = forms.ChoiceField(label='Hiển thị', choices=((True, 'Hoạt động'), (False, 'Đã bỏ')), widget=BaseSelect(), required=False, initial=True)
    
class QuestionFormSearch(BaseFormSearch):
    keyword = forms.CharField(widget=BaseTextInput(attrs={'placeholder': 'Từ khoá'}))
    is_active = forms.ChoiceField(choices=((None, '- Hiển thị -'), (False, 'Không hoạt động'), (True, 'Hoạt động')), widget=BaseSelect())