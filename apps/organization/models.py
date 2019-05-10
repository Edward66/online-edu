# _*_encoding:utf-8_*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = verbose_name_plural = u'城市'

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    tag = models.CharField(default=u'全国知名', max_length=10, verbose_name=u'机构标签')
    category = models.CharField(max_length=20, choices=(('pxjg', u'培训机构'), ('gr', u'个人'), ('gx', u'高校')),
                                verbose_name=u'机构类别', default='pxjg')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='logo', max_length=100)
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市',on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    courses_num = models.IntegerField(default=0, verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = verbose_name_plural = u'课程机构'

    def __str__(self):
        return self.name

    def get_teacher_nums(self):
        # 获取课程机构的教师数量
        return self.teachers.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属结构', related_name='teachers',on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u'教师名')
    age = models.IntegerField(default=18, verbose_name=u'年龄')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    feature = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name=u'头像', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = verbose_name_plural = u'教师'

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.courses.all()
