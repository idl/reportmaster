from django.conf.urls import patterns, url

from reporting import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^report/delete/(?P<pk>\d+)/$', views.delete_report, name='delete_report'),
	url(r'^report/save/$', views.save_report, name='save_report'),
	url(r'^report/view/(?P<pk>\d+)/$', views.view_report, name='view_report'),
	url(r'^reportItem/save/$', views.save_item, name='save_item'),
	url(r'^reportItem/edit/(?P<pk>\d+)/$', views.edit_item, name='edit_item'),
	)