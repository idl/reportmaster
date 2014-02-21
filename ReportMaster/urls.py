from django.conf.urls import patterns, include, url
from ReportMaster import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ReportMaster.views.home', name='home'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^reporting/', include('reporting.urls', namespace="reporting")),
    url(r'^admin/', include(admin.site.urls)),
)
