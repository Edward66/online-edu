# _*_ coding:utf-8 _*_

from pure_pagination import Paginator, PageNotAnInteger

from django.shortcuts import HttpResponse, render
from django.views.generic import View
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse

from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    """
    课程列表页
    """

    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

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

        if request.user.is_authenticated:
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


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            course.students += 1
            course.save()
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]

        # 获取学过该用户的学过其他的所有课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums').exclude(id=course.id)[:4]

        all_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'course_resources': all_resources,
            'related_courses': related_courses,

        }
        return render(request, 'course-video.html', context)


class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course).order_by('-add_time')
        all_resources = CourseResource.objects.filter(course=course)

        #  相关课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums').exclude(id=course.id)[:4]

        context = {
            'course': course,
            'all_comments': all_comments,
            'related_courses': related_courses,
            'all_resources': all_resources,
        }
        return render(request, 'course-comment.html', context)


class AddCommentView(View):
    """
    用户添加课程评论
    """

    def post(self, request):
        if not request.user.is_authenticate:
            return HttpResponse('{"status":"fail","msg":"用户未登陆"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.user = request.user
            course_comments.comments = comments
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type='application/json')


class VideoPlayView(View):
    """
    视频播放页面
    """

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        # 查询用户是否已经关联了该课程
        course = video.lesson.course
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]

        # 获取学过该用户的学过其他的所有课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'course_resources': all_resources,
            'related_courses': related_courses,
            'video': video,
        }
        return render(request, 'course_play.html', context)
