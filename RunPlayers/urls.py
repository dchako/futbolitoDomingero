from django.conf.urls import patterns, include, url
from FutboolGruops.views import ExtraDataView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'FutboolGruops.views.home', name='home'),
    url(r'^invitacion$', 'FutboolGruops.views.invitacion', name='invitacion'),
    url(r'^invitar$', 'FutboolGruops.views.invitar', name='invitar'),
    url(r'^login$', 'FutboolGruops.views.login', name='login'),
    url(r'^registrar$', ExtraDataView.as_view(), name='registrar'),
    #url(r'^registrar$', 'FutboolGruops.views.registrar', name='registrar'),
    url(r'^error$', 'FutboolGruops.views.error', name='error'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
)
