# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-05-02 08:23'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):  # 函数名称和参数必须这么写
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
