# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-04-22 15:38'

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u'用  户  名',
        widget=forms.TextInput(attrs={'placeholder': u'手机号/邮箱'}),
    )
    password = forms.CharField(
        required=True,
        min_length=6,  # 小于6根本就不会去查，会减少数据库压力
        label=u'密 码',
        widget=forms.PasswordInput(attrs={'placeholder': u'请输入您的密码'}),
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label=u'邮      箱',
        widget=forms.EmailInput(attrs={'placeholder': u'请输入您的邮箱'})
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        label=u'密     码',
        widget=forms.PasswordInput(attrs={'placeholder': u'请输入6-20位非中文字符密码'})
    )
    captcha = CaptchaField(
        error_messages={'invalid': u'验证码错误'},
        label='验  证  码',
    )


class ForgetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label=u'邮      箱',
        widget=forms.EmailInput(attrs={'placeholder': u'请输入您的邮箱'})
    )
    captcha = CaptchaField(
        error_messages={'invalid': u'验证码错误'},
        label='验  证  码',
    )


class ModifyPwdForm(forms.Form):
    password = forms.CharField(
        required=True,
        label=u'密   码',
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': u'6-20为非中文字符'}),

    )

    re_password = forms.CharField(
        required=True,
        label=u'确 认 密 码',
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': u'6-20为非中文字符'})
    )

    def clean_re_password(self):
        passwrod = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if passwrod and re_password:
            if passwrod != re_password:
                raise forms.ValidationError('密码不一致')
            else:
                return self.cleaned_data
