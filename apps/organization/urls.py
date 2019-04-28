# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-04-27 11:08'

from django.conf.urls import url

from .views import OrgView, AddUserAskView

urlpatterns = [
    # 课程结构列表页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),

]
