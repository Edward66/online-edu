# _*_encoding:utf-8_*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'机构课程', null=True, blank=True, related_name='courses')
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=50, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', blank=True, null=True, related_name='courses')
    degree = models.CharField(max_length=2, choices=(('cj', '初级'), ('zj', u'中级'), ('gj', u'高级')), verbose_name=u'难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟显示)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(max_length=100, upload_to='courses/%Y/%m', verbose_name=u'封面图')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(default=u'后端开发', max_length=300, verbose_name=u'课程类别')
    tag = models.CharField(default='', verbose_name=u'课程标签', max_length=10)
    need_know = models.CharField(default='', max_length=300, verbose_name=u'课程须知')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name=u'老师告诉你能学到什么')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = verbose_name_plural = u'课程'

    def __str__(self):
        return self.name

    def get_zj_number(self):
        """获取课程章节数"""
        return self.lessons.all().count()

    def get_learn_user(self):
        return self.users.all()[:5]

    def get_course_lesson(self):
        """获取所有章节"""
        return self.lessons.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', related_name='lessons')
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = verbose_name_plural = u'章节'

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        """获取所有视频"""
        return self.videos.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节', related_name='videos')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, default='', verbose_name=u'访问地址')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟显示)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = verbose_name_plural = u'视频'

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(max_length=100, upload_to='course/resource/%Y/%m', verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = verbose_name_plural = u'课程资源'
