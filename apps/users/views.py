# _*_ coding: utf-8 _*_
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import LoginForm
from .models import UserProfile


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})

        return render(request, 'login.html', {'login_form': login_form})


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 支持用户名和邮箱登陆
            if user.check_password(password):  # 把明文的密码加密，因为数据库里储存的密码是密文的
                return user
        except Exception as e:
            return None
