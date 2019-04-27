# _*_ encoding:utf-8 _*_
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.views.generic import View

from .models import CourseOrg, CityDict


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
        }
        return render(request, 'org-list.html', context)
