from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'rcpe_web.search.views.home'),
    url(r'^index.html$', 'rcpe_web.search.views.home'),
    url(r'^search.html$', 'rcpe_web.search.views.search'),
    url(r'^search.action$', 'rcpe_web.search.views.searchQuery'),
    url(r'^searchRC.action$','rcpe_web.search.views.searchPairs'),
    url(r'^search_pair.html$','rcpe_web.search.views.search_pair_html'),
    url(r'^searchRCPair.action$','rcpe_web.search.views.searchRCPair'),
    url(r'^contacts.html$','rcpe_web.search.views.contacts_html'),
    url(r'^label.html$', 'rcpe_web.labeling.views.home' ),
    url(r'^label_next.action$', 'rcpe_web.labeling.views.next_label'),
    url(r'^label_refresh.action$', 'rcpe_web.labeling.views.refresh'),
    
    # url(r'^rcpe_web/', include('rcpe_web.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    #Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tracking/', include('tracking.urls')),
)
