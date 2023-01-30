from django.forms import ModelForm
from django import forms
from ..models import *
from ..models.choices import *
 
# define the class of a form
class CateForm(forms.Form):
    alias_category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    active = forms.BooleanField(required=False)

class ArtForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    alias_article = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label=None,widget=forms.Select(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(choices = form_select,widget=forms.Select(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget = forms.FileInput(attrs = {'class': 'form-control'}))