# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-04-30 09:25'

from django.conf.urls import url

from .views import (
    CourseListView, CourseDetailView
)

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

]
