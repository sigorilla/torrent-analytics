from django.conf.urls import patterns, include, url
from get import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^history/', views.history, name='history'),
	url(r'^about/', views.about, name='about'),
	url(r'^analytics/', views.analytics, name='analytics'),
)

