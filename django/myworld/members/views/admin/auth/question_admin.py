from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from ....models import Category,Article,Question
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def question(request):
    template = loader.get_template('admin/question/index.html')
    list_obj = Question.objects.all()
    context = {
        'title': 'Article',
        'list_obj': list_obj,
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_question(request):
    template = loader.get_template('admin/question/add.html')
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        try: 
            question = Question.objects.get(question = question)
            context = {
                'title': 'Add Category',
                'noti': 'Câu hỏi tồn tại!'
            }
        except:
            new_ques = Question(question = question,answer = answer)
            new_ques.save()
            context = {
                'title': 'Add Category',
                'noti': 'Thêm thành công!'
            }
    else:
        context = {
            'title': 'Add Question',
    }
    return HttpResponse(template.render(context, request))

@login_required
def update_question(request,id):
    template = loader.get_template('admin/question/update.html')
    ques = Question.objects.get(id=id)
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        try: 
            ques = Question.objects.get(id = id)
            ques.question = question
            ques.answer = answer
            ques.save()
            context = {
                'title': 'Update Question',
                'noti': 'Sửa thành công!',
            }
        except:
            context = {
                'title': 'Update Question',
                'noti': 'Sửa thất bại!'
            }
    else:
        context = {
            'title': 'Update Question',
            'ques': ques,
    }
    return HttpResponse(template.render(context, request))

@login_required
def delete_ques(request, id):
    ques = Question.objects.get(id = id)
    ques.delete()
    return redirect('/question-admin')