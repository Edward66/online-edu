# _*_ coding:utf-8 _*_

from pure_pagination import Paginator, PageNotAnInteger

from django.shortcuts import HttpResponse, render
from django.views.generic import View

from .models import Course
from operation.models import UserFavorite


class CourseListView(View):
    """
    课程列表页
    """

    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 课程排序
        rank = request.GET.get('rank', '')
        if rank:
            if rank == 'students':
                all_courses = all_courses.order_by('-students')
            elif rank == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)  # 此插件可以携带原参数，这样做分页的时候不影响筛选。

        courses = p.page(page)

        context = {
            'all_courses': courses,
            'rank': rank,
            'hot_courses': hot_courses,
        }
        return render(request, 'course-list.html', context)


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            related_course = Course.objects.filter(tag=tag)[:1]
        else:
            related_course = []

        context = {
            'course': course,
            'related_courses': related_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        }
        return render(request, 'course-detail.html', context)
