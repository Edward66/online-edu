# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-04-23 15:43'

from random import Random

from django.core.mail import send_mail
from django.conf import settings

from users.models import EmailVerifyRecord


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '请点击下面的链接激活你的账号（10分钟内有效）：http://127.0.0.1:8000/active/{code}'.format(code=code)
        send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])

    elif send_type == 'forget':
        email_title = '慕学在线网密码重置链接'
        email_body = '请点击下面的链接重置密码（10分钟内有效）：http://127.0.0.1:8000/reset/{code}'.format(code=code)
        send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])

    elif send_type == 'update':
        email_title = '幕学在线修改邮箱验证码'
        email_body = '您的邮箱验证码为（10分钟内有效）：{code}'.format(code=code)
        send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


