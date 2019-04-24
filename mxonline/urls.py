import xadmin

from django.conf.urls import url, include
from django.views.generic import TemplateView

from users.views import (
    LoginView, RegisterView, ActiveUserView,
    ForgetPwdView, ResetPwdView, ModifyPwdView
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
]
