# _*_ coding: utf-8 _*_
from datetime import datetime
import json

from pure_pagination import Paginator, PageNotAnInteger

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.shortcuts import reverse
from django.db.models import Q
from django.shortcuts import HttpResponse, render, redirect, render_to_response
from django.views.generic.base import View

from courses.models import Course
from .forms import (LoginForm, RegisterForm, ForgetForm,
                    ModifyPwdForm, UploadImageForm, UserInfoModelForm)
from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    """
    实现用户名邮箱均可登录
    继承ModelBackend类，因为它有方法authenticate，可点进源码查看
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
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


class LogoutView(View):
    """
    用户登出
    """

    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


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

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册幕学在线网'
            user_message.save()

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
    """
    修改用户密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            re_password = request.POST.get('password2', '')
            print
            re_password
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


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_info_form = UserInfoModelForm(request.POST, instance=request.user)  # 如果不指定实例，它会默认新增加一个用户
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    个人中心修改用户密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd2 = request.POST.get('password2', '')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'update')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update').first()
        if record:
            send_time = record.send_time
            print
            send_time
            now = datetime.now()
            duration = (now - send_time).seconds
            if duration > 600:
                return HttpResponse('{"email":"验证码过期了，请重新获取"}', content_type='application/json')
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        context = {
            'user_courses': user_courses
        }
        return render(request, 'usercenter-mycourse.html', context)


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        context = {
            'org_list': org_list
        }
        return render(request, 'usercenter-fav-org.html', context)


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的授课讲师
    """

    def get(self, request):
        teacher_list = []
        # fav_type：1课程，2授课机构，3讲师
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        context = {
            'teacher_list': teacher_list
        }
        return render(request, 'usercenter-fav-teacher.html', context)


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的授课讲师
    """

    def get(self, request):
        course_list = []
        # fav_type：1课程，2授课机构，3讲师
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        context = {
            'course_list': course_list
        }
        return render(request, 'usercenter-fav-course.html', context)


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空个人消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)  # 此插件可以携带原参数，这样做分页的时候不影响筛选。

        messages = p.page(page)
        context = {
            'messages': messages

        }
        return render(request, 'usercenter-message.html', context)


class IndexView(View):
    """
    幕学在线网首页
    """

    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        context = {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        }
        return render(request, 'index.html', context)


def page_not_found(request):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局404处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
