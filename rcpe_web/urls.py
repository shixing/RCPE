from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'rcpe_web.search.views.home'),
    url(r'^index.html$', 'rcpe_web.search.views.home'),
    url(r'^search.html$', 'rcpe_web.search.views.search'),
    url(r'^search.action$', 'rcpe_web.search.views.searchQuery'),
    url(r'^searchRC.action$','rcpe_web.search.views.searchPairs'),
    # url(r'^rcpe_web/', include('rcpe_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
