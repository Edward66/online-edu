# _*_ encoding:utf-8 _*_
from pure_pagination import Paginator, PageNotAnInteger

from django.db.models import Q
from django.shortcuts import HttpResponse, render
from django.views.generic import View

from courses.models import Course
from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskModelForm
from operation.models import UserFavorite

from utils.inc_dec_fav_num import inc_fav_num, dec_fav_num


class OrgView(View):
    """
    课程结构列表功能
    """

    def get(self, request):
        # 课程结构
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        # 城市
        all_cities = CityDict.objects.all()
        hot_orgs = all_orgs.order_by('-click_num')[:3]

        # 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        rank = request.GET.get('rank', '')
        if rank:
            if rank == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif rank == 'courses':
                all_orgs = all_orgs.order_by('-courses_num')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)  # 此插件可以携带原参数，这样做分页的时候不影响筛选。

        orgs = p.page(page)

        context = {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'rank': rank,
        }
        return render(request, 'org-list.html', context)


class AddUserAskView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        userask_form = UserAskModelForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)  # 不指定commit=True的话不会真正的保存
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        all_courses = course_org.courses.all()[:3]
        all_teachers = course_org.teachers.all()[:1]
        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2).first():
                has_fav = True
        context = {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        }
        return render(request, 'org-detail-homepage.html', context)


class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.courses.all()
        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2).first():
                has_fav = True
        context = {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        }
        return render(request, 'org-detail-course.html', context)


class OrgDescView(View):
    """
    机构课程介绍页
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2).first():
                has_fav = True
        context = {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        }
        return render(request, 'org-detail-desc.html', context)


class OrgTeacherView(View):
    """
    机构课程介绍页
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teachers.all()
        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2).first():
                has_fav = True
        context = {
            'course_org': course_org,
            'current_page': current_page,
            'all_teachers': all_teachers,
            'has_fav': has_fav,
        }
        return render(request, 'org-detail-teachers.html', context)


class AddFavView(View):
    """
    用户收藏和取消收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户登录状态
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登陆"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id),
                                                   fav_type=int(fav_type)).first()
        if exist_record:
            # 如果记录已经存在，则表示用户取消收藏
            exist_record.delete()

            dec_fav_num(int(fav_id), int(fav_type))

            return HttpResponse('{"status":"success","msg":"取消收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                inc_fav_num(int(fav_id), int(fav_type))

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    课程讲师类表业
    """

    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 讲师搜搜
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        rank = request.GET.get('rank', '')
        if rank and rank == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except  PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        teachers = p.page(page)

        context = {
            'all_teachers': teachers,
            'sorted_teacher': sorted_teacher,
            'rank': rank,
        }
        return render(request, 'teachers-list.html', context)


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()

        # 讲师排行
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_fav = True

        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_fav = True

        context = {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav,
        }
        return render(request, 'teacher-detail.html', context)
