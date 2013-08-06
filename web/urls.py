from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'base.views.index', name='index'),

    url(r'^event/$', 'base.views.event'),
    url(r'^event/(?P<event_id>\d+)/$', 'base.views.event'),
    url(r'^event/(?P<event_id>\d+)/task/$', 'base.views.task'),
    url(r'^event/(?P<event_id>\d+)/task/(?P<task_id>\d+)$', 'base.views.task'),

#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += staticfiles_urlpatterns()

