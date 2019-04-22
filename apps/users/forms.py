# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-04-22 15:38'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='用  户  名',
        widget=forms.TextInput(attrs={'placeholder': '手机号/邮箱'}),
    )
    password = forms.CharField(
        required=True,
        min_length=6,  # 小于6根本就不会去查，会减少数据库压力
        label='密码',
        widget=forms.PasswordInput(attrs={'placeholder': '请输入您的密码'}),
    )
