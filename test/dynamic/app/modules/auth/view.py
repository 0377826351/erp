from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .form import AuthLoginForm
from base.views import BaseView

class AuthLoginView(View):
    template = 'auth/login.html'
    context = {'page_title': 'Đăng nhập', 'form': AuthLoginForm(), 'message': None}

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.HOME_URL)

        return render(request, 'auth/login.html', self.context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if 'remember_me' not in request.POST:
                self.request.session.set_expiry(0)
                self.request.session.modified = True
            return redirect(settings.HOME_URL)
        
        self.context['message'] = 'Tài khoản hoặc mật khẩu không đúng'
        self.context['form_data'] = request.POST
        return render(request, self.template, self.context)


class AuthLogoutView(BaseView, View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)