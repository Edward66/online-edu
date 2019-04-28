# _*_ encoding:utf-8 _*_
from pure_pagination import Paginator, PageNotAnInteger

from django.shortcuts import HttpResponse, render
from django.views.generic import View

from .models import CourseOrg, CityDict
from forms import UserAskModelForm


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

        p = Paginator(all_orgs, 3, request=request)  # 此插件可以携带原参数，这样做分页的时候不影响筛选。

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
