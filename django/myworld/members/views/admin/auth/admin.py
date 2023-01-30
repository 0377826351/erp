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
def index(request):
    template = loader.get_template('admin/home/index.html')
    return HttpResponse(template.render({'title': 'Home-Admin'}, request))

def log_out(request):
    logout(request)
    return redirect('/login')

@login_required
def profile(request):
    template = loader.get_template('admin/home/profile.html')
    user = request.user
    print(user)
    context = {
        'title': 'User Profile',
        'user': user,
    }
    return HttpResponse(template.render(context, request))

@login_required
def edit_profile(request):
    template = loader.get_template('admin/home/update_profile.html')
    user = request.user
    context = {
        'title': 'Edit Profile',
        'user': user,
    }
    return HttpResponse(template.render(context, request))

def update_profile(request):
    new_username = request.POST.get('username')
    new_email = request.POST.get('email')
    user = request.user
    user.username = new_username
    user.email = new_email
    user.save()
    return redirect("/profile")

@login_required
def change_password(request):
    template = loader.get_template('admin/auth/changepassword.html')
    user = request.user
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('n1_password')
        confirm_new_password = request.POST.get('n2_password')
        if new_password == confirm_new_password and user.check_password(current_password):
            user.set_password(new_password)
            user.save() 
            context = {
                'title': 'Change Password',
                'noti':' Đổi mật khẩu thành công!'
            }
        elif new_password != confirm_new_password:
            context = {
                'title': 'Change Password',
                'noti':' Mật khẩu hiện tại không đúng!'
            }
        else:
            context = {
                'title': 'Change Password',
                'noti':' Mật khẩu không trùng khớp!'

            }
    else:
        context = {
            "title": "Change Password"
        }
    return HttpResponse(template.render(context,request))

@login_required
def contact(request):
    template = loader.get_template('admin/contact/index.html')
    context = {
        'title': 'Contact-Us',
    }
    return HttpResponse(template.render(context, request))