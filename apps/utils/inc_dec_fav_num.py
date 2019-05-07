# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-05-07 10:53'

from courses.models import Course
from organization.models import CourseOrg, Teacher


def dec_fav_num(fav_id, fav_type):
    # 1是课程，2是机构，3是老师
    if int(fav_type) == 1:
        course = Course.objects.get(id=int(fav_id))
        course.fav_nums -= 1
        if course.fav_nums < 0:
            course.fav_nums = 0
        course.save()
    elif int(fav_type) == 2:
        course_org = CourseOrg.objects.get(id=int(fav_id))
        course_org.fav_nums -= 1
        if course_org.fav_nums < 0:
            course_org.fav_nums = 0
        course_org.save()
    elif int(fav_type) == 3:
        teacher = Teacher.objects.get(int=int(fav_id))
        teacher.fav_nums -= 1
        if teacher.fav_nums < 0:
            teacher.fav_nums = 0
        teacher.save()


def inc_fav_num(fav_id, fav_type):
    # 1是课程，2是机构，3是老师
    if int(fav_type) == 1:
        course = Course.objects.get(id=int(fav_id))
        course.fav_nums += 1
        course.save()
    elif int(fav_type) == 2:
        course_org = CourseOrg.objects.get(id=int(fav_id))
        course_org.fav_nums += 1
        course_org.save()
    elif int(fav_type) == 3:
        teacher = Teacher.objects.get(int=int(fav_id))
        teacher.fav_nums += 1
        teacher.save()
