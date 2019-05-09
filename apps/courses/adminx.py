# _*_ coding: utf-8 _*_
__author__ = 'edward'
__date__ = '2019-04-20 16:22'

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg


class LesssonInLine(object):
    model = Lesson
    extra = 0


class CourseResourceInLine(object):
    model = CourseResource
    extra = 0


class CourseAadmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums',
                    'get_zj_number', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums', 'students']
    list_editable = ['degree', 'desc']  # 在列表页编辑
    exclude = ['fav_nums']
    refresh_times = [3, 5]  # 每3秒或每5秒刷新一次页面
    inlines = [LesssonInLine, CourseResourceInLine]
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj  # 取得新增的Course实例
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.courses_num = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAadmin, self).post(request, args, kwargs)


class BannerCourseAadmin(object):
    """
    只管理为轮播图的课程
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums', 'students']
    exclude = ['fav_nums']
    inlines = [LesssonInLine, CourseResourceInLine]

    def queryset(self):
        qs = super(BannerCourseAadmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_display = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAadmin)
xadmin.site.register(BannerCourse, BannerCourseAadmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
