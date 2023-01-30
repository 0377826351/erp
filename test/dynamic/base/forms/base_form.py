from django import forms

class BaseForm(forms.Form):
    template_name = 'form_layout/form_default.html'
    
class BaseFormSearch(forms.Form):
    template_name = 'form_layout/form_search.html'