from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('get.urls', namespace="get")),
    # url(r'^get/', views.history, name='history'),
    # url(r'^admin/', include(admin.site.urls)),
)
