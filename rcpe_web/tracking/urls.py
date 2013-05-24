from django.conf.urls.defaults import *
from django.conf import settings
from tracking import views

urlpatterns = patterns('',
    url(r'^refresh/$', views.update_active_users, name='tracking-refresh-active-users'),
    url(r'^refresh/json/$', views.get_active_users, name='tracking-get-active-users'),
    url(r'^all_visitors/json',views.get_all_users,name='tracking-get-all-users'),
    url(r'^all_ips/json',views.get_all_ips,name='tracking-get-all-ips'),
)

if getattr(settings, 'TRACKING_USE_GEOIP', False):
    urlpatterns += patterns('',
        url(r'^map/$', views.display_map, name='tracking-visitor-map'),
    )
