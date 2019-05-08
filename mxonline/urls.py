# _*_ encoding:utf-8 _*_
import xadmin

from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve

from users.views import (
    IndexView, LoginView, LogoutView, RegisterView, ActiveUserView,
    ForgetPwdView, ResetPwdView, ModifyPwdView,
)

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name='register'),

    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程相关
    url(r'^course/', include('courses.urls', namespace='course')),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 用户相关
    url(r'^users/', include('users.urls', namespace='users')),

]
