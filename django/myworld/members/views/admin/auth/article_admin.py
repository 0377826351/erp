from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from ....forms import ArtForm
from ....models import Category,Article,Question
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def article(request):
    template = loader.get_template('admin/article/index.html')
    list_obj = Article.objects.all()
    context = {
        'title': 'Article',
        'list_obj': list_obj,
    }
    return HttpResponse(template.render(context, request))

@login_required
def form_art(request, alias=None):
    template = loader.get_template('admin/article/form-art.html')
    user = request.user
    article=None
    noti={}
    title_page='Add Article'
    form = ArtForm()
    if (alias != None):
        title_page = 'Update Article'
        article = Article.objects.get(alias_article = alias)
        form = ArtForm(initial=article.__dict__)
    if request.method == 'POST':
        form = ArtForm(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            alias_article = form.cleaned_data['alias_article']
            category = form.cleaned_data['category_id']
            content = form.cleaned_data['content']
            type = form.cleaned_data['type']
            image = form.cleaned_data['image']
            print(type,content,image)
            if alias != None:
                try: 
                    article = Article.objects.get(alias_article = alias)
                    article.title = title
                    article.alias_article = alias_article
                    article.category_id = category
                    article.content = content
                    article.type = type
                    article.image = image
                    article.save()
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
                    article = Article.objects.get(alias_article = alias_article)
                    noti = {
                        'message': 'Mã đã tồn tại!',
                        'status' : 'danger'
                    }
                except:
                    new_article = Article(title=title,alias_article=alias_article,category_id=category,created_id=user.id,content=content,type=type,image=image)
                    new_article.save()
                    noti = {
                        'status' :'success',
                        'message':'Thêm thành công!'
                    }
    context = {
            'title_page': title_page,
            'noti':noti,
            'article':article,
            'form':form,
        }
    return HttpResponse(template.render(context, request))

@login_required
def delete_article(request, alias):
    article = Article.objects.get(alias_article = alias)
    article.delete()
    return redirect('/article-admin')

