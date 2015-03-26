from django.conf.urls import patterns, include, url
import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.need_login(views.IndexView.as_view()), name='index'),
    url(r'^(?P<pk>\d+)/$', views.question_view, name='detail'),
    url(r'^signup/$', views.UserCreate.as_view(), name='user_add'),
    url(r'^set-user/(?P<user_id>\d+)/$', views.set_user, name='set_user'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^result/(?P<pk>\d+)/$', views.test_result, name='test_result'),
    url(r'^report/$', views.report, name='report'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)