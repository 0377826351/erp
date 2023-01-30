from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from ....models import Extend_User
from datetime import datetime
from django.utils import timezone
import hashlib
import string
import random

# from django.core.mail import send_mail, BadHeaderError
# from django.http import HttpResponse
# from django.contrib.auth.forms import PasswordResetForm
# from django.template.loader import render_tzo_string
# from django.db.models.query_utils import Q
# from django.utils.http import urlsafe_base64_encode
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes

def login(request):
    next = request.GET.get('next')
    if next is None:
        next = "/home-admin"
    if request.user.is_authenticated:
        return redirect(next)
    template = loader.get_template('admin/auth/login.html')
    context={}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(next)
        else:
            context={
                'title': 'Login',
                'error':'Sai tài khoản hoặc mật khẩu'
            }
    else:
        context = {
            "title": "Login"
        }
    return HttpResponse(template.render(context,request))
    
def regis(request):
    if request.user.is_authenticated:
        return redirect("/home-admin")
    template = loader.get_template('admin/auth/register.html')
    return HttpResponse(template.render({'title': 'Register'}, request))

def adduser(request):
    fullName = request.POST['fullname']
    email = request.POST['email']
    passWord = request.POST['password']
    user = User(username=fullName, email=email)
    user.set_password(passWord)
    user.save()
    return redirect("/login")

def forgot(request):
    if request.user.is_authenticated:
        return redirect("/home-admin")
    template = loader.get_template('admin/password/forgotps.html')
    context ={}
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            time_now = timezone.now()
            time_hash = hashlib.sha256(str(time_now).encode('utf-8')).hexdigest()
            token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
            try:
                extend_user = Extend_User.objects.get(user_id = user.id)
                extend_user.token = token
                extend_user.token_date = time_now
                extend_user.save()
            except:
                new_extend_user = Extend_User(token = token,token_date = time_now,user_id = user.id)
                new_extend_user.save()
            return redirect("reset_password_done_index",id = user.id,token = token,token_date = time_hash)
        except:
            context = {
                'title': 'Recover PassWord',
                'error':'Sai Email'
            }
    else:
        context = {
            'title': 'Recover PassWord'
        }
    return HttpResponse(template.render(context, request))

# def reset_password_done(request):
    # template = loader.get_template('admin/password/password_reset_done.html')
    # return HttpResponse(template.render({'title': 'Forgot-Password'}, request))

def reset_password_confirm(request,id,token,token_date):
    template = loader.get_template('admin/password/password_reset_confirm.html')
    extend = Extend_User.objects.get(user_id = id   )
    token_date_extend = extend.token_date
    print(token_date)
    if( timezone.now() - token_date_extend).seconds <300:
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm = request.POST.get('confirmPassword')
            user = User.objects.get(id=id)
            if new_password  == confirm:
                user.set_password(new_password)
                user.save()
                user = authenticate(username=user.username, password=new_password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('/home-admin')
                else:
                    context = {
                    "title": "Confirm PassWord",
                    'error':'Mật khẩu không trùng khớp'
                    }
            else:
                context = {
                    "title": "Confirm PassWord",
                    'error':'Mật khẩu không trùng khớp'
                }
        else:
            context = {
                "title": "Confirm PassWord"
            }
    else:
        return redirect('/forgot-password')
    return HttpResponse(template.render(context,request))
    


# def password_reset_request(request):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = User.objects.filter(Q(email=data))
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
# 					email_template_name = "main/password/password_reset_email.txt"
# 					c = {
# 					"email":user.email,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return redirect ("/password_reset/done/")
# 	password_reset_form = PasswordResetForm()
# 	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})

