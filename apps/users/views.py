# _*_ coding: utf-8 _*_
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 支持用户名和邮箱登陆
            if user.check_password(password):  # 把明文的密码加密，因为数据库里储存的密码是密文的
                return user
        except Exception as e:
            return None


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
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活', 'login_form': login_form})
            return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})

        return render(request, 'login.html', {'login_form': login_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.filter(code=active_code).first()
        if record:
            send_time = record.send_time
            now = datetime.now()
            duration = (now - send_time).seconds
            if duration > 600:
                return render(request, 'active_fail.html', {'msg': u'链接已超时'})
            email = record.email
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            return redirect(reverse('login'))
        else:
            return render(request, 'active_fail.html')


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username).exists():
                return render(request, 'register.html', {'msg': '邮箱已被注册', 'register_form': register_form})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(username, 'register')
            return redirect(reverse('login'))
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            re_password = request.POST.get('re_password', '')
            email = request.POST.get('email', '')  # TODO：这里有安全漏洞
            user = UserProfile.objects.get(email=email)
            user.password = make_password(re_password)
            user.save()
            return redirect(reverse('login'))
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modify_form': modify_form, 'email': email})


class ResetPwdView(View):
    def get(self, request, reset_code):
        record = EmailVerifyRecord.objects.filter(code=reset_code).first()
        if record:
            send_time = record.send_time
            now = datetime.now()
            duration = (now - send_time).seconds
            if duration > 600:
                return render(request, 'active_fail.html', {'msg': u'链接已超时'})
            modify_form = ModifyPwdForm()
            email = record.email
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})
        else:
            return render(request, 'active_fail.html')
