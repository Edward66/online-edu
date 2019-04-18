# _*_encoding:utf-8_*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
    birthday = models.DateTimeField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(max_length=5, choices=(('mail', u'男'), ('female', u'女')), default='female')
    address = models.CharField(max_length=100, default=u'')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(max_length=100, upload_to='image/%Y/%m', default=u'image/default.png')

    class Meta:
        verbose_name = verbose_name_plural = u'用户信息'

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10, choices=(('register', u'注册'), ('forget', u'找回密码')))
    send_time = models.DateTimeField(
        default=datetime.now)  # 如果不去掉括号，就会根据EmailVeryfiRecord编译的时间来生成默认时间。去掉括号了才会根据class实例化的时间来生成

    class Meta:
        verbose_name = verbose_name_plural = u'邮箱验证码'


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(max_length=100, upload_to='banner/%Y/%m', verbose_name=u'轮播图')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = verbose_name_plural = '轮播图'