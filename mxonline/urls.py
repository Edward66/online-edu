# _*_ encoding:utf-8 _*_
import xadmin

from django.conf.urls import url, include
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import (
    LoginView, RegisterView, ActiveUserView,
    ForgetPwdView, ResetPwdView, ModifyPwdView
)
from organization.views import (
    OrgView
)

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^register/$', RegisterView.as_view(), name='register'),

    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程结构首页
    url(r'^org_list/$', OrgView.as_view(), name='org_list'),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
