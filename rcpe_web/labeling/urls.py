from django.conf.urls.defaults import *
from django.conf import settings
from labeling import views

urlpatterns = patterns('',
                       url(r'^$', views.home ),
                       url(r'^next.action$', views.next_label),
                       url(r'^start.action$',views.start_label),
)

