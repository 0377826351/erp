from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django import forms
from ....models import Category
from ....forms import CateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def category(request):
    template = loader.get_template('admin/category/index.html')
    list_obj = Category.objects.all()
    context = {
        'title': 'Category',
        'list_obj': list_obj,
    }
    return HttpResponse(template.render(context, request))

@login_required
def form_cate(request, alias=None):
    template = loader.get_template('admin/category/form-cate.html')
    cate = None
    form = CateForm()
    noti = {}
    title='Add Category'
    if (alias != None):
        title = 'Update Category'
        cate = Category.objects.get(alias_category = alias)
        form = CateForm(initial=cate.__dict__)
        form.fields['alias_category'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = CateForm(request.POST)
        if form.is_valid():
            alias_cate = form.cleaned_data['alias_category']
            name_cate = form.cleaned_data['name']
            active_cate = form.cleaned_data['active']
            if alias != None:
                try:
                    cate = Category.objects.get(alias_category = alias_cate)
                    cate.name = name_cate
                    cate.active = active_cate
                    cate.save()
                    noti = {
                        'status' :'success',
                        'message':'Sửa thành công!'
                    }
                except:
                    noti = {
                        'message': 'Sửa thất bại!',
                        'status' : 'danger'
                    }
            else:
                try: 
                    cate = Category.objects.get(alias_category = alias_cate)
                    noti = {
                        'message': 'Mã đã tồn tại!',
                        'status' : 'danger'
                    }
                except:
                    new_cate = Category(alias_category = alias_cate,name = name_cate,active = active_cate)
                    new_cate.save()
                    noti = {
                        'status' :'success',
                        'message':'Thêm thành công!'
                    }
    context = {
            'form': form,
            'title': title,
            'cate': cate,
            'noti':noti,
        }
    return HttpResponse(template.render(context, request))


def delete_cate(request,alias):
    cate = Category.objects.get(alias_category = alias)
    cate.delete()
    return redirect('/category-admin')