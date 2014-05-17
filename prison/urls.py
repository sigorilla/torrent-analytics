from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='index/index.html')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^get/', include('get.urls', namespace='get')),
    url(r'^admin/', include(admin.site.urls)),
)
