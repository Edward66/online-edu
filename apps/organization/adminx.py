# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-04-20 16:49'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_filed = ['name', 'desc', ]
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_nums', 'address', 'city', 'add_time']
    search_filed = ['name', 'desc', 'address', 'city']
    list_filter = ['name', 'desc', 'click_num', 'fav_nums',  'address', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'teaching_char', 'click_num',
                    'fav_nums', 'add_time']
    search_filed = ['org', 'name', 'work_company']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'teaching_char', 'click_num',
                   'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
